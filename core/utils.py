# core/utils.py
import os
import numpy as np
from typing import List, Dict, Any, Union
import json
from core.logger import get_logger

logger = get_logger()

def ensure_directory(path: str) -> str:
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(path):
        logger.info(f"Creating directory: {path}")
        os.makedirs(path)
    return path

def load_text_file(filepath: str, encoding: str = 'utf-8') -> str:
    """Load text content from file"""
    logger.debug(f"Loading text file: {filepath} with encoding {encoding}")
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        logger.warning(f"UnicodeDecodeError with {encoding}, trying latin-1")
        # Try with different encoding
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading text file {filepath}: {e}", exc_info=True)
        raise

def save_text_file(filepath: str, content: str, encoding: str = 'utf-8') -> None:
    """Save text content to file"""
    logger.debug(f"Saving text file: {filepath}")
    try:
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        logger.error(f"Error saving text file {filepath}: {e}", exc_info=True)
        raise

def calculate_compression_ratio(original_size: int, compressed_size: int) -> float:
    """Calculate compression ratio"""
    logger.debug(f"Calculating compression ratio: original={original_size}, compressed={compressed_size}")
    if compressed_size == 0:
        return float('inf')
    return original_size / compressed_size

def calculate_space_savings(original_size: int, compressed_size: int) -> float:
    """Calculate space savings percentage"""
    logger.debug(f"Calculating space savings: original={original_size}, compressed={compressed_size}")
    if original_size == 0:
        return 0.0
    return ((original_size - compressed_size) / original_size) * 100

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    size_bytes = float(size_bytes)
    i = 0
    
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_input_data(data: Any, data_type: str) -> bool:
    """Validate input data based on type"""
    logger.debug(f"Validating input data of type {data_type}")
    if data_type == "text":
        is_valid = isinstance(data, str) and len(data) > 0
    elif data_type == "audio":
        is_valid = isinstance(data, list) and all(isinstance(x, (int, float)) for x in data)
    elif data_type == "image":
        is_valid = data is not None
    elif data_type == "video":
        is_valid = isinstance(data, str) and os.path.exists(data)
    else:
        is_valid = False
    
    logger.debug(f"Validation result for {data_type}: {is_valid}")
    return is_valid

def export_results_to_json(data: Dict[str, Any], filepath: str) -> None:
    """Export results to JSON file with proper serialization"""
    logger.info(f"Exporting results to JSON: {filepath}")
    def serialize_numpy(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=serialize_numpy)
    except Exception as e:
        logger.error(f"Error exporting results to JSON {filepath}: {e}", exc_info=True)
        raise

def import_results_from_json(filepath: str) -> Dict[str, Any]:
    """Import results from JSON file"""
    logger.info(f"Importing results from JSON: {filepath}")
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error importing results from JSON {filepath}: {e}", exc_info=True)
        raise

def calculate_entropy(data: str) -> float:
    """Calculate Shannon entropy of text data"""
    if not data:
        return 0.0
    
    # Count character frequencies
    char_counts = {}
    for char in data:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    # Calculate entropy
    entropy = 0.0
    data_length = len(data)
    
    for count in char_counts.values():
        probability = count / data_length
        if probability > 0:
            entropy -= probability * np.log2(probability)
    
    logger.debug(f"Calculated entropy for data of length {len(data)}: {entropy}")
    return entropy

def pad_to_multiple(data: Union[str, List], multiple: int, pad_char: str = '0') -> Union[str, List]:
    """Pad data to be multiple of specified length"""
    if isinstance(data, str):
        remainder = len(data) % multiple
        if remainder != 0:
            padding = multiple - remainder
            return data + (pad_char * padding)
        return data
    elif isinstance(data, list):
        remainder = len(data) % multiple
        if remainder != 0:
            padding = multiple - remainder
            return data + [0] * padding
        return data
    
    return data

def binary_to_string(binary_data: str) -> str:
    """Convert binary string to ASCII string"""
    result = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            result += chr(int(byte, 2))
    return result

def string_to_binary(text: str) -> str:
    """Convert ASCII string to binary string"""
    return ''.join(format(ord(char), '08b') for char in text)

class PerformanceTimer:
    """Simple performance timer for measuring execution time"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.logger = get_logger()
    
    def start(self):
        import time
        self.start_time = time.time()
        self.logger.info("Timer started.")
    
    def stop(self):
        import time
        self.end_time = time.time()
        self.logger.info(f"Timer stopped. Elapsed time: {self.elapsed_str()}")
    
    def elapsed(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def elapsed_str(self) -> str:
        elapsed = self.elapsed()
        if elapsed < 1:
            return f"{elapsed*1000:.2f} ms"
        elif elapsed < 60:
            return f"{elapsed:.2f} seconds"
        else:
            minutes = int(elapsed // 60)
            seconds = elapsed % 60
            return f"{minutes}m {seconds:.2f}s"

def create_progress_callback(progress_var=None, status_label=None):
    """Create a progress callback function for long-running operations"""
    def callback(current: int, total: int, message: str = ""):
        if progress_var:
            progress = (current / total) * 100
            progress_var.set(progress)
        
        if status_label:
            if message:
                status_label.config(text=f"{message} ({current}/{total})")
            else:
                status_label.config(text=f"Progress: {current}/{total}")
    
    return callback
