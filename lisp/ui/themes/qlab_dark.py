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
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication

from lisp.ui.themes import Theme


class QLab_Dark_Theme(Theme):
    """Modern dark theme inspired by QLab's interface"""
    
    Name = "QLab Dark"
    
    @staticmethod
    def apply(app: QApplication):
        """Apply the QLab dark theme to the application"""
        
        # Main stylesheet with QLab-inspired colors and design
        stylesheet = """
        /* Main Application Window */
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d2d2d, stop:1 #1a1a1a);
            color: #ffffff;
        }

        /* Menu Bar */
        QMenuBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #404040, stop:1 #353535);
            color: white;
            border-bottom: 1px solid #555;
            padding: 2px;
        }
        
        QMenuBar::item {
            background: transparent;
            padding: 6px 12px;
            border-radius: 4px;
            margin: 1px;
        }
        
        QMenuBar::item:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #005a9e);
        }

        /* Menu */
        QMenu {
            background: #2d2d2d;
            color: white;
            border: 1px solid #555;
            border-radius: 6px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 20px;
            border-radius: 4px;
            margin: 1px;
        }
        
        QMenu::item:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #005a9e);
        }
        
        QMenu::separator {
            height: 1px;
            background: #555;
            margin: 4px 8px;
        }

        /* Buttons */
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4a4a4a, stop:1 #3a3a3a);
            border: 1px solid #555;
            border-radius: 6px;
            color: white;
            font-weight: bold;
            padding: 8px 16px;
            margin: 2px;
            font-size: 11px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #5a5a5a, stop:1 #4a4a4a);
            border: 1px solid #666;
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3a3a3a, stop:1 #2a2a2a);
            border: 1px solid #444;
        }
        
        QPushButton:disabled {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2a2a2a, stop:1 #1a1a1a);
            border: 1px solid #333;
            color: #666;
        }

        /* Primary Action Buttons */
        QPushButton[primary="true"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4CAF50, stop:1 #45a049);
            border: 1px solid #45a049;
        }
        
        QPushButton[primary="true"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #5CBF60, stop:1 #4CAF50);
        }

        /* Danger Buttons */
        QPushButton[danger="true"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f44336, stop:1 #da190b);
            border: 1px solid #da190b;
        }
        
        QPushButton[danger="true"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff6659, stop:1 #f44336);
        }

        /* Tree Views and Lists */
        QTreeView, QListView, QTableView {
            background: #2d2d2d;
            alternate-background-color: #323232;
            color: white;
            border: 1px solid #404040;
            border-radius: 4px;
            gridline-color: #404040;
            selection-background-color: #0078d4;
            selection-color: white;
            font-size: 11px;
        }
        
        QTreeView::item, QListView::item, QTableView::item {
            padding: 6px 4px;
            border-bottom: 1px solid #383838;
        }
        
        QTreeView::item:selected, QListView::item:selected, QTableView::item:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #005a9e);
            border: none;
        }
        
        QTreeView::item:hover, QListView::item:hover, QTableView::item:hover {
            background: #404040;
        }

        /* Header Views */
        QHeaderView::section {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #404040, stop:1 #353535);
            color: white;
            padding: 8px 4px;
            border: 1px solid #555;
            border-radius: 0px;
            font-weight: bold;
            font-size: 10px;
        }

        /* Splitters */
        QSplitter::handle {
            background: #555;
            border: 1px solid #666;
        }
        
        QSplitter::handle:horizontal {
            width: 4px;
        }
        
        QSplitter::handle:vertical {
            height: 4px;
        }
        
        QSplitter::handle:hover {
            background: #777;
        }

        /* Text Inputs */
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {
            background: #1a1a1a;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 6px 8px;
            selection-background-color: #0078d4;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, 
        QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #0078d4;
        }

        /* Combo Boxes */
        QComboBox {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4a4a4a, stop:1 #3a3a3a);
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 6px 30px 6px 8px;
            min-width: 80px;
        }
        
        QComboBox:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #5a5a5a, stop:1 #4a4a4a);
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iI2ZmZmZmZiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            width: 12px;
            height: 8px;
        }
        
        QComboBox QAbstractItemView {
            background: #2d2d2d;
            border: 1px solid #555;
            border-radius: 4px;
            color: white;
            selection-background-color: #0078d4;
        }

        /* Sliders */
        QSlider::groove:horizontal {
            border: 1px solid #555;
            height: 8px;
            background: #2a2a2a;
            border-radius: 4px;
        }
        
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #cccccc);
            border: 1px solid #888;
            width: 18px;
            border-radius: 9px;
            margin: -5px 0;
        }
        
        QSlider::handle:horizontal:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f0f0, stop:1 #e0e0e0);
        }
        
        QSlider::sub-page:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #005a9e);
            border-radius: 4px;
        }

        /* Checkboxes and Radio Buttons */
        QCheckBox, QRadioButton {
            color: white;
            font-size: 11px;
        }
        
        QCheckBox::indicator, QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #555;
            border-radius: 3px;
            background: #1a1a1a;
        }
        
        QCheckBox::indicator:checked {
            background: #0078d4;
            border: 1px solid #005a9e;
        }
        
        QRadioButton::indicator {
            border-radius: 8px;
        }
        
        QRadioButton::indicator:checked {
            background: #0078d4;
            border: 1px solid #005a9e;
        }

        /* Group Boxes */
        QGroupBox {
            color: white;
            border: 1px solid #555;
            border-radius: 6px;
            margin-top: 12px;
            font-weight: bold;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 8px 0 8px;
            background: #2d2d2d;
        }

        /* Progress Bars */
        QProgressBar {
            border: 1px solid #555;
            border-radius: 4px;
            background: #1a1a1a;
            text-align: center;
            color: white;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4CAF50, stop:1 #45a049);
            border-radius: 3px;
        }

        /* Scroll Bars */
        QScrollBar:vertical {
            background: #2a2a2a;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #555;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #666;
        }
        
        QScrollBar:horizontal {
            background: #2a2a2a;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background: #555;
            border-radius: 6px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #666;
        }

        /* Status Bar */
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #353535, stop:1 #2a2a2a);
            color: white;
            border-top: 1px solid #555;
        }

        /* Tabs */
        QTabWidget::pane {
            border: 1px solid #555;
            border-radius: 4px;
            background: #2d2d2d;
        }
        
        QTabBar::tab {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #404040, stop:1 #353535);
            color: white;
            border: 1px solid #555;
            padding: 8px 16px;
            margin: 1px;
        }
        
        QTabBar::tab:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #005a9e);
        }
        
        QTabBar::tab:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #5a5a5a, stop:1 #4a4a4a);
        }

        /* Dialogs */
        QDialog {
            background: #2d2d2d;
            color: white;
        }

        /* Labels */
        QLabel {
            color: #cccccc;
            font-size: 11px;
        }
        
        QLabel[heading="true"] {
            color: white;
            font-size: 14px;
            font-weight: bold;
        }

        /* Tool Tips */
        QToolTip {
            background: #404040;
            color: white;
            border: 1px solid #666;
            border-radius: 4px;
            padding: 4px;
            font-size: 11px;
        }
        """
        
        app.setStyleSheet(stylesheet)
        
        # Set application palette for elements not covered by stylesheet
        palette = QPalette()
        
        # Window colors
        palette.setColor(QPalette.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        
        # Base colors (for input fields)
        palette.setColor(QPalette.Base, QColor(26, 26, 26))
        palette.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
        
        # Text colors
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        
        # Button colors
        palette.setColor(QPalette.Button, QColor(58, 58, 58))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        
        # Highlight colors
        palette.setColor(QPalette.Highlight, QColor(0, 120, 212))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(102, 102, 102))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(102, 102, 102))
        
        app.setPalette(palette)