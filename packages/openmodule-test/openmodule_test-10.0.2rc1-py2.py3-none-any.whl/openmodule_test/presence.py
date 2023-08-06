import random
import time
from datetime import datetime
from typing import Optional, Callable

from openmodule.models.base import Direction, Gateway, datetime_to_timestamp
from openmodule.models.presence import PresenceBaseMessage, PresenceEnterMessage, PresenceLeaveMessage, \
    PresenceForwardMessage, PresenceBackwardMessage, PresenceMedia, PresenceChangeMessage
from openmodule.models.vehicle import LPRMedium, LPRCountry, Medium, Vehicle, MakeModel, PresenceAllIds, EnterDirection


class VehicleBuilder:
    vehicle_id: int
    medium: PresenceMedia

    def __init__(self):
        self.vehicle_id = int(time.time() * 1e9) + random.randint(0, 1000000)
        self.medium = PresenceMedia()
        self.make_model = MakeModel(make="UNKNOWN", make_confidence=0.7, model="UNKNOWN", model_confidence=-1.0)
        self.enter_direction = EnterDirection.unknown

    def vehicle(self) -> Vehicle:
        return Vehicle(
            id=self.vehicle_id,
            lpr=self.medium.lpr,
            qr=self.medium.qr,
            nfc=self.medium.nfc,
            pin=self.medium.pin,
            make_model=self.make_model,
            enter_direction=self.enter_direction
        )

    def id(self, id: int) -> 'VehicleBuilder':
        self.vehicle_id = id
        return self

    def lpr(self, country, plate=None) -> 'VehicleBuilder':
        if country is None:
            self.medium.lpr = None
        else:
            self.medium.lpr = LPRMedium(
                id=plate,
                country=LPRCountry(code=country)
            )
        return self

    def nfc(self, id) -> 'VehicleBuilder':
        if id is None:
            self.medium.nfc = id
        else:
            self.medium.nfc = Medium(id=id, type="nfc")
        return self

    def qr(self, id) -> 'VehicleBuilder':
        if id is None:
            self.medium.qr = id
        else:
            self.medium.qr = Medium(id=id, type="qr")
        return self

    def pin(self, id) -> 'VehicleBuilder':
        if id is None:
            self.medium.pin = id
        else:
            self.medium.pin = Medium(id=id, type="pin")
        return self

    def set_make_model(self, make_model) -> 'VehicleBuilder':
        self.make_model = make_model
        return self

    def set_enter_direction(self, enter_direction: EnterDirection) -> 'VehicleBuilder':
        self.enter_direction = enter_direction
        return self


class PresenceSimulator:
    current_present: Optional[VehicleBuilder] = None

    def __init__(self, gate: str, direction: Direction, emit: Callable[[PresenceBaseMessage], None],
                 present_area_name: Optional[str] = None):
        self.gateway = Gateway(gate=gate, direction=direction)
        self.emit = emit
        self.present_area_name = present_area_name or f"{self.gateway.gate}-present"

    def vehicle(self):
        return VehicleBuilder()

    def _common_kwargs(self, vehicle):
        timestamp = datetime_to_timestamp(datetime.utcnow())
        all_ids = PresenceAllIds(lpr=None if vehicle.medium.lpr is None else [vehicle.medium.lpr],
                                 qr=None if vehicle.medium.qr is None else [vehicle.medium.qr],
                                 nfc=None if vehicle.medium.nfc is None else [vehicle.medium.nfc],
                                 pin=None if vehicle.medium.pin is None else [vehicle.medium.pin])
        return {
            "vehicle_id": vehicle.vehicle_id,
            "present-area-name": self.present_area_name,
            "last_update": timestamp,
            "name": "presence-sim",
            "source": self.gateway.gate,
            "gateway": self.gateway,
            "medium": vehicle.medium,
            "make_model": vehicle.make_model,
            "all_ids": all_ids,
            "enter_direction": vehicle.enter_direction
        }

    def enter(self, vehicle: VehicleBuilder):
        if self.current_present:
            self.leave()
        self.current_present = vehicle
        self.emit(PresenceEnterMessage(**self._common_kwargs(vehicle)))

    def leave(self):
        self.emit(PresenceLeaveMessage(**self._common_kwargs(self.current_present)))
        temp = self.current_present
        self.current_present = None
        return temp

    def forward(self, vehicle: Optional[VehicleBuilder] = None):
        assert vehicle or self.current_present, "a vehicle must be present, or you have to pass a vehicle"
        if not vehicle:
            vehicle = self.leave()
        self.emit(PresenceForwardMessage(
            **self._common_kwargs(vehicle),
            **{"leave-time": datetime_to_timestamp(datetime.utcnow())}
        ))

    def backward(self, vehicle: Optional[VehicleBuilder] = None):
        assert vehicle or self.current_present, "a vehicle must be present, or you have to pass a vehicle"
        if not vehicle:
            vehicle = self.leave()
        self.emit(PresenceBackwardMessage(
            **self._common_kwargs(vehicle),
            **{"leave-time": datetime_to_timestamp(datetime.utcnow())}
        ))

    def change(self, vehicle: VehicleBuilder):
        assert self.current_present, "a vehicle must be present"
        assert self.current_present.id == vehicle.id, "vehicle id must stay the same"
        self.current_present = vehicle
        self.emit(PresenceChangeMessage(
            **self._common_kwargs(vehicle),
        ))

    def change_before_enter(self, vehicle: VehicleBuilder):
        if self.current_present:
            self.leave()
        self.current_present = vehicle
        self.emit(PresenceChangeMessage(**self._common_kwargs(vehicle)))

    def change_vehicle_and_id(self, vehicle: VehicleBuilder):
        assert self.current_present, "a vehicle must be present"
        assert self.current_present.id != vehicle.id, "vehicle id must change"
        self.current_present = vehicle
        self.emit(PresenceChangeMessage(
            **self._common_kwargs(vehicle),
            change_vehicle_id=True
        ))
