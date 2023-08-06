from collections import defaultdict
from datetime import datetime
from typing import Callable, Dict, Optional

from openmodule.models.base import Gateway
from openmodule.models.io import IoMessage, IoState


def generate_example_states(count: Optional[int] = 8) -> Dict[str, IoState]:
    """
    Creates a dict with pin as key and IoState as value.
    param count: how many pins should be created.
    Each gateway has 4 pins: gate_x_button, gate_x_cloop, gate_x_ploop, gate_x_gate (this is the only output type)
    Gateways with even x have direction in, odds have out.
    All pins created low and not inverted.
    """
    states: Dict[str, IoState] = defaultdict(IoState)
    for i in range(count):
        gate = int(i/4)
        direction = "in" if gate % 2 == 0 else "out"
        gateway = Gateway(gate="gate_{}".format(gate), direction=direction)
        state = IoState(pin="", gateway=gateway, value=0, physical=0, inverted=False, type="input",
                        last_timestamp=datetime.utcnow())
        if i % 4 == 0:
            state.pin = "gate_{}_button".format(gate)
        elif i % 4 == 1:
            state.pin = "gate_{}_cloop".format(gate)
        if i % 4 == 2:
            state.pin = "gate_{}_ploop".format(gate)
        if i % 4 == 3:
            state.type = "output"
            state.pin = "gate_{}_gate".format(gate)
        states[state.pin] = state
    return states


class IoSimulator:
    """
    IOSimulator
    Creates virtual gates and has a change_gate_state function for opening/closing
    param states: a dict of all pins and their IoState
    param emit: the function that will be called to send a message

    **Note:**
    There can be a race condition during init if the emitted messages have not yet been received by
    an io handler. See tests.test_io_listen.IoTest's comment in setUp()
    """
    def __init__(self, states: Dict[str, IoState], emit: Callable[[IoMessage], None]):
        self.pin_states = states
        self.emit = emit
        for state in self.pin_states.values():
            self.emit(IoMessage(gateway=state.gateway, type=state.type, pin=state.pin, value=state.value,
                                inverted=state.inverted, physical=state.physical, edge=1))

    def get_pin_states(self) -> Dict[str, IoState]:
        return self.pin_states

    def change_pin_sate(self, pin: str):
        self._emit(pin, 1 - self.pin_states[pin].value)

    def emit_current_pin_state(self, pin: str):
        self._emit(pin, self.pin_states[pin].value)

    def set_all_pins_low(self):
        for pin in self.pin_states:
            self._emit(pin, 0)

    def set_pin_low(self, pin: str):
        self._emit(pin, 0)

    def set_all_pins_high(self):
        for pin in self.pin_states:
            self._emit(pin, 1)

    def set_pin_high(self, pin: str):
        self._emit(pin, 1)

    def emit_custom_io_message(self, pin: str, value: int = None, physical: int = None, inverted: bool = None,
                               edge: int = None):
        state = self.pin_states[pin]
        if edge is None:
            if state.value != value or state.is_inverted != inverted:
                edge = 1
            else:
                edge = 0
        state.value = value if value is not None else state.value
        state.physical = physical if physical is not None else state.physical
        state.inverted = inverted if inverted is not None else state.inverted
        self.emit(IoMessage(gateway=state.gateway, type=state.type, pin=state.pin, value=state.value,
                            inverted=state.inverted, physical=state.physical, edge=edge))

    def _emit(self, pin: str, value: int):
        state = self.pin_states[pin]
        edge = 0 if value == state.value else 1
        state.value = value
        state.physical = value if state.inverted else 1 - value
        self.emit(IoMessage(gateway=state.gateway, type=state.type, pin=state.pin, value=state.value,
                            inverted=state.inverted, physical=state.physical, edge=edge))
