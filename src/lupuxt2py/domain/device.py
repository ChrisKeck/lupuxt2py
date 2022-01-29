from abc import ABC, abstractmethod
from enum import Enum

from lupuxt2py.lupusec.dtos.actor import Actor


class DeviceClass(Enum):
    POWER = "power"
    LIGHT = "light"
    SWITCH = "switch"
    UNKNOWN = "unkown"
    SAFETY = "safety",
    HUMIDITY = "humidity",
    TEMPERATURE = "temperature",
    WINDOW = "window",
    MOTION = "motion",
    SMOKE = "smoke",
    MOISTURE = "moisture"


class Component(Enum):
    ALARM_CONTROL_PANEL = "alarm_control_panel",
    BINARY_SENSOR = "binary_sensor",
    SENSOR = "sensor",
    LIGHT = "light",
    LOCK = "lock",
    SWITCH = "switch"


class Getable(ABC):
    @property
    @abstractmethod
    def state(self) -> str:
        pass

    @property
    @abstractmethod
    def unique_id(self) -> str:
        pass


class Setable(Getable, ABC):
    @property
    @abstractmethod
    def state(self) -> str:
        pass

    @state.setter
    @abstractmethod
    def state(self, state: str) -> None:
        pass


class Device(ABC):
    def __init__(self, actor: Actor):
        self.__actor = actor

    @property
    def _actor(self) -> Actor:
        return self.__actor

    @property
    def name(self) -> str:
        return self.__actor.friendly_name

    @property
    def unique_id(self) -> str:
        return self.__actor.identifier

    @property
    @abstractmethod
    def component(self) -> Component:
        pass

    @property
    @abstractmethod
    def device_class(self) -> DeviceClass:
        pass
