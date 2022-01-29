import logging
from typing import Any, List

import jsons
import requests
from requests import Response

from lupuxt2py.constants import urlrecordListGet, urlDevicePSSListGet, urlDeviceListGet, urlPanelCondGet
from lupuxt2py.lupusec.dtos.actor import Actor, Entity, SensorActor
from lupuxt2py.lupusec.dtos.panel_condition import PanelCondition, AlarmMode
from lupuxt2py.lupusec.dtos.power_switch_list import PowerSwitchList
from lupuxt2py.lupusec.dtos.record_list import RecordList
from lupuxt2py.lupusec.dtos.sensor_list import SensorList

_LOGGER = logging.getLogger(__name__)


def extract_text(text: str):
    return text.replace("\n", "").replace("\t", "").replace("\r", "")


class LupusecSevice:
    """Interface to Lupusec Webservices."""

    def __init__(self, username, password, ip_address):
        """LupsecAPI constructor requires IP and credentials to the
        Lupusec Webinterface.
        """
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.api_url = "http://{}".format(ip_address)
        self.headers = {}
        token = self.__get_token()

        self.headers = {"X-Token": token}

    """action/deviceListGet"""

    def get_sensor_list(self) -> List[SensorActor]:
        response = self.__get_request(urlDeviceListGet)
        text = response.text
        _LOGGER.info("Antwort von Lupusec %s:\n%s", urlDeviceListGet, text)
        lst = jsons.loads(extract_text(text), SensorList)

        return lst.senrows

    """ public async Task<PanelCondition> GetpowerswitchesAsync()"""

    def get_switch_list(self) -> List[Actor]:
        response = self.__get_request(urlDevicePSSListGet)
        text = response.text
        _LOGGER.info("Antwort von Lupusec %s:\n%s", urlDevicePSSListGet, text)
        lst = jsons.loads(extract_text(text), PowerSwitchList)
        return lst.pssrows

    """ public async Task<RecordList> GetRecordsAsync()"""

    def get_record_list(self) -> List[Entity]:
        response = self.__get_request(urlrecordListGet)
        text = response.text
        _LOGGER.info("Antwort von Lupusec %s:\n%s", urlrecordListGet, text)
        lst = jsons.loads(extract_text(text), RecordList)
        return lst.logrows

    """ public async Task<PanelCondition> GetPanelConditionAsync()"""

    def get_panel_condition(self) -> PanelCondition:
        response = self.__get_request(urlPanelCondGet)
        text = response.text
        _LOGGER.info("Antwort von Lupusec %s:\n%s", urlPanelCondGet, text)
        return jsons.loads(extract_text(text), PanelCondition)

    """ic async Task<ActionResult> SetAlarmMode(int area, AlarmMode """

    def post_alarm_mode(self, area: int, alarmMode: AlarmMode) -> None:
        self.__post_request('/action/panelCondPost',
                            {"area": str(area), "mode": str(alarmMode.value)}
                            )

    """ic async Task<ActionResult> SetAlarmMode(int area, AlarmMode """

    def post_switch_list(self, onOff: bool, id: str) -> None:
        encodedFormParams = {"switch": str(onOff.__int__()),
                             "pd": "",
                             "id": id}
        self.__post_request('/action/deviceSwitchPSSPost', encodedFormParams)

    def __get_request(self, apiPart: str) -> Response:
        response = self.session.get(
            self.api_url + apiPart,
            timeout=15,
            headers=self.headers
        )
        return response

    def __post_request(self, apiPart: str, data: Any) -> Response:
        response = self.session.post(
            self.api_url + apiPart, timeout=15, headers=self.headers, data=data
        )
        return response

    def __get_token(self) -> str:
        response = self.session.get(
            self.api_url + '/action/tokenGet', timeout=15, headers=self.headers
        )
        return response.json()["message"]
