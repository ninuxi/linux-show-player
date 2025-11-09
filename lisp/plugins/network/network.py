# This file is part of Linux Show Player
#
# Copyright 2017 Francesco Ceruti <ceppofrancy@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

from falcon import App

from lisp.core.plugin import Plugin, logger
from lisp.plugins.network.api import route_all
from lisp.plugins.network.discovery import Announcer
from lisp.plugins.network.server import APIServerThread
from lisp.ui.ui_utils import translate


class Network(Plugin):
    Name = "Network"
    Description = "Allow the application to be controlled via network."
    Authors = ("Francesco Ceruti",)

    def __init__(self, app):
        super().__init__(app)
        self.api = App()
        # We don't support HTTPS (yet?)
        self.api.resp_options.secure_cookies_by_default = False
        # Load all the api endpoints
        route_all(self.app, self.api)
        # WSGI Server (best-effort)
        self.server = None
        try:
            self.server = APIServerThread(
                Network.Config["host"], Network.Config["port"], self.api
            )
            self.server.start()
        except Exception as e:
            logger.exception(
                translate(
                    "PluginsError",
                    'Network plugin: could not start API server: "{}"',
                ).format(str(e))
            )

        # Announcer (best-effort)
        self.announcer = None
        try:
            self.announcer = Announcer(
                Network.Config["host"],
                Network.Config["discovery.port"],
                Network.Config["discovery.magic"],
            )
            self.announcer.start()
        except Exception as e:
            logger.exception(
                translate(
                    "PluginsError",
                    'Network plugin: could not start discovery announcer: "{}"',
                ).format(str(e))
            )

    def terminate(self):
        try:
            if getattr(self, "announcer", None) is not None:
                self.announcer.stop()
        except Exception:
            logger.exception("Error while stopping network announcer")

        try:
            if getattr(self, "server", None) is not None:
                self.server.stop()
        except Exception:
            logger.exception("Error while stopping network server")
