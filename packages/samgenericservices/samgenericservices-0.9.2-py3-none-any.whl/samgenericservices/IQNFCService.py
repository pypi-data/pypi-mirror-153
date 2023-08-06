# coding=utf-8
"""
Base class for the service
"""
import asyncio
import hashlib
import time
from copy import deepcopy
from datetime import datetime
from inspect import FrameInfo, stack as i_stack
from json import dumps, loads
from traceback import format_exc
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union

import aio_pika
import asyncpg.prepared_stmt

from .BaseMicroService import BaseMicroService
from .FAAPIService import FAAPIService


class IQNFCService(BaseMicroService):
    """
    Base class for the service
    """

    def __init__(self,
                 evloop: asyncio.AbstractEventLoop,
                 appname: str,
                 configfile: str,
                 dbname: Optional[str] = None,
                 servicename: Optional[str] = None,
                 tcpport: Optional[int] = None,
                 httpmwares: Optional[List] = None,
                 pikattl: int = 60):
        """
        Init the base class

        :param evloop: asyncio event loop to run in
        :param appname: name of the application
        :param configfile: config file name
        :param dbname: name of database to use
        :param servicename: name of the current service
        :param tcpport: optional TCP port number for web server to listen at
        :param httpmwares: list of aiohttp middleware callables as is passed to aiohttp.web.Application
                           middlewares= option
        :param pikattl: RabbitMQ messages ttl
        """
        super().__init__(evloop, appname, configfile, dbname, servicename, tcpport, httpmwares, pikattl)
        # SQL statements
        self._q = {
                "get_domains":            "SELECT * FROM public.fadomains;",
                "get_domain":             "SELECT * FROM public.fadomains WHERE fa_domain = $1;",
                "check_domain":           "SELECT enabled FROM public.fadomains WHERE fa_domain = $1;",
                "get_admin_record":       "SELECT * FROM public.adminusers WHERE fa_domain = $1;",
                "add_admin":              ("INSERT INTO public.adminusers VALUES ($1, $2, $3, $4, $5, $6) "
                                           "RETURNING fa_domain;"),
                "upd_admin_session":      ("UPDATE public.adminusers "
                                           "SET fa_session_id = $2, fa_session_id_timestamp = $3 "
                                           "WHERE fa_domain = $1 "
                                           "RETURNING fa_session_id;"),
                "upsert_fa_user":         ("INSERT INTO public.refusers VALUES ($1, $2, $3, $4, $5, $6, $7) "
                                           "ON CONFLICT (fa_domain, fa_id) DO UPDATE SET "
                                           "(fa_username, fa_name, fa_email, fa_phone, fa_disable_login)"
                                           " = "
                                           "($3, $4, $5, $6, $7) "
                                           "RETURNING fa_domain, fa_id;"),
                "upsert_fa_site":         ("INSERT INTO public.refsites VALUES ($1, $2, $3, $4, $5, $6, $7) "
                                           "ON CONFLICT (fa_domain, fa_id) DO UPDATE SET "
                                           "(fa_key, fa_name, fa_region_name, fa_address_city, fa_address)"
                                           " = "
                                           "($3, $4, $5, $6, $7) "
                                           "RETURNING fa_domain, fa_id;"),
                "search_site":            "SELECT * FROM public.refsites WHERE fa_domain = $1 AND fa_name = $2;",
                "search_site_by_key":     "SELECT * FROM public.refsites WHERE fa_domain = $1 AND fa_key = $2;",
                "get_site":               "SELECT * FROM public.refsites WHERE fa_domain = $1 AND fa_id = $2;",
                "get_sites":              "SELECT * FROM public.refsites WHERE fa_domain = $1;",
                "search_floor":           ("SELECT * FROM public.reffloors "
                                           "WHERE fa_domain = $1 AND fa_floor_name = $2 AND fa_site_id = $3;"),
                "get_floor":              ("SELECT * FROM public.reffloors "
                                           "WHERE fa_domain = $1 AND fa_site_id = $2 AND fa_floor_id = $3;"),
                "search_space":           ("SELECT * FROM public.refspaces "
                                           "WHERE fa_domain = $1 AND fa_space_name = $2 "
                                           "AND fa_site_id = $3 AND fa_floor_id = $4;"),
                "get_space":              ("SELECT * FROM public.refspaces "
                                           "WHERE fa_domain = $1 AND fa_site_id = $2 "
                                           "AND fa_floor_id = $3 AND fa_space_id = $4;"),
                "search_user":            "SELECT * FROM public.refusers WHERE fa_domain = $1 AND fa_name = $2;",
                "get_user":               "SELECT * FROM public.refusers WHERE fa_domain = $1 AND fa_id = $2;",
                "get_users":              "SELECT * FROM public.refusers WHERE fa_domain = $1;",
                "update_domain":          "UPDATE public.fadomains SET tz = $2 WHERE fa_domain = $1;",
                "insert_log":             ("INSERT INTO public.log "
                                           "VALUES (nextval('idcounter'), "
                                           "now(), $1, $2, $3, $4::jsonb, $5, $6, $7);"),
                "get_logs_by_key":        ("SELECT * FROM public.log WHERE key = $1 "
                                           "AND timestamp > (now() - make_interval(secs := $2));"),
                "insert_timereg":         (
                        "INSERT INTO public.timeregs VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) "
                        "RETURNING *;"),
                "get_timeregs":           "SELECT * FROM public.timeregs WHERE fa_domain = $1 AND fa_time_tz >= $2;",
                "get_timereg_keys":       ("SELECT key FROM public.timeregs "
                                           "WHERE timeregs.fa_domain = $1 AND fa_time_tz >= $2;"),
                "get_tasks":              ("SELECT * FROM public.reftasks WHERE "
                                           "fa_domain = $1 AND fa_time_start >= $2;"),
                "get_task":               ("SELECT * FROM public.reftasks WHERE "
                                           "fa_domain = $1 AND fa_task_id = $2 AND fa_task_sequence = $3;"),
                "upsert_task":            ("INSERT INTO public.reftasks "
                                           "VALUES ($1, $2, $3, $4::jsonb, $5, $6, $7, "
                                           "$8, $9, $10, $11, $12, $13, $14, $15, $16) "
                                           "ON CONFLICT (fa_domain, fa_task_id, fa_task_sequence) DO UPDATE SET "
                                           "(json, fa_site_id, fa_floor_id, fa_space_id, fa_owner_id, "
                                           "fa_time_start, fa_time_end, nfc_status, fa_substatus, fa_status, "
                                           "fa_translation, nfc_algorithm, nfc_status_timestamp) "
                                           " = "
                                           "($4::jsonb, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)"
                                           "RETURNING fa_domain, fa_task_id, fa_task_sequence;"),
                "update_task_nfc_status": ("UPDATE public.reftasks SET nfc_status = $4, "
                                           "nfc_status_timestamp = $5 WHERE "
                                           "fa_domain = $1 AND fa_task_id = $2 AND fa_task_sequence = $3 "
                                           "RETURNING nfc_status;"),
                "upsert_nfc_ref":         ("INSERT INTO public.tasknfcs "
                                           "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) "
                                           "ON CONFLICT (fa_domain, fa_site_id, fa_floor_id, "
                                           "fa_space_id, task_order, nfc_action) "
                                           "DO UPDATE SET "
                                           "(fa_task_id, fa_task_sequence, "
                                           "nfc_algorithm, nfc_index) = ($7, $8, $9, $10) "
                                           "RETURNING fa_task_id, fa_task_sequence, nfc_algorithm, nfc_index;"),
                "get_nfc_ref":            (
                        "SELECT tnfc.task_order, tnfc.fa_task_id, tnfc.fa_task_sequence, tnfc.nfc_action, "
                        "tsk.fa_time_start, tsk.fa_time_end, tsk.fa_owner_id, tsk.nfc_status, "
                        "tsk.fa_substatus, tsk.fa_status, tsk.json, tnfc.nfc_algorithm, "
                        "tnfc.nfc_index, tsk.nfc_status_timestamp "
                        "FROM public.tasknfcs AS tnfc, public.reftasks AS tsk "
                        "WHERE tnfc.fa_domain = tsk.fa_domain "
                        "AND tnfc.fa_task_id = tsk.fa_task_id AND tnfc.fa_task_sequence = tsk.fa_task_sequence "
                        "AND tnfc.fa_domain = $1 AND tnfc.fa_site_id = $2 "
                        "AND tnfc.fa_floor_id = $3 AND tnfc.fa_space_id = $4;"),
                "delete_nfc_ref":         "DELETE FROM public.tasknfcs WHERE fa_domain = $1;",
                "get_overdue":            (
                        "SELECT t.fa_domain, t.fa_task_id, t.fa_task_sequence, t.fa_site_id, s.fa_name, "
                        "s.fa_region_name, t.fa_translation, t.fa_floor_id, t.fa_space_id, t.fa_substatus,"
                        "t.fa_status, t.fa_time_start, t.fa_time_end, t.fa_owner_id, t.nfc_algorithm "
                        "FROM public.reftasks AS t, public.refsites AS s "
                        "WHERE s.fa_domain = t.fa_domain AND s.fa_id = t.fa_site_id AND t.fa_domain = $1 "
                        "AND (t.fa_status NOT IN (2, 3, 4) OR t.fa_status IS NULL) AND t.nfc_status NOT IN (2, 3) "
                        "AND t.fa_time_end >= $2 AND t.fa_time_end < $3;"),
                "get_not_begun":          (
                        "SELECT t.fa_domain, t.fa_task_id, t.fa_task_sequence, t.fa_site_id, s.fa_name, "
                        "s.fa_region_name, t.fa_translation, t.fa_floor_id, t.fa_space_id, t.fa_substatus,"
                        "t.fa_status, t.fa_time_start, t.fa_time_end, t.fa_owner_id, t.nfc_algorithm "
                        "FROM public.reftasks AS t, public.refsites AS s "
                        "WHERE s.fa_domain = t.fa_domain AND s.fa_id = t.fa_site_id AND t.fa_domain = $1 "
                        "AND t.nfc_status IN (-1, 0) "
                        "AND t.fa_time_start >= $2 AND t.fa_time_start < $3;"),
                "get_manual_begun":       (
                        "SELECT t.fa_domain, t.fa_task_id, t.fa_task_sequence, t.fa_site_id, s.fa_name, "
                        "s.fa_region_name, t.fa_translation, t.fa_floor_id, t.fa_space_id, t.fa_substatus,"
                        "t.fa_status, t.fa_time_start, t.fa_time_end, t.fa_owner_id, t.nfc_algorithm "
                        "FROM public.reftasks AS t, public.refsites AS s "
                        "WHERE s.fa_domain = t.fa_domain AND s.fa_id = t.fa_site_id AND t.fa_domain = $1 "
                        "AND t.fa_status = 1 AND t.fa_substatus IS NULL AND t.nfc_status = -1 "
                        "AND t.fa_time_start >= $2;"),
                "upsert_submitted_form":  ("INSERT INTO public.formssubmitted "
                                           "VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb) "
                                           "ON CONFLICT (fa_domain, fa_form_id, fa_submision_id, fa_timestamp) "
                                           "DO UPDATE SET "
                                           "(fa_site_id, fa_element_id, fa_user_id, parsed_json) "
                                           "= ($5, $6, $7, $8::jsonb) "
                                           "RETURNING fa_domain, fa_form_id, fa_submision_id, fa_timestamp;"),
                "get_submitted_forms":    ("SELECT * FROM public.formssubmitted WHERE fa_domain = $1 "
                                           "AND fa_form_id = $2 AND fa_timestamp >= $3 AND fa_timestamp < $4;"),
                "get_site_timeregs":      ("SELECT * FROM public.timeregs "
                                           "WHERE fa_domain = $1 AND fa_time_tz >= $2 AND fa_time_tz < $3 "
                                           "AND NOT space_precise ORDER BY fa_time_tz;"),
                "get_space_timeregs":     ("SELECT fa_site_id, fa_user_id, COUNT(key) AS fa_user_id_cnt "
                                           "FROM public.timeregs WHERE fa_domain = $1 "
                                           "AND space_precise AND fa_time_tz >= $2 AND fa_time_tz < $3 "
                                           "GROUP BY fa_site_id, fa_user_id;"),
                "upsert_siteregreport":   ("INSERT INTO public.siteregreport "
                                           "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) "
                                           "ON CONFLICT (fa_domain, fa_site_id, fa_user_id, fa_date) "
                                           "DO UPDATE SET "
                                           "(fa_time_tz_beg, fa_time_tz_end, "
                                           "time_interval, space_checkins, site_checkins) = ($5, $6, $7, $8, $9) "
                                           "RETURNING fa_domain, fa_site_id, fa_user_id, fa_date;")
                }
        # FA domains and admin users list to serve
        self._domains: List[asyncpg.Record] = list()
        self._admin_records = list()
        # Create the FA API service
        self._fa = FAAPIService(self._log_cloud,
                                self._config["vapp"],
                                self._config["uagent"])
        # Container for logged in domains / users
        self._admin_records_auth = list()
        # Standard queues to listen
        self._queue_control: Optional[aio_pika.queue.Queue] = None
        # Control commands handlers
        # key is command name,
        # value is callable coroutine, it should accept only one argument - json received from RabbitMQ control queue
        self._control_handlers: Dict[str, Callable[..., Coroutine[Any, Any, Any]]] = dict()

    async def declare_standard_queues(self) -> None:
        """
        Declaring standard queues - control and report
        """
        pass
        # Queue for handling control messages
        self._queue_control = await self._rmq_rcv_channel.declare_queue(f"{self._dbname}.{self._servicename}.control",
                                                                        durable=True)
        await self._queue_control.consume(self._rmq_handle_control)
        # Queue with responses to control messages
        await self._rmq_snd_channel.declare_queue(f"{self._dbname}.{self._servicename}.response",
                                                  durable=True)
        # Logging queue
        await self._rmq_snd_channel.declare_queue(f"{self._dbname}.{self._servicename}.log",
                                                  durable=True)

    async def _rmq_handle_control(self, msg: aio_pika.IncomingMessage):
        """
        Consumes messages from the control queue, and performs requested actions

        :param msg: aio-pika incoming message object
        """
        try:
            async with msg.process():
                _command_json = msg.body
            _command = loads(_command_json.decode("utf-8"))
            if isinstance(_command, dict):
                if "cmd" in _command.keys():
                    if _command["cmd"] == "stop":
                        # Stop the cycle
                        self._run_cycle = False
                    else:
                        if _command["cmd"] in self._control_handlers.keys():
                            await self._control_handlers[_command["cmd"]](_command)
                        else:
                            await self._log_cloud(i_stack(),
                                                  "warning",
                                                  (f"unknown command '{_command['cmd']}' received "
                                                   f"from {self._dbname}.{self._servicename}.control queue"),
                                                  copyresponse=True)
                else:
                    await self._log_cloud(i_stack(),
                                          "warning",
                                          (f"no 'cmd' key in command object received "
                                           f"from {self._dbname}.{self._servicename}.control queue"),
                                          copyresponse=True)
            else:
                await self._log_cloud(i_stack(),
                                      "warning",
                                      (f"wrong message received "
                                       f"from {self._dbname}.{self._servicename}.control, must be JSON object"),
                                      copyresponse=True)
        except Exception as _exc:
            await self._log_cloud(i_stack(),
                                  "error",
                                  (f"processing command message "
                                   f"from {self._dbname}.{self._servicename}.control queue"),
                                  exc=_exc,
                                  fexc=format_exc(),
                                  copyresponse=True)

    async def _log_cloud(self,
                         stack: List[FrameInfo],
                         logl: str,
                         logm: str,
                         exc: Optional[Exception] = None,
                         fexc: Optional[str] = None,
                         logo: Optional[Union[List, Dict]] = None,
                         copyresponse: bool = False) -> None:
        """
        Logs to stdout / stderr, to RabbitMQ log queue and to logging DB table

        :param stack: result of inspect.stack()
        :param logl: logging level
        :param logm: message to log
        :param exc: optional Exception object
        :param fexc: optional contents format_exc()
        :param logo: optional object to log with dumps, may be list or dict
        :param copyresponse: if True, then copy same message to control response queue
        """
        _time = time.time()
        # Define log level
        if str(logl).upper() not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]:
            _logl = "INFO"
        else:
            _logl = str(logl).upper()
        _loglevel = {
                "CRITICAL": 50,
                "ERROR":    40,
                "WARNING":  30,
                "INFO":     20,
                "DEBUG":    10,
                "NOTSET":   0
                }[_logl]
        # Add the exception name and arguments, if any,
        if isinstance(exc, Exception):
            _logm = f"{str(logm)} {exc.__class__.__name__} {exc.args}"
        else:
            _logm = str(logm)
        # Format object to log
        _logo = logo if isinstance(logo, (list, dict)) else None
        # Need to log if issue with both RabbitMQ and DB
        _need_to_log = False
        # If needed to log into RabbitMQ, due to such log already exists in the DB or not
        _rmq_logging = True
        # Log to DB
        if self._need_psg:
            try:
                _rmq_logging = await self._log_db(stack, logl, logm, exc, fexc, logo)
            except Exception as _exc:
                _need_to_log = True
                self._log.info(f"{self.get_stack_str(i_stack())}: {_exc.__class__.__name__} {_exc.args}")
        # Log to RabbitMQ queue
        if self._need_rmq:
            try:
                _json_to_rmq = {"timestamp": _time,
                                "level":     _logl.lower(),
                                "stack":     self.get_stack_str(stack),
                                "message":   _logm,
                                "exception": fexc.replace(chr(10), ' ') if isinstance(fexc, str) else None,
                                "object":    _logo
                                }
            except Exception as _exc:
                _json_to_rmq = None
                _need_to_log = True
                self._log.info(f"{self.get_stack_str(i_stack())}: "
                               f"_json_to_rmq {_exc.__class__.__name__} {_exc.args}")
            if isinstance(_json_to_rmq, dict):
                try:
                    await self._send_rmq(f"{self._dbname}.{self._servicename}.log",
                                         _json_to_rmq,
                                         customttl=self._config["logrmqttl"])
                except Exception as _exc:
                    _need_to_log = True
                    self._log.info(f"{self.get_stack_str(i_stack())}: "
                                   f".log {_exc.__class__.__name__} {_exc.args}")
                if copyresponse:
                    try:
                        await self._send_rmq(f"{self._dbname}.{self._servicename}.response",
                                             _json_to_rmq,
                                             customttl=self._config["logrmqttl"])
                    except Exception as _exc:
                        self._log.info(f"{self.get_stack_str(i_stack())}: "
                                       f".response {_exc.__class__.__name__} {_exc.args}")
        # Log to stderr / stdout
        if _need_to_log or (not self._need_rmq and not self._need_psg):
            _stack_to_log = f"{self.get_stack_str(stack)}: " if isinstance(self.get_stack_str(stack), str) else str()
            if isinstance(fexc, str):
                self._log.log(_loglevel, f"{_stack_to_log}{_logm} {fexc.replace(chr(10), ' ')}")
            else:
                self._log.log(_loglevel, f"{_stack_to_log}{_logm}")

    async def _log_db(self,
                      stack: List[FrameInfo],
                      logl: str,
                      logm: str,
                      exc: Optional[Exception] = None,
                      fexc: Optional[str] = None,
                      logo: Optional[Any] = None) -> bool:
        """
        Logs to stdout / stderr, to RabbitMQ log queue and to logging DB table

        :param stack: result of inspect.stack()
        :param logl: logging level
        :param logm: message to log
        :param exc: optional Exception object
        :param fexc: optional contents format_exc()
        :param logo: optional object to log with dumps, may be list or dict
        :return: False if such same log was already recently added otherwise True
        """
        _perform_db_logging = True
        if self._need_psg:
            # Call stack value to insert
            _stack_insert = self.get_stack_str(stack) if isinstance(self.get_stack_str(stack), str) else None
            # Define log level
            if str(logl).upper() not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]:
                _logl = "INFO"
            else:
                _logl = str(logl).upper()
            # Add the exception name and arguments, if any,
            if isinstance(exc, Exception):
                _logm = f"{str(logm)} {exc.__class__.__name__} {exc.args}"
            else:
                _logm = str(logm)
            # Make uniqueness key
            _key = hashlib.sha256(dumps({"level":     _logl.lower(),
                                         "stack":     self.get_stack_str(stack),
                                         "message":   _logm,
                                         "exception": fexc.replace(chr(10), ' ') if isinstance(fexc, str) else None
                                         },
                                        ensure_ascii=False).encode("utf-8")).hexdigest()
            # For warnings, errors and debugs - check if such errors already in the database, not to log duplicates
            if _logl in ["ERROR", "WARNING", "INFO", "DEBUG"]:
                try:
                    async with self._pg.acquire() as _c:
                        _get_logs_by_key_r = await _c.fetch(self._q["get_logs_by_key"],
                                                            _key,
                                                            float(self._config["logdbintvl"]))
                        if len(_get_logs_by_key_r) > 0:
                            _perform_db_logging = False
                except Exception as _exc:
                    self._log.info(f"{self.get_stack_str(i_stack())}: "
                                   f"get_logs_by_key {_exc.__class__.__name__} - {_exc.args}")
            if _perform_db_logging:
                # Format object to log
                _logo = dumps(logo,
                              ensure_ascii=False,
                              default=self._dumps_default) if isinstance(logo, (list, dict)) else None
                # And insert into DB
                try:
                    async with self._pg.acquire() as _c:
                        await _c.execute(self._q["insert_log"],
                                         _logl.lower(),
                                         _logm,
                                         fexc if isinstance(fexc, str) else None,
                                         _logo,
                                         _key,
                                         _stack_insert,
                                         self._servicename)
                except Exception as _exc:
                    self._log.info(f"{self.get_stack_str(i_stack())}: "
                                   f"insert_log {_exc.__class__.__name__} - {_exc.args}")
        return _perform_db_logging

    async def search_site(self, domain: str, name: str) -> Optional[int]:
        """
        Searches site by name, there should be only one, otherwise returns first match and logs error

        :param domain: FA domain name
        :param name: name to search for
        :return: ID of entry in FA backend
        """
        try:
            async with self._pg.acquire() as _c:
                _query_r = await _c.fetch(self._q["search_site"], domain, name)
            if len(_query_r) == 1:
                return _query_r[0]["fa_id"]
            elif len(_query_r) == 0:
                return None
            else:
                raise ValueError(f"{len(_query_r)} entries found")
        except Exception as _exc:
            await self._log_cloud(i_stack(), "error", str(), _exc, format_exc())
            return None

    async def search_site_by_key(self, domain: str, key: str) -> Optional[int]:
        """
        Searches site by key id string, there should be only one, otherwise returns first match and logs error

        :param domain: FA domain name
        :param key: name to search for
        :return: ID of entry in FA backend
        """
        try:
            async with self._pg.acquire() as _c:
                _query_r = await _c.fetch(self._q["search_site_by_key"], domain, key)
            if len(_query_r) == 1:
                return _query_r[0]["fa_id"]
            elif len(_query_r) == 0:
                return None
            else:
                raise ValueError(f"{len(_query_r)} entries found")
        except Exception as _exc:
            await self._log_cloud(i_stack(), "error", str(), _exc, format_exc())
            return None

    async def search_floor(self, domain: str, name: str, siteid: int) -> Optional[int]:
        """
        Searches floor by name, there should be only one, otherwise returns first match and logs error

        :param domain: FA domain name
        :param name: name to search for
        :param siteid: FA backed ID of site
        :return: ID of entry in FA backend
        """
        try:
            async with self._pg.acquire() as _c:
                _query_r = await _c.fetch(self._q["search_floor"], domain, name, siteid)
            if len(_query_r) == 1:
                return _query_r[0]["fa_floor_id"]
            elif len(_query_r) == 0:
                return None
            else:
                raise ValueError(f"{len(_query_r)} entries found")
        except Exception as _exc:
            await self._log_cloud(i_stack(), "error", str(), _exc, format_exc())
            return None

    async def search_space(self,
                           domain: str,
                           name: str,
                           siteid: int,
                           floorid: Optional[int] = None) -> Optional[int]:
        """
        Searches space by name, there should be only one, otherwise returns first match and logs error

        :param domain: FA domain name
        :param name: name to search for
        :param siteid: FA backed ID of site
        :param floorid: FA backed ID of floor
        :return: ID of entry in FA backend
        """
        try:
            if floorid is None:
                return None
            async with self._pg.acquire() as _c:
                _query_r = await _c.fetch(self._q["search_space"], domain, name, siteid, floorid)
            if len(_query_r) == 1:
                return _query_r[0]["fa_space_id"]
            elif len(_query_r) == 0:
                return None
            else:
                raise ValueError(f"{len(_query_r)} entries found: '{domain}' name '{name}' "
                                 f"site ID {siteid} floor ID {floorid}")
        except Exception as _exc:
            await self._log_cloud(i_stack(), "error", str(), _exc, format_exc())
            return None

    async def search_user(self, domain: str, name: str) -> Optional[int]:
        """
        Searches user by name, there should be only one, otherwise returns first match and logs error

        :param domain: FA domain name
        :param name: name to search for
        :return: ID of entry in FA backend
        """
        try:
            async with self._pg.acquire() as _c:
                _query_r = await _c.fetch(self._q["search_user"], domain, name)
            if len(_query_r) == 1:
                return _query_r[0]["fa_id"]
            elif len(_query_r) == 0:
                return None
            else:
                raise ValueError(f"{len(_query_r)} entries found")
        except Exception as _exc:
            await self._log_cloud(i_stack(), "error", str(), _exc, format_exc())
            return None

    async def get_admin_records(self) -> None:
        """
        Get domains list and all enabled domain records
        """
        async with self._pg.acquire() as _c:
            self._domains = await _c.fetch(self._q["get_domains"])
        _admin_records = list()
        for _domain in self._domains:
            if _domain["enabled"]:
                async with self._pg.acquire() as _c:
                    _admin_record = await _c.fetch(self._q["get_admin_record"],
                                                   _domain["fa_domain"])
                if len(_admin_record) == 1:
                    _admin_record_dict = dict(_admin_record[0])
                    _admin_record_dict["tz"] = _domain["tz"]
                    _admin_records.append(_admin_record_dict)
                    await self._log_cloud(i_stack(),
                                          "debug",
                                          (f"OK FA domain '{_admin_record[0]['fa_domain']}' "
                                           f"user '{_admin_record[0]['fa_usr']}' "
                                           f"language {_admin_record[0]['fa_forms_language']}"))
                else:
                    await self._log_cloud(i_stack(),
                                          "debug",
                                          (f"found {len(_admin_record)} admin records "
                                           f"for domain '{_domain['fa_domain']}', skipping domain"))
        self._admin_records = deepcopy(_admin_records)

    async def login_to_fa(self) -> None:
        """
        Login to FA and create corresponding sessions
        """
        _admin_records_auth = list()
        for _admin_record in self._admin_records:
            _fa_web_login_res = await self._fa.faweb_login(_admin_record["fa_domain"],
                                                           _admin_record["fa_usr"],
                                                           _admin_record["fa_pwd"])
            if _fa_web_login_res:
                _admin_records_auth.append(_admin_record)
                await self._log_cloud(i_stack(),
                                      "info",
                                      (f"OK logged in to domain '{_admin_record['fa_domain']}' "
                                       f"user '{_admin_record['fa_usr']}'"))
            else:
                await self._log_cloud(i_stack(),
                                      "warning",
                                      (f"can not login to domain '{_admin_record['fa_domain']}' "
                                       f"user '{_admin_record['fa_usr']}'"))
        self._admin_records_auth = deepcopy(_admin_records_auth)

    async def logout_from_fa(self) -> None:
        """
        Log out accounts from FA API
        """
        for _admin_record_auth in self._admin_records_auth:
            await self._fa.faweb_logout(_admin_record_auth["fa_domain"],
                                        _admin_record_auth["fa_usr"])
        self._admin_records_auth = list()

    async def _shutdown_clear(self):
        """
        Generic clearing before shutdown overriden
        """
        # await self.logout_from_fa()
        pass

    @staticmethod
    def _unique_key(domain: str,
                    timetz: datetime,
                    siteid: int,
                    userid: int,
                    floorid: Optional[int] = None,
                    spaceid: Optional[int] = None) -> str:
        """
        Make unique key string for time reg entry
        :param domain: FA domain name
        :param timetz: timezone aware timestamp where time was registered
        :param siteid: FA backed ID of site
        :param userid: FA backed ID of site
        :param floorid: FA backed ID of floor
        :param spaceid: FA backed ID of space
        """
        return hashlib.sha256(dumps({"domain":  domain,
                                     "timetz":  int(timetz.timestamp()),
                                     "siteid":  siteid,
                                     "userid":  userid,
                                     "floorid": floorid,
                                     "spaceid": spaceid
                                     }, ensure_ascii=False).encode("utf-8")).hexdigest()

    async def _app_logins_update(self) -> None:
        """
        Update FA mobile API logins in the PostgreSQL database
        """
        # First get admin records to serve
        await self.get_admin_records()
        # Login to FA mobile API for each admin record and update session_id values into the admin records
        for _admin_record in self._admin_records:
            _fa_app_login_res = await self._fa.faapp_login(_admin_record["fa_domain"],
                                                           _admin_record["fa_usr"],
                                                           _admin_record["fa_pwd"])
            if isinstance(_fa_app_login_res, dict) and "LoggedIn" in _fa_app_login_res.keys():
                if _fa_app_login_res["LoggedIn"] and "session_id" in _fa_app_login_res.keys():
                    await self._log_cloud(i_stack(),
                                          "info",
                                          (f"OK mobile logged in to domain '{_admin_record['fa_domain']}' "
                                           f"user '{_admin_record['fa_usr']}'"))
                    async with self._pg.acquire() as _c:
                        await _c.execute(self._q["upd_admin_session"],
                                         _admin_record["fa_domain"],
                                         _fa_app_login_res["session_id"],
                                         int(time.time()))
                else:
                    await self._log_cloud(i_stack(),
                                          "warning",
                                          (f"refused mobile login to domain '{_admin_record['fa_domain']}' "
                                           f"user '{_admin_record['fa_usr']}': {str(_fa_app_login_res)}"))
            else:
                await self._log_cloud(i_stack(),
                                      "warning",
                                      (f"can not mobile login to domain '{_admin_record['fa_domain']}' "
                                       f"user '{_admin_record['fa_usr']}' "
                                       f"failed API response: {str(_fa_app_login_res)}"))
        # Log success
        await self._log_cloud(i_stack(),
                              "info",
                              f"OK completed app logins update")
