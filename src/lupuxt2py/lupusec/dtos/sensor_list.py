# Generated by https://quicktype.io
#
# To change quicktype's target language, run command:
#
#   "Set quicktype target language"
from dataclasses import dataclass
from enum import Enum
from typing import List

from lupuxt2py.lupusec.dtos.actor import SensorActor


class Status(Enum):
    EMPTY = ""
    WEB_MSG_DC_CLOSE = "{WEB_MSG_DC_CLOSE}"
    WEB_MSG_DC_OPEN = "{WEB_MSG_DC_OPEN}"
    WEB_MSG_PSS_OFF = "{WEB_MSG_PSS_OFF}"
    WEB_MSG_PSS_ON = "{WEB_MSG_PSS_ON}"


@dataclass(init=False)
class Senrow(SensorActor):
    type: int
    name: str
    battery_ok: int
    sid: str
    status: str

    @property
    def identifier(self) -> str:
        return self.sid

    @property
    def type_of(self) -> int:
        return self.type

    @property
    def state(self) -> str:
        return self.status

    @property
    def friendly_name(self) -> str:
        return self.name

    @property
    def battery_in_percent(self) -> str:
        if self.battery_ok == 1:
            return "100%"
        return "0%"


@dataclass(frozen=True)
class SensorList:
    senrows: List[Senrow]