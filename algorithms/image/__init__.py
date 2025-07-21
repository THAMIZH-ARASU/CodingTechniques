# algorithms/image/__init__.py
"""
Image coding algorithms implementation.

Contains implementations of image compression algorithms including
JPEG coding with both lossy and lossless options.
"""

from algorithms.image.jpeg import JPEGCoder

__all__ = ['JPEGCoder']
