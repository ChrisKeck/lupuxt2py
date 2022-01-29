import logging
from typing import TypeVar, Dict

from domain.sensors import *
from domain.switchs import *
from lupusec.dtos.actor import Actor, Entity
from lupuxt2py.domain.conversionable import Conversable

_LOGGER = logging.getLogger(__name__)
K = TypeVar("K")
V = TypeVar("V")


def get_item(key: K, container: Dict[K, V], default_value: V = None) -> V:
    if key in container:
        return container[key]
    return default_value


_devices_from_sensor_switch = {
    4: lambda act, lst, service: list([BinarySensor(act, lst, service)]),
    33: lambda act, lst, service: list([BinarySensor(act, lst, service)]),
    9: lambda act, lst, service: list([BinarySensor(act, lst, service)]),
    11: lambda act, lst, service: list([BinarySensor(act, lst, service)]),
    5: lambda act, lst, service: list([BinarySensor(act, lst, service)])
}

_device_from_sensor_switch = {
    24: lambda act, service: Switch(act, service),
    81: lambda act, service: Switch(act, service),
    48: lambda act, service: Switch(act, service),
    74: lambda act, service: Light(act, service)
}


def convert_move_state(act: Actor, logs: List[Entity], opts: dict) -> str:
    logs.sort(key=lambda x: x.time, reverse=True)
    match_found: bool = False
    for row in logs:
        if row.identifier == act.identifier and \
                (row.state.startswith("{ALARM_HISTORY_20}") or
                 row.state.startswith("{ALARM_HISTORY_183}")) and \
                act.time_stamp.__sub__(row.time_stamp).total_seconds() <= opts["motionDetectionDuration"]:
            match_found = True
            break
    if match_found:
        return "ON"
    return "OFF"


def convert_open_state(act) -> str:
    if act.state == "{WEB_MSG_DC_OPEN}":
        return "ON"
    return "OFF"


def convert_smoke_state(act) -> str:
    if act.state == "{RPT_CID_111}":
        return "ON"
    return "OFF"


_state_from_actor_switch = {
    4: lambda act, lst, opts: convert_open_state(act),
    33: lambda act, lst, opts: convert_open_state(act),
    9: lambda act, lst, opts: convert_move_state(act, lst, opts),
    11: lambda act, lst, opts: convert_smoke_state(act)
}
_deviceclass_from_actor_switch = {
    4: DeviceClass.WINDOW,
    33: DeviceClass.WINDOW,
    9: DeviceClass.MOTION,
    11: DeviceClass.SMOKE,
    5: DeviceClass.MOISTURE
}


class ConversationService(Conversable):

    def __init__(self, motion_detection_duration: int, service: LupusecSevice):
        self.__motionDetectionDuration = motion_detection_duration
        self.__service = service

    def get_devices_from_sensor(self, actor: Actor, senrows: List[Entity] = None) -> List[Device]:
        if senrows is None:
            senrows: List[Entity] = list()
        results: List[Device] = list()
        if actor.type_of in [24, 48, 74, 57]:
            _LOGGER.info("This is already a device like a switch or light! %s", actor.friendly_name)
        elif actor.type_of in [54, 46, 45, 37, 22]:
            _LOGGER.info("humidity-sensor, temperature-sensor, outdoor/indoor hooter, keypad and state-viewer need to be integrated %s", actor.friendly_name)
        else:
            result = get_item(actor.type_of, _devices_from_sensor_switch, lambda act, lst, service: list())
            results.extend(result(actor, senrows, self))
        return results

    def get_device_from_switch(self, actor: Actor) -> Switch:
        if actor.type_of in [57]:
            _LOGGER.info("NotSupportedType!")
            return None
        _LOGGER.info("get_device_from_switch %s", repr(actor.friendly_name))
        it = get_item(actor.type_of, _device_from_sensor_switch, lambda act: None)
        return it(actor, self.__service)

    def get_devices_class(self, actor: Actor) -> DeviceClass:
        result: DeviceClass = get_item(actor.type_of, _deviceclass_from_actor_switch, DeviceClass.UNKNOWN)
        return result

    def get_state_by_actor(self, actor: Actor, logrows: List[Entity]) -> str:
        result = get_item(actor.type_of, _state_from_actor_switch, lambda act, lst: "OFF")
        return result(actor, logrows, {"motionDetectionDuration": self.__motionDetectionDuration})
