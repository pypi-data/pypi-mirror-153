from typing import Optional

from openmodule_test.zeromq import ZMQTestMixin


def _get_health_filter(name):
    return lambda topic, message: (topic == b"healthz") and \
                                  ("pong" in message) and \
                                  (name is None or message.get("name") == name)


class HealthTestMixin(ZMQTestMixin):
    def get_health(self, name: Optional[str] = None, timeout: float = 3):
        self.assertSubscription(b"healthz")
        self.zmq_client.send("healthz", {"type": "ping", "ping": "ping"})
        _, message = self.zmq_client.wait_for_message(
            _get_health_filter(name),
            timeout=timeout
        )
        return message

    def assertHealthOk(self, message):
        self.assertIn("pong", message)
        pong = message.get("pong", {})
        self.assertEqual("ok", pong.get("status"))

    def assertHealthError(self, message):
        self.assertIn("pong", message)
        pong = message.get("pong", {})
        self.assertEqual("error", pong.get("status"))

    def wait_for_health(self, name: Optional[str] = None):
        """
        :param name: if specified the function waits for a specific service name on startup
        """

        for x in range(self.zmq_client.startup_check_iterations):
            try:
                self.get_health(name, timeout=self.zmq_client.startup_check_delay)
            except TimeoutError:
                pass
            else:
                return

        assert False, f"health did not answer within " \
                      f"{self.zmq_client.startup_check_delay * self.zmq_client.startup_check_iterations} seconds"
