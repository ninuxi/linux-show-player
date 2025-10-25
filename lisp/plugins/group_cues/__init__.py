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

from lisp.core.plugin import Plugin
from lisp.cues.group_cue import GroupCue


class GroupCues(Plugin):
    """Plugin to enable Group Cues functionality"""
    
    Name = "Group Cues"
    Authors = ("Francesco Ceruti",)
    Description = "QLab-style group cues with simultaneous, sequential, and random execution modes"
    
    def __init__(self, app):
        super().__init__(app)
        
        # Register GroupCue type with the factory
        print(f"🔌 Loading plugin: {self.Name}")
        app.cue_factory.register_factory(GroupCue.__name__, GroupCue)
        app.window.registerSimpleCueMenu(GroupCue, GroupCue.Category)
        print(f"✅ Registered GroupCue in cue factory and menu")
        
        # Import settings to register them
        from lisp.cues import group_cue_settings  # noqa: F401
        print(f"✅ Registered GroupCue settings page")
