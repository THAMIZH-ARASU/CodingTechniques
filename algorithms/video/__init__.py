# algorithms/video/__init__.py
"""
Video coding algorithms implementation.

Contains implementations of video compression algorithms including
H.261 with motion estimation and compensation.
"""

from algorithms.video.h261 import H261Coder

__all__ = ['H261Coder']
