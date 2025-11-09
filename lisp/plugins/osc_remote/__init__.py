# This file is part of Linux Show Player
#
# Copyright 2025 Francesco Ceruti <ceppofrancy@gmail.com>
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

"""OSC Server Plugin

Modern OSC server for controlling Linux Show Player via OSC commands.
Supports simple commands like /lsp/cue/1/start and /lsp/go.
Also includes automatic Companion/Stream Deck integration.
"""

from lisp.core.plugin import Plugin
from lisp.plugins.osc_remote.osc_bridge import OscBridge
from lisp.plugins.osc_remote.osc_settings import OscSettings
from lisp.ui.settings.app_configuration import AppConfigurationDialog


class OscRemote(Plugin):
    """OSC Remote Control for external devices"""

    Name = "OSC Remote"
    Authors = ("Linux Show Player Team",)
    Description = "OSC remote control for Companion/Stream Deck and other devices"

    def __init__(self, app):
        super().__init__(app)

        # Register settings page
        AppConfigurationDialog.registerSettingsPage(
            "plugins.osc_remote",
            OscSettings,
            OscRemote.Config
        )

        # Create bridge instance
        self.__bridge = OscBridge(
            app=app,
            config=OscRemote.Config
        )
        self.__bridge.start()

        # React to config changes
        OscRemote.Config.changed.connect(self.__config_change)
        OscRemote.Config.updated.connect(self.__config_update)

    @property
    def bridge(self):
        return self.__bridge

    def terminate(self):
        self.__bridge.stop()

    def __config_change(self, key, value):
        if key == "enabled":
            if value:
                self.__bridge.start()
            else:
                self.__bridge.stop()
        elif key == "osc_port":
            self.__bridge.osc_port = value
        elif key == "auto_map_cues":
            self.__bridge.auto_map = value

    def __config_update(self, diff):
        for key, value in diff.items():
            self.__config_change(key, value)
