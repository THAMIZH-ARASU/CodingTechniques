# algorithms/text/huffman.py
from collections import Counter
from typing import Dict, Tuple, Any, Optional
from core.base_coder import TextCoder

class HuffmanNode:
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

class HuffmanCoder(TextCoder):
    """Huffman coding implementation"""
    
    @property
    def algorithm_name(self) -> str:
        return "Huffman"
    
    def _build_tree(self, frequencies: Dict[str, int]) -> HuffmanNode:
        nodes = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
        
        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x: x.freq)
            left = nodes.pop(0)
            right = nodes.pop(0)
            
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            nodes.append(merged)
        
        self.logger.debug("Built Huffman tree")
        return nodes[0] if nodes else None
    
    def _generate_codes(self, node: HuffmanNode, code: str = '', codes: Dict = None) -> Dict:
        if codes is None:
            codes = {}
        
        if node:
            if node.char:  # Leaf node
                codes[node.char] = code if code else "0"
            else:
                self._generate_codes(node.left, code + '0', codes)
                self._generate_codes(node.right, code + '1', codes)
        
        return codes
    
    def encode(self, data: str) -> Tuple[str, Dict]:
        super().encode(data)
        if not data:
            return "", {"codes": {}, "tree_structure": None}
        
        frequencies = Counter(data)
        self.logger.debug(f"Calculated frequencies: {dict(frequencies)}")
        root = self._build_tree(frequencies)
        codes = self._generate_codes(root)
        self.logger.debug(f"Generated Huffman codes: {codes}")
        
        encoded_message = ''.join(codes.get(char, '') for char in data)
        
        metadata = {
            'codes': codes,
            'frequencies': dict(frequencies),
            'original_length': len(data),
            'encoded_length': len(encoded_message)
        }
        
        self.logger.info(f"Encoded {metadata['original_length']} chars to {metadata['encoded_length']} bits.")
        return encoded_message, metadata
    
    def decode(self, encoded_data: str, metadata: Dict) -> str:
        super().decode(encoded_data, metadata)
        if not encoded_data or not metadata.get('codes'):
            return ""
        
        # Rebuild tree from frequencies
        frequencies = metadata['frequencies']
        root = self._build_tree(frequencies)
        
        decoded = []
        node = root
        
        for bit in encoded_data:
            node = node.left if bit == '0' else node.right
            if node and node.char:  # Leaf node
                decoded.append(node.char)
                node = root
        
        self.logger.info(f"Decoded {len(encoded_data)} bits to {len(decoded)} chars.")
        return ''.join(decoded)
