# main.py
import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.logger import get_logger
from ui.main_window import MainWindow
from core.factory import coder_factory

def register_algorithms():
    """Register all available algorithms with the factory"""
    # Text algorithms
    from algorithms.text.shannon_fano import ShannonFanoCoder
    from algorithms.text.huffman import HuffmanCoder
    from algorithms.text.arithmetic import ArithmeticCoder
    from algorithms.text.run_length import RunLengthCoder
    from algorithms.text.lzw import LZWCoder
    
    coder_factory.register_text_coder("Shannon-Fano", ShannonFanoCoder)
    coder_factory.register_text_coder("Huffman", HuffmanCoder)
    coder_factory.register_text_coder("Arithmetic", ArithmeticCoder)
    coder_factory.register_text_coder("Run Length", RunLengthCoder)
    coder_factory.register_text_coder("LZW", LZWCoder)
    
    # Image algorithms
    from algorithms.image.jpeg import JPEGCoder
    coder_factory.register_image_coder("JPEG", JPEGCoder)
    
    # Audio algorithms
    from algorithms.audio.lpc import LPCCoder
    coder_factory.register_audio_coder("LPC", LPCCoder)
    
    # Video algorithms
    from algorithms.video.h261 import H261Coder
    coder_factory.register_video_coder("H.261", H261Coder)

def main():
    """Main application entry point"""
    logger = get_logger()
    try:
        logger.info("Starting application")
        register_algorithms()
        logger.info("Registered all algorithms")
        app = MainWindow()
        logger.info("Initialized main window")
        app.run()
        logger.info("Application finished")
    except Exception as e:
        logger.critical(f"Application error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
