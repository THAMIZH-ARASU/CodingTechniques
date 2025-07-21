# ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from ui.text_coding_tab import TextCodingTab
from ui.image_coding_tab import ImageCodingTab
from ui.audio_coding_tab import AudioCodingTab
from ui.video_coding_tab import VideoCodingTab
from core.logger import get_logger

logger = get_logger(__name__)

class MainWindow:
    def __init__(self):
        logger.info("Creating main window")
        self.root = tk.Tk()
        self.root.title("Information Coding Techniques Learning Application")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        self.setup_ui()
    
    def setup_ui(self):
        logger.debug("Setting up UI")
        # Create main menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.text_tab = TextCodingTab(self.notebook)
        self.image_tab = ImageCodingTab(self.notebook)
        self.audio_tab = AudioCodingTab(self.notebook)
        self.video_tab = VideoCodingTab(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.text_tab.frame, text="Text Coding")
        self.notebook.add(self.image_tab.frame, text="Image Coding")
        self.notebook.add(self.audio_tab.frame, text="Audio Coding")
        self.notebook.add(self.video_tab.frame, text="Video Coding")
    
    def show_about(self):
        logger.debug("Showing about dialog")
        about_text = """
Information Coding Techniques Learning Application

This application demonstrates various coding techniques:
- Text: Shannon-Fano, Huffman, Arithmetic, Run Length, LZW
- Image: JPEG (Lossy and Lossless)
- Audio: LPC, MPEG-Audio
- Video: Motion Estimation & Compensation, H.261

Designed for educational purposes to understand
information theory and coding algorithms.
        """
        messagebox.showinfo("About", about_text)
    
    def run(self):
        logger.info("Starting main event loop")
        self.root.mainloop()
        logger.info("Main event loop finished")
