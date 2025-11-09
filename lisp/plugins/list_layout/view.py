# This file is part of Linux Show Player
#
# Copyright 2018 Francesco Ceruti <ceppofrancy@gmail.com>
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
from PyQt5.QtWidgets import QWidget, QSizePolicy, QSplitter, QVBoxLayout

from lisp.plugins.list_layout.list_view import CueListView
from lisp.plugins.list_layout.playing_view import RunningCuesListWidget
from lisp.ui.widgets.dynamicfontsize import DynamicFontSizePushButton
from lisp.ui.widgets.cue_control_panel import CueControlPanel
from lisp.ui.ui_utils import css_to_dict, dict_to_css
from lisp.cues.group_cue import GroupCue
from lisp.command.cue import UpdateCueCommand
from lisp.application import Application
from .control_buttons import ShowControlButtons
from .info_panel import InfoPanel


class ListLayoutView(QWidget):
    def __init__(self, listModel, runModel, config, *args):
        super().__init__(*args)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.listModel = listModel

        self.mainSplitter = QSplitter(Qt.Vertical, self)
        self.layout().addWidget(self.mainSplitter)

        self.topSplitter = QSplitter(Qt.Horizontal, self)
        self.centralSplitter = QSplitter(Qt.Horizontal, self)

        # GO-BUTTON (top-left)
        self.goButton = DynamicFontSizePushButton(parent=self)
        self.goButton.setText("GO")
        self.goButton.setMinimumWidth(60)
        self.goButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.goButton.setFocusPolicy(Qt.NoFocus)
        self.topSplitter.addWidget(self.goButton)
        
        # CREATE GROUP BUTTON (top-left-2)
        self.createGroupButton = DynamicFontSizePushButton(parent=self)
        self.createGroupButton.setText("+ Group")
        self.createGroupButton.setMinimumWidth(80)
        self.createGroupButton.setMaximumWidth(120)
        self.createGroupButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.createGroupButton.setFocusPolicy(Qt.NoFocus)
        self.createGroupButton.setStyleSheet("""
            QPushButton {
                background-color: #2a5a3a;
                border: 2px solid #3a7a4a;
                color: #e8fff0;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a7a4a;
                border: 2px solid #4a9a5a;
            }
            QPushButton:pressed {
                background-color: #1a4a2a;
            }
        """)
        self.topSplitter.addWidget(self.createGroupButton)

        # INFO PANEL (top-center)
        self.infoPanel = InfoPanel(self)
        self.infoPanel.setMinimumWidth(300)
        self.infoPanel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Ignored)
        self.infoPanel.cueDescription.setFontPointSize(
            config.get(
                "infoPanelFontSize",
                self.infoPanel.cueDescription.fontPointSize(),
            )
        )
        self.topSplitter.addWidget(self.infoPanel)

        # CONTROL-BUTTONS (top-right)
        self.controlButtons = ShowControlButtons(self)
        self.controlButtons.setMinimumWidth(100)
        self.controlButtons.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Minimum
        )
        self.topSplitter.addWidget(self.controlButtons)

        # CUE VIEW (center-left)
        self.listView = CueListView(listModel, self)
        self.listView.setMinimumWidth(200)
        self.listView.currentItemChanged.connect(self.__listViewCurrentChanged)
        self.centralSplitter.addWidget(self.listView)
        self.centralSplitter.setCollapsible(0, False)

        # PLAYING VIEW (center-right)
        self.runView = RunningCuesListWidget(runModel, config, parent=self)
        self.runView.setMinimumWidth(200)
        self.runView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.centralSplitter.addWidget(self.runView)
        
        # Add top and central to main splitter
        self.mainSplitter.addWidget(self.topSplitter)
        self.mainSplitter.addWidget(self.centralSplitter)

        # CONTROL PANEL (bottom) - MUST BE VISIBLE!
        self.controlPanel = CueControlPanel(self)
        self.controlPanel.setMinimumHeight(280)
        self.controlPanel.setMaximumHeight(400)
        self.mainSplitter.addWidget(self.controlPanel)
        self.mainSplitter.setCollapsible(2, False)  # Panel cannot be collapsed
        
        # Set initial splitter sizes explicitly (before showEvent)
        # Use reasonable defaults: 100px top, 400px center, 300px panel
        self.mainSplitter.setSizes([100, 400, 300])
        
        print("✅ Control Panel added to layout!")
        
        # Connect control panel signals (Apply button removed - now auto-apply)
        self.controlPanel.edit_full_btn.clicked.connect(self.__openFullSettings)
        self.__userResized = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self.__userResized:
            self.resetSize()

    def resetSize(self):
        # Main splitter has 3 widgets: topSplitter, centralSplitter, controlPanel
        # Give most space to central, some to top, fixed to control panel
        total_height = self.height()
        
        # Ensure we have a reasonable height (at least 500px)
        if total_height < 500:
            total_height = 600
            
        panel_height = 300  # Larger panel to show all controls without scrolling
        top_height = max(80, int(0.15 * total_height))  # At least 80px for top bar
        center_height = total_height - top_height - panel_height  # Rest for cue list
        
        # Ensure center gets some space
        if center_height < 200:
            center_height = 200
        
        self.mainSplitter.setSizes([top_height, center_height, panel_height])
        
        self.centralSplitter.setSizes(
            (int(0.78 * self.width()), int(0.22 * self.width()))
        )
        self.topSplitter.setSizes(
            (
                int(0.08 * self.width()),  # GO button (reduced)
                int(0.10 * self.width()),  # Group button (new)
                int(0.60 * self.width()),  # Info panel (reduced)
                int(0.22 * self.width()),  # Control buttons
            )
        )

    def getSplitterSizes(self):
        return [
            self.mainSplitter.sizes(),
            self.topSplitter.sizes(),
            self.centralSplitter.sizes(),
        ]

    def setSplitterSize(self, sizes):
        if len(sizes) >= 3:
            self.mainSplitter.setSizes(sizes[0])
            self.topSplitter.setSizes(sizes[1])
            self.centralSplitter.setSizes(sizes[2])

            self.__userResized = True

    def setResizeHandlesEnabled(self, enabled):
        self.__setSplitterHandlesEnabled(self.mainSplitter, enabled)
        self.__setSplitterHandlesEnabled(self.topSplitter, enabled)
        self.__setSplitterHandlesEnabled(self.centralSplitter, enabled)

    def __setSplitterHandlesEnabled(self, splitter: QSplitter, enabled):
        for n in range(splitter.count()):
            splitter.handle(n).setEnabled(enabled)

    def __listViewCurrentChanged(self, current, _):
        cue = None
        if current is not None:
            index = self.listView.indexOfTopLevelItem(current)
            if index < len(self.listModel):
                cue = self.listModel.item(index)

        self.infoPanel.cue = cue
        
        # Update control panel with selected cue
        print(f"🔵 Loading cue into panel: {cue.name if cue else 'None'}")
        self.controlPanel.setCue(cue)
    
    def __applyControlPanelChanges(self):
        """Apply changes from control panel to cue"""
        cue = self.controlPanel.getCurrentCue()
        print(f"🟡 Apply button pressed. Current cue: {cue.name if cue else 'None'}")
        
        if cue is None:
            print("❌ No cue to apply changes to")
            return
        
        try:
            # Get timing updates from panel (returns seconds as floats)
            fade_in = self.controlPanel.fade_in_spin.value()
            fade_out = self.controlPanel.fade_out_spin.value()
            pre_wait = self.controlPanel.pre_wait_spin.value()
            post_wait = self.controlPanel.post_wait_spin.value()
            
            print(f"   Fade In: {fade_in}s, Fade Out: {fade_out}s")
            print(f"   Pre-Wait: {pre_wait}s, Post-Wait: {post_wait}s")
            
            # Apply timing (convert seconds to milliseconds)
            cue.fadein_duration = int(fade_in * 1000)
            cue.fadeout_duration = int(fade_out * 1000)
            cue.pre_wait = int(pre_wait * 1000)
            cue.post_wait = int(post_wait * 1000)
            
            print(f"   ✅ Applied values: fadein={cue.fadein_duration}ms, fadeout={cue.fadeout_duration}ms")
            print(f"   ✅ Applied values: pre_wait={cue.pre_wait}ms, post_wait={cue.post_wait}ms")
            
            # Apply auto-follow
            from lisp.cues.cue import CueNextAction
            if self.controlPanel.auto_follow_check.isChecked():
                cue.next_action = CueNextAction.TriggerAfterEnd.value
            else:
                cue.next_action = CueNextAction.DoNothing.value
            
            # Apply color: merge into CSS stylesheet
            try:
                css = css_to_dict(getattr(cue, 'stylesheet', '') or '')
            except Exception:
                css = {}
            css['background'] = self.controlPanel._cue_color.name()
            # If text color not set, compute a contrasting one
            if 'color' not in css:
                css['color'] = self.__contrast_text(self.controlPanel._cue_color.name())
            cue.stylesheet = dict_to_css(css)
            
            # Apply media properties (volume, loop) if this is a MediaCue
            if hasattr(cue, 'media') and cue.media is not None:
                print(f"   Media cue detected, updating volume and loop...")
                
                # Update volume
                volume_elem = cue.media.element('Volume')
                if volume_elem is not None:
                    # Convert from 0-200% to 0.0-10.0 range
                    new_volume = self.controlPanel.volume_slider.value() / 100.0
                    print(f"   Volume: {self.controlPanel.volume_slider.value()}% -> {new_volume}")
                    volume_elem.volume = new_volume
                    volume_elem.normal_volume = new_volume
                else:
                    print("   ⚠️ No Volume element found in media")
                
                # Update loop
                loop_checked = self.controlPanel.loop_check.isChecked()
                print(f"   Loop checkbox: {loop_checked}")
                if loop_checked:
                    cue.media.loop = -1  # Infinite loop
                    print(f"   Set loop to: -1 (infinite)")
                else:
                    cue.media.loop = 0  # No loop
                    print(f"   Set loop to: 0 (no loop)")
            else:
                print(f"   ⚠️ Not a media cue or media is None")
                # GroupCue: apply loop flag
                if isinstance(cue, GroupCue):
                    cue.loop = -1 if self.controlPanel.loop_check.isChecked() else 0
            
            print(f"✅ Applied changes to cue: {cue.name}")
            
        except Exception as e:
            print(f"❌ Error applying changes: {e}")
            import traceback
            traceback.print_exc()
    
    def __openFullSettings(self, page_hint: str = None):
        """Open full settings dialog"""
        cue = self.controlPanel.getCurrentCue()
        if cue is None:
            return
        
        # Emit signal to parent layout to open settings
        # The layout will handle opening the CueSettingsDialog
        from lisp.ui.settings.cue_settings import CueSettingsDialog
        
        dialog = CueSettingsDialog(cue, parent=self)

        # If caller requested a specific protocol page, attempt to select it
        if page_hint:
            try:
                pages = dialog.mainPage._pages
                hint = page_hint.lower()
                for idx, p in enumerate(pages):
                    try:
                        clsname = p.__class__.__name__.lower()
                        if hint in clsname:
                            dialog.mainPage.tabWidget.setCurrentIndex(idx)
                            break
                    except Exception:
                        continue
            except Exception:
                # If anything fails, ignore and show dialog normally
                pass
        
        def on_apply(settings):
            app = Application()
            app.commands_stack.do(UpdateCueCommand(settings, cue))
        
        dialog.onApply.connect(on_apply)
        dialog.exec()
        
        # Reload control panel after editing
        self.controlPanel.setCue(cue)

    # --- helpers ---
    def __contrast_text(self, hex_color: str) -> str:
        # hex_color like '#rrggbb'
        try:
            h = hex_color.lstrip('#')
            r = int(h[0:2], 16) / 255.0
            g = int(h[2:4], 16) / 255.0
            b = int(h[4:6], 16) / 255.0
            def lin(c):
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            L = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
            return '#000000' if L > 0.6 else '#ffffff'
        except Exception:
            return '#ffffff'
