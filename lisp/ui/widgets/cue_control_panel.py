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

"""Compact control panel for cues"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QDoubleSpinBox, QCheckBox, QSlider, QPushButton, QFrame,
    QColorDialog, QScrollArea, QGridLayout, QSizePolicy
)
from PyQt5.QtGui import QColor

from lisp.ui.ui_utils import translate, css_to_dict, dict_to_css
from lisp.cues.group_cue import GroupCue


class CueControlPanel(QWidget):
    def _controller_flag_changed(self, state):
        """Applica subito la modifica controller e aggiorna la cue"""
        self._auto_apply()  # aggiorna il pannello
        # Aggiorna la cue nel modello tramite UpdateCueCommand
        try:
            from lisp.command.cue import UpdateCueCommand
            from lisp.application import Application
            cue = self.getCurrentCue()
            if cue is None:
                return
            updates = self.applyCue()
            if 'controller' in updates:
                app = Application()
                app.commands_stack.do(UpdateCueCommand(updates, cue))
                print(f"✅ Controller aggiornato per cue: {cue.name}")
        except Exception as e:
            print(f"❌ Errore aggiornamento controller: {e}")
    """Compact control panel at bottom"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_cue = None
        # Keep an initial snapshot of controller mappings so we can detect removals
        self._controller_initial = {}
        self._setup_ui()
        # Larger panel so everything is visible without scrolling
        self.setMinimumHeight(280)
        self.setMaximumHeight(400)
        
        # Make it visible with background color
        self.setStyleSheet(
            """
            CueControlPanel {
                background-color: #2a2a35;
                border-top: 3px solid #4a5a8f;
            }
            CueControlPanel, CueControlPanel * {
                color: #e8eaf1;
                font-size: 12px;
            }
            QGroupBox { 
                font-size: 12px; font-weight: 600; 
                border: 1px solid #3b415c; border-radius: 6px; margin-top: 10px; 
            }
            QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; color: #c7d1ff; }
            QLabel { color: #cfd3e0; }
            QDoubleSpinBox, QSpinBox { 
                background-color: #1f2230; border: 1px solid #5965a8; border-radius: 4px; 
                padding: 2px 6px; min-height: 26px; color: #e8eaf1; 
            }
            QSlider::groove:horizontal { background: #40455f; height: 6px; border-radius: 3px; }
            QSlider::handle:horizontal { background: #67a3ff; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }
            QCheckBox { spacing: 6px; }
            QPushButton { background-color: #30354b; border: 1px solid #5965a8; border-radius: 4px; padding: 4px 8px; }
            QPushButton:hover { background-color: #3a4060; }
            """
        )
        
    def _setup_ui(self):
        """Setup compact UI with improved readability"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        # Optional small header
        header = QLabel("Quick Controls")
        header.setStyleSheet("font-weight: 700; color: #c7d1ff;")
        main_layout.addWidget(header)

        # Make the panel scrollable in case of small screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        container = QWidget()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # Main controls grid (2x2)
        controls_layout = QGridLayout(container)
        controls_layout.setContentsMargins(4, 4, 4, 4)
        controls_layout.setHorizontalSpacing(12)
        controls_layout.setVerticalSpacing(10)

        # === TIMING GROUP ===
        timing_group = QGroupBox("Timing")
        timing_layout = QVBoxLayout(timing_group)
        timing_layout.setSpacing(4)

        # Fade In/Out in one row
        fade_layout = QHBoxLayout()
        fade_layout.addWidget(QLabel("Fade In:"))
        self.fade_in_spin = QDoubleSpinBox()
        self.fade_in_spin.setRange(0, 60)
        self.fade_in_spin.setSuffix(" s")
        self.fade_in_spin.setSingleStep(0.5)
        self.fade_in_spin.setMaximumWidth(100)
        fade_layout.addWidget(self.fade_in_spin)

        fade_layout.addSpacing(10)
        fade_layout.addWidget(QLabel("Out:"))
        self.fade_out_spin = QDoubleSpinBox()
        self.fade_out_spin.setRange(0, 60)
        self.fade_out_spin.setSuffix(" s")
        self.fade_out_spin.setSingleStep(0.5)
        self.fade_out_spin.setMaximumWidth(100)
        fade_layout.addWidget(self.fade_out_spin)
        timing_layout.addLayout(fade_layout)

        # Pre/Post Wait in one row
        wait_layout = QHBoxLayout()
        wait_layout.addWidget(QLabel("Pre-Wait:"))
        self.pre_wait_spin = QDoubleSpinBox()
        self.pre_wait_spin.setRange(0, 999)
        self.pre_wait_spin.setSuffix(" s")
        self.pre_wait_spin.setSingleStep(0.5)
        self.pre_wait_spin.setMaximumWidth(100)
        wait_layout.addWidget(self.pre_wait_spin)

        wait_layout.addSpacing(10)
        wait_layout.addWidget(QLabel("Post:"))
        self.post_wait_spin = QDoubleSpinBox()
        self.post_wait_spin.setRange(0, 999)
        self.post_wait_spin.setSuffix(" s")
        self.post_wait_spin.setSingleStep(0.5)
        self.post_wait_spin.setMaximumWidth(100)
        wait_layout.addWidget(self.post_wait_spin)
        timing_layout.addLayout(wait_layout)

        controls_layout.addWidget(timing_group, 0, 0)

        # === PLAYBACK GROUP ===
        playback_group = QGroupBox("Playback")
        playback_layout = QVBoxLayout(playback_group)
        playback_layout.setSpacing(4)

        # Volume with slider
        vol_layout = QHBoxLayout()
        vol_layout.addWidget(QLabel("Vol:"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 200)
        self.volume_slider.setValue(100)
        self.volume_slider.setMaximumWidth(220)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.setTickInterval(10)
        vol_layout.addWidget(self.volume_slider)
        self.volume_label = QLabel("100%")
        self.volume_label.setMinimumWidth(48)
        self.volume_label.setStyleSheet("font-weight: 600;")
        vol_layout.addWidget(self.volume_label)
        playback_layout.addLayout(vol_layout)

        # Checkboxes row
        checks_layout = QHBoxLayout()
        self.loop_check = QCheckBox("Loop")
        checks_layout.addWidget(self.loop_check)

        self.auto_follow_check = QCheckBox("Auto-follow")
        checks_layout.addWidget(self.auto_follow_check)
        checks_layout.addStretch()
        playback_layout.addLayout(checks_layout)

        controls_layout.addWidget(playback_group, 0, 1)

        # === CONTROLLERS GROUP ===
        controllers_group = QGroupBox("Controllers")
        controllers_layout = QVBoxLayout(controllers_group)
        controllers_layout.setSpacing(4)

        # MIDI
        midi_layout = QHBoxLayout()
        self.midi_check = QCheckBox("MIDI")
        self.midi_btn = QPushButton("Config")
        self.midi_btn.setMaximumWidth(70)
        self.midi_btn.setMaximumHeight(28)
        midi_layout.addWidget(self.midi_check)
        midi_layout.addWidget(self.midi_btn)
        midi_layout.addStretch()
        controllers_layout.addLayout(midi_layout)

        # OSC
        osc_layout = QHBoxLayout()
        self.osc_check = QCheckBox("OSC")
        self.osc_btn = QPushButton("Config")
        self.osc_btn.setMaximumWidth(70)
        self.osc_btn.setMaximumHeight(28)
        osc_layout.addWidget(self.osc_check)
        osc_layout.addWidget(self.osc_btn)
        osc_layout.addStretch()
        controllers_layout.addLayout(osc_layout)

        # Keyboard
        kbd_layout = QHBoxLayout()
        self.kbd_check = QCheckBox("Keyboard")
        self.kbd_btn = QPushButton("Set Key")
        self.kbd_btn.setMaximumWidth(80)
        self.kbd_btn.setMaximumHeight(28)
        kbd_layout.addWidget(self.kbd_check)
        kbd_layout.addWidget(self.kbd_btn)
        kbd_layout.addStretch()
        controllers_layout.addLayout(kbd_layout)

        controls_layout.addWidget(controllers_group, 1, 0)

        # === ACTIONS GROUP ===
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setSpacing(4)

        # Color picker
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_btn = QPushButton()
        self.color_btn.setMaximumWidth(60)
        self.color_btn.setMaximumHeight(26)
        self._cue_color = QColor(100, 150, 200)  # Default blue
        self.color_btn.setStyleSheet(f"QPushButton {{ background-color: {self._cue_color.name()}; border: 1px solid #333; }}")
        self.color_btn.clicked.connect(self._choose_color)
        color_layout.addWidget(self.color_btn)
        color_layout.addStretch()
        actions_layout.addLayout(color_layout)

        # Edit full settings button (Apply removed - now auto-apply)
        self.edit_full_btn = QPushButton("⚙ Full Settings...")
        self.edit_full_btn.setStyleSheet("QPushButton { padding: 6px 8px; }")
        actions_layout.addWidget(self.edit_full_btn)

        actions_layout.addStretch()
        controls_layout.addWidget(actions_group, 1, 1)

        # Improve stretching so the grid fills width nicely
        controls_layout.setColumnStretch(0, 1)
        controls_layout.setColumnStretch(1, 1)
        controls_layout.setRowStretch(0, 1)
        controls_layout.setRowStretch(1, 1)

        # Connect signals for auto-apply
        self.volume_slider.valueChanged.connect(
            lambda v: self.volume_label.setText(f"{v}%")
        )
        
        # Connect all controls to auto-apply changes
        self.fade_in_spin.valueChanged.connect(self._auto_apply)
        self.fade_out_spin.valueChanged.connect(self._auto_apply)
        self.pre_wait_spin.valueChanged.connect(self._auto_apply)
        self.post_wait_spin.valueChanged.connect(self._auto_apply)
        self.volume_slider.valueChanged.connect(self._auto_apply)
        self.loop_check.stateChanged.connect(self._auto_apply)
        self.auto_follow_check.stateChanged.connect(self._auto_apply)
        self.midi_check.stateChanged.connect(self._controller_flag_changed)
        self.osc_check.stateChanged.connect(self._controller_flag_changed)
        self.kbd_check.stateChanged.connect(self._controller_flag_changed)

        # Initially disabled
        self.setEnabled(False)
    
        """Applica subito la modifica controller e aggiorna la cue"""
        self._auto_apply()  # aggiorna il pannello
        # Aggiorna la cue nel modello tramite UpdateCueCommand
        try:
            from lisp.command.cue import UpdateCueCommand
            from lisp.application import Application
            cue = self.getCurrentCue()
            if cue is None:
                return
            updates = self.applyCue()
            if 'controller' in updates:
                app = Application()
                app.commands_stack.do(UpdateCueCommand(updates, cue))
                print(f"✅ Controller aggiornato per cue: {cue.name}")
        except Exception as e:
            print(f"❌ Errore aggiornamento controller: {e}")
    def _auto_apply(self):
        """Automatically apply changes when controls are modified"""
        # Don't apply if signals are blocked (loading cue data)
        if self.signalsBlocked():
            return
        
        if self._current_cue is None:
            return
        
        # Emit signal to parent to apply changes
        # The parent view will handle the actual application
        try:
            # Get parent view and trigger apply
            parent = self.parent()
            while parent and not hasattr(parent, '_ListLayoutView__applyControlPanelChanges'):
                parent = parent.parent()
            
            if parent and hasattr(parent, '_ListLayoutView__applyControlPanelChanges'):
                parent._ListLayoutView__applyControlPanelChanges()
        except Exception as e:
            print(f"⚠️ Auto-apply error: {e}")
    
    def _choose_color(self):
        """Open color picker dialog"""
        color = QColorDialog.getColor(self._cue_color, self, "Choose Cue Color")
        if color.isValid():
            self._cue_color = color
            self.color_btn.setStyleSheet(f"QPushButton {{ background-color: {color.name()}; border: 1px solid #333; }}")
            # Auto-apply color change
            self._auto_apply()
    
    def setCue(self, cue):
        """Load cue data into panel"""
        self._current_cue = cue
        self._controller_initial = {}
        
        if cue is None:
            self.setEnabled(False)
            return
        
        self.setEnabled(True)
        
        print(f"📥 setCue called with: {cue.name if cue else 'None'}")
        
        # Block signals while loading
        self.blockSignals(True)
        
        try:
            # Timing - convert milliseconds to seconds
            self.fade_in_spin.setValue(cue.fadein_duration / 1000.0)
            self.fade_out_spin.setValue(cue.fadeout_duration / 1000.0)
            self.pre_wait_spin.setValue(cue.pre_wait / 1000.0)
            self.post_wait_spin.setValue(cue.post_wait / 1000.0)
            
            print(f"   Loaded timing: FadeIn={cue.fadein_duration}ms, FadeOut={cue.fadeout_duration}ms")
            
            # Playback - get volume/loop
            volume_value = 100  # default
            loop_value = 0  # default
            
            # Try to get volume and loop from media (only for MediaCue)
            if hasattr(cue, 'media') and cue.media is not None:
                print(f"   Media found: {type(cue.media)}")
                
                # Get volume element
                volume_elem = cue.media.element('Volume')
                if volume_elem is not None:
                    # Convert from 0.0-10.0 range to 0-200% range
                    volume_value = int(volume_elem.volume * 100)
                    print(f"   Volume element: {volume_elem.volume} -> {volume_value}%")
                else:
                    print(f"   ⚠️ No Volume element in media")
                
                # Get loop count
                loop_value = cue.media.loop
                print(f"   Loop value from media: {loop_value}")
            else:
                print(f"   ⚠️ No media attribute or media is None")

            # If GroupCue (no media), use group-level loop property
            if isinstance(cue, GroupCue):
                loop_value = getattr(cue, 'loop', 0)
            
            self.volume_slider.setValue(volume_value)
            self.loop_check.setChecked(loop_value != 0)  # Any non-zero = loop enabled
            
            print(f"   Set UI: Volume={volume_value}%, Loop={'ON' if loop_value != 0 else 'OFF'}")
            
            # Auto-follow (next_action)
            from lisp.cues.cue import CueNextAction
            self.auto_follow_check.setChecked(
                cue.next_action == CueNextAction.TriggerAfterWait.value or
                cue.next_action == CueNextAction.TriggerAfterEnd.value
            )
            
            # Controllers - check if settings exist
            # For now just disable them - will implement later
            self.midi_check.setChecked(False)
            self.osc_check.setChecked(False)
            self.kbd_check.setChecked(False)
            
            # Color - get from cue stylesheet (CSS -> dict)
            try:
                css = css_to_dict(getattr(cue, 'stylesheet', '') or '')
                bg = css.get('background') or '#6496c8'
            except Exception:
                bg = '#6496c8'
            self._cue_color = QColor(bg)
            self.color_btn.setStyleSheet(f"QPushButton {{ background-color: {self._cue_color.name()}; border: 1px solid #333; }}")
            
        finally:
            self.blockSignals(False)
            print(f"✅ setCue completed")
    
    def applyCue(self):
        """Get changes to apply to cue (returns dict for UpdateCueCommand)"""
        if self._current_cue is None:
            return {}

        updates = {}

        # Timing (convert seconds to milliseconds)
        updates['fadein_duration'] = int(self.fade_in_spin.value() * 1000)
        updates['fadeout_duration'] = int(self.fade_out_spin.value() * 1000)
        updates['pre_wait'] = int(self.pre_wait_spin.value() * 1000)
        updates['post_wait'] = int(self.post_wait_spin.value() * 1000)

        # Auto-follow - set next_action
        from lisp.cues.cue import CueNextAction
        if self.auto_follow_check.isChecked():
            updates['next_action'] = CueNextAction.TriggerAfterEnd.value
        else:
            updates['next_action'] = CueNextAction.DoNothing.value

        # Color - update stylesheet (dict -> CSS string)
        try:
            css = css_to_dict(getattr(self._current_cue, 'stylesheet', '') or '')
        except Exception:
            css = {}
        css['background'] = self._cue_color.name()
        if 'color' not in css:
            css['color'] = self._auto_contrast_text(self._cue_color)
        updates['stylesheet'] = dict_to_css(css)

        # Media properties (volume, loop)
        if hasattr(self._current_cue, 'media') and self._current_cue.media is not None:
            media_updates = {}
            volume_elem = self._current_cue.media.element('Volume')
            if volume_elem is not None:
                new_volume = self.volume_slider.value() / 100.0
                media_updates['Volume'] = {
                    'volume': new_volume,
                    'normal_volume': new_volume
                }
            if self.loop_check.isChecked():
                media_updates['loop'] = -1
            else:
                media_updates['loop'] = 0
            if media_updates:
                media_props = self._current_cue.media.properties()
                if 'loop' in media_updates:
                    media_props['loop'] = media_updates['loop']
                if 'Volume' in media_updates:
                    if 'elements' not in media_props:
                        media_props['elements'] = {}
                    if 'Volume' not in media_props['elements']:
                        media_props['elements']['Volume'] = {}
                    media_props['elements']['Volume'].update(media_updates['Volume'])
                updates['media'] = media_props
        elif isinstance(self._current_cue, GroupCue):
            updates['loop'] = -1 if self.loop_check.isChecked() else 0

        return updates
    
    def getCurrentCue(self):
        """Get current cue"""
        return self._current_cue

    # --- helpers ---
    def _auto_contrast_text(self, qcolor: QColor) -> str:
        """Return '#000000' or '#ffffff' based on perceived luminance.

        Uses the WCAG relative luminance approximation.
        """
        r, g, b, _ = qcolor.getRgb()
        # Normalize 0..1
        r /= 255.0
        g /= 255.0
        b /= 255.0
        # Gamma expansion
        def lin(c):
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        L = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
        return '#000000' if L > 0.6 else '#ffffff'
