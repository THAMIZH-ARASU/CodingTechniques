# algorithms/text/lzw.py
from typing import Dict, Tuple, Any, List
from core.base_coder import TextCoder

class LZWCoder(TextCoder):
    """LZW (Dictionary-based) coding implementation"""
    
    @property
    def algorithm_name(self) -> str:
        return "LZW (Dictionary-based)"
    
    def encode(self, data: str) -> Tuple[List[int], Dict]:
        super().encode(data)
        dictionary = {chr(i): i for i in range(256)}
        current_string = ""
        encoded_output = []
        
        for char in data:
            combined_string = current_string + char
            if combined_string in dictionary:
                current_string = combined_string
            else:
                self.logger.debug(f"Adding '{combined_string}' to dictionary at index {len(dictionary)}")
                encoded_output.append(dictionary[current_string])
                dictionary[combined_string] = len(dictionary)
                current_string = char
        
        if current_string:
            encoded_output.append(dictionary[current_string])
        
        self.logger.debug(f"Final dictionary size: {len(dictionary)}")
        
        metadata = {
            'original_length': len(data),
            'encoded_length': len(encoded_output),
            'dictionary_size': len(dictionary)
        }
        
        self.logger.info(f"Encoded {metadata['original_length']} chars to {metadata['encoded_length']} codes.")
        return encoded_output, metadata
    
    def decode(self, encoded_data: List[int], metadata: Dict) -> str:
        super().decode(encoded_data, metadata)
        if not encoded_data:
            return ""
        
        dictionary = {i: chr(i) for i in range(256)}
        current_code = encoded_data[0]
        current_string = dictionary[current_code]
        decoded_output = [current_string]
        
        for code in encoded_data[1:]:
            if code in dictionary:
                entry = dictionary[code]
            else:
                entry = current_string + current_string[0]
            
            decoded_output.append(entry)
            self.logger.debug(f"Adding '{current_string + entry[0]}' to dictionary at index {len(dictionary)}")
            dictionary[len(dictionary)] = current_string + entry[0]
            current_string = entry
        
        decoded_string = ''.join(decoded_output)
        self.logger.info(f"Decoded {len(encoded_data)} codes to {len(decoded_string)} chars.")
        return decoded_string
