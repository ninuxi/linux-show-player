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

"""OSC Server Settings"""

from PyQt5.QtCore import QT_TRANSLATE_NOOP, Qt
from PyQt5.QtWidgets import (
    QCheckBox, QGroupBox, QHBoxLayout, QLabel,
    QSpinBox, QVBoxLayout, QPushButton, QTextEdit,
    QTableWidget, QTableWidgetItem, QComboBox, QHeaderView,
    QAbstractItemView
)

from lisp.application import Application
from lisp.ui.settings.pages import SettingsPage
from lisp.ui.ui_utils import translate


class OscSettings(SettingsPage):
    Name = QT_TRANSLATE_NOOP("SettingsPageName", "OSC Remote")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setLayout(QVBoxLayout())
        
        # === MAIN GROUP ===
        self.mainGroup = QGroupBox(self)
        self.mainGroup.setTitle(translate("OscSettings", "OSC Server"))
        self.mainGroup.setLayout(QVBoxLayout())
        self.layout().addWidget(self.mainGroup)
        
        # Enable checkbox
        self.enableCheck = QCheckBox(
            translate("OscSettings", "Enable OSC Server"),
            self.mainGroup
        )
        self.enableCheck.setToolTip(
            translate(
                "OscSettings",
                "Receive OSC commands for remote control"
            )
        )
        self.mainGroup.layout().addWidget(self.enableCheck)
        
        # Port setting
        portLayout = QHBoxLayout()
        portLabel = QLabel(translate("OscSettings", "Listen Port:"))
        portLayout.addWidget(portLabel)
        
        self.portSpin = QSpinBox()
        self.portSpin.setRange(1024, 65535)
        self.portSpin.setValue(12321)  # Default OSC port
        self.portSpin.setToolTip(
            translate(
                "OscSettings",
                "Port to receive OSC commands (default: 12321)"
            )
        )
        portLayout.addWidget(self.portSpin)
        portLayout.addStretch()
        self.mainGroup.layout().addLayout(portLayout)
        
        # Auto-map checkbox
        self.autoMapCheck = QCheckBox(
            translate("OscSettings", "Auto-map buttons to cues (Companion/Stream Deck)"),
            self.mainGroup
        )
        self.autoMapCheck.setChecked(True)
        self.autoMapCheck.setToolTip(
            translate(
                "OscSettings",
                "Automatically assign button 0=GO, button 1=cue 0, button 2=cue 1, etc."
            )
        )
        self.mainGroup.layout().addWidget(self.autoMapCheck)
        
        # === CUSTOM MAPPING GROUP ===
        mappingGroup = QGroupBox(self)
        mappingGroup.setTitle(translate("OscSettings", "Custom Button Mapping"))
        mappingGroup.setLayout(QVBoxLayout())
        self.layout().addWidget(mappingGroup)
        
        infoLabel = QLabel(
            translate(
                "OscSettings",
                "Customize which Stream Deck button triggers which cue. Leave 'Cue' empty for no action."
            )
        )
        infoLabel.setWordWrap(True)
        infoLabel.setStyleSheet("color: #888; font-style: italic; padding: 5px;")
        mappingGroup.layout().addWidget(infoLabel)
        
        # Mapping table
        self.mappingTable = QTableWidget()
        self.mappingTable.setColumnCount(4)
        self.mappingTable.setHorizontalHeaderLabels([
            translate("OscSettings", "Button"),
            translate("OscSettings", "Row"),
            translate("OscSettings", "Column"),
            translate("OscSettings", "Cue")
        ])
        self.mappingTable.horizontalHeader().setStretchLastSection(True)
        self.mappingTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.mappingTable.setAlternatingRowColors(True)
        self.mappingTable.setMinimumHeight(250)
        mappingGroup.layout().addWidget(self.mappingTable)
        
        # Buttons for mapping
        buttonLayout = QHBoxLayout()
        
        self.addMappingBtn = QPushButton(
            translate("OscSettings", "➕ Add Mapping"),
            mappingGroup
        )
        self.addMappingBtn.clicked.connect(self._add_mapping_row)
        buttonLayout.addWidget(self.addMappingBtn)
        
        self.removeMappingBtn = QPushButton(
            translate("OscSettings", "➖ Remove"),
            mappingGroup
        )
        self.removeMappingBtn.clicked.connect(self._remove_mapping_row)
        buttonLayout.addWidget(self.removeMappingBtn)
        
        self.autoFillBtn = QPushButton(
            translate("OscSettings", "🔄 Auto-Fill from Cues"),
            mappingGroup
        )
        self.autoFillBtn.clicked.connect(self._auto_fill_mapping)
        buttonLayout.addWidget(self.autoFillBtn)
        
        buttonLayout.addStretch()
        mappingGroup.layout().addLayout(buttonLayout)
        
        # Note about auto-map override
        noteLabel = QLabel(
            translate(
                "OscSettings",
                "Note: Custom mappings override auto-map. Disable auto-map to use only custom mappings."
            )
        )
        noteLabel.setWordWrap(True)
        noteLabel.setStyleSheet("color: #FF8800; font-weight: bold; padding: 5px;")
        mappingGroup.layout().addWidget(noteLabel)
        
        # === HELP GROUP ===
        helpGroup = QGroupBox(self)
        helpGroup.setTitle(translate("OscSettings", "OSC Commands & Setup"))
        helpGroup.setLayout(QVBoxLayout())
        self.layout().addWidget(helpGroup)
        
        helpText = QTextEdit()
        helpText.setReadOnly(True)
        helpText.setMaximumHeight(250)
        helpText.setHtml("""
<b>Simple OSC Commands (recommended):</b><br>
<code>/lsp/go</code> → Execute GO (next cue)<br>
<code>/lsp/stop_all</code> → Stop all cues<br>
<code>/lsp/cue/0/start</code> → Start cue at index 0<br>
<code>/lsp/cue/1/stop</code> → Stop cue at index 1<br>
<code>/lsp/cue/2/pause</code> → Pause cue at index 2<br>
<br>
<b>Legacy Companion/Stream Deck Commands:</b><br>
<code>/location/1/0/0/press</code> → GO button<br>
<code>/location/1/0/1/press</code> → Cue 0<br>
<code>/location/1/0/2/press</code> → Cue 1<br>
<br>
<b>Connection Settings:</b><br>
<b>IP:</b> 127.0.0.1 (local) or your PC IP<br>
<b>Port:</b> 12321 (default)<br>
<br>
<b>Companion Setup:</b><br>
1. Add "Generic OSC" connection in Companion<br>
2. Set target IP to this computer's IP<br>
3. Set target port to 12321<br>
4. Use OSC commands above in button actions<br>
        """)
        helpGroup.layout().addWidget(helpText)
        
        # Test button
        self.testButton = QPushButton(
            translate("OscSettings", "📡 Test Connection"),
            helpGroup
        )
        self.testButton.setToolTip(
            translate(
                "OscSettings",
                "Send a test command to verify Companion is listening"
            )
        )
        self.testButton.clicked.connect(self._test_connection)
        helpGroup.layout().addWidget(self.testButton)
        
        self.layout().addStretch()
    
    def enableCheck(self, enabled):
        """Enable/disable settings"""
        self.setGroupEnabled(self.mainGroup, enabled)
    
    def loadSettings(self, settings):
        """Load settings from config"""
        companion = settings.get("osc_remote", {})
        
        self.enableCheck.setChecked(companion.get("enabled", False))
        self.portSpin.setValue(companion.get("osc_port", 12321))
        self.autoMapCheck.setChecked(companion.get("auto_map_cues", True))
        
        # Load custom mappings
        mappings = companion.get("custom_mappings", [])
        self._load_mappings(mappings)
    
    def getSettings(self):
        """Get settings to save"""
        if not self.isGroupEnabled(self.mainGroup):
            return {}
        
        # Get custom mappings from table
        mappings = []
        for row in range(self.mappingTable.rowCount()):
            row_widget = self.mappingTable.cellWidget(row, 1)
            col_widget = self.mappingTable.cellWidget(row, 2)
            cue_widget = self.mappingTable.cellWidget(row, 3)
            
            if row_widget and col_widget and cue_widget:
                row_val = row_widget.value()
                col_val = col_widget.value()
                cue_id = cue_widget.currentData()
                
                if cue_id:  # Only save if a cue is selected
                    mappings.append({
                        "row": row_val,
                        "column": col_val,
                        "cue_id": cue_id
                    })
        
        return {
            "osc_remote": {
                "enabled": self.enableCheck.isChecked(),
                "osc_port": self.portSpin.value(),
                "auto_map_cues": self.autoMapCheck.isChecked(),
                "listen_ip": "0.0.0.0",
                "custom_mappings": mappings
            }
        }
    
    def _test_connection(self):
        """Test OSC connection to Companion"""
        from PyQt5.QtWidgets import QMessageBox
        
        # Try to send a test OSC message
        try:
            from pythonosc import udp_client
            
            client = udp_client.SimpleUDPClient("127.0.0.1", 12321)
            client.send_message("/companion/test", ["LSP", "hello"])
            
            QMessageBox.information(
                self,
                translate("OscSettings", "Test Sent"),
                translate(
                    "OscSettings",
                    "Test message sent to Companion on port 12321.\n"
                    "Check Companion's OSC log to verify reception."
                )
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                translate("OscSettings", "Test Failed"),
                translate(
                    "OscSettings",
                    f"Could not send test message: {e}\n\n"
                    "Make sure python-osc is installed:\n"
                    "pip install python-osc"
                )
            )
    
    def _add_mapping_row(self):
        """Add new mapping row"""
        row = self.mappingTable.rowCount()
        self.mappingTable.insertRow(row)
        
        # Button index (calculated automatically)
        button_idx = QTableWidgetItem(str(row * 5))
        button_idx.setFlags(Qt.ItemIsEnabled)
        self.mappingTable.setItem(row, 0, button_idx)
        
        # Row spinbox
        row_spin = QSpinBox()
        row_spin.setRange(0, 9)
        row_spin.setValue(0)
        row_spin.valueChanged.connect(lambda v, r=row: self._update_button_index(r))
        self.mappingTable.setCellWidget(row, 1, row_spin)
        
        # Column spinbox
        col_spin = QSpinBox()
        col_spin.setRange(0, 9)
        col_spin.setValue(row % 5)
        col_spin.valueChanged.connect(lambda v, r=row: self._update_button_index(r))
        self.mappingTable.setCellWidget(row, 2, col_spin)
        
        # Cue combo
        cue_combo = self._create_cue_combo()
        self.mappingTable.setCellWidget(row, 3, cue_combo)
    
    def _remove_mapping_row(self):
        """Remove selected mapping row"""
        current_row = self.mappingTable.currentRow()
        if current_row >= 0:
            self.mappingTable.removeRow(current_row)
    
    def _auto_fill_mapping(self):
        """Auto-fill mapping table from current cues"""
        self.mappingTable.setRowCount(0)
        
        app = Application()
        if not app or not hasattr(app, 'cue_model'):
            return
        
        # Button 0,0 reserved for GO - skip it
        # Start from button 0,1
        for i, cue in enumerate(app.cue_model):
            row = self.mappingTable.rowCount()
            self.mappingTable.insertRow(row)
            
            # Calculate row/col (assuming 5 columns)
            button_idx = i + 1
            btn_row = button_idx // 5
            btn_col = button_idx % 5
            
            # Button index
            button_item = QTableWidgetItem(str(button_idx))
            button_item.setFlags(Qt.ItemIsEnabled)
            self.mappingTable.setItem(row, 0, button_item)
            
            # Row spinbox
            row_spin = QSpinBox()
            row_spin.setRange(0, 9)
            row_spin.setValue(btn_row)
            row_spin.valueChanged.connect(lambda v, r=row: self._update_button_index(r))
            self.mappingTable.setCellWidget(row, 1, row_spin)
            
            # Column spinbox
            col_spin = QSpinBox()
            col_spin.setRange(0, 9)
            col_spin.setValue(btn_col)
            col_spin.valueChanged.connect(lambda v, r=row: self._update_button_index(r))
            self.mappingTable.setCellWidget(row, 2, col_spin)
            
            # Cue combo
            cue_combo = self._create_cue_combo()
            # Select this cue
            idx = cue_combo.findData(cue.id)
            if idx >= 0:
                cue_combo.setCurrentIndex(idx)
            self.mappingTable.setCellWidget(row, 3, cue_combo)
    
    def _create_cue_combo(self):
        """Create cue selection combo box"""
        combo = QComboBox()
        combo.addItem("-- None --", None)
        
        app = Application()
        if app and hasattr(app, 'cue_model'):
            for i, cue in enumerate(app.cue_model):
                combo.addItem(f"{i}: {cue.name}", cue.id)
        
        return combo
    
    def _update_button_index(self, table_row):
        """Update button index when row/col changes"""
        row_widget = self.mappingTable.cellWidget(table_row, 1)
        col_widget = self.mappingTable.cellWidget(table_row, 2)
        
        if row_widget and col_widget:
            btn_row = row_widget.value()
            btn_col = col_widget.value()
            button_idx = btn_row * 5 + btn_col
            
            item = self.mappingTable.item(table_row, 0)
            if item:
                item.setText(str(button_idx))
    
    def _load_mappings(self, mappings):
        """Load mappings into table"""
        self.mappingTable.setRowCount(0)
        
        for mapping in mappings:
            row = self.mappingTable.rowCount()
            self.mappingTable.insertRow(row)
            
            btn_row = mapping.get("row", 0)
            btn_col = mapping.get("column", 0)
            cue_id = mapping.get("cue_id")
            
            # Button index
            button_idx = btn_row * 5 + btn_col
            button_item = QTableWidgetItem(str(button_idx))
            button_item.setFlags(Qt.ItemIsEnabled)
            self.mappingTable.setItem(row, 0, button_item)
            
            # Row spinbox
            row_spin = QSpinBox()
            row_spin.setRange(0, 9)
            row_spin.setValue(btn_row)
            row_spin.valueChanged.connect(lambda v, r=row: self._update_button_index(r))
            self.mappingTable.setCellWidget(row, 1, row_spin)
            
            # Column spinbox
            col_spin = QSpinBox()
            col_spin.setRange(0, 9)
            col_spin.setValue(btn_col)
            col_spin.valueChanged.connect(lambda v, r=row: self._update_button_index(r))
            self.mappingTable.setCellWidget(row, 2, col_spin)
            
            # Cue combo
            cue_combo = self._create_cue_combo()
            if cue_id:
                idx = cue_combo.findData(cue_id)
                if idx >= 0:
                    cue_combo.setCurrentIndex(idx)
            self.mappingTable.setCellWidget(row, 3, cue_combo)
