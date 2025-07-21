# algorithms/text/shannon_fano.py
from collections import defaultdict
from typing import Dict, Tuple, Any
from core.base_coder import TextCoder

class ShannonFanoCoder(TextCoder):
    """Shannon-Fano coding implementation"""
    
    @property
    def algorithm_name(self) -> str:
        return "Shannon-Fano"
    
    def _sort_by_frequency(self, frequencies):
        return sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    
    def _shannon_fano_code(self, symbols, code_dict, prefix=""):
        if len(symbols) == 1:
            symbol, _ = symbols[0]
            code_dict[symbol] = prefix if prefix else "0"
            return
        
        total = sum(freq for _, freq in symbols)
        cumulative = 0
        split_index = 0
        
        for i, (_, freq) in enumerate(symbols):
            cumulative += freq
            if cumulative >= total / 2:
                split_index = i + 1
                break
        
        self.logger.debug(f"Splitting at index {split_index} with prefix '{prefix}'")
        self._shannon_fano_code(symbols[:split_index], code_dict, prefix + "0")
        self._shannon_fano_code(symbols[split_index:], code_dict, prefix + "1")
    
    def encode(self, data: str) -> Tuple[str, Dict]:
        super().encode(data)
        frequencies = defaultdict(int)
        for char in data:
            frequencies[char] += 1
        
        self.logger.debug(f"Calculated frequencies: {dict(frequencies)}")
        
        sorted_symbols = self._sort_by_frequency(frequencies)
        code_dict = {}
        self._shannon_fano_code(sorted_symbols, code_dict)
        self.logger.debug(f"Generated Shannon-Fano code dict: {code_dict}")
        
        encoded_message = ''.join(code_dict.get(char, '') for char in data)
        
        metadata = {
            'code_dict': code_dict,
            'original_length': len(data),
            'encoded_length': len(encoded_message)
        }
        
        self.logger.info(f"Encoded {metadata['original_length']} chars to {metadata['encoded_length']} bits.")
        return encoded_message, metadata
    
    def decode(self, encoded_data: str, metadata: Dict) -> str:
        super().decode(encoded_data, metadata)
        reverse_code_dict = {v: k for k, v in metadata['code_dict'].items()}
        decoded_message = ''
        current_code = ''
        
        for bit in encoded_data:
            current_code += bit
            if current_code in reverse_code_dict:
                decoded_message += reverse_code_dict[current_code]
                current_code = ''
        
        self.logger.info(f"Decoded {len(encoded_data)} bits to {len(decoded_message)} chars.")
        return decoded_message
