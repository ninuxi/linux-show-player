# This file is part of Linux Show Player
#
# Copyright 2024 Francesco Ceruti <ceppofrancy@gmail.com>
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

from PyQt5.QtCore import QT_TRANSLATE_NOOP

from lisp.backend.media_element import ElementType, MediaType
from lisp.plugins.gst_backend.gi_repository import Gst
from lisp.plugins.gst_backend.gst_element import GstMediaElement


class AutoVideoSink(GstMediaElement):
    ElementType = ElementType.Output
    MediaType = MediaType.Video
    Name = QT_TRANSLATE_NOOP("MediaElementName", "Auto Video Out")

    def __init__(self, pipeline):
        super().__init__(pipeline)

        # Create a proper video sink element that can be linked
        self.video_sink = Gst.ElementFactory.make("autovideosink", "videosink")
        if self.video_sink is None:
            # Fallback to xvimagesink
            self.video_sink = Gst.ElementFactory.make("xvimagesink", "videosink")
        if self.video_sink is None:
            # Second fallback to ximagesink  
            self.video_sink = Gst.ElementFactory.make("ximagesink", "videosink")
            
        if self.video_sink is not None:
            self.pipeline.add(self.video_sink)

    def sink(self):
        return self.video_sink