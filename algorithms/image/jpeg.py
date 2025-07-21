# algorithms/image/jpeg.py
import numpy as np
from PIL import Image
from typing import Dict, Tuple, Any, Union
from core.base_coder import ImageCoder

class JPEGCoder(ImageCoder):
    """JPEG coding implementation (both lossy and lossless)"""
    
    @property
    def algorithm_name(self) -> str:
        return "JPEG"
    
    def __init__(self, quality: int = 90, lossless: bool = False):
        super().__init__()
        self.quality = quality
        self.lossless = lossless
        self.logger.info(f"Initialized JPEG Coder with quality={quality}, lossless={lossless}")
    
    def encode(self, data: Union[str, np.ndarray, Image.Image]) -> Tuple[bytes, Dict]:
        """Encode image data"""
        super().encode(data)
        if isinstance(data, str):  # File path
            self.logger.debug(f"Loading image from path: {data}")
            image = Image.open(data)
        elif isinstance(data, np.ndarray):  # numpy array
            self.logger.debug("Loading image from numpy array")
            image = Image.fromarray(data)
        elif isinstance(data, Image.Image): # Already a PIL Image
            self.logger.debug("Using provided PIL Image object")
            image = data
        else:
            raise TypeError(f"Unsupported data type for encoding: {type(data)}")
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            self.logger.debug(f"Converting image from {image.mode} to RGB")
            image = image.convert('RGB')
        
        # Save to bytes
        import io
        output = io.BytesIO()
        
        if self.lossless:
            # Use PNG for lossless compression
            self.logger.info("Encoding image using lossless (PNG) format")
            image.save(output, format='PNG', optimize=True)
            format_used = 'PNG'
        else:
            # Use JPEG for lossy compression
            self.logger.info(f"Encoding image using lossy (JPEG) format with quality={self.quality}")
            image.save(output, format='JPEG', quality=self.quality, optimize=True)
            format_used = 'JPEG'
        
        compressed_data = output.getvalue()
        
        metadata = {
            'original_size': image.size,
            'original_mode': image.mode,
            'format': format_used,
            'quality': self.quality if not self.lossless else 100,
            'lossless': self.lossless,
            'compressed_size': len(compressed_data),
            'original_data_size': len(image.tobytes())
        }
        
        self.logger.info(f"Encoded image from {metadata['original_data_size']} bytes to {metadata['compressed_size']} bytes.")
        return compressed_data, metadata
    
    def decode(self, encoded_data: bytes, metadata: Dict) -> Image.Image:
        """Decode image data"""
        super().decode(encoded_data, metadata)
        import io
        input_stream = io.BytesIO(encoded_data)
        image = Image.open(input_stream)
        self.logger.info(f"Decoded image with size {image.size} and mode {image.mode}")
        return image
