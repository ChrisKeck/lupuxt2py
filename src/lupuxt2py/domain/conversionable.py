from abc import abstractmethod, ABC
from typing import List

from lupuxt2py.domain.device import Device, DeviceClass
from lupuxt2py.domain.switchs import Switch
from lupuxt2py.lupusec.dtos.actor import Actor, Entity, SensorActor


class Conversable(ABC):

    @abstractmethod
    def get_devices_from_sensor(self, actor: SensorActor, logrows: List[Entity] = None) -> List[Device]:
        pass

    @abstractmethod
    def get_device_from_switch(self, actor: Actor) -> Switch:
        pass

    @abstractmethod
    def get_devices_class(self, actor: Actor) -> DeviceClass:
        pass

    @abstractmethod
    def get_state_by_actor(self, actor: Actor, logrows: List[Entity]) -> str:
        pass
