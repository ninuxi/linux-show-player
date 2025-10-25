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
from PyQt5.QtWidgets import QWidget

from lisp.core.properties import Property
from lisp.core.signal import Signal
from lisp.cues.media_cue import MediaCue


class VideoCue(MediaCue):
    """Video cue with video-specific features"""
    Name = QT_TRANSLATE_NOOP("CueName", "Video Cue")
    
    # Video-specific properties
    video_output = Property(default="default")
    fullscreen = Property(default=False)
    aspect_ratio = Property(default="auto")
    brightness = Property(default=0.5)
    contrast = Property(default=0.5)
    saturation = Property(default=0.5)
    hue = Property(default=0.5)
    video_fade = Property(default=False)  # Enable video fade effects
    
    # Signals for video-specific events (using lisp Signal instead of PyQt)
    video_output_changed = Signal()
    
    def __init__(self, app, media, id=None, video_widget=None):
        super().__init__(app, media, id=id)
        self._video_widget = video_widget
        self._is_fullscreen = False
        
        # Connect to property changes
        self.changed('fullscreen').connect(self._on_fullscreen_changed)
        self.changed('video_output').connect(self._on_video_output_changed)
        
    @property
    def video_widget(self):
        """Get the video widget for this cue"""
        return self._video_widget
    
    @video_widget.setter
    def video_widget(self, widget):
        """Set the video widget for this cue"""
        self._video_widget = widget
        
    def set_fullscreen(self, fullscreen: bool):
        """Toggle fullscreen mode for video output"""
        self.fullscreen = fullscreen
        
    def _on_fullscreen_changed(self, fullscreen):
        """Handle fullscreen property change"""
        if self._video_widget and self._state.is_running():
            if fullscreen and not self._is_fullscreen:
                self._video_widget.showFullScreen()
                self._is_fullscreen = True
            elif not fullscreen and self._is_fullscreen:
                self._video_widget.showNormal()
                self._is_fullscreen = False
                
    def _on_video_output_changed(self, output):
        """Handle video output change"""
        self.video_output_changed.emit()
        
    def get_video_element(self):
        """Get the video element from the media pipeline"""
        if hasattr(self.media, 'element'):
            return self.media.element('VideoSink')
        return None
        
    def apply_video_effects(self):
        """Apply video effects like brightness, contrast, etc."""
        video_element = self.get_video_element()
        if video_element:
            video_element.brightness = self.brightness
            video_element.contrast = self.contrast
            video_element.saturation = self.saturation
            video_element.hue = self.hue
            
    def __start__(self, fade=False):
        """Override start to apply video-specific settings"""
        # Apply video effects before starting
        self.apply_video_effects()
        
        # Handle fullscreen if needed
        if self.fullscreen and self._video_widget:
            self._video_widget.showFullScreen()
            self._is_fullscreen = True
            
        return super().__start__(fade)
        
    def __stop__(self, fade=False):
        """Override stop to handle video-specific cleanup"""
        # Exit fullscreen if needed
        if self._is_fullscreen and self._video_widget:
            self._video_widget.showNormal()
            self._is_fullscreen = False
            
        return super().__stop__(fade)