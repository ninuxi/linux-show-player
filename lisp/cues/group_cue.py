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

import random
from enum import Enum

from PyQt5.QtCore import QT_TRANSLATE_NOOP

from lisp.core.properties import Property
from lisp.cues.cue import Cue, CueAction
from lisp.ui.ui_utils import translate


class GroupMode(Enum):
    """Group execution modes"""
    SIMULTANEOUS = "simultaneous"  # All cues start at once
    SEQUENTIAL = "sequential"      # Cues play one after another
    RANDOM = "random"              # Random order, then sequential


class GroupCue(Cue):
    """Group Cue - Container for multiple cues with various execution modes
    
    Similar to QLab's Group Cue, this allows organizing multiple audio cues
    that can be executed simultaneously, sequentially, or in random order.
    """
    
    Name = QT_TRANSLATE_NOOP("CueName", "Group Cue")
    Category = QT_TRANSLATE_NOOP("CueCategory", "Group cues")

    CueActions = (
        CueAction.Default,
        CueAction.Start,
        CueAction.Stop,
        CueAction.Pause,
        CueAction.Resume,
        CueAction.Interrupt,
    )

    # Properties
    children = Property(default=[])  # List of child cue IDs
    mode = Property(default=GroupMode.SIMULTANEOUS.value)  # Execution mode
    # Loop semantics: 0 = no loop, -1 = infinite loop (match MediaCue convention)
    loop = Property(default=0)
    # Whether the group's children are visible/expanded in the UI
    open = Property(default=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = translate("CueName", self.Name)
        self._current_child_index = 0  # For sequential mode
        self._execution_order = []     # Computed execution order
        self._remaining_loops = 0      # Finite loops counter (runtime only)
        
    def __start__(self, fade=False):
        """Start the group cue based on execution mode"""
        if not self.children:
            print("⚠️ GroupCue: No children to execute")
            return False
            
        mode = GroupMode(self.mode)
        # Initialize loops counter at each explicit start
        if self.loop == -1:
            self._remaining_loops = -1
        elif self.loop > 0:
            self._remaining_loops = self.loop
        else:
            self._remaining_loops = 0
        
        print(f"🎵 GroupCue '{self.name}' starting in {mode.value} mode with {len(self.children)} children")
        
        if mode == GroupMode.SIMULTANEOUS:
            return self._start_simultaneous(fade)
        elif mode == GroupMode.SEQUENTIAL:
            return self._start_sequential(fade)
        elif mode == GroupMode.RANDOM:
            return self._start_random(fade)
            
        return False
    
    def _start_simultaneous(self, fade=False):
        """Start all child cues at once"""
        print("  🔄 Starting all children simultaneously...")
        # Track running children so we can determine when the group is finished
        self._sim_children_remaining = 0
        for child_id in self.children:
            child_cue = self.app.cue_model.get(child_id)
            if child_cue and child_cue is not self:
                # Connect to child's end to know when all finished
                try:
                    child_cue.end.connect(self._on_sim_child_ended)
                except Exception:
                    pass
                action = CueAction.FadeInStart if fade else CueAction.Start
                print(f"    ▶️ Starting child: {child_cue.name}")
                child_cue.execute(action=action)
                self._sim_children_remaining += 1

        # If we started any children, keep the group running until they finish
        return self._sim_children_remaining > 0
    
    def _start_sequential(self, fade=False):
        """Start child cues one after another"""
        if not self._execution_order:
            self._execution_order = list(self.children)
            self._current_child_index = 0
            
        print(f"  📋 Sequential mode: {len(self._execution_order)} children in order")
        
        if self._current_child_index < len(self._execution_order):
            child_id = self._execution_order[self._current_child_index]
            child_cue = self.app.cue_model.get(child_id)
            
            if child_cue and child_cue is not self:
                # Connect to child's end signal to start next
                child_cue.end.connect(self._on_child_ended)
                
                action = CueAction.FadeInStart if fade else CueAction.Start
                print(f"    ▶️ Starting child {self._current_child_index + 1}/{len(self._execution_order)}: {child_cue.name}")
                child_cue.execute(action=action)
                
        # We started an asynchronous sequence; keep the group running
        return True
    
    def _start_random(self, fade=False):
        """Shuffle children and play sequentially"""
        # Shuffle the execution order
        self._execution_order = list(self.children)
        random.shuffle(self._execution_order)
        self._current_child_index = 0
        
        print(f"  🎲 Random mode: shuffled {len(self._execution_order)} children")
        print(f"    Order: {[self.app.cue_model.get(cid).name if self.app.cue_model.get(cid) else 'N/A' for cid in self._execution_order]}")
        
        # Start like sequential
        return self._start_sequential(fade)
    
    def _on_child_ended(self, cue):
        """Called when a child cue ends in sequential/random mode"""
        print(f"    ✅ Child ended: {cue.name}")
        
        # Disconnect from this child outside of the emission loop
        try:
            from PyQt5.QtCore import QTimer
            def _safe_disconnect(c=cue):
                try:
                    c.end.disconnect(self._on_child_ended)
                except:
                    pass
            QTimer.singleShot(0, _safe_disconnect)
        except Exception:
            # Fallback to direct disconnect (may warn if during iteration)
            try:
                cue.end.disconnect(self._on_child_ended)
            except:
                pass
        
        # Move to next child
        self._current_child_index += 1
        
        if self._current_child_index < len(self._execution_order):
            child_id = self._execution_order[self._current_child_index]
            child_cue = self.app.cue_model.get(child_id)
            
            if child_cue and child_cue is not self:
                child_cue.end.connect(self._on_child_ended)
                print(f"    ▶️ Starting next child {self._current_child_index + 1}/{len(self._execution_order)}: {child_cue.name}")
                child_cue.execute(action=CueAction.Start)
        else:
            print(f"  ✅ GroupCue '{self.name}' completed all children")
            finished_mode = GroupMode(self.mode)
            # Determine loop behavior: infinite (-1) or finite (>0)
            if self._remaining_loops == -1 or self._remaining_loops > 1:
                if self._remaining_loops > 0:
                    self._remaining_loops -= 1
                print("  🔁 GroupCue loop — restarting sequence")
                # Reset state and restart according to current mode (Sequential/Random)
                self._execution_order = []
                self._current_child_index = 0
                if finished_mode == GroupMode.RANDOM:
                    self._start_random(False)
                elif finished_mode == GroupMode.SEQUENTIAL:
                    self._start_sequential(False)
                else:
                    # For simultaneous we currently don't auto-loop at end (no aggregate end tracking)
                    pass
            else:
                # Sequence finished with no more loops -> mark group as ended
                self._execution_order = []
                self._current_child_index = 0
                # Signal that the group itself has ended so next_action/auto-follow works
                try:
                    self._ended()
                except Exception:
                    pass

    def _on_sim_child_ended(self, cue):
        """Handler for simultaneous children end events"""
        try:
            cue.end.disconnect(self._on_sim_child_ended)
        except Exception:
            pass

        try:
            self._sim_children_remaining -= 1
        except Exception:
            self._sim_children_remaining = max(0, getattr(self, '_sim_children_remaining', 0) - 1)

        if getattr(self, '_sim_children_remaining', 0) <= 0:
            # All children finished
            finished_mode = GroupMode(self.mode)
            if self._remaining_loops == -1 or self._remaining_loops > 1:
                if self._remaining_loops > 0:
                    self._remaining_loops -= 1
                print("  🔁 GroupCue loop — restarting simultaneous sequence")
                # Restart depending on mode
                if finished_mode == GroupMode.RANDOM:
                    self._start_random(False)
                elif finished_mode == GroupMode.SEQUENTIAL:
                    self._start_sequential(False)
                else:
                    self._start_simultaneous(False)
            else:
                # No more loops -> end group
                try:
                    self._ended()
                except Exception:
                    pass
    
    def __stop__(self, fade=False):
        """Stop all child cues"""
        print(f"⏹️ GroupCue '{self.name}' stopping all children")
        action = CueAction.FadeOutStop if fade else CueAction.Stop
        
        for child_id in self.children:
            child_cue = self.app.cue_model.get(child_id)
            if child_cue and child_cue is not self:
                try:
                    child_cue.end.disconnect(self._on_child_ended)
                except:
                    pass
                child_cue.execute(action=action)
        
        self._execution_order = []
        self._current_child_index = 0
        return True
    
    def __pause__(self, fade=False):
        """Pause all child cues"""
        print(f"⏸️ GroupCue '{self.name}' pausing all children")
        action = CueAction.FadeOutPause if fade else CueAction.Pause
        
        for child_id in self.children:
            child_cue = self.app.cue_model.get(child_id)
            if child_cue and child_cue is not self:
                child_cue.execute(action=action)
        return True
    
    def __resume__(self, fade=False):
        """Resume all child cues"""
        print(f"▶️ GroupCue '{self.name}' resuming all children")
        action = CueAction.FadeInResume if fade else CueAction.Resume
        
        for child_id in self.children:
            child_cue = self.app.cue_model.get(child_id)
            if child_cue and child_cue is not self:
                child_cue.execute(action=action)
        return True
    
    def __interrupt__(self, fade=False):
        """Interrupt all child cues"""
        print(f"⏹️ GroupCue '{self.name}' interrupting all children")
        action = CueAction.FadeOutInterrupt if fade else CueAction.Interrupt
        
        for child_id in self.children:
            child_cue = self.app.cue_model.get(child_id)
            if child_cue and child_cue is not self:
                try:
                    child_cue.end.disconnect(self._on_child_ended)
                except:
                    pass
                child_cue.execute(action=action)
        
        self._execution_order = []
        self._current_child_index = 0
        return True
