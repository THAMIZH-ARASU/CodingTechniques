# core/factory.py
from typing import Dict, Type
from core.base_coder import BaseCoder, TextCoder, ImageCoder, AudioCoder, VideoCoder
from core.logger import get_logger

logger = get_logger()

class CoderFactory:
    """Factory for creating coding algorithm instances"""
    
    def __init__(self):
        self._text_coders: Dict[str, Type[TextCoder]] = {}
        self._image_coders: Dict[str, Type[ImageCoder]] = {}
        self._audio_coders: Dict[str, Type[AudioCoder]] = {}
        self._video_coders: Dict[str, Type[VideoCoder]] = {}
    
    def register_text_coder(self, name: str, coder_class: Type[TextCoder]):
        logger.debug(f"Registering text coder: {name}")
        self._text_coders[name] = coder_class
    
    def register_image_coder(self, name: str, coder_class: Type[ImageCoder]):
        logger.debug(f"Registering image coder: {name}")
        self._image_coders[name] = coder_class
    
    def register_audio_coder(self, name: str, coder_class: Type[AudioCoder]):
        logger.debug(f"Registering audio coder: {name}")
        self._audio_coders[name] = coder_class
    
    def register_video_coder(self, name: str, coder_class: Type[VideoCoder]):
        logger.debug(f"Registering video coder: {name}")
        self._video_coders[name] = coder_class
    
    def create_text_coder(self, name: str) -> TextCoder:
        logger.info(f"Creating text coder: {name}")
        if name not in self._text_coders:
            logger.error(f"Unknown text coder: {name}")
            raise ValueError(f"Unknown text coder: {name}")
        return self._text_coders[name]()
    
    def create_image_coder(self, name: str) -> ImageCoder:
        logger.info(f"Creating image coder: {name}")
        if name not in self._image_coders:
            logger.error(f"Unknown image coder: {name}")
            raise ValueError(f"Unknown image coder: {name}")
        return self._image_coders[name]()
    
    def create_audio_coder(self, name: str) -> AudioCoder:
        logger.info(f"Creating audio coder: {name}")
        if name not in self._audio_coders:
            logger.error(f"Unknown audio coder: {name}")
            raise ValueError(f"Unknown audio coder: {name}")
        return self._audio_coders[name]()
    
    def create_video_coder(self, name: str) -> VideoCoder:
        logger.info(f"Creating video coder: {name}")
        if name not in self._video_coders:
            logger.error(f"Unknown video coder: {name}")
            raise ValueError(f"Unknown video coder: {name}")
        return self._video_coders[name]()
    
    def get_available_coders(self):
        return {
            'text': list(self._text_coders.keys()),
            'image': list(self._image_coders.keys()),
            'audio': list(self._audio_coders.keys()),
            'video': list(self._video_coders.keys())
        }

# Global factory instance
coder_factory = CoderFactory()
