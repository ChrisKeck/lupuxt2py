from lupuxt2py.domain.device import Setable, Device, Component, DeviceClass
from lupuxt2py.lupusec.dtos.actor import Actor
from lupuxt2py.lupusec.lupusec_service import LupusecSevice


def is_on(state: str) -> bool:
    return "ON" == str(state).upper()


class Switch(Device, Setable):

    def __init__(self, actor: Actor, lupu_service: LupusecSevice):
        super().__init__(actor)
        self.__lupu_service = lupu_service

    @property
    def component(self) -> Component:
        return Component.SWITCH

    @property
    def device_class(self) -> DeviceClass:
        return DeviceClass.SWITCH

    @property
    def state(self) -> str:
        if "{WEB_MSG_PSS_ON}" in self._actor.state:
            return "ON"
        else:
            return "OFF"

    @state.setter
    def state(self, state: str):
        self.__lupu_service.post_switch_list(is_on(state), self.unique_id)


class Light(Switch):
    def __init__(self, actor: Actor, service: LupusecSevice):
        super().__init__(actor, service)

    @property
    def component(self) -> Component:
        return Component.LIGHT

    @property
    def device_class(self) -> DeviceClass:
        return DeviceClass.LIGHT

    @property
    def state(self) -> str:
        if "{WEB_MSG_DIMMER_ON}" in self._actor.state:
            return "ON"
        else:
            return "OFF"
