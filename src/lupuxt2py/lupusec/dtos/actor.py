import datetime
from abc import ABC, abstractmethod
from datetime import datetime


class Entity(ABC):

    def __init__(self):
        self.__currentTime = datetime.utcnow()

    @property
    @abstractmethod
    def identifier(self) -> str:
        pass

    @property
    @abstractmethod
    def state(self) -> str:
        pass

    @property
    def time_stamp(self) -> datetime:
        return self.__currentTime


class Actor(Entity, ABC):

    @property
    @abstractmethod
    def type_of(self) -> int:
        pass

    @property
    @abstractmethod
    def friendly_name(self) -> str:
        pass


class SensorActor(Actor, ABC):

    @property
    @abstractmethod
    def battery_in_percent(self) -> str:
        pass
