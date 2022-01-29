from typing import List

from lupuxt2py.domain.conversionable import Conversable
from lupuxt2py.domain.device import Getable, Device, DeviceClass, Component
from lupuxt2py.lupusec.dtos.actor import SensorActor
from lupuxt2py.lupusec.dtos.record_list import Logrow


class BinarySensor(Device, Getable):
    def __init__(self, actor: SensorActor, logrows: List[Logrow], service: Conversable):
        super().__init__(actor)
        if logrows is None:
            logrows: List[Logrow] = list()
        self.__logrows = logrows
        self.__service = service
        self.__battery_by_actor = actor.battery_in_percent

    @property
    def state(self) -> str:
        return self.__service.get_state_by_actor(self._actor, self.__logrows)

    @property
    def component(self) -> Component:
        return Component.BINARY_SENSOR

    @property
    def battery(self) -> str:
        return self.__battery_by_actor

    @property
    def device_class(self) -> DeviceClass:
        return self.__service.get_devices_class(self._actor)
