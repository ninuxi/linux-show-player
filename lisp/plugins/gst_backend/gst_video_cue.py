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

from lisp.plugins.gst_backend.gst_media_cue import GstMediaCue
from lisp.plugins.gst_backend.gi_repository import Gst
from lisp.plugins.gst_backend.gst_media import GstMedia


class GstVideoCue(GstMediaCue):
    """GStreamer-based video cue implementation extending the existing GstMediaCue"""
    Name = QT_TRANSLATE_NOOP("CueName", "Video Cue")

    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        
        # Set video-specific properties
        self.name = "Video Cue"
        
        print(f"Creating GstVideoCue with pipeline: {self.media.pipe if hasattr(self.media, 'pipe') else 'No pipe'}")
        
    def play(self):
        """Override play to add video-specific behavior"""
        print(f"Playing video cue with pipeline: {self.media.pipe}")
        super().play()
        
    def stop(self):
        """Override stop to add video-specific behavior"""  
        print("Stopping video cue")
        super().stop()
        

class GstVideoCueFactory:
    """Factory for creating GStreamer video cues using existing infrastructure"""
    
    def __init__(self, base_pipeline):
        self.base_pipeline = base_pipeline
        self.input = "UriInput"
        
    def __call__(self, app, id=None, **kwargs):
        """Create a new GStreamer video cue using existing factory pattern"""
        # Create using the existing GstMediaCue infrastructure  
        cue = GstVideoCue(app, id=id)
        
        # Set the pipeline to handle video files properly
        if self.base_pipeline and self.input:
            cue.media.pipe = [self.input] + self.base_pipeline
            
        return cue
    
    def pipeline(self):
        """Get the pipeline configuration"""
        if self.base_pipeline and self.input:
            return [self.input] + self.base_pipeline
        return []


# Alternative factory that creates video-enabled media cues  
class UriVideoCueFactory(GstVideoCueFactory):
    """Factory for URI-based video cues"""
    
    def __init__(self, base_pipeline):
        super().__init__(base_pipeline)
        self.input = "UriInput"
        
    def __call__(self, app, id=None, uri=None, **kwargs):
        """Create a video-capable media cue"""
        cue = super().__call__(app, id=id, **kwargs)
        
        # Set the URI like the audio cues do
        if uri is not None:
            try:
                cue.media.elements.UriInput.uri = uri
            except AttributeError:
                pass
        
        return cue