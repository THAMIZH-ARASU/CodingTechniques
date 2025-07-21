# core/base_coder.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
from core.logger import get_logger

class BaseCoder(ABC):
    """Abstract base class for all coding algorithms"""
    
    def __init__(self):
        self.logger = get_logger()

    @abstractmethod
    def encode(self, data: Any) -> Tuple[Any, Dict]:
        """Encode data and return encoded result with metadata"""
        self.logger.info(f"Encoding data with {self.algorithm_name}")

    @abstractmethod
    def decode(self, encoded_data: Any, metadata: Dict) -> Any:
        """Decode data using metadata"""
        self.logger.info(f"Decoding data with {self.algorithm_name}")
    
    @property
    @abstractmethod
    def algorithm_name(self) -> str:
        """Return the name of the algorithm"""
        pass

class TextCoder(BaseCoder):
    """Base class for text coding algorithms"""
    pass

class ImageCoder(BaseCoder):
    """Base class for image coding algorithms"""
    pass

class AudioCoder(BaseCoder):
    """Base class for audio coding algorithms"""
    pass

class VideoCoder(BaseCoder):
    """Base class for video coding algorithms"""
    pass
