# __init__.py (root)
"""
Information Coding Techniques Learning Application

A comprehensive educational tool for learning various information
coding and compression algorithms including text, image, audio,
and video coding techniques.
"""

__version__ = "1.0.0"
__author__ = "Educational Software Team"
__description__ = "Information Coding Techniques Learning Application"

from core.factory import coder_factory
from core.base_coder import BaseCoder, TextCoder, ImageCoder, AudioCoder, VideoCoder

# Register all algorithms on import
def _register_algorithms():
    """Register all available algorithms"""
    try:
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
        
    except ImportError as e:
        print(f"Warning: Could not register some algorithms: {e}")

# Auto-register algorithms
_register_algorithms()

__all__ = [
    'coder_factory',
    'BaseCoder',
    'TextCoder', 
    'ImageCoder',
    'AudioCoder',
    'VideoCoder'
]
