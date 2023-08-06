# coding=utf-8
"""
BaseMicroService
"""

import asyncio
import logging
import signal
from contextlib import suppress
from datetime import datetime
from inspect import FrameInfo
from json import dumps, load
from traceback import format_exc
from typing import Any, Dict, List, Optional, Union

import aio_pika
import aiohttp
import asyncpg
import boto3
from aiohttp import web
from botocore.client import BaseClient


# noinspection SqlNoDataSourceInspection
class BaseMicroService:
    """
    Base class to build microservices on top
    """

    def __init__(self,
                 evloop: asyncio.AbstractEventLoop,
                 appname: str,
                 configfile: str,
                 dbname: Optional[str] = None,
                 servicename: Optional[str] = None,
                 tcpport: Optional[int] = None,
                 httpmwares: Optional[List] = None,
                 pikattl: int = 60,
                 pikassl: bool = False):
        """
        Init the base class

        :param evloop: asyncio event loop to run in
        :param appname: name of the whole application
        :param configfile: config file name
        :param dbname: name of database to use
        :param servicename: name of the current service
        :param tcpport: optional TCP port number for web server to listen at
        :param httpmwares: list of aiohttp middleware callables as is passed to aiohttp.web.Application
                           middlewares= option
        :param pikattl: RabbitMQ messages ttl
        :param pikassl: use TLS for RabbitMQ connection
        """
        # Constants
        self._TTL = pikattl
        self._SSL = pikassl
        # Event loop
        self._evloop = evloop
        # Set application name
        self._appname: str = appname
        # Set service name
        if servicename is None:
            self._servicename: str = appname
        else:
            self._servicename: str = servicename
        # Load config
        self._config: Optional[dict] = None
        with open(configfile, "r") as _config_file_fd:
            self._config = load(_config_file_fd)
        # Load secrets
        with open(f"/home/{dbname}/.secret/.secret", "r") as _secret_file_fd:
            self._secrets = load(_secret_file_fd)
        # Run cycle flag
        self._run_cycle = True
        # Create logging formatter
        self._log_formatter = logging.Formatter(fmt="{asctime}.{msecs:03.0f} {levelname} {process} {name}: {message}",
                                                datefmt="%Y.%m.%d %H:%M:%S",
                                                style="{")
        # Get the logging level from config
        self._base_loglevel = {
            "CRITICAL": 50,
            "ERROR": 40,
            "WARNING": 30,
            "INFO": 20,
            "DEBUG": 10,
            "NOTSET": 0
        }[self._config["loglevel"].upper()]
        # Create service logger
        self._log = logging.getLogger(self._servicename)
        self._log.setLevel(self._base_loglevel)
        self._log_streamhandler = logging.StreamHandler()
        self._log_streamhandler.setFormatter(self._log_formatter)
        self._log.addHandler(self._log_streamhandler)
        self._log.propagate = False
        # Create the generic logger
        # noinspection PyArgumentList
        logging.basicConfig(format="{asctime}.{msecs:03.0f} {levelname} {process} {name}: {message}",
                            datefmt="%Y.%m.%d %H:%M:%S",
                            style="{",
                            level=self._base_loglevel)
        # S3
        self._s3session: Optional[boto3.session.Session] = None
        self._s3client: Optional[BaseClient] = None
        # aiohttp Server
        self._port: Optional[int] = tcpport
        if httpmwares is not None:
            self._aiohttp_app: aiohttp.web.Application = web.Application(middlewares=httpmwares)
        else:
            self._aiohttp_app: aiohttp.web.Application = web.Application()
        # aiohttp Runner
        self._aiohttp_app_runner: Optional[aiohttp.web.AppRunner] = web.AppRunner(self._aiohttp_app)
        self._aiohttp_control_site: Optional[aiohttp.web.UnixSite] = None
        self._aiohttp_site: Optional[aiohttp.web.TCPSite] = None
        # aiohttp Routes
        self._routes: List[aiohttp.web.RouteDef] = list()
        self._routes_registered: List[Dict[str, Any]] = list()
        # aiohttp client sessions pool
        self._http_sessions: Dict[str, aiohttp.ClientSession] = dict()
        # RabbitMQ
        self._need_rmq = False
        self._rmq_snd_conn: Optional[aio_pika.connection.Connection] = None
        self._rmq_snd_channel: Optional[aio_pika.channel.Channel] = None
        self._rmq_rcv_conn: Optional[aio_pika.connection.Connection] = None
        self._rmq_rcv_channel: Optional[aio_pika.channel.Channel] = None
        # PostgreSQL
        self._need_psg = False
        # Name of database
        self._dbname = dbname
        # Connection pool
        self._pg: Optional[asyncpg.pool.Pool] = None

    async def _conn_s3(self) -> None:
        """
        Setup the S3 connection to Yandex Object Storage.
        """
        # Create session
        self._s3session = boto3.session.Session(aws_access_key_id=self._config["s3key"],
                                                aws_secret_access_key=self._secrets["s3"])
        # Create client
        self._s3client = self._s3session.client(service_name="s3",
                                                endpoint_url=self._config["s3host"])

    def _init_web_routes(self) -> None:
        """
        Setup the aiohttp web server.
        """
        # Set routes
        _registered = self._aiohttp_app.add_routes(self._routes)
        # Remember routes for logging
        for _route in _registered:
            self._routes_registered.append({"method": _route.method,
                                            "path": _route.resource.canonical
                                            })

    async def _conn_rmq(self) -> None:
        """
        Setup connections and channels to RabbitMQ broker.
        """
        # Default port 5672, if "rmqport" is not provided in config file
        _rmq_port = 5672 if "rmqport" not in self._config.keys() else int(self._config["rmqport"])
        # Connection and channel to send
        self._rmq_snd_conn = await aio_pika.connect_robust(host=self._config["rmqhost"],
                                                           port=_rmq_port,
                                                           client_properties={
                                                               "connection_name": (f"{self._dbname}"
                                                                                   f".{self._servicename}.snd")
                                                           },
                                                           login=self._dbname,
                                                           password=self._secrets["rmq"],
                                                           ssl=self._SSL)
        self._rmq_snd_channel: aio_pika.abc.AbstractRobustChannel = await self._rmq_snd_conn.channel(
            publisher_confirms=True)
        # Connection and channel to receive
        self._rmq_rcv_conn = await aio_pika.connect_robust(host=self._config["rmqhost"],
                                                           port=_rmq_port,
                                                           client_properties={
                                                               "connection_name": (f"{self._dbname}"
                                                                                   f".{self._servicename}.rcv")
                                                           },
                                                           login=self._dbname,
                                                           password=self._secrets["rmq"],
                                                           ssl=self._SSL)
        self._rmq_rcv_channel: aio_pika.abc.AbstractRobustChannel = await self._rmq_rcv_conn.channel(
            publisher_confirms=True)

    async def _send_rmq(self, qname: str, o: Dict[str, Any], customttl: Optional[int] = None) -> bool:
        """
        Send standard message to RabbitMQ queue

        :param qname: queue name
        :param o: dict object to send
        :param customttl: set custom TTL otherwise service default is used
        """
        try:
            _qmsg = aio_pika.Message(body=dumps(o, ensure_ascii=False, default=self._dumps_time_float).encode("utf-8"),
                                     expiration=(self._TTL if customttl is None else customttl))
            _confirm = await self._rmq_snd_channel.default_exchange.publish(_qmsg,
                                                                            routing_key=qname)
            if not _confirm:
                self._log.warning(f"_send_rmq() not confirmed by broker: {qname}")
                return False
            else:
                return True
        except Exception as _exc:
            self._log.warning(f"_send_rmq() "
                              f"{_exc.__class__.__name__} - {_exc.args}:\n{format_exc().replace(chr(10), ' ')}")
            return False

    @staticmethod
    def get_stack_str(stack: List[FrameInfo]) -> Optional[str]:
        """
        Format call stack into string

        :param stack: result of inspect.stack()
        :return: string representing call stack
        """
        # Compose calling stack string
        if isinstance(stack, list):
            if len(stack) > 0:
                _stack = str()
                for _stack_item in stack:
                    if isinstance(_stack_item, FrameInfo):
                        _stack = f"{_stack_item.function}." + _stack
                return _stack.strip(".")
            else:
                return None
        else:
            return None

    @staticmethod
    def _dumps_default(o: Any) -> Union[str, int, float]:
        """
        Serialize to JSON recognized values
        """
        return str(o)

    @staticmethod
    def _dumps_time_float(o: Any) -> Union[str, int, float]:
        """
        Serialize datetime to JSON as float
        """
        if isinstance(o, datetime):
            return o.timestamp()

    def _log_dump(self, fname: str, o: Any) -> None:
        with open(f"/tmp/{fname}", "w") as _fd:
            _fd.write(dumps(o, ensure_ascii=False, indent=3, default=self._dumps_default))

    def _configure_psg_connections(self, cnames: List[str]) -> None:
        """
        Configure PostgreSQL connections before running setup

        :param cnames: list of connection names to establish to PostgreSQL
        """
        self._pg_conns_names = cnames

    async def _conn_psg(self) -> None:
        """
        Setup connections to PostgreSQL database.
        """
        self._pg = await asyncpg.create_pool(host=self._config["psqlhost"],
                                             user=self._dbname,
                                             password=self._secrets["psql"],
                                             database=self._dbname,
                                             max_inactive_connection_lifetime=65,
                                             statement_cache_size=256,
                                             max_cached_statement_lifetime=0,
                                             ssl=False,
                                             min_size=2,
                                             max_size=16)
        async with self._pg.acquire() as _c:
            _pg_version = _c.get_server_version()
            self._log.info(f"OK PostgreSQL connection pool created ["
                           f"{not _c.is_closed()}] server version "
                           f"{_pg_version[0]}.{_pg_version[1]}.{_pg_version[2]} {_pg_version[3]}")

    async def _shutdown_clear(self):
        """
        Generic clearing before shutdown virtual - to override in child classes
        """
        raise NotImplementedError("Must override _shutdown_clear()")

    async def _shutdown(self) -> None:
        """
        Safe shutdown
        """
        self._log.info(f"OK received SIGTERM")
        self._evloop.remove_signal_handler(signal.SIGTERM)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        with suppress(Exception):
            await self._rmq_snd_channel.close()
        with suppress(Exception):
            await self._rmq_rcv_channel.close()
        self._log.info(f"OK closed RabbitMQ channels")
        with suppress(Exception):
            await self._rmq_snd_conn.close()
        with suppress(Exception):
            await self._rmq_rcv_conn.close()
        self._log.info(f"OK closed RabbitMQ connections")
        with suppress(Exception):
            await self._aiohttp_control_site.stop()
        with suppress(Exception):
            await self._aiohttp_site.stop()
        with suppress(Exception):
            await self._aiohttp_app_runner.cleanup()
        with suppress(Exception):
            await self._aiohttp_app.cleanup()
        self._log.info(f"OK closed aiohttp server")
        with suppress(Exception):
            await self._pg.close()
        self._log.info(f"OK closed PostgreSQL database pool and driver")
        # Clear custom
        with suppress(Exception):
            await self._shutdown_clear()
        # Stop the cycle if it runs
        self._run_cycle = False
        # Wait for not finished tasks
        _tasks = [_t for _t in asyncio.all_tasks() if _t is not asyncio.current_task()]
        for _task in _tasks:
            with suppress(asyncio.exceptions.CancelledError):
                _task.cancel()
        with suppress(asyncio.exceptions.CancelledError):
            await asyncio.gather(*_tasks, return_exceptions=True)
        self._log.info(f"OK cancelled {len(_tasks)} outstanding tasks")
        self._evloop.stop()
        self._log.info(f"OK shut down")

    async def setup(self,
                    need_s3: bool = False,
                    need_web: bool = False,
                    need_rmq: bool = False,
                    need_psg: bool = False):
        """
        Setup routine

        :param need_s3: Set true to initiate S3 Storage client
        :param need_web: Set true to initiate web server, routes must already be initiated
        :param need_rmq: Set true to initiate RabbitMQ connections and channels
        :param need_psg: Connect to PostgreSQL database and acquire connection pool
        """
        # Configure web routes
        self._init_web_routes()
        # Log registered routes
        self._log.info(f"OK web server registered routes: {dumps(self._routes_registered, ensure_ascii=False)}")
        # Configure control web server
        await self._aiohttp_app_runner.setup()
        # Connect to the Object Storage
        if need_s3:
            await self._conn_s3()
            self._log.info(f"OK S3 init complete")
        # Initiate web server
        if need_web:
            self._aiohttp_site = web.TCPSite(self._aiohttp_app_runner, port=self._port)
            await self._aiohttp_site.start()
            self._log.info(f"OK TCPSite started")
        # Connect to RabbitMQ
        if need_rmq:
            await self._conn_rmq()
            self._need_rmq = True
            self._log.info(f"OK connected to RabbitMQ")
        # Connect to PostgreSQL database
        if need_psg:
            await self._conn_psg()
            self._need_psg = True
            self._log.info(f"OK connected to PostgreSQL")
        self._log.info(f"OK service {self._servicename} setup complete")
        # Ignore all not needed signals
        for snum in range(15):
            if snum + 1 not in [signal.SIGTERM, signal.SIGKILL]:
                signal.signal(snum + 1, signal.SIG_IGN)
        # And add linux signal handler for SIGTERM
        self._evloop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self._shutdown()))
