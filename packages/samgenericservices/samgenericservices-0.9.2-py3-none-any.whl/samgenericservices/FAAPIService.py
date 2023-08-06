# coding=utf-8
"""
FAAPIService
"""

from datetime import datetime, timedelta, tzinfo
from inspect import stack as i_stack
from json import dumps
from time import time
from traceback import format_exc
from typing import Any, Callable, Coroutine, Dict, List, Optional

import aiohttp
import bs4
from multidict import MultiDict
from viledatools import FARequests, getcookieval


class FAAPIService:
    """
    Base class to build FA API services
    """

    def __init__(self,
                 log: Callable[..., Coroutine[Any, Any, Any]],
                 vapp: str,
                 uagent: str):
        """
        Init the base class

        :param log: logger callable coroutine to use
        :param vapp: FA mobile API app version to use
        :param uagent: User-Agent string to use for mobile API
        """
        # Reference logging object of the caller
        self._base_log: Callable[..., Coroutine[Any, Any, Any]] = log
        # FA mobile API version
        self._vapp = vapp
        # FA mobile API standard headers to provide
        self._app_headers = {"version":    vapp,
                             "Accept":     "*/*",
                             "User-Agent": uagent
                             }
        # Multiple client sessions
        self._s: Dict[str, Any] = dict()
        # FA web api time reg draw counter
        self._fa_api_draw = 1

    def _faapp_get_session_name(self, domain: str, usr: str) -> str:
        """
        Generate aiohttp session name and create the session itself for FA mobile API to persist it

        :param domain: FA domain name
        :param usr: FA user login name
        :return: generated aiohttp session name to persiste the session in self._s
        """
        _s_name = f"app-{domain}-{usr}".lower()
        if _s_name not in self._s.keys():
            self._s[_s_name] = aiohttp.ClientSession()
        return _s_name

    def _faweb_get_session_name(self, domain: str, usr: str) -> str:
        """
        Generate aiohttp session name and create the session itself for FA web API to persist it

        :param domain: FA domain name
        :param usr: FA user login name
        :return: generated aiohttp session name to persiste the session in self._s
        """
        _s_name = f"web-{domain}-{usr}".lower()
        if _s_name not in self._s.keys():
            self._s[_s_name] = aiohttp.ClientSession()
        return _s_name

    async def faweb_login(self, domain: str, usr: str, pwd: str) -> Optional[bool]:
        """
        Login to FA web API, keep session, and return True if successful

        :param domain: FA domain name
        :param usr: FA user login name
        :param pwd: FA password
        :return: True if successful, None or False if not
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            r = await self._s[_s_name].head(f"https://{domain}.facilityapps.com/login")
            await self._base_log(i_stack(),
                                 "debug",
                                 (f"OK got init XSRF-TOKEN cookie = "
                                  f"{getcookieval(self._s[_s_name], 'XSRF-TOKEN')} from {r.url.path}"))
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/login",
                                            data={"_token":   getcookieval(self._s[_s_name], "XSRF-TOKEN"),
                                                  "username": usr,
                                                  "password": pwd,
                                                  "submit":   str()
                                                  })
            if getcookieval(self._s[_s_name], "laravel_token") and (r.url.path == "/site_manager/view"):
                # Successfully authenticated
                # Log the OK
                await self._base_log(i_stack(), "info", (f"OK logged in to {r.url.path} -> {r.content_type} "
                                                         f"[{r.content_length}B] redirects counted: {len(r.history)}"))
                #
                return True
            else:
                await self._base_log(i_stack(), "error", (f"FAILED to log in web API, redirected to {r.url.path} "
                                                          f"redirects counted: {len(r.history)}"))
                return False
        except aiohttp.ClientResponseError as _badstatus:
            await self._base_log(i_stack(), "debug", f"Full failed URL: {_badstatus.request_info.url}")
            await self._base_log(i_stack(), "error", f"Error {_badstatus.request_info.method} "
                                                     f"{_badstatus.request_info.url.path} - "
                                                     f"{_badstatus.status} {_badstatus.message}")
        return False

    async def faapp_login(self, domain: str, usr: str, pwd: str) -> Optional[Dict[str, Any]]:
        """
        Login to FA mobile app API and return the main user record

        :param domain: FA domain name
        :param usr: FA user login name
        :param pwd: FA password
        :return: dict with FA user full record
        """
        _form = {"T":           "LogIn_v2",
                 "username":    usr,
                 "password":    pwd,
                 "version":     self._vapp,
                 "mode":        "LogIn",
                 "auth_method": "basic"
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA mobile API login request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None

    async def faapp_get_forms(self, domain: str, usr: str, language: str, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Call FA mobile API GetChecklists and return result

        :param domain: FA domain name
        :param usr: FA user login name
        :param language: language code in form of en_EN to use for language and region form fields
        :param session_id: FA mobile API session_id
        :return: dict with FA API output of GetChecklists
        """
        _form = {"session_id":  session_id,
                 "T":           "GetChecklists",
                 "L":           language,
                 "region_code": language
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API GetChecklists request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None

    async def faweb_get_configview(self,
                                   domain: str,
                                   usr: str) -> Optional[Dict[str, Any]]:
        """
        Get the config parameters for enfironment for FA API domain

        :param domain: FA domain name
        :param usr: FA user login name
        :return: dict mapping user ID: site object
        """
        # Output dict
        _c = dict()
        _s_name = self._faweb_get_session_name(domain, usr)
        r = await self._s[_s_name].get(f"https://{domain}.facilityapps.com/system_configuration/view",
                                       headers={"Accept": "text/html, application/xhtml+xml"})
        if r.ok:
            _raw_html = await r.text()
        else:
            await self._base_log(i_stack(), "error",
                                 f"FAILED requesting system config for domain '{domain}' user '{usr}': "
                                 f"HTTP {r.status} {r.reason}")
            return None
        _strainer_tz = bs4.SoupStrainer(name="select", id="SystemConfiguration_timezone")
        _bs = bs4.BeautifulSoup(_raw_html, features="lxml", parse_only=_strainer_tz)
        _opts = _bs.find_all(name="option")
        for _o in _opts:
            if isinstance(_o.get("selected"), str):
                _c["tz"] = _o["value"]
        # _strainer_langs = bs4.SoupStrainer(name="select", id="SystemConfiguration_timezone")
        # bs = bs4.BeautifulSoup(await r.text(), features="lxml", parse_only=_strainer_langs)
        # _opts = bs.find_all(name="option")
        # for _o in _opts:
        #     if isinstance(_o.get("selected"), str):
        #         _c["tz"] = timezone(_o["value"])
        return _c

    async def faweb_logout(self, domain: str, usr: str) -> None:
        """
        Logout from FA web API for all accounts
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        r = await self._s[_s_name].get(f"https://{domain}.facilityapps.com/logout")
        if r.ok:
            await self._base_log(i_stack(), "info", f"OK logged out from domain '{domain}' user '{usr}'")
        else:
            await self._base_log(i_stack(), "info",
                                 f"FAILED logging out from domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}")

    async def faweb_get_timereg(self,
                                domain: str,
                                usr: str,
                                tbeg: datetime,
                                tend: datetime) -> Optional[List[Dict[str, Any]]]:
        """
        Get time registration data from the  FA web API for specified domain and time interval

        :param domain: FA domain name
        :param usr: FA user login name
        :param tbeg: date and time from which to select tasks
        :param tend: date and time till which to select tasks
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        # Check cookies
        if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
            raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/time_registration/data",
                                         headers={"Accept":       "application/json",
                                                  "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                  },
                                         params={"fields": FARequests.timeregquery()},
                                         data=FARequests.timeregform(self._fa_api_draw,
                                                                     tbeg,
                                                                     tend)) as r:
            self._fa_api_draw += 1
            if r.status == 200:
                _json = await r.json()
                return _json["data"]
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API time reg data request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return list()

    async def faweb_get_users_view(self,
                                   domain: str,
                                   usr: str) -> Optional[List[Dict[str, Any]]]:
        """
        Gets users view from FA web API

        :param domain: FA domain name
        :param usr: FA user login name
        :return: dict loaded from FA web API response JSON
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Get all users
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/users_manager/data",
                                            headers={"Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            params={"fields": FARequests.userquery()},
                                            data=FARequests.userform())
            if r.ok:
                _users_json = await r.json()
                return _users_json["data"]
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API user view request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error",
                                 f"FAILED faweb_get_users_view(): {format_exc().replace(chr(10), ' ')}")
            return None

    async def faweb_get_user_details(self,
                                     domain: str,
                                     usr: str,
                                     fauserid: int) -> Optional[Dict[str, Any]]:
        """
        Gets user details from FA web API

        :param domain: FA domain name
        :param usr: FA user login name
        :param fauserid: FA user id to get details for
        :return: user details parameters in dict
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Get user details
            r = await self._s[_s_name].get(f"https://{domain}.facilityapps.com/users_manager/details/{fauserid}",
                                           headers={"Accept": "text/html, application/xhtml+xml",
                                                    }
                                           )
            if r.ok:
                _bs = bs4.BeautifulSoup(await r.text(), features="lxml", parse_only=bs4.SoupStrainer(name="p"))
                return {"username": _bs.find(id="username").contents[0]
                        }
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API user details request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error",
                                 f"FAILED faweb_get_user_details(): {format_exc().replace(chr(10), ' ')}")
            return None

    async def faweb_get_sites_view(self,
                                   domain: str,
                                   usr: str) -> Optional[List[Dict[str, Any]]]:
        """
        Gets sites view from FA web API

        :param domain: FA domain name
        :param usr: FA user login name
        :return: dict loaded from FA web API response JSON
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Get all sites
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/site_manager/site_data",
                                            headers={"Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            params={"fields": FARequests.sitequery()},
                                            data=FARequests.siteform())
            if r.ok:
                _sites_json = await r.json()
                return _sites_json["data"]
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API site view request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error",
                                 f"FAILED faweb_get_sites_view(): {format_exc().replace(chr(10), ' ')}")
            return None

    # noinspection PyUnusedLocal
    async def faweb_get_spaces_view(self,
                                    domain: str,
                                    usr: str,
                                    sitename: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Gets spaces view from FA web API

        :param domain: FA domain name
        :param usr: FA user login name
        :param sitename: if given, then search for items only under this site name
        :return: list of dicts with spaces parameters loaded from FA web API JSON
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Get all spaces
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/floorplan/spaces/list",
                                            headers={"Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            params={"fields": FARequests.spacesquery()},
                                            data=FARequests.spacesform())
            if r.ok:
                _spaces_json = await r.json()
                _result = list()
                for _space in _spaces_json["data"]:
                    _bs_space = bs4.BeautifulSoup(_space["name"],
                                                  features="lxml",
                                                  parse_only=bs4.SoupStrainer(name="a"))
                    _result.append({"site_id":     int(_space["site.id"]),
                                    "floor_id":    int(_space["floor.id"]),
                                    "space_id":    _space["id"],
                                    "space_nr":    _space["nr"],
                                    "space_order": _space["order"],
                                    "space_name":  _bs_space.find_all(True)[0].contents[0]
                                    })
                return _result
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API spaces view request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error",
                                 f"FAILED faweb_get_spaces_view(): {format_exc().replace(chr(10), ' ')}")
            return None

    # noinspection PyUnusedLocal
    async def faweb_get_floors_view(self,
                                    domain: str,
                                    usr: str,
                                    sitename: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Gets floors view from FA web API

        :param domain: FA domain name
        :param usr: FA user login name
        :param sitename: if given, then search for items only under this site name
        :return: list of dicts with floors parameters loaded from FA web API JSON
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Get all floors
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/floorplan/floors/list",
                                            headers={"Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            params={"fields": FARequests.floorsquery()},
                                            data=FARequests.floorsform())
            if r.ok:
                _floors_json = await r.json()
                _result = list()
                for _floor in _floors_json["data"]:
                    _bs_floor = bs4.BeautifulSoup(_floor["name"],
                                                  features="lxml",
                                                  parse_only=bs4.SoupStrainer(name="a"))
                    _result.append({"site_id":     int(_floor["site.id"]),
                                    "floor_id":    _floor["id"],
                                    "floor_name":  _bs_floor.find_all(True)[0].contents[0],
                                    "floor_type":  _floor["type"],
                                    "floor_level": _floor["level"]
                                    })
                return _result
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API floors view request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error",
                                 f"FAILED faweb_get_floors_view(): {format_exc().replace(chr(10), ' ')}")
            return None

    async def faweb_get_tasks(self,
                              domain: str,
                              usr: str,
                              tbeg: datetime,
                              tend: datetime) -> Optional[List[Dict[str, Any]]]:
        """
        Gets all tasks for domain from FA web API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param tbeg: date and time from which to select tasks
        :param tend: date and time till which to select tasks
        :return: dict loaded from FA web API response JSON
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Get all tasks
            r = await self._s[_s_name].post((f"https://{domain}.facilityapps.com"
                                             f"/api/1.0/planning/data?fields={FARequests.tasksquery()}"),
                                            headers={"Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            data=FARequests.tasksform(1, tbeg, tend))
            if r.ok:
                _tasks_json = await r.json()
                return _tasks_json["data"]
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API tasks request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error", f"FAILED faweb_get_tasks(): {format_exc().replace(chr(10), ' ')}")
            return None

    async def faweb_send_push(self,
                              domain: str,
                              usr: str,
                              useridlist: List[int],
                              msg: str) -> None:
        """
        Gets all tasks for domain from FA web API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param useridlist: list of FA user IDs to whom to send push
        :param msg: message to send
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            _form = MultiDict([("_token", getcookieval(self._s[_s_name], "XSRF-TOKEN"))])
            for _recipient in useridlist:
                _form.add("recipients[]", str(int(_recipient)))
            _form.add("everyone", str())
            _form.add("pushContent", msg)
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/pushmessaging/send",
                                            headers={"Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            data=_form)
            if r.ok:
                pass
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API push message send request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
        except Exception as _exc:
            await self._base_log(i_stack(), "error", f"FAILED faweb_send_push(): {format_exc().replace(chr(10), ' ')}")

    async def faapp_task_begin(self,
                               domain: str,
                               usr: str,
                               language: str,
                               session_id: str,
                               siteid: int,
                               taskid: int,
                               taskseq: int,
                               stime: datetime) -> bool:
        """
        Set task to begin

        :param domain: FA domain name
        :param usr: FA user login name
        :param language: language code in form of en_EN to use for language and region form fields
        :param session_id: FA mobile API session_id
        :param siteid: FA backend site ID
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param stime: date and time to set status at
        :return: True if successful
        """
        _form = {"T":                "StartProgressOnTask",
                 "L":                language,
                 "FormData":         dumps({"task_id":            str(taskid),
                                            "sequence_number":    taskseq,
                                            "time_of_change":     str(int(stime.timestamp())),
                                            "latitude":           None,
                                            "longitude":          None,
                                            "time_registrations": None
                                            }, ensure_ascii=False),
                 "ReferenceId":      siteid,
                 "ReferenceType":    1,
                 "Timestamp":        int(stime.timestamp()),
                 "session_id":       session_id,
                 "AppVersionNumber": self._vapp,
                 "TaskData":         "null"
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API StartProgressOnTask request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return False

    async def faapp_task_set_status(self,
                                    domain: str,
                                    usr: str,
                                    session_id: str,
                                    taskid: int,
                                    taskseq: int,
                                    status: int,
                                    stime: datetime) -> bool:
        """
        Set status to task

        :param domain: FA domain name
        :param usr: FA user login name
        :param session_id: FA mobile API session_id
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param status: integer FA backend status to set
        :param stime: date and time to set status at
        :return: True if successful
        """
        _form = {"T":               "SetCalendarSubStatus",
                 "task_id":         taskid,
                 "sequence_number": taskseq,
                 "option":          status,
                 "latitude":        str(),
                 "longitude":       str(),
                 "timestamp":       int(stime.timestamp()),
                 "extra":           '{"clock_log_list":null}',
                 "session_id":      session_id
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API SetCalendarSubStatus request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return False

    async def faapp_task_chat(self,
                              domain: str,
                              usr: str,
                              language: str,
                              session_id: str,
                              siteid: int,
                              taskid: int,
                              taskseq: int,
                              msg: str,
                              fauserid: int,
                              dtz: tzinfo) -> bool:
        """
        Send chat message to the task

        :param domain: FA domain name
        :param usr: FA user login name
        :param language: language code in form of en_EN to use for language and region form fields
        :param session_id: FA mobile API session_id
        :param siteid: FA backend site ID
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param msg: text message to append to chat
        :param fauserid: FA user id under which to send message
        :param dtz: tzinfo time zone of the domain
        :return: True if successful
        """
        _time = int(time())
        _time_tz = datetime.fromtimestamp(_time, dtz)
        _form = {"T":                "SaveTaskMessage",
                 "L":                language,
                 "FormData":         dumps({"id":              0,
                                            "task_id":         taskid,
                                            "subtask_id":      None,
                                            "sequence_number": taskseq,
                                            "message":         msg,
                                            "user":            str(fauserid),
                                            "timestamp":       _time_tz.strftime("%Y-%m-%d %H:%M:%S"),
                                            "images":          []
                                            }, ensure_ascii=False),
                 "ReferenceId":      siteid,
                 "ReferenceType":    1,
                 "Timestamp":        _time,
                 "session_id":       session_id,
                 "AppVersionNumber": self._vapp,
                 "TaskData":         "null"
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API StartProgressOnTask request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return False

    async def faapp_task_drop_begin(self,
                                    domain: str,
                                    usr: str,
                                    language: str,
                                    session_id: str,
                                    siteid: int,
                                    taskid: int,
                                    taskseq: int,
                                    stime: datetime) -> bool:
        """
        Set task back to blue open state

        :param domain: FA domain name
        :param usr: FA user login name
        :param language: language code in form of en_EN to use for language and region form fields
        :param session_id: FA mobile API session_id
        :param siteid: FA backend site ID
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param stime: date and time to set status at
        :return: True if successful
        """
        _form = {"T":                "TaskToBacklog",
                 "L":                language,
                 "FormData":         dumps({"task_id":            str(taskid),
                                            "sequence_number":    taskseq,
                                            "time_of_change":     str(int(stime.timestamp())),
                                            "latitude":           None,
                                            "longitude":          None,
                                            "time_registrations": list()
                                            }, ensure_ascii=False),
                 "ReferenceId":      siteid,
                 "ReferenceType":    1,
                 "Timestamp":        int(stime.timestamp()),
                 "session_id":       session_id,
                 "AppVersionNumber": self._vapp,
                 "TaskData":         "null"
                 }
        _s_name = self._faapp_get_session_name(domain, usr)
        async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/FacilityAppsAPI.php",
                                         headers=self._app_headers,
                                         data=_form) as r:
            if r.status == 200:
                _json = await r.json()
                return _json
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA API TaskToBacklog request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return False

    async def faweb_update_duration(self,
                                    domain: str,
                                    usr: str,
                                    taskid: int,
                                    taskseq: int,
                                    d: timedelta) -> None:
        """
        Gets all tasks for domain from FA web API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param taskid: FA backend task ID
        :param taskseq: FA backend task sequence number
        :param d: duration to set
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            _json = {"id":                   str(taskid),
                     "sequence_number":      str(taskseq),
                     "_token":               getcookieval(self._s[_s_name], "XSRF-TOKEN"),
                     "duration_hour":        str((d.seconds // 60) // 60),
                     "duration_minute":      str((d.seconds // 60) % 60),
                     "duration_second":      str(d.seconds % 60),
                     "editMode":             "single",
                     "excludeExceptions":    "",
                     "task_complete_emails": 0,
                     "task_canceled_emails": 0
                     }
            r = await self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/planning/save",
                                            headers={"Accept":       "application/json",
                                                     "Content-Type": "application/json; charset=utf-8",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            data=dumps(_json, ensure_ascii=False))
            if r.ok:
                _res = await r.json()
                if "result" not in _res.keys() or _res["result"] is not True:
                    await self._base_log(i_stack(), "warning", f"FAILED FA web API update duration request - "
                                                               f"domain '{domain}' user '{usr}': API response = {_res}")
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API update duration request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
        except Exception as _exc:
            await self._base_log(i_stack(), "error",
                                 f"FAILED faweb_update_duration(): {format_exc().replace(chr(10), ' ')}")

    async def faapp_get_tasks(self,
                              domain: str,
                              usr: str,
                              session_id: str,
                              tbeg: datetime,
                              tend: datetime,
                              language: str,
                              sitelist: List[int]) -> Optional[Dict[str, Any]]:
        """
        Gets all tasks for domain from FA mobile API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param session_id: FA mobile API session_id
        :param tbeg: date and time from which to select tasks
        :param tend: date and time till which to select tasks
        :param language: language code in form of en_EN to use for language and region form fields
        :param sitelist: list of integer FA backend site IDs
        :return: dict loaded from FA web API response JSON
        """
        _s_name = self._faapp_get_session_name(domain, usr)
        try:
            _json = {"CurrentView":       "custom",
                     "start":             tbeg.strftime("%Y-%m-%d"),
                     "end":               tend.strftime("%Y-%m-%d"),
                     "sites":             sitelist,
                     "includeExceptions": True,
                     "region_code":       language
                     }
            async with self._s[_s_name].post(f"https://{domain}.facilityapps.com/api/1.0/planning/planning_data",
                                             headers={**self._app_headers,
                                                      **{"Content-Type":  "application/json; charset=utf-8",
                                                         "Authorization": f"Bearer {session_id}"
                                                         }
                                                      },
                                             data=dumps(_json, ensure_ascii=False)) as r:
                if r.status == 200:
                    _json_response = await r.json()
                    if "exceptions" in _json_response.keys() and _json_response["exceptions"]:
                        await self._base_log(i_stack(),
                                             "info",
                                             f"got exception field in FA API /api/1.0/planning/planning_data "
                                             f"response JSON - domain '{domain}' user '{usr}'",
                                             logo=_json_response["exceptions"])
                    return _json_response
                else:
                    await self._base_log(i_stack(), "warning",
                                         f"FAILED FA API /api/1.0/planning/planning_data request - "
                                         f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}")
                    return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error", str(), _exc, format_exc())
            return None

    async def faweb_get_submitted_forms(self,
                                        domain: str,
                                        usr: str,
                                        tbeg: datetime,
                                        tend: datetime) -> Optional[List[Dict[str, Any]]]:
        """
        Gets all submitted forms for domain from FA web API for specified period

        :param domain: FA domain name
        :param usr: FA user login name
        :param tbeg: date and time from which to select tasks
        :param tend: date and time till which to select tasks
        :return: dict loaded from FA web API response JSON
        """
        _s_name = self._faweb_get_session_name(domain, usr)
        try:
            # Check cookies
            if not isinstance(getcookieval(self._s[_s_name], "XSRF-TOKEN"), str):
                raise ValueError(f"no XSRF-TOKEN: {getcookieval(self._s[_s_name], 'XSRF-TOKEN')}")
            # Get all submitted forms
            r = await self._s[_s_name].post((f"https://{domain}.facilityapps.com"
                                             f"/api/1.0/forms/reporting?fields={FARequests.formsreportingquery()}"),
                                            headers={"Accept":       "application/json",
                                                     "X-CSRF-TOKEN": getcookieval(self._s[_s_name], "XSRF-TOKEN")
                                                     },
                                            data=FARequests.formsreportingform(1, tbeg, tend))
            if r.ok:
                _forms_list_json = await r.json()
                return _forms_list_json["data"]
            else:
                await self._base_log(i_stack(),
                                     "warning",
                                     (f"FAILED FA web API submitted forms list request - "
                                      f"domain '{domain}' user '{usr}': HTTP {r.status} {r.reason}"))
                return None
        except Exception as _exc:
            await self._base_log(i_stack(), "error", f"FAILED faweb_get_submitted_forms(): "
                                                     f"{format_exc().replace(chr(10), ' ')}")
            return None

    async def faweb_get_form_details(self,
                                     domain: str,
                                     usr: str,
                                     submissionid: int) -> Optional[Dict[str, Any]]:
        """
        Get submitted form details and parse with parse_form_html()

        :param domain: FA domain name
        :param usr: FA user login name
        :param submissionid: ID of form submission
        :return: dictionary with submitted form contents
        """
        # Output dict
        _out = dict()
        _s_name = self._faweb_get_session_name(domain, usr)
        r = await self._s[_s_name].get(f"https://{domain}.facilityapps.com/forms/submission/view/{submissionid}",
                                       headers={"Accept": "text/html, application/xhtml+xml"})
        if r.ok:
            _raw_html = await r.text()
        else:
            await self._base_log(i_stack(), "error",
                                 f"FAILED requesting details for form submission id = {submissionid} for "
                                 f"domain '{domain}' user '{usr}': "
                                 f"HTTP {r.status} {r.reason}")
            return None
        return self.parse_form_html(_raw_html)

    @staticmethod
    def fa_extract_recurrence(recurrence: Dict[str, Any],
                              taskid: int) -> List[Dict[str, Any]]:
        """
        Extracts task sequence by date from response of FA mobile API tasks request

        :param recurrence: contents of FA mobile API tasks request "recurrence"
        :param taskid: FA backend task ID
        :return: corresponding task sequence
        """
        _res = list()
        for _task_str_id in recurrence.keys():
            if int(_task_str_id) == taskid:
                for _seq_nr_str, _seq_dates_list in recurrence[_task_str_id].items():
                    _res.append({"sequenceNumber": int(_seq_nr_str),
                                 "_date_start":    _seq_dates_list[0],
                                 "_date_end":      _seq_dates_list[1]
                                 })
                return _res
        return _res

    @staticmethod
    def parse_form_html(rawhtml: str) -> Dict[str, Any]:
        """
        Parses the raw FA form submission questions page HTML into structured dict

        :param rawhtml: raw string with HTML contents
        :result: dictionary with submitted form contents
        """
        _strainer_content = bs4.SoupStrainer(name="content", id="Content")
        _bs_content = bs4.BeautifulSoup(rawhtml, features="lxml", parse_only=_strainer_content)
        _out = dict()
        for _child in _bs_content.content.children:
            if isinstance(_child,
                          bs4.element.Tag) and _child.name == "div" and "card" in _child["class"]:
                if "card-header" in _child.div["class"]:
                    _category_name = _child.div.contents[0]
                else:
                    _category_name = None
                _category_fields = list()
                if "card-body" in _child.ul["class"]:
                    for _ul_child in _child.ul:
                        _field = dict()
                        if isinstance(_ul_child,
                                      bs4.element.Tag) and _ul_child.name == "li" and "list-group-item" in _ul_child[
                                                                                                            "class"]:
                            _field["name"] = _ul_child.label.contents[0].replace(chr(10), '').strip()
                            _field["question"] = int(_ul_child.label["for"].split("question-")[1])
                            if _ul_child.div is not None:
                                _field_img = _ul_child.div.find(name="img")
                                _field_lookup = _ul_child.div.find_all(name="div", class_="lookup-table-answers")
                                if _field_img is not None and not _field_lookup:
                                    _field["type"] = "image"
                                    _field["val"] = _field_img["src"]
                                elif _field_img is None and not _field_lookup:
                                    _field["type"] = "value"
                                    _field["val"] = _ul_child.div.contents[0].replace(chr(10), '').strip()
                                elif _field_lookup:
                                    _field["type"] = "lookup"
                                    _selections = list()
                                    for _lookup in _field_lookup:
                                        _selection_item = dict()
                                        _lookup_selection = _lookup.find(name="div", class_="lookup-table-selection")
                                        _selection_item_key = _lookup_selection.contents[0].replace(chr(10), '').strip()
                                        _lookup_subanswers = _lookup.find(name="div", class_="sub-answers")
                                        # Parse subanswers into tuples
                                        _sa_names = list()
                                        _sa_vals = list()
                                        for _sa_child in _lookup_subanswers:
                                            if isinstance(_sa_child, bs4.element.Tag):
                                                if _sa_child.name == "label":
                                                    _sa_names.append(_sa_child.contents[0].replace(chr(10), '').strip())
                                                elif _sa_child.name == "div":
                                                    if _sa_child.contents:
                                                        try:
                                                            _sa_val = int(
                                                                _sa_child.contents[0].replace(chr(10), '').strip())
                                                        except ValueError:
                                                            _sa_val = _sa_child.contents[0].replace(chr(10), '').strip()
                                                        _sa_vals.append(_sa_val)
                                                    else:
                                                        _sa_vals.append(None)
                                        _lookup_subanswers_tuples = list()
                                        if len(_sa_names) == len(_sa_vals):
                                            for _i in range(len(_sa_names)):
                                                _lookup_subanswers_tuples.append((_sa_names[_i], _sa_vals[_i]))
                                        else:
                                            # Parsing exception
                                            pass
                                        _selection_item[_selection_item_key] = _lookup_subanswers_tuples
                                        _selections.append(_selection_item)
                                    _field["val"] = _selections
                            if _field:
                                _category_fields.append(_field)
                _out[_category_name] = _category_fields
        return _out
