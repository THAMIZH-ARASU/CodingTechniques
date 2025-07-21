# algorithms/text/arithmetic.py
from collections import defaultdict
from typing import Dict, Tuple, Any
from core.base_coder import TextCoder
from decimal import Decimal, getcontext

class ArithmeticCoder(TextCoder):
    """
    Arithmetic coding implementation based on the user-provided reference.
    This version uses an iterative interval refinement approach to minimize precision errors.
    """

    def __init__(self, precision: int = 50):
        super().__init__()
        getcontext().prec = precision
        self.logger.info(f"ArithmeticCoder initialized with precision {precision}")

    @property
    def algorithm_name(self) -> str:
        return "Arithmetic"

    def _get_probability_table(self, frequencies: Dict[str, int]) -> Dict[str, Decimal]:
        """Calculates the probability table using Decimal for high precision."""
        total_frequency = sum(frequencies.values())
        if total_frequency == 0:
            return {}

        probability_table = {}
        for key, value in frequencies.items():
            probability_table[key] = Decimal(value) / Decimal(total_frequency)

        return probability_table

    def encode(self, data: str) -> Tuple[Decimal, Dict]:
        """Encodes a message using arithmetic encoding."""
        super().encode(data)
        if not data:
            return Decimal(0), {"frequencies": {}}

        frequencies = defaultdict(int)
        for char in data:
            frequencies[char] += 1
        
        self.logger.debug(f"Calculated frequencies: {dict(frequencies)}")
        probability_table = self._get_probability_table(frequencies)
        
        # Sort symbols for consistent ordering
        sorted_symbols = sorted(probability_table.keys())

        stage_min = Decimal(0)
        stage_max = Decimal(1)

        for msg_term in data:
            stage_domain = stage_max - stage_min
            
            temp_stage_min = stage_min
            for symbol in sorted_symbols:
                term_prob = probability_table[symbol]
                cum_prob = temp_stage_min + term_prob * stage_domain
                
                if msg_term == symbol:
                    stage_min = temp_stage_min
                    stage_max = cum_prob
                    break
                temp_stage_min = cum_prob

        encoded_value = (stage_min + stage_max) / 2
        self.logger.debug(f"Final range: ({stage_min}, {stage_max}), encoded value: {encoded_value}")

        metadata = {
            'frequencies': dict(frequencies),
            'message_length': len(data),
            'original_length': len(data),
        }
        
        self.logger.info(f"Encoded {metadata['original_length']} chars to a Decimal.")
        return encoded_value, metadata

    def decode(self, encoded_data: Decimal, metadata: Dict) -> str:
        """Decodes a message from a high-precision Decimal number."""
        super().decode(encoded_data, metadata)
        if not metadata.get('frequencies'):
            return ""

        frequencies = metadata['frequencies']
        message_length = metadata.get('message_length')
        if not message_length:
            return ""

        probability_table = self._get_probability_table(frequencies)
        sorted_symbols = sorted(probability_table.keys())
        
        decoded_msg = []
        encoded_value = encoded_data

        stage_min = Decimal(0)
        stage_max = Decimal(1)

        for _ in range(message_length):
            stage_domain = stage_max - stage_min
            
            temp_stage_min = stage_min
            found_symbol = False
            for symbol in sorted_symbols:
                term_prob = probability_table[symbol]
                cum_prob = temp_stage_min + term_prob * stage_domain
                
                # Check if encoded value falls into the current symbol's range
                if temp_stage_min <= encoded_value < cum_prob:
                    decoded_msg.append(symbol)
                    stage_min = temp_stage_min
                    stage_max = cum_prob
                    found_symbol = True
                    break
                temp_stage_min = cum_prob

            if not found_symbol:
                # This can happen if the encoded_value is exactly the upper bound of the last interval
                # due to floating point inaccuracies. In this case, we assume it's the last symbol.
                last_symbol = sorted_symbols[-1]
                decoded_msg.append(last_symbol)
                self.logger.warning(f"Encoded value was at the boundary. Fallback to last symbol '{last_symbol}'.")
                
                # We need to update the interval to continue decoding correctly
                temp_stage_min = stage_min
                stage_domain = stage_max - stage_min
                for symbol in sorted_symbols:
                    term_prob = probability_table[symbol]
                    cum_prob = temp_stage_min + term_prob * stage_domain
                    if symbol == last_symbol:
                        stage_min = temp_stage_min
                        stage_max = cum_prob
                        break
                    temp_stage_min = cum_prob

        self.logger.info(f"Decoded Decimal to {len(decoded_msg)} chars.")
        return "".join(decoded_msg)
