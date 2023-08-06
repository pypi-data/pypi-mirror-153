import time
import warnings
from _weakrefset import WeakSet
from unittest.mock import Mock

from openmodule_test.utils import DeveloperError

_all_mocks = WeakSet()


class MockEvent(Mock):
    _wait_sleep = 0.05
    _wait_called_since_reset = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _all_mocks.add(self)

    @classmethod
    def reset_all_call_counts(cls):
        warnings.warn(
            '\n\n`.reset_all_call_counts()` is deprecated, please switch to using `.reset_all_mocks()``\n',
            DeprecationWarning
        )
        cls.reset_all_mocks()

    @classmethod
    def reset_all_mocks(cls, visited=None, *, return_value=False, side_effect=False):
        for x in _all_mocks:
            x.reset_mock(visited, return_value=return_value, side_effect=side_effect)

    def reset_call_count(self):
        warnings.warn(
            '\n\n`.reset_call_count()` is deprecated, please switch to using `.reset_mock()``\n',
            DeprecationWarning
        )
        self.reset_mock()

    def reset_mock(self, visited=None, *, return_value=False, side_effect=False):
        self._wait_called_since_reset = False
        super().reset_mock(visited, return_value=return_value, side_effect=side_effect)

    def wait_for_call(self, *, timeout=3, minimum_call_count=1):
        if self._wait_called_since_reset:
            raise DeveloperError(
                "The test-case MUST reset the call count to zero on its own before calling wait_for_call.\n"
                "This is in order to prevent a race-condition which is impossible to prevent otherwise.\n"
                "Please call `.reset_call_count()` or `MockEvent.reset_all_call_counts()`"
            )
        """
        Explanation: Take the following code for example
        ```
        1:  self.zmq_client.send("some-message")
        2:  self.my_event.wait_for_call()
        3:  self.zmq_client.send("some-message")
        4:  self.my_event.wait_for_call()
        ```
        If the unit-test thread is scheduled away after 3, and the mock event is called before 4
        the mock event CANNOT possibly know if it's call count is at 1 because it has been called
        by the event triggered in line 1, or by the event triggered in line 3. Also resetting the 
        call count at the start of `.wait_for_call()` would not help, because in line 4, the call
        count is already at 2, and thus producing an incorrect timeout error.
        
        Only the developer knows what the earliest possible time is that an event can trigger, and
        then has to reset the call count one line before. In the case above between line 2 and 3
        """
        self._wait_called_since_reset = True
        for x in range(int(timeout // self._wait_sleep)):
            time.sleep(self._wait_sleep)
            if self.call_count >= minimum_call_count:
                return
        if self.call_count < minimum_call_count:
            raise TimeoutError()
