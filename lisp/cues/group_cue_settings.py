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

from PyQt5.QtCore import QT_TRANSLATE_NOOP, Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QVBoxLayout,
)

from lisp.application import Application
from lisp.cues.group_cue import GroupCue, GroupMode
from lisp.ui.cuelistdialog import CueSelectDialog
from lisp.ui.settings.cue_settings import CueSettingsRegistry
from lisp.ui.settings.pages import SettingsPage
from lisp.ui.ui_utils import translate


class GroupCueSettings(SettingsPage):
    """Settings page for GroupCue configuration"""
    
    Name = QT_TRANSLATE_NOOP("SettingsPageName", "Group Settings")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setLayout(QVBoxLayout(self))
        
        # Execution Mode Group
        self.modeGroup = QGroupBox(self)
        self.modeGroup.setTitle(translate("GroupCue", "Execution Mode"))
        self.modeGroup.setLayout(QVBoxLayout())
        self.layout().addWidget(self.modeGroup)
        
        self.modeButtonGroup = QButtonGroup(self)
        
        self.simultaneousRadio = QRadioButton(
            translate("GroupCue", "Simultaneous (all at once)"), 
            self.modeGroup
        )
        self.modeButtonGroup.addButton(self.simultaneousRadio, 0)
        self.modeGroup.layout().addWidget(self.simultaneousRadio)
        
        self.sequentialRadio = QRadioButton(
            translate("GroupCue", "Sequential (one after another)"), 
            self.modeGroup
        )
        self.modeButtonGroup.addButton(self.sequentialRadio, 1)
        self.modeGroup.layout().addWidget(self.sequentialRadio)
        
        self.randomRadio = QRadioButton(
            translate("GroupCue", "Random order"), 
            self.modeGroup
        )
        self.modeButtonGroup.addButton(self.randomRadio, 2)
        self.modeGroup.layout().addWidget(self.randomRadio)
        
        # Default to simultaneous
        self.simultaneousRadio.setChecked(True)
        
        # Children Management Group
        self.childrenGroup = QGroupBox(self)
        self.childrenGroup.setTitle(translate("GroupCue", "Child Cues"))
        self.childrenGroup.setLayout(QVBoxLayout())
        self.layout().addWidget(self.childrenGroup)
        
        # Help text
        self.helpLabel = QLabel(
            translate("GroupCue", "Add audio cues to this group. They will be executed according to the mode above."),
            self.childrenGroup
        )
        self.helpLabel.setWordWrap(True)
        self.helpLabel.setStyleSheet("color: #888; font-style: italic; padding: 5px;")
        self.childrenGroup.layout().addWidget(self.helpLabel)
        
        # Children list
        self.childrenList = QListWidget(self.childrenGroup)
        self.childrenList.setAlternatingRowColors(True)
        self.childrenList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.childrenList.setMinimumHeight(200)
        self.childrenGroup.layout().addWidget(self.childrenList)
        
        # Buttons
        self.buttonsLayout = QHBoxLayout()
        self.childrenGroup.layout().addLayout(self.buttonsLayout)
        
        self.addButton = QPushButton(translate("GroupCue", "Add Cue"), self.childrenGroup)
        self.addButton.clicked.connect(self._showAddCueDialog)
        self.buttonsLayout.addWidget(self.addButton)
        
        self.removeButton = QPushButton(translate("GroupCue", "Remove"), self.childrenGroup)
        self.removeButton.clicked.connect(self._removeCurrentCue)
        self.removeButton.setEnabled(False)
        self.buttonsLayout.addWidget(self.removeButton)
        
        self.moveUpButton = QPushButton(translate("GroupCue", "Move Up"), self.childrenGroup)
        self.moveUpButton.clicked.connect(self._moveUp)
        self.moveUpButton.setEnabled(False)
        self.buttonsLayout.addWidget(self.moveUpButton)
        
        self.moveDownButton = QPushButton(translate("GroupCue", "Move Down"), self.childrenGroup)
        self.moveDownButton.clicked.connect(self._moveDown)
        self.moveDownButton.setEnabled(False)
        self.buttonsLayout.addWidget(self.moveDownButton)
        
        # Cue selection dialog
        self.cueDialog = CueSelectDialog(
            cues=Application().cue_model,
            selection_mode=QAbstractItemView.ExtendedSelection,
            parent=self
        )
        
        # Connect list selection to button states
        self.childrenList.itemSelectionChanged.connect(self._updateButtonStates)
        
    def _updateButtonStates(self):
        """Update button enabled states based on selection"""
        selected_items = self.childrenList.selectedItems()
        has_selection = len(selected_items) > 0
        
        self.removeButton.setEnabled(has_selection)
        
        if has_selection:
            current_row = self.childrenList.row(selected_items[0])
            self.moveUpButton.setEnabled(current_row > 0)
            self.moveDownButton.setEnabled(current_row < self.childrenList.count() - 1)
        else:
            self.moveUpButton.setEnabled(False)
            self.moveDownButton.setEnabled(False)
    
    def _showAddCueDialog(self):
        """Show dialog to add cues to the group"""
        if self.cueDialog.exec() == QDialog.Accepted:
            for cue in self.cueDialog.selected_cues():
                # Don't add if already in list
                existing_ids = [
                    self.childrenList.item(i).data(Qt.UserRole) 
                    for i in range(self.childrenList.count())
                ]
                if cue.id not in existing_ids:
                    item = QListWidgetItem(f"{cue.index + 1} | {cue.name}")
                    item.setData(Qt.UserRole, cue.id)
                    self.childrenList.addItem(item)
                    print(f"  ➕ Added cue to group: {cue.name}")
            
            self._updateButtonStates()
    
    def _removeCurrentCue(self):
        """Remove selected cue from the group"""
        current_item = self.childrenList.currentItem()
        if current_item:
            cue_id = current_item.data(Qt.UserRole)
            cue = Application().cue_model.get(cue_id)
            if cue:
                print(f"  ➖ Removed cue from group: {cue.name}")
            
            row = self.childrenList.row(current_item)
            self.childrenList.takeItem(row)
            self._updateButtonStates()
    
    def _moveUp(self):
        """Move selected cue up in the list"""
        current_row = self.childrenList.currentRow()
        if current_row > 0:
            item = self.childrenList.takeItem(current_row)
            self.childrenList.insertItem(current_row - 1, item)
            self.childrenList.setCurrentRow(current_row - 1)
            self._updateButtonStates()
    
    def _moveDown(self):
        """Move selected cue down in the list"""
        current_row = self.childrenList.currentRow()
        if current_row < self.childrenList.count() - 1:
            item = self.childrenList.takeItem(current_row)
            self.childrenList.insertItem(current_row + 1, item)
            self.childrenList.setCurrentRow(current_row + 1)
            self._updateButtonStates()
    
    def enableCheck(self, enabled):
        """Enable/disable the settings page"""
        self.setGroupEnabled(self.modeGroup, enabled)
        self.setGroupEnabled(self.childrenGroup, enabled)
    
    def loadSettings(self, settings):
        """Load settings into the UI"""
        # Load execution mode
        mode = settings.get("mode", GroupMode.SIMULTANEOUS.value)
        if mode == GroupMode.SIMULTANEOUS.value:
            self.simultaneousRadio.setChecked(True)
        elif mode == GroupMode.SEQUENTIAL.value:
            self.sequentialRadio.setChecked(True)
        elif mode == GroupMode.RANDOM.value:
            self.randomRadio.setChecked(True)
        
        # Load children
        self.childrenList.clear()
        for child_id in settings.get("children", []):
            cue = Application().cue_model.get(child_id)
            if cue:
                item = QListWidgetItem(f"{cue.index + 1} | {cue.name}")
                item.setData(Qt.UserRole, cue.id)
                self.childrenList.addItem(item)
        
        self._updateButtonStates()
    
    def getSettings(self):
        """Get settings from the UI"""
        if not self.isGroupEnabled(self.modeGroup):
            return {}
        
        # Get execution mode
        if self.simultaneousRadio.isChecked():
            mode = GroupMode.SIMULTANEOUS.value
        elif self.sequentialRadio.isChecked():
            mode = GroupMode.SEQUENTIAL.value
        else:
            mode = GroupMode.RANDOM.value
        
        # Get children IDs
        children = []
        for i in range(self.childrenList.count()):
            item = self.childrenList.item(i)
            children.append(item.data(Qt.UserRole))
        
        print(f"💾 GroupCue settings: mode={mode}, children={len(children)}")
        
        return {
            "mode": mode,
            "children": children
        }


# Register the settings page
CueSettingsRegistry().add(GroupCueSettings, GroupCue)
