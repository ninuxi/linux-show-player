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

from PyQt5.QtCore import pyqtSignal

from lisp.backend.media_element import ElementType, MediaType
from lisp.core.properties import Property
from lisp.plugins.gst_backend.gst_element import GstMediaElement


class VideoSink(GstMediaElement):
    ElementType = ElementType.Output
    MediaType = MediaType.Video
    Name = "VideoSink"

    # Video-specific properties
    brightness = Property(default=0.5)
    contrast = Property(default=1.0)
    saturation = Property(default=1.0) 
    hue = Property(default=0.5)
    
    # Signals
    video_size_changed = pyqtSignal(int, int)

    def __init__(self, pipeline):
        super().__init__(pipeline)
        
        # GStreamer video elements
        self.videosink = None
        self.videobalance = None
        
    def sink(self):
        """Get the video sink element"""
        return self.videosink
        
    def prepare(self, to_start=False):
        """Prepare the video sink"""
        super().prepare(to_start)
        
        if self.videosink is not None:
            # Apply video properties
            if self.videobalance is not None:
                self.videobalance.set_property("brightness", self.brightness * 2 - 1)  # -1 to 1
                self.videobalance.set_property("contrast", self.contrast)  # 0 to 2
                self.videobalance.set_property("saturation", self.saturation)  # 0 to 2
                self.videobalance.set_property("hue", self.hue * 2 - 1)  # -1 to 1


class VideoBalance(GstMediaElement):
    ElementType = ElementType.Plugin
    MediaType = MediaType.Video
    Name = "VideoBalance"

    # Balance properties
    brightness = Property(default=0.0)
    contrast = Property(default=1.0)
    saturation = Property(default=1.0)
    hue = Property(default=0.0)

    def __init__(self, pipeline):
        super().__init__(pipeline)
        self.videobalance = None

    def prepare(self, to_start=False):
        """Prepare the video balance element"""
        super().prepare(to_start)
        
        if self.videobalance is not None:
            # Apply balance settings
            self.videobalance.set_property("brightness", self.brightness)
            self.videobalance.set_property("contrast", self.contrast) 
            self.videobalance.set_property("saturation", self.saturation)
            self.videobalance.set_property("hue", self.hue)