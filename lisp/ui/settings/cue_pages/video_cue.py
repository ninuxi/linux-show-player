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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, 
    QSlider, QCheckBox, QComboBox, QPushButton,
    QSpinBox, QDoubleSpinBox
)

from lisp.ui.settings.pages import CueSettingsPage
from lisp.ui.ui_utils import translate


class VideoCueSettings(CueSettingsPage):
    Name = "Video"

    def __init__(self, cueType, **kwargs):
        # Conform to CueSettingsPage signature: first arg is cueType (cue class)
        super().__init__(cueType, **kwargs)
        self.setLayout(QVBoxLayout())
        
        # Video Output Settings
        self.outputGroup = QGroupBox(translate("VideoCueSettings", "Video Output"))
        self.outputGroup.setLayout(QVBoxLayout())
        self.layout().addWidget(self.outputGroup)
        
        # Output selection
        outputLayout = QHBoxLayout()
        outputLayout.addWidget(QLabel(translate("VideoCueSettings", "Output:")))
        
        self.outputCombo = QComboBox()
        self.outputCombo.addItems([
            translate("VideoCueSettings", "Default"),
            translate("VideoCueSettings", "Primary Display"),
            translate("VideoCueSettings", "Secondary Display"),
            translate("VideoCueSettings", "Custom Window")
        ])
        outputLayout.addWidget(self.outputCombo)
        outputLayout.addStretch()
        
        self.outputGroup.layout().addLayout(outputLayout)
        
        # Fullscreen option
        fullscreenLayout = QHBoxLayout()
        self.fullscreenCheck = QCheckBox(translate("VideoCueSettings", "Start in fullscreen"))
        fullscreenLayout.addWidget(self.fullscreenCheck)
        fullscreenLayout.addStretch()
        self.outputGroup.layout().addLayout(fullscreenLayout)
        
        # Video Properties
        self.propertiesGroup = QGroupBox(translate("VideoCueSettings", "Video Properties"))
        self.propertiesGroup.setLayout(QVBoxLayout())
        self.layout().addWidget(self.propertiesGroup)
        
        # Aspect Ratio
        aspectLayout = QHBoxLayout()
        aspectLayout.addWidget(QLabel(translate("VideoCueSettings", "Aspect Ratio:")))
        
        self.aspectCombo = QComboBox()
        self.aspectCombo.addItems([
            translate("VideoCueSettings", "Auto"),
            translate("VideoCueSettings", "4:3"),
            translate("VideoCueSettings", "16:9"),
            translate("VideoCueSettings", "16:10"),
            translate("VideoCueSettings", "Custom")
        ])
        aspectLayout.addWidget(self.aspectCombo)
        aspectLayout.addStretch()
        
        self.propertiesGroup.layout().addLayout(aspectLayout)
        
        # Video Effects
        self.effectsGroup = QGroupBox(translate("VideoCueSettings", "Video Effects"))
        self.effectsGroup.setLayout(QVBoxLayout())
        self.layout().addWidget(self.effectsGroup)
        
        # Brightness
        brightnessLayout = QHBoxLayout()
        brightnessLayout.addWidget(QLabel(translate("VideoCueSettings", "Brightness:")))
        
        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setRange(-100, 100)
        self.brightnessSlider.setValue(0)
        brightnessLayout.addWidget(self.brightnessSlider)
        
        self.brightnessLabel = QLabel("0")
        self.brightnessLabel.setMinimumWidth(30)
        brightnessLayout.addWidget(self.brightnessLabel)
        
        self.effectsGroup.layout().addLayout(brightnessLayout)
        
        # Contrast
        contrastLayout = QHBoxLayout()
        contrastLayout.addWidget(QLabel(translate("VideoCueSettings", "Contrast:")))
        
        self.contrastSlider = QSlider(Qt.Horizontal)
        self.contrastSlider.setRange(-100, 100)
        self.contrastSlider.setValue(0)
        contrastLayout.addWidget(self.contrastSlider)
        
        self.contrastLabel = QLabel("0")
        self.contrastLabel.setMinimumWidth(30)
        contrastLayout.addWidget(self.contrastLabel)
        
        self.effectsGroup.layout().addLayout(contrastLayout)
        
        # Saturation
        saturationLayout = QHBoxLayout()
        saturationLayout.addWidget(QLabel(translate("VideoCueSettings", "Saturation:")))
        
        self.saturationSlider = QSlider(Qt.Horizontal)
        self.saturationSlider.setRange(-100, 100)
        self.saturationSlider.setValue(0)
        saturationLayout.addWidget(self.saturationSlider)
        
        self.saturationLabel = QLabel("0")
        self.saturationLabel.setMinimumWidth(30)
        saturationLayout.addWidget(self.saturationLabel)
        
        self.effectsGroup.layout().addLayout(saturationLayout)
        
        # Hue
        hueLayout = QHBoxLayout()
        hueLayout.addWidget(QLabel(translate("VideoCueSettings", "Hue:")))
        
        self.hueSlider = QSlider(Qt.Horizontal)
        self.hueSlider.setRange(-180, 180)
        self.hueSlider.setValue(0)
        hueLayout.addWidget(self.hueSlider)
        
        self.hueLabel = QLabel("0°")
        self.hueLabel.setMinimumWidth(40)
        hueLayout.addWidget(self.hueLabel)
        
        self.effectsGroup.layout().addLayout(hueLayout)
        
        # Video Fade
        fadeLayout = QHBoxLayout()
        self.videoFadeCheck = QCheckBox(translate("VideoCueSettings", "Enable video fade effects"))
        fadeLayout.addWidget(self.videoFadeCheck)
        fadeLayout.addStretch()
        self.effectsGroup.layout().addLayout(fadeLayout)
        
        self.layout().addStretch()
        
        # Connect signals
        self._connectSignals()
        
    def _connectSignals(self):
        """Connect widget signals to update methods"""
        self.outputCombo.currentTextChanged.connect(self._updateVideoOutput)
        self.fullscreenCheck.toggled.connect(self._updateFullscreen)
        self.aspectCombo.currentTextChanged.connect(self._updateAspectRatio)
        
        self.brightnessSlider.valueChanged.connect(self._updateBrightness)
        self.contrastSlider.valueChanged.connect(self._updateContrast)
        self.saturationSlider.valueChanged.connect(self._updateSaturation)
        self.hueSlider.valueChanged.connect(self._updateHue)
        self.videoFadeCheck.toggled.connect(self._updateVideoFade)
        
    def _updateBrightness(self, value):
        """Update brightness label and cue property"""
        self.brightnessLabel.setText(str(value))
        if hasattr(self.cue, 'brightness'):
            self.cue.brightness = (value + 100) / 200.0  # Convert to 0.0-1.0 range
            
    def _updateContrast(self, value):
        """Update contrast label and cue property"""
        self.contrastLabel.setText(str(value))
        if hasattr(self.cue, 'contrast'):
            self.cue.contrast = (value + 100) / 200.0  # Convert to 0.0-1.0 range
            
    def _updateSaturation(self, value):
        """Update saturation label and cue property"""
        self.saturationLabel.setText(str(value))
        if hasattr(self.cue, 'saturation'):
            self.cue.saturation = (value + 100) / 200.0  # Convert to 0.0-1.0 range
            
    def _updateHue(self, value):
        """Update hue label and cue property"""
        self.hueLabel.setText(f"{value}°")
        if hasattr(self.cue, 'hue'):
            self.cue.hue = (value + 180) / 360.0  # Convert to 0.0-1.0 range
            
    def _updateVideoOutput(self, output):
        """Update video output setting"""
        if hasattr(self.cue, 'video_output'):
            self.cue.video_output = output.lower().replace(" ", "_")
            
    def _updateFullscreen(self, fullscreen):
        """Update fullscreen setting"""
        if hasattr(self.cue, 'fullscreen'):
            self.cue.fullscreen = fullscreen
            
    def _updateAspectRatio(self, aspect):
        """Update aspect ratio setting"""
        if hasattr(self.cue, 'aspect_ratio'):
            self.cue.aspect_ratio = aspect.lower().replace(":", "_")
            
    def _updateVideoFade(self, enabled):
        """Update video fade setting"""
        if hasattr(self.cue, 'video_fade'):
            self.cue.video_fade = enabled

    def getSettings(self):
        """Get current settings from widgets"""
        settings = {}
        
        if hasattr(self.cue, 'video_output'):
            settings['video_output'] = self.outputCombo.currentText().lower().replace(" ", "_")
        if hasattr(self.cue, 'fullscreen'):
            settings['fullscreen'] = self.fullscreenCheck.isChecked()
        if hasattr(self.cue, 'aspect_ratio'):
            settings['aspect_ratio'] = self.aspectCombo.currentText().lower().replace(":", "_")
            
        if hasattr(self.cue, 'brightness'):
            settings['brightness'] = (self.brightnessSlider.value() + 100) / 200.0
        if hasattr(self.cue, 'contrast'):
            settings['contrast'] = (self.contrastSlider.value() + 100) / 200.0
        if hasattr(self.cue, 'saturation'):
            settings['saturation'] = (self.saturationSlider.value() + 100) / 200.0
        if hasattr(self.cue, 'hue'):
            settings['hue'] = (self.hueSlider.value() + 180) / 360.0
            
        if hasattr(self.cue, 'video_fade'):
            settings['video_fade'] = self.videoFadeCheck.isChecked()
            
        return settings

    def loadSettings(self, settings):
        """Load settings into widgets"""
        if 'video_output' in settings:
            output = settings['video_output'].replace("_", " ").title()
            index = self.outputCombo.findText(output)
            if index >= 0:
                self.outputCombo.setCurrentIndex(index)
                
        if 'fullscreen' in settings:
            self.fullscreenCheck.setChecked(settings['fullscreen'])
            
        if 'aspect_ratio' in settings:
            aspect = settings['aspect_ratio'].replace("_", ":")
            index = self.aspectCombo.findText(aspect)
            if index >= 0:
                self.aspectCombo.setCurrentIndex(index)
                
        if 'brightness' in settings:
            value = int(settings['brightness'] * 200 - 100)
            self.brightnessSlider.setValue(value)
            
        if 'contrast' in settings:
            value = int(settings['contrast'] * 200 - 100)
            self.contrastSlider.setValue(value)
            
        if 'saturation' in settings:
            value = int(settings['saturation'] * 200 - 100)
            self.saturationSlider.setValue(value)
            
        if 'hue' in settings:
            value = int(settings['hue'] * 360 - 180)
            self.hueSlider.setValue(value)
            
        if 'video_fade' in settings:
            self.videoFadeCheck.setChecked(settings['video_fade'])