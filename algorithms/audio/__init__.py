# algorithms/audio/__init__.py
"""
Audio coding algorithms implementation.

Contains implementations of audio compression and coding algorithms
including Linear Predictive Coding (LPC) and MPEG-Audio.
"""

from algorithms.audio.lpc import LPCCoder

# MPEG-Audio implementation would be added here
# from algorithms.audio.mpeg_audio import MPEGAudioCoder

__all__ = [
    'LPCCoder'
    # 'MPEGAudioCoder'  # When implemented
]
