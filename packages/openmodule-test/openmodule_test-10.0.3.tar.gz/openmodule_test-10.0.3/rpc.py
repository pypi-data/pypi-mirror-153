import random
import string
import threading
import time
from contextlib import suppress
from functools import partial

from pydantic.main import BaseModel

from openmodule_test.zeromq import ZMQTestMixin


class _EmptyModel(BaseModel):
    pass


class RPCServerTestMixin(ZMQTestMixin):
    def wait_for_rpc_response(self, channel: str, type: str, request: BaseModel):
        """
        waits until a rpc server is responding to the channel/type
        """
        for x in range(self.zmq_client.startup_check_iterations):
            try:
                self.rpc(channel, type, request, timeout=0.1)
                return
            except TimeoutError:
                pass

            time.sleep(self.zmq_client.startup_check_delay)

        assert False, "error during startup and connect"

    def wait_for_rpc_server(self, server):
        message_received = False

        def handler(_, __):
            nonlocal message_received
            message_received = True

        """
        waits until a rpc server is responding on the last channel we registered
        this assumes that the subscription we issue is the last and if it is connected, 
        all previous subscriptions will also be connected
        """
        assert server.handlers, "you need to register the handlers beforehand"
        random_channel = "_test" + "".join(random.choices(string.ascii_letters, k=10))

        server.register_handler(random_channel, "ping", _EmptyModel, _EmptyModel, handler, register_schema=False)

        for x in range(self.zmq_client.startup_check_iterations):
            self.rpc(random_channel, "ping", {}, receive_response=False)
            time.sleep(self.zmq_client.startup_check_delay)
            if message_received:
                break

        assert message_received, "error during startup and connect"
