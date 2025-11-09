#!/usr/bin/env python3
"""
Test script for drag-and-drop functionality in group cues
"""
import sys
import os
sys.path.insert(0, '/home/nto/linux-show-player-master')

from PyQt5.QtCore import QUrl
from lisp.application import Application
from lisp.cues.group_cue import GroupCue
from lisp.plugins.list_layout.list_view import CueListView
from lisp.plugins.list_layout.models import CueListModel

def test_drag_drop_to_group():
    """Test adding audio files to a group cue via drag-and-drop simulation"""

    # Initialize application
    app = Application()
    app._Application__new_session(app.layout.get_layout("ListLayout"))

    # Create a group cue
    group_cue = app.cue_factory.create_cue("GroupCue", cue_id=1)
    group_cue.name = "Test Group"
    app.cue_model.add(group_cue)

    print(f"✅ Created group cue: {group_cue.name} (ID: {group_cue.id})")

    # Create a mock list view to test the method
    model = CueListModel(app.cue_model)
    list_view = CueListView(model)

    # Create mock URLs for the test audio file
    test_file_path = "/home/nto/linux-show-player-master/test_audio.wav"
    if not os.path.exists(test_file_path):
        print("❌ Test audio file not found")
        return False

    urls = [QUrl.fromLocalFile(test_file_path)]
    print(f"📁 Testing with file: {test_file_path}")

    # Test the drag-drop method
    try:
        list_view._add_cues_to_group_from_urls(group_cue, urls)
        print("✅ Drag-drop method executed successfully")
    except Exception as e:
        print(f"❌ Error during drag-drop: {e}")
        return False

    # Verify the cue was added to the group
    if len(group_cue.children) == 0:
        print("❌ No children added to group")
        return False

    child_id = group_cue.children[0]
    child_cue = app.cue_model.get(child_id)

    if child_cue is None:
        print("❌ Child cue not found in cue model")
        return False

    print(f"✅ Successfully added child cue: {child_cue.name} (ID: {child_cue.id})")
    print(f"📊 Group now has {len(group_cue.children)} children")

    # Verify the child cue has the correct properties
    if child_cue.name != "test_audio":
        print(f"⚠️  Child cue name is '{child_cue.name}', expected 'test_audio'")

    print("🎉 Test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_drag_drop_to_group()
    sys.exit(0 if success else 1)