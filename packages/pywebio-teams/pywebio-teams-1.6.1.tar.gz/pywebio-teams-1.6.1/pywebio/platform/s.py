import asyncio
import fnmatch
import json
import logging
import os
import threading
import time
import webbrowser
from functools import partial
from typing import Dict
from urllib.parse import urlparse
import typing
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.websocket

from .adaptor import ws as ws_adaptor
from . import page
from .remote_access import start_remote_access_service
from .page import make_applications, render_page
from .utils import cdn_validation, deserialize_binary_event, print_listen_address
from ..session import CoroutineBasedSession, ThreadBasedSession, ScriptModeSession, \
    register_session_implement_for_target, Session
from ..session.base import get_session_info_from_headers
from ..utils import get_free_port, wait_host_port, STATIC_PATH, iscoroutinefunction, isgeneratorfunction, \
    check_webio_js, parse_file_size, random_str, LRUDict

logger = logging.getLogger(__name__)


class WebSocketConnection(ws_adaptor.WebSocketConnection):

    def __init__(self, context: tornado.websocket.WebSocketHandler):
        self.context = context

    def get_query_argument(self, name) -> typing.Optional[str]:
        return self.context.get_query_argument(name, None)

    def make_session_info(self) -> dict:
        session_info = get_session_info_from_headers(self.context.request.headers)
        session_info['user_ip'] = self.context.request.remote_ip
        session_info['request'] = self.context.request
        session_info['backend'] = 'tornado'
        session_info['protocol'] = 'websocket'
        return session_info

    def write_message(self, message: dict):
        self.context.write_message(json.dumps(message))

    def closed(self) -> bool:
        return bool(self.context.ws_connection)

    def close(self):
        self.context.close()


def _webio_handler(applications=None, cdn=True, reconnect_timeout=0, check_origin_func=_is_same_site):  # noqa: C901
    """
    :param dict applications: dict of `name -> task function`
    :param bool/str cdn: Whether to load front-end static resources from CDN
    :param callable check_origin_func: check_origin_func(origin, handler) -> bool
    :return: Tornado RequestHandler class
    """
    check_webio_js()

    if applications is None:
        applications = dict(index=lambda: None)  # mock PyWebIO app

    ws_adaptor.set_expire_second(reconnect_timeout)
    tornado.ioloop.IOLoop.current().spawn_callback(ws_adaptor.session_clean_task)

    class Handler(tornado.websocket.WebSocketHandler):

        def get_app(self):
            app_name = self.get_query_argument('app', 'index')
            app = applications.get(app_name) or applications['index']
            return app

        def get_cdn(self):
            if cdn is True and self.get_query_argument('_pywebio_cdn', '') == 'false':
                return False
            return cdn

        async def get(self, *args, **kwargs) -> None:
            """http GET request"""
            if self.request.headers.get("Upgrade", "").lower() != "websocket":
                # Backward compatible
                # Frontend detect whether the backend is http server
                if self.get_query_argument('test', ''):
                    return self.write('')

                app = self.get_app()
                html = render_page(app, protocol='ws', cdn=self.get_cdn())
                return self.write(html)
            else:
                await super().get()

        def check_origin(self, origin):
            return check_origin_func(origin=origin, handler=self)

        def get_compression_options(self):
            # Non-None enables compression with default options.
            return {}

        _handler: ws_adaptor.WebSocketHandler

        def open(self):
            conn = WebSocketConnection(self)
            self._handler = ws_adaptor.WebSocketHandler(
                connection=conn, application=self.get_app(), reconnectable=bool(reconnect_timeout)
            )

        def on_message(self, message):
            self._handler.send_client_data(message)

        def on_close(self):
            self._handler.notify_connection_lost()

    return Handler
