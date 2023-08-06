import time
from _weakrefset import WeakSet

from openmodule.dispatcher import MessageDispatcher
from openmodule.models.base import Direction, Gateway, OpenModuleModel
from openmodule_test.utils import DeveloperError


class TestGateAccessMessage(OpenModuleModel):
    gateway: Gateway


_all_gates = WeakSet()


class TestGate:
    __test__ = False

    _wait_sleep = 0.05
    _wait_called_since_reset = False

    open_count = 0
    reject_count = 0

    def __init__(self, gate: str, direction: Direction, dispatcher: MessageDispatcher):
        self.gate = gate
        self.direction = direction
        dispatcher.register_handler(b"access_accept", TestGateAccessMessage, self._access_accept,
                                    register_schema=False, match_type=False)
        dispatcher.register_handler(b"access_reject", TestGateAccessMessage, self._access_reject,
                                    register_schema=False, match_type=False)
        _all_gates.add(self)

    @classmethod
    def reset_all_counts(cls):
        for x in _all_gates:
            x.reset_call_count()

    def reset_call_count(self):
        self.open_count = 0
        self.reject_count = 0
        self._wait_called_since_reset = False

    def _access_accept(self, message: TestGateAccessMessage):
        if message.gateway.gate == self.gate:
            self.open_count += 1

    def _access_reject(self, message: TestGateAccessMessage):
        if message.gateway.gate == self.gate:
            self.reject_count += 1

    def assert_opened(self):
        assert self.open_count > 0

    def assert_rejected(self):
        assert self.open_count == 0 and self.reject_count > 0

    def wait_for_open(self, timeout: float = 3, minimum_open_count=1):
        self._wait_for("open_count", timeout=timeout, minimum_count=minimum_open_count)

    def wait_for_reject(self, timeout: float = 3, minimum_open_count=1):
        self._wait_for("reject_count", timeout=timeout, minimum_count=minimum_open_count)
        try:
            # we always wait half as long for any open messages which may arrive late, so the sequence
            # Reject -> Accept, does correctly raise a TimeoutError
            self._wait_called_since_reset = False
            self.wait_for_open(timeout=timeout / 2)
        except TimeoutError:
            pass
        self.assert_rejected()

    def _wait_for(self, var_name: str, timeout: float = 3, minimum_count=1):
        if self._wait_called_since_reset:
            # Explanation? -> see MockEvent.wait_for_call
            raise DeveloperError(
                "The test-case MUST reset the call count to zero on its own before calling wait_for_call.\n"
                "This is in order to prevent a race-condition which is impossible to prevent otherwise.\n"
                "Please call `.reset_counts()` or `TestGate.reset_all_counts()`"
            )
        self._wait_called_since_reset = True
        for x in range(int(timeout // self._wait_sleep)):
            time.sleep(self._wait_sleep)
            if getattr(self, var_name) >= minimum_count:
                return
        if getattr(self, var_name) < minimum_count:
            raise TimeoutError()
