# algorithms/audio/lpc.py
import numpy as np
from typing import Dict, Tuple, Any, List
from core.base_coder import AudioCoder

class LPCCoder(AudioCoder):
    """Linear Predictive Coding implementation"""
    
    @property
    def algorithm_name(self) -> str:
        return "LPC (Linear Predictive Coding)"
    
    def __init__(self, order: int = 10):
        super().__init__()
        self.order = order
        self.logger.info(f"Initialized LPC Coder with order={order}")
    
    def _normalize(self, signal: np.ndarray) -> Tuple[np.ndarray, float, float]:
        mean = np.mean(signal)
        max_abs = np.max(np.abs(signal - mean))
        if max_abs == 0:
            max_abs = 1
        self.logger.debug(f"Normalized signal with mean={mean}, max_abs={max_abs}")
        return (signal - mean) / max_abs, mean, max_abs
    
    def _denormalize(self, signal: np.ndarray, mean: float, max_abs: float) -> np.ndarray:
        self.logger.debug(f"Denormalizing signal with mean={mean}, max_abs={max_abs}")
        return signal * max_abs + mean
    
    def _lpc_coefficients(self, signal: np.ndarray, order: int) -> np.ndarray:
        """
        Calculates LPC coefficients using the Levinson-Durbin recursion.
        This is a more robust implementation that avoids vectorization pitfalls.
        """
        n = len(signal)
        if n <= order:
            self.logger.warning(f"Signal length ({n}) must be greater than LPC order ({order}).")
            return np.array([])

        autocorr = np.correlate(signal, signal, mode='full')[n - 1:]
        
        if len(autocorr) <= order:
            self.logger.warning(f"Autocorrelation length is too short for the given LPC order.")
            return np.array([])

        R = autocorr
        a_coeffs = np.zeros(order + 1)
        E = R[0]

        if E == 0:
            self.logger.warning("Zero energy in signal, LPC coefficients cannot be calculated.")
            return np.array([])

        a_coeffs[0] = 1.0

        for i in range(1, order + 1):
            dot_product = np.dot(a_coeffs[1:i], R[i-1:0:-1])
            k = (R[i] - dot_product) / E
            
            old_a = a_coeffs.copy()
            a_coeffs[i] = k
            for j in range(1, i):
                a_coeffs[j] = old_a[j] - k * old_a[i-j]

            E = (1 - k**2) * E
            if E <= 0:
                self.logger.warning("Energy became non-positive, stopping LPC calculation.")
                break
        
        self.logger.debug(f"Calculated LPC coefficients (order {order}): {a_coeffs}")
        return a_coeffs
    
    def encode(self, data: List[float]) -> Tuple[np.ndarray, Dict]:
        super().encode(data)
        signal = np.array(data)
        normalized_signal, mean, max_abs = self._normalize(signal)
        
        coefficients = self._lpc_coefficients(normalized_signal, self.order)
        
        metadata = {
            'order': self.order,
            'mean': mean,
            'max_abs': max_abs,
            'signal_length': len(signal),
            'original_signal': signal[:self.order].tolist()  # Store initial samples
        }
        
        self.logger.info(f"Encoded {metadata['signal_length']} samples to {len(coefficients)} LPC coefficients.")
        return coefficients, metadata
    
    def decode(self, encoded_data: np.ndarray, metadata: Dict) -> List[float]:
        super().decode(encoded_data, metadata)
        coeffs = encoded_data
        order = metadata['order']
        mean = metadata['mean']
        max_abs = metadata['max_abs']
        signal_length = metadata['signal_length']
        initial_samples = np.array(metadata['original_signal'])
        
        decoded_signal = np.zeros(signal_length)
        decoded_signal[:order] = initial_samples
        
        for n in range(order, signal_length):
            decoded_signal[n] = -np.dot(coeffs[1:], decoded_signal[n-order:n][::-1])
        
        self.logger.debug("Reconstructed signal from LPC coefficients.")
        
        # Apply enhancement for small values
        for i in range(len(decoded_signal)):
            if abs(decoded_signal[i]) < 0.4:
                decoded_signal[i] *= 10
        
        denormalized_signal = self._denormalize(decoded_signal, mean, max_abs)
        self.logger.info(f"Decoded {len(coeffs)} LPC coefficients to {len(denormalized_signal)} samples.")
        return denormalized_signal.tolist()
