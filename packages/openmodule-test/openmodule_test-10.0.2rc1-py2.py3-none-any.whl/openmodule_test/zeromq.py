from __future__ import unicode_literals

import logging
import random
import socket
import string
import threading
import time
import types
from _weakrefset import WeakSet
from contextlib import closing
from enum import Enum
from typing import List, Tuple, Optional, Union, Dict
from unittest import TestCase
from uuid import uuid4, UUID

import orjson
import zmq
from pydantic import BaseModel, Field

from openmodule.config import settings
from openmodule.dispatcher import SubscribingMessageDispatcher
from openmodule.utils.schema import Schema
from openmodule_test.utils import DeveloperError


def patch_bind_string(bind_string: str) -> str:
    """
    patches bind strings from zmq.Socket.bind so they can be used with zmq.Socket.connect
    """
    return bind_string.replace("://*", "://127.0.0.1")


class TestBroker(threading.Thread):
    __test__ = False

    _termination_watcher_timeout = 10

    xsub: zmq.Socket = None
    xpub: zmq.Socket = None

    def __init__(self, sub_bind, pub_bind):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.sub_bind = sub_bind
        self.pub_bind = pub_bind
        self.running = False
        self.context = zmq.Context()

    def start(self) -> None:
        # overwriting start ensures that the sockets are bound after calling start()
        # if we bind in run(...) we might bind after another thread, and in the constructor
        # may be surprising to someone using the class aswell
        self.running = True
        self.xsub = self.context.socket(zmq.XSUB)
        self.xpub = self.context.socket(zmq.XPUB)
        self.xsub.setsockopt(zmq.LINGER, 0)
        self.xpub.setsockopt(zmq.LINGER, 0)
        self.log.debug(f"binding on sub->{self.sub_bind} and pub->{self.pub_bind}")
        self.xsub.bind(self.sub_bind)
        self.xpub.bind(self.pub_bind)
        super().start()

    def run(self):
        try:
            self.log.debug("proxy started")
            zmq.proxy(self.xsub, self.xpub)
        except zmq.ContextTerminated:
            self.log.debug("broker thread received context terminated")
        self.xsub.close()
        self.xpub.close()

    def _detect_and_close_bad_linger(self):
        sockets = self.context._sockets  # noqa, modified version of context.destroy() has to use private member
        self.context._sockets = WeakSet()
        has_bad_linger = False
        for s in sockets:
            closed = False
            if s and not s.closed:
                linger = s.getsockopt(zmq.LINGER)
                if linger is None or linger == -1:
                    has_bad_linger = True
                    s.close(linger=0)
                    closed = True

            if not closed:  # we may need them later, for forcefully closing in the termination watcher
                self.context._sockets.add(s)
        return has_bad_linger

    def stop(self):
        terminated = False
        had_open_sockets = False

        def termination_watcher():
            nonlocal had_open_sockets
            for x in range(self._termination_watcher_timeout * 10):
                if terminated:
                    return
                else:
                    time.sleep(0.1)

            if not terminated:
                had_open_sockets = True
                sockets = self.context._sockets  # noqa
                self.context._sockets = WeakSet()
                for socket in sockets:
                    if socket and not socket.closed:
                        socket.close()

        has_bad_linger = self._detect_and_close_bad_linger()
        watcher = threading.Thread(target=termination_watcher)
        watcher.start()
        self.context.term()
        terminated = True
        self.join()

        assert not has_bad_linger, (
            "you have a socket with infinite linger time, this can cause blocking during shutdown, preventing\n"
            "your application from ever shutting down. Please specify a linger timeout via setsockopt(...)\n"
            "or use get_(s/p)ub_socket(...)"
        )

        assert not had_open_sockets, (
            "You have open sockets which did not close after 10 seconds. Some component in your testcase\n"
            "did not shutdown properly. I am forcefully closing the sockets from a different thread to\n"
            "prevent job from getting stuck for hours in the CI/CD. This can cause various internal ZMQ errors."
        )

        self.log.debug("proxy stopped")


class TestClient(threading.Thread):
    __test__ = False

    startup_check_delay = 0.05
    startup_check_iterations = 20  # 40 * 0.05 = 2 seconds

    _command_topic: bytes
    subscribed_topics: set
    pending_topics: Dict[bytes, None]
    zmq_dispatcher: SubscribingMessageDispatcher

    pub: zmq.Socket = None
    sub: zmq.Socket = None

    def __init__(self, broker: TestBroker):
        super().__init__()
        self._command_topic = b"_testclient_" + str(uuid4()).encode("ascii")
        self.subscribed_topics = set()
        self.pending_topics = dict()

        self.broker = broker
        self.connected = threading.Event()
        self.log = logging.getLogger(self.__class__.__name__)
        self.recv_lock = threading.Lock()
        self.recv_messages = []
        self.zmq_dispatcher = SubscribingMessageDispatcher(subscribe=self._assert_subscription,
                                                           raise_validation_errors=True, raise_handler_errors=True)
        self.has_messages = threading.Event()
        self.receiving_thread_id = None
        self.send_lock = threading.Lock()
        self.running = True

    def _assert_subscription(self, topic: bytes):
        assert topic in self.subscribed_topics, f"please subscribe to {topic} in your testcase"

    def subscribe(self, *topics: bytes):
        for topic in topics:
            self.sub.subscribe(topic)
            self.subscribed_topics.add(topic)
            self.pending_topics[topic] = None
        self.wait_for_topics()

    def wait_for_topics(self):
        for x in range(self.startup_check_iterations):
            with self.recv_lock:
                pending_topics = list(self.pending_topics.keys())
            if pending_topics:
                for topic in pending_topics:
                    self._zmq_cmd("hi", topic=topic)
                time.sleep(self.startup_check_delay)
            else:
                break

        assert not self.pending_topics, "error during startup and connect"

    def start(self):
        self.pub = self.broker.context.socket(zmq.PUB)
        self.sub = self.broker.context.socket(zmq.SUB)
        self.pub.setsockopt(zmq.LINGER, 0)
        self.sub.setsockopt(zmq.LINGER, 0)
        self.pub.connect(patch_bind_string(self.broker.sub_bind))
        self.sub.connect(patch_bind_string(self.broker.pub_bind))
        super().start()
        self.subscribe(self._command_topic)

    def _zmq_cmd(self, cmd, topic=None):
        if not self.broker.context.closed:
            message = {"__testcommand": cmd, "name": "testclient", "type": "cmd"}
            self.pub.send_multipart((topic or self._command_topic, orjson.dumps(message)))

    def run(self):
        try:
            while self.running:
                try:
                    topic, message = self.sub.recv_multipart()
                    message = orjson.loads(message)
                except (KeyError, TypeError, ValueError) as e:
                    self.log.exception("Received an invalid message on the message queue")
                    raise e from None

                if topic == self._command_topic or "__testcommand" in message:
                    if message["__testcommand"] == "exit":
                        break
                    else:
                        with self.recv_lock:
                            if topic in self.pending_topics:
                                del self.pending_topics[topic]
                        continue

                self.zmq_dispatcher.dispatch(topic, message)
                with self.recv_lock:
                    self.recv_messages.append((topic, message))
                    self.has_messages.set()
        except zmq.ContextTerminated:
            pass
        except Exception:  # pragma: no cover
            self.log.error("Internal exception, shutting down")
        else:
            self.log.debug("client thread stopped gracefully")
        finally:
            self.sub.close()
            self.pub.close()

    def send(self, topic: Union[bytes, str], _message=None, **kwargs):
        """
        sends a message on the topic
        :param topic:
        :param _message:
        :param kwargs:
        :return:
        """
        if hasattr(topic, "encode"):
            topic = topic.encode("ascii")

        if isinstance(_message, BaseModel):
            with self.send_lock:
                self.pub.send_multipart((topic, orjson.dumps(_message.dict())))
        else:
            assert not (_message and kwargs), (
                "pass the message dict as the first parameter, or use the kwargs, not both"
            )
            data = _message or kwargs
            assert "type" in data, "a message must always have a type"
            data.setdefault("name", "testcase")
            data.setdefault("timestamp", time.time())
            with self.send_lock:
                self.pub.send_multipart((topic, orjson.dumps(data)))

    def _zmq_pop_from_front(self):
        with self.recv_lock:
            msg = self.recv_messages.pop(0)
            if not self.recv_messages:
                self.has_messages.clear()
            return msg

    def wait_for_message(self, filter, timeout=3) -> Tuple[bytes, dict]:
        """
        :param filter: filter function of type (topic: bytes, message: dict) -> bool
        :return: tuple containing [topic, message]
        """

        # protect the developer from using the client in multiple threads, this is not supported
        with self.recv_lock:
            if self.receiving_thread_id is not None:
                raise DeveloperError(
                    "the test client is not thread safe! you have to use a separate client for each thread which"
                    "wants to receive messages"
                )
            self.receiving_thread_id = threading.get_ident()

        try:
            start = time.time()
            while True:
                if not self.has_messages.wait(timeout=timeout):
                    raise TimeoutError()

                while self.recv_messages:
                    message_topic, message = self._zmq_pop_from_front()
                    if filter(message_topic, message):
                        return message_topic, message

                time_diff = time.time() - start
                if time_diff > timeout:
                    raise TimeoutError()
        finally:
            self.receiving_thread_id = None

    def wait_for_message_on_topic(self, topic: Union[str, bytes], timeout=3) -> dict:
        """
        :return: tuple containing [topic, message]
        """
        if topic and hasattr(topic, "encode"):
            topic = topic.encode()

        if topic not in self.subscribed_topics:
            raise DeveloperError(
                "please subscribe to the topic you want to receive from first! call:\n"
                f'  > zmq_client.subscribe("{topic.decode()}")\n'
                f'or set\n'
                f'  > topics = ["{topic.decode()}"] in your test class'
            )
        return self.wait_for_message(lambda recv_topic, _: (not topic) or recv_topic == topic, timeout=timeout)[1]

    def stop(self):
        self._zmq_cmd("exit")
        self.join()


def fake_config(broker: Optional[TestBroker] = None, **kwargs):
    result = {
        "NAME": "test",
        "RESOURCE": "test-resource",
        "VERSION": "test-version",
        "LOG_LEVEL": logging.DEBUG,
        "TESTING": True,
        "DEBUG": False
    }
    if broker:
        result["BROKER_SUB"] = patch_bind_string(broker.sub_bind)
        result["BROKER_PUB"] = patch_bind_string(broker.pub_bind)

    result.update(kwargs)

    # converts to an object
    config = types.SimpleNamespace()
    for k, v in result.items():
        setattr(config, k, v)
    return config


def _find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('127.0.0.1', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class _TestRPCRequest(BaseModel):
    """
    we do not want to depend on openmodule, this is a minimal version of the zmq message for the rpc function
    """
    timestamp: float = Field(default_factory=time.time)
    resource: Optional[str] = None
    name: str
    type: str
    rpc_id: UUID
    request: Optional[Dict]

    def __init__(self, **kwargs):
        resource = kwargs.pop("resource")
        if not resource:
            # this avoids evaluating settings.RESOURCE if resource is set in order to not trigger the settings module
            # to start up unnecessarily (and maybe throw import errors)
            resource = settings.RESOURCE
        super().__init__(resource=resource, **kwargs)


class ZMQProcotol(str, Enum):
    inproc = "inproc://"
    tcp = "tcp://"


class ZMQTestMixin(TestCase):
    topics: List[Union[bytes, str]] = []
    rpc_channels: List[Union[bytes, str]] = []
    protocol: ZMQProcotol = "inproc://"

    zmq_broker: TestBroker = None
    zmq_client: TestClient = None

    _cleanup_called = False

    def setUp(self):
        self._cleanup_called = False

        super(ZMQTestMixin, self).setUp()

        assert self.protocol in ["tcp://", "inproc://"], "only tcp:// and inproc:// protocols are allowed"
        if self.protocol == "inproc://":
            random_suffix = "".join(random.choices(string.ascii_letters, k=10))
            sub = f"inproc://test-sub-{random_suffix}"
            pub = f"inproc://test-pub-{random_suffix}"
        else:
            sub = f"tcp://127.0.0.1:{_find_free_port()}"
            pub = f"tcp://127.0.0.1:{_find_free_port()}"

        settings.override(
            BROKER_SUB=sub,
            BROKER_PUB=pub
        )
        self.addCleanup(settings.reset)
        self.addCleanup(self._cleanup)

        self.zmq_broker = TestBroker(settings.BROKER_SUB, settings.BROKER_PUB)
        self.zmq_broker.start()

        self.zmq_client = TestClient(self.zmq_broker)
        self.zmq_client.start()

        topics = set(self.topics + [f"rpc-rep-{x}" for x in self.rpc_channels])
        topics = [x.encode("ascii") if isinstance(x, str) else x for x in topics]
        self.zmq_client.subscribe(*topics)

    def wait_for_dispatcher(self, dispatcher):
        received = False

        def handler(_):
            """wait for dispatcher handler"""
            nonlocal received
            received = True

        """
        waits until a message dispatcher receives messages, this assumes that the subscription we issue is the last
        and if it is connected, all previous subscriptions will also be connected
        """
        random_topic = "_test" + "".join(random.choices(string.ascii_letters, k=10))
        random_topic = random_topic.encode()
        dispatcher.register_handler(random_topic, BaseModel, handler, register_schema=False, match_type=False)

        for x in range(self.zmq_client.startup_check_iterations):
            self.zmq_client.send(random_topic, {"type": "connection-check"})
            time.sleep(self.zmq_client.startup_check_delay)
            if received:
                break
        assert received, "error during startup and connect"

    def zmq_context(self):
        return self.zmq_broker.context

    def zmq_config(self):
        return settings

    def _cleanup(self):
        if self._cleanup_called:
            return

        # this is a bit hacky, we always want the broker to stop first so the lingering
        # socket detection works properly, but this is not possible if the testcase fails
        # during setup. in this case the cleanup is run via cleanup at the end
        if self.zmq_client:
            self.zmq_client.stop()

        if self.zmq_broker:
            self.zmq_broker.stop()

        self._cleanup_called = True

    def tearDown(self):
        assert hasattr(self, "zmq_client"), (
            "testcase has no zmq_client member, did you forget to call super().setUp()?"
        )
        self._cleanup()
        super(ZMQTestMixin, self).tearDown()
        Schema.to_file()

    def rpc(self, channel: str, type: str, request, timeout=3, receive_response=True, resource=None) \
            -> Union[str, dict]:
        """
        :return: the rpc id, which can be used with `receive_rpc` to receive the response async if `receive_response` is set to False
        :return: the rpc response as a dictionary if `receive_response` is set to True
        """
        rpc_id = str(uuid4())
        rpc_request = _TestRPCRequest(name="testclient", type=type, rpc_id=rpc_id,
                                      resource=resource, request=request)
        self.zmq_client.send(f"rpc-req-{channel}".encode("ascii"), rpc_request)
        if receive_response:
            return self.receive_rpc_response(channel, rpc_id, timeout=timeout)
        else:
            return rpc_id

    def receive_rpc_response(self, channel: str, rpc_id: str, timeout=3) -> dict:
        response_topic = f"rpc-rep-{channel}".encode("ascii")
        if response_topic not in self.zmq_client.subscribed_topics:
            raise DeveloperError(
                "you have to list the rpc channels you want to use beforehand. please set:\n"
                f'  > rpc_channels = ["{channel}"] in your test class '
            )
        _, response = self.zmq_client.wait_for_message(
            filter=lambda topic, message: topic == response_topic and message.get("rpc_id") == rpc_id,
            timeout=timeout
        )
        return response

    def assertRPCFailure(self, response: dict, expected_status="error"):
        self.assertEqual(expected_status, response.get("response", {}).get("status"),
                         msg=f"Expected status to not be ok, got {response.get('response')}")

    def assertRPCSuccess(self, response: dict):
        self.assertEqual("ok", response.get("response", {}).get("status"),
                         msg=f"Expected status to be ok, got {response.get('response')}")

    def assertSubscription(self, *topics: bytes):
        assert all((x in self.zmq_client.subscribed_topics) for x in topics), (
            f"some test functions require topics {b', '.join(topics).decode()}, please set "
            f"""topics = [{', '.join(f'"{x}"' for x in topics)}] in your test class"""
        )
