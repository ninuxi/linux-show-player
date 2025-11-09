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

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QSplitter, QVBoxLayout, QLabel, QHBoxLayout

from lisp.plugins.list_layout.list_view import CueListView
from lisp.plugins.list_layout.playing_view import RunningCuesListWidget
from lisp.ui.widgets.dynamicfontsize import DynamicFontSizePushButton
from lisp.ui.widgets.qiconpushbutton import QIconPushButton
from lisp.ui.icons import IconTheme
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
        # Spacer to push everything except GO to the right
        from PyQt5.QtWidgets import QWidget as _SpacerWidget
        self.topSpacer = _SpacerWidget(self)
        self.topSpacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.topSplitter.addWidget(self.topSpacer)
        
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
        # The +Group quick button is hidden by default: GroupCue is still
        # available via menu and other flows, but the quick green button
        # was removed per user request.
        self.createGroupButton.hide()

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
        # Centralized Panic button (single visible control). We style it
        # distinctly and connect it to the immediate interrupt/stop-all
        # behavior so users have one clear emergency stop.
        try:
            # Create a compact panic widget: a small label with the OSC
            # command and a smaller red button beneath it. This keeps the
            # top bar tidy while showing the command to the user.
            panic_container = QWidget(self)
            panic_layout = QVBoxLayout(panic_container)
            panic_layout.setContentsMargins(6, 6, 6, 6)
            panic_layout.setSpacing(4)

            cmd_label = QLabel("/lsp/stop_all", panic_container)
            cmd_label.setAlignment(Qt.AlignCenter)
            cmd_label.setStyleSheet("color: #ffdede; font-size: 10px;")
            panic_layout.addWidget(cmd_label)

            btn_row = QHBoxLayout()
            btn_row.setContentsMargins(0, 0, 0, 0)
            btn_row.setSpacing(0)

            small_btn = QIconPushButton(panic_container)
            small_btn.setFocusPolicy(Qt.NoFocus)
            small_btn.setIcon(IconTheme.get("cue-stop"))
            small_btn.setIconSize(QSize(20, 20))
            small_btn.setFixedSize(40, 40)
            small_btn.setStyleSheet(
                "QPushButton { background-color: #d9534f; border: 1px solid #b02a26; color: white; border-radius: 4px; }"
            )
            btn_row.addStretch()
            btn_row.addWidget(small_btn)
            btn_row.addStretch()

            panic_layout.addLayout(btn_row)

            # Place the compact widget on the right area
            self.topSplitter.addWidget(panic_container)

            def _panic_action():
                try:
                    from lisp import plugins
                    osc = None
                    for name in ("osc_remote", "OscRemote", "Osc", "osc"):
                        try:
                            osc = plugins.get_plugin(name)
                            break
                        except Exception:
                            osc = None

                    if osc is not None and hasattr(osc, "bridge"):
                        try:
                            osc.bridge._handle_stop_all("/lsp/stop_all")
                            return
                        except Exception:
                            pass
                except Exception:
                    pass

                try:
                    Application().layout.interrupt_all()
                except Exception:
                    pass

            small_btn.clicked.connect(_panic_action)
        except Exception:
            pass

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
        # Now the top splitter has 5 widgets (GO, spacer, infoPanel,
        # controlButtons, panicButton) so provide 5 size hints.
        self.topSplitter.setSizes(
            (
                int(0.06 * self.width()),  # GO button (reduced)
                int(0.12 * self.width()),  # Spacer
                int(0.56 * self.width()),  # Info panel
                int(0.18 * self.width()),  # Control buttons
                int(0.08 * self.width()),  # Panic button
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
            # Use UpdateCueCommand for consistency with full settings dialog
            updates = self.controlPanel.applyCue()
            if not updates:
                print("⚠️ No updates to apply")
                return

            app = Application()
            app.commands_stack.do(UpdateCueCommand(updates, cue))
            print(f"✅ Applied changes to cue: {cue.name} using UpdateCueCommand")

            # If the cue is a GroupCue and we changed the stylesheet, propagate
            # the same stylesheet to all children so they keep the group's color.
            if isinstance(cue, GroupCue) and "stylesheet" in updates:
                try:
                    child_ids = list(cue.children)
                    child_cues = [app.cue_model.get(cid) for cid in child_ids]
                    # Filter out any None results (missing cues)
                    child_cues = [c for c in child_cues if c is not None]
                    if child_cues:
                        from lisp.command.cue import UpdateCuesCommand

                        child_updates = {"stylesheet": updates["stylesheet"]}
                        app.commands_stack.do(
                            UpdateCuesCommand(child_updates, child_cues)
                        )
                        print(f"🔁 Propagated stylesheet to {len(child_cues)} children")
                except Exception as e:
                    print(f"❌ Failed to propagate stylesheet to children: {e}")

        except Exception as e:
            print(f"❌ Error applying changes: {e}")
            import traceback
            traceback.print_exc()
    
    def __openFullSettings(self):
        """Open full settings dialog"""
        cue = self.controlPanel.getCurrentCue()
        if cue is None:
            return
        
        # Emit signal to parent layout to open settings
        # The layout will handle opening the CueSettingsDialog
        from lisp.ui.settings.cue_settings import CueSettingsDialog
        
        dialog = CueSettingsDialog(cue, parent=self)
        
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
