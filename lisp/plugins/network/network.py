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

from lisp.core.plugin import Plugin
from lisp.plugins.network.api import route_all
from lisp.plugins.network.discovery import Announcer
from lisp.plugins.network.server import APIServerThread


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

        # WSGI Server
        self.server = None
        try:
            self.server = APIServerThread(
                Network.Config["host"], Network.Config["port"], self.api
            )
            self.server.start()
        except Exception:
            # If binding fails or any other error, keep plugin loaded but without network server
            self.server = None

        # Announcer
        self.announcer = None
        try:
            self.announcer = Announcer(
                Network.Config["host"],
                Network.Config["discovery.port"],
                Network.Config["discovery.magic"],
            )
            self.announcer.start()
        except Exception:
            self.announcer = None

    def finalize(self=None):
        # Allow being called on class or instance safely
        try:
            if self is not None and getattr(self, 'announcer', None) is not None:
                self.announcer.stop()
        except Exception:
            pass
        try:
            if self is not None and getattr(self, 'server', None) is not None:
                self.server.stop()
        except Exception:
            pass
        try:
            if self is not None:
                super(Network, self).finalize()
        except Exception:
            pass
