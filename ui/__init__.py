# ui/__init__.py
"""
User Interface components for the Information Coding application.

This package contains all the Tkinter-based GUI components including
the main window and specialized tabs for different coding categories.
"""

from ui.main_window import MainWindow
from ui.text_coding_tab import TextCodingTab
from ui.image_coding_tab import ImageCodingTab
from ui.audio_coding_tab import AudioCodingTab
from ui.video_coding_tab import VideoCodingTab

__all__ = [
    'MainWindow',
    'TextCodingTab',
    'ImageCodingTab',
    'AudioCodingTab',
    'VideoCodingTab'
]
