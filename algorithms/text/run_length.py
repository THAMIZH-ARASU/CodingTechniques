# algorithms/text/run_length.py
from typing import Dict, Tuple, Any
from core.base_coder import TextCoder

class RunLengthCoder(TextCoder):
    """Run Length Encoding implementation"""
    
    @property
    def algorithm_name(self) -> str:
        return "Run Length Encoding"
    
    def encode(self, data: str) -> Tuple[str, Dict]:
        super().encode(data)
        if not data:
            return "", {"original_length": 0}
        
        encoded = []
        current_char = data[0]
        count = 1
        
        for char in data[1:]:
            if char == current_char:
                count += 1
            else:
                encoded.append(f"{count}{current_char}")
                current_char = char
                count = 1
        
        encoded.append(f"{count}{current_char}")
        encoded_string = ''.join(encoded)
        
        self.logger.debug(f"Encoded string: {encoded_string}")
        
        metadata = {
            'original_length': len(data),
            'encoded_length': len(encoded_string),
            'compression_ratio': len(data) / len(encoded_string) if encoded_string else 1
        }
        
        self.logger.info(f"Encoded {metadata['original_length']} chars to {metadata['encoded_length']} chars.")
        return encoded_string, metadata
    
    def decode(self, encoded_data: str, metadata: Dict) -> str:
        super().decode(encoded_data, metadata)
        if not encoded_data:
            return ""
        
        decoded = []
        i = 0
        
        while i < len(encoded_data):
            count_str = ""
            
            # Extract count
            while i < len(encoded_data) and encoded_data[i].isdigit():
                count_str += encoded_data[i]
                i += 1
            
            if i < len(encoded_data) and count_str:
                count = int(count_str)
                char = encoded_data[i]
                decoded.append(char * count)
                self.logger.debug(f"Decoded run: count={count}, char='{char}'")
                i += 1
        
        decoded_string = ''.join(decoded)
        self.logger.info(f"Decoded {len(encoded_data)} chars to {len(decoded_string)} chars.")
        return decoded_string
