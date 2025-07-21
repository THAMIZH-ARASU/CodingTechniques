# algorithms/__init__.py
"""
Information coding algorithms implementation.

This package contains implementations of various coding and compression
algorithms organized by data type (text, image, audio, video).
"""

# Import all algorithm modules to ensure they're available
from algorithms import text, image, audio, video

__all__ = ['text', 'image', 'audio', 'video']
