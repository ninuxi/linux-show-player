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

from lisp.backend.media_element import MediaType
from lisp.core.properties import Property
from lisp.plugins.gst_backend.gst_element import GstMediaElement
from lisp.plugins.gst_backend.gi_repository import Gst


class VideoBalance(GstMediaElement):
    """GStreamer video balance element for color correction"""
    
    ElementType = "videobalance"
    MediaType = MediaType.Video
    Name = "Video Balance"

    brightness = Property(default=0.0)  # -1.0 to 1.0
    contrast = Property(default=0.0)    # -1.0 to 1.0
    saturation = Property(default=0.0)  # -1.0 to 1.0
    hue = Property(default=0.0)         # -1.0 to 1.0

    def __init__(self):
        super().__init__()
        
        # Connect property changes to GStreamer element
        self.changed("brightness").connect(self._update_brightness)
        self.changed("contrast").connect(self._update_contrast) 
        self.changed("saturation").connect(self._update_saturation)
        self.changed("hue").connect(self._update_hue)

    def _update_brightness(self, value):
        if self.gst_element:
            self.gst_element.set_property("brightness", value)

    def _update_contrast(self, value):
        if self.gst_element:
            self.gst_element.set_property("contrast", value)

    def _update_saturation(self, value):
        if self.gst_element:
            self.gst_element.set_property("saturation", value)

    def _update_hue(self, value):
        if self.gst_element:
            self.gst_element.set_property("hue", value)

    def setup_gst_element(self):
        """Setup the GStreamer element with initial properties"""
        if self.gst_element:
            self.gst_element.set_property("brightness", self.brightness)
            self.gst_element.set_property("contrast", self.contrast)
            self.gst_element.set_property("saturation", self.saturation)
            self.gst_element.set_property("hue", self.hue)


class VideoSink(GstMediaElement):
    """GStreamer video sink element for video output"""
    
    ElementType = "autovideosink"  # Auto-detect best video sink
    MediaType = MediaType.Video
    Name = "Video Sink"

    # Video sink properties
    video_output = Property(default="default")
    fullscreen = Property(default=False)
    
    # Signals
    video_size_changed = pyqtSignal(int, int)  # width, height

    def __init__(self):
        super().__init__()
        
        # Connect property changes
        self.changed("video_output").connect(self._update_output)
        self.changed("fullscreen").connect(self._update_fullscreen)

    def _update_output(self, output):
        """Update video output configuration"""
        # Implementation depends on the specific sink being used
        pass

    def _update_fullscreen(self, fullscreen):
        """Update fullscreen mode"""
        # Implementation depends on the specific sink being used
        pass

    def setup_gst_element(self):
        """Setup the GStreamer element"""
        # Configure the video sink based on available options
        if self.gst_element:
            # Set up any initial properties
            pass


class VideoConverter(GstMediaElement):
    """GStreamer video converter element"""
    
    ElementType = "videoconvert"
    MediaType = MediaType.Video
    Name = "Video Convert"

    def __init__(self):
        super().__init__()


class VideoScale(GstMediaElement):
    """GStreamer video scale element for resizing"""
    
    ElementType = "videoscale"
    MediaType = MediaType.Video
    Name = "Video Scale"

    # Scaling properties
    method = Property(default="bilinear")
    add_borders = Property(default=False)

    def __init__(self):
        super().__init__()
        
        self.changed("method").connect(self._update_method)
        self.changed("add_borders").connect(self._update_borders)

    def _update_method(self, method):
        if self.gst_element:
            # Convert method name to GStreamer constant
            method_map = {
                "nearest": 0,
                "bilinear": 1, 
                "bicubic": 2,
                "lanczos": 3
            }
            if method in method_map:
                self.gst_element.set_property("method", method_map[method])

    def _update_borders(self, add_borders):
        if self.gst_element:
            self.gst_element.set_property("add-borders", add_borders)

    def setup_gst_element(self):
        if self.gst_element:
            self._update_method(self.method)
            self._update_borders(self.add_borders)


class VideoRate(GstMediaElement):
    """GStreamer video rate element for framerate control"""
    
    ElementType = "videorate"
    MediaType = MediaType.Video
    Name = "Video Rate"

    # Rate properties
    max_rate = Property(default=0)  # 0 = no limit
    drop_only = Property(default=False)

    def __init__(self):
        super().__init__()
        
        self.changed("max_rate").connect(self._update_max_rate)
        self.changed("drop_only").connect(self._update_drop_only)

    def _update_max_rate(self, max_rate):
        if self.gst_element and max_rate > 0:
            # Set max framerate
            caps = Gst.Caps.from_string(f"video/x-raw,framerate={max_rate}/1")
            # Apply caps filter if needed

    def _update_drop_only(self, drop_only):
        if self.gst_element:
            self.gst_element.set_property("drop-only", drop_only)

    def setup_gst_element(self):
        if self.gst_element:
            self._update_drop_only(self.drop_only)


class VideoFilter(GstMediaElement):
    """Base class for video filter elements"""
    
    MediaType = MediaType.Video

    def __init__(self):
        super().__init__()


# Register video elements
def register_video_elements():
    """Register all video elements with the GStreamer backend"""
    from lisp.plugins.gst_backend.elements import register_element
    from lisp.plugins.gst_backend.elements.auto_video_sink import AutoVideoSink
    
    # Register video processing elements
    register_element(VideoBalance)
    register_element(VideoConverter) 
    register_element(VideoScale)
    register_element(VideoRate)
    register_element(VideoSink)
    register_element(VideoFilter)
    
    # Register video output elements
    register_element(AutoVideoSink)