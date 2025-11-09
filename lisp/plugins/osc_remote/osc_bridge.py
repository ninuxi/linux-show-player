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

"""OSC Bridge - OSC listener and command handler"""

import logging
from pythonosc import dispatcher, osc_server
from pythonosc.osc_server import ThreadingOSCUDPServer
from PyQt5.QtCore import QThread, pyqtSignal

from lisp.cues.cue import CueAction

logger = logging.getLogger(__name__)


class OscBridge(QThread):
    """OSC Server for remote control of LSP
    
    Supports simple commands like:
      /lsp/go                  -> GO (execute next cue)
      /lsp/stop_all            -> Stop all cues
      /lsp/cue/1/start         -> Start cue at index 1
      /lsp/cue/1/stop          -> Stop cue at index 1
      /lsp/cue/1/pause         -> Pause cue at index 1
      
    Also supports Companion Stream Deck mapping:
      /location/1/0/5/press    -> Execute cue at index 5
      /location/1/0/0/press    -> GO
    """
    
    commandReceived = pyqtSignal(str, list)  # path, args
    
    def __init__(self, app, config, parent=None):
        super().__init__(parent)
        self.app = app
        self.config = config
        self._server = None
        self._running = False
        
        # Default mapping: button index -> cue action
        self._button_mapping = {}
        self._custom_mappings = {}  # Custom user-defined mappings
        self._auto_map = config.get("auto_map_cues", True)
        
        # OSC server port (default 12321 for Companion compatibility)
        self._osc_port = config.get("osc_port", 12321)
        self._listen_ip = config.get("listen_ip", "0.0.0.0")
        
    @property
    def osc_port(self):
        return self._osc_port
    
    @osc_port.setter
    def osc_port(self, value):
        if self._osc_port != value:
            self._osc_port = value
            if self._running:
                self.restart()
    
    @property
    def auto_map(self):
        return self._auto_map
    
    @auto_map.setter
    def auto_map(self, value):
        self._auto_map = value
        if value:
            self._rebuild_mapping()
    
    def start(self):
        """Start OSC listener"""
        if self._running:
            return
        
        if not self.config.get("enabled", False):
            logger.info("OSC Server disabled in settings")
            return
        
        super().start()
    
    def stop(self):
        """Stop OSC listener"""
        self._running = False
        if self._server:
            self._server.shutdown()
            self._server = None
        self.wait()
        logger.info("🔌 OSC Server stopped")
    
    def restart(self):
        """Restart with new settings"""
        self.stop()
        self.start()
    
    def run(self):
        """Thread main loop - runs OSC server"""
        self._running = True
        
        # Build OSC dispatcher
        disp = dispatcher.Dispatcher()
        
        # === Modern LSP Commands ===
        disp.map("/lsp/go", self._handle_go)
        disp.map("/lsp/stop_all", self._handle_stop_all)
        disp.map("/lsp/cue/*/start", self._handle_cue_start)
        disp.map("/lsp/cue/*/stop", self._handle_cue_stop)
        disp.map("/lsp/cue/*/pause", self._handle_cue_pause)
        
        # === Legacy Companion/Stream Deck Commands ===
        disp.map("/location/*/*/*/*", self._handle_location_command)
        
        # Fallback handler
        disp.set_default_handler(self._handle_unknown)
        
        try:
            self._server = ThreadingOSCUDPServer(
                (self._listen_ip, self._osc_port),
                disp
            )
            logger.info(f"🎛️ OSC Server listening on {self._listen_ip}:{self._osc_port}")
            logger.info(f"   Commands: /lsp/go, /lsp/stop_all, /lsp/cue/N/start|stop|pause")
            logger.info(f"   Legacy: /location/<page>/<row>/<col>/<action> (Companion)")
            
            # Build initial mapping
            if self._auto_map:
                self._rebuild_mapping()
            
            # Load custom mappings
            self._load_custom_mappings()
            
            # Serve forever (blocks until shutdown)
            self._server.serve_forever()
            
        except Exception as e:
            logger.error(f"❌ OSC Server error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._running = False
    
    def _handle_location_command(self, address, *args):
        """Handle /location/<page>/<row>/<column>/<action>"""
        # Parse address: /location/1/0/5/press
        parts = address.strip("/").split("/")
        
        if len(parts) < 5:
            logger.warning(f"⚠️ Invalid location command: {address}")
            return
        
        try:
            page = int(parts[1])
            row = int(parts[2])
            column = int(parts[3])
            action = parts[4]
            
            logger.debug(f"📥 Companion: page={page}, row={row}, col={column}, action={action}")
            
            # Emit signal
            self.commandReceived.emit(address, list(args))
            
            # Auto-execute if action is press/down
            if action in ("press", "down"):
                self._execute_button(page, row, column)
                
        except (ValueError, IndexError) as e:
            logger.warning(f"⚠️ Could not parse location command {address}: {e}")
    
    def _handle_unknown(self, address, *args):
        """Log unknown commands"""
        logger.debug(f"📭 OSC unknown: {address} {args}")
    
    # === Modern LSP Command Handlers ===
    
    def _handle_go(self, address, *args):
        """/lsp/go - Execute GO action"""
        logger.info(f"⏩ OSC: GO command received")
        self._execute_go()
    
    def _handle_stop_all(self, address, *args):
        """/lsp/stop_all - Stop all cues"""
        logger.info(f"⏹️ OSC: STOP ALL command received")
        try:
            # Stop all cues in the model
            for i in range(len(self.app.cue_model)):
                cue = self.app.cue_model.item(i)
                if cue:
                    cue.execute(action=CueAction.Stop)
        except Exception as e:
            logger.error(f"❌ Error in stop_all: {e}")
    
    def _handle_cue_start(self, address, *args):
        """/lsp/cue/N/start - Start cue at index N"""
        # Extract cue number from address: /lsp/cue/1/start
        parts = address.strip("/").split("/")
        if len(parts) < 4:
            logger.warning(f"⚠️ Invalid cue command: {address}")
            return
        
        try:
            cue_index = int(parts[2])
            logger.info(f"▶️ OSC: Start cue {cue_index}")
            
            if cue_index < len(self.app.cue_model):
                cue = self.app.cue_model.item(cue_index)
                if cue:
                    cue.execute(action=CueAction.Start)
            else:
                logger.warning(f"⚠️ Cue index {cue_index} out of range")
        except (ValueError, IndexError) as e:
            logger.warning(f"⚠️ Could not parse cue index from {address}: {e}")
    
    def _handle_cue_stop(self, address, *args):
        """/lsp/cue/N/stop - Stop cue at index N"""
        parts = address.strip("/").split("/")
        if len(parts) < 4:
            logger.warning(f"⚠️ Invalid cue command: {address}")
            return
        
        try:
            cue_index = int(parts[2])
            logger.info(f"⏹️ OSC: Stop cue {cue_index}")
            
            if cue_index < len(self.app.cue_model):
                cue = self.app.cue_model.item(cue_index)
                if cue:
                    cue.execute(action=CueAction.Stop)
            else:
                logger.warning(f"⚠️ Cue index {cue_index} out of range")
        except (ValueError, IndexError) as e:
            logger.warning(f"⚠️ Could not parse cue index from {address}: {e}")
    
    def _handle_cue_pause(self, address, *args):
        """/lsp/cue/N/pause - Pause cue at index N"""
        parts = address.strip("/").split("/")
        if len(parts) < 4:
            logger.warning(f"⚠️ Invalid cue command: {address}")
            return
        
        try:
            cue_index = int(parts[2])
            logger.info(f"⏸️ OSC: Pause cue {cue_index}")
            
            if cue_index < len(self.app.cue_model):
                cue = self.app.cue_model.item(cue_index)
                if cue:
                    cue.execute(action=CueAction.Pause)
            else:
                logger.warning(f"⚠️ Cue index {cue_index} out of range")
        except (ValueError, IndexError) as e:
            logger.warning(f"⚠️ Could not parse cue index from {address}: {e}")
    
    # === Legacy Companion Handler ===
    
    def _execute_button(self, page, row, column):
        """Execute LSP cue based on button coordinates"""
        # Calculate button index (assuming row-major grid)
        # Standard Stream Deck has 5 columns, 3 rows (15 buttons)
        button_index = row * 5 + column
        
        logger.info(f"🎯 Button pressed: page={page}, index={button_index}")
        
        # Special case: button 0 = GO
        if button_index == 0:
            self._execute_go()
            return
        
        # Check custom mappings first
        custom_key = (row, column)
        if custom_key in self._custom_mappings:
            cue_id = self._custom_mappings[custom_key]
            cue = self.app.cue_model.get(cue_id)
            if cue:
                logger.info(f"▶️ Executing custom-mapped cue: {cue.name}")
                cue.execute(action=CueAction.Start)
                return
            else:
                logger.warning(f"⚠️ Custom-mapped cue not found: {cue_id}")
        
        # Check if we have an auto-mapping
        if button_index in self._button_mapping:
            cue_id = self._button_mapping[button_index]
            cue = self.app.cue_model.get(cue_id)
            if cue:
                logger.info(f"▶️ Executing cue: {cue.name}")
                cue.execute(action=CueAction.Start)
            else:
                logger.warning(f"⚠️ Cue not found: {cue_id}")
        else:
            # Auto-map: try to execute cue at index button_index - 1
            if self._auto_map and button_index > 0:
                cue_index = button_index - 1
                if cue_index < len(self.app.cue_model):
                    cue = self.app.cue_model.item(cue_index)
                    logger.info(f"▶️ Auto-executing cue {cue_index}: {cue.name}")
                    cue.execute(action=CueAction.Start)
                else:
                    logger.warning(f"⚠️ No cue at index {cue_index}")
    
    def _execute_go(self):
        """Execute GO button - start next cue"""
        logger.info("🎬 GO button pressed")
        # Find the next cue to execute
        # Simple approach: find first cue that's not running
        for cue in self.app.cue_model:
            if not cue.is_running():
                logger.info(f"▶️ GO → {cue.name}")
                cue.execute(action=CueAction.Start)
                break
    
    def _load_custom_mappings(self):
        """Load custom button→cue mappings from config"""
        self._custom_mappings.clear()
        
        custom_mappings = self.config.get("custom_mappings", [])
        if not custom_mappings:
            return
        
        logger.info(f"📋 Loading {len(custom_mappings)} custom mappings")
        for mapping in custom_mappings:
            row = mapping.get("row", 0)
            column = mapping.get("column", 0)
            cue_id = mapping.get("cue_id")
            
            if cue_id is not None:
                key = (row, column)
                self._custom_mappings[key] = cue_id
                logger.debug(f"  Button ({row},{column}) → Cue {cue_id}")
    
    def _rebuild_mapping(self):
        """Rebuild button -> cue mapping"""
        self._button_mapping.clear()
        
        # Button 0 is reserved for GO
        # Buttons 1-N map to cue indices 0-(N-1)
        for i, cue in enumerate(self.app.cue_model):
            button_index = i + 1
            self._button_mapping[button_index] = cue.id
            
        logger.info(f"🗺️ Auto-mapped {len(self._button_mapping)} buttons to cues")
