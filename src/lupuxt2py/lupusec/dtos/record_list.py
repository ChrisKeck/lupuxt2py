# Generated by https://quicktype.io
#
# To change quicktype's target language, run command:
#
#   "Set quicktype target language"
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from lupuxt2py.lupusec.dtos.actor import Entity


class Event(Enum):
    ALARM_HISTORY_1832 = "{ALARM_HISTORY_183}\t2"
    ALARM_HISTORY_202 = "{ALARM_HISTORY_20}\t2"
    ALARM_HISTORY_42 = "{ALARM_HISTORY_4}\t2"


@dataclass(init=False)
class Logrow(Entity):
    time: int
    sid: str
    event: str

    @property
    def identifier(self) -> str:
        return self.sid

    @property
    def state(self) -> str:
        return self.event

    @property
    def time_stamp(self) -> datetime:
        return datetime.utcfromtimestamp(self.time)


@dataclass(init=False)
class RecordList:
    logrows: List[Logrow]
