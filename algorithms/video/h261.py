# algorithms/video/h261.py
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from core.base_coder import VideoCoder

class H261Coder(VideoCoder):
    """H.261 video coding with motion estimation and compensation (robust block-based version)"""
    
    @property
    def algorithm_name(self) -> str:
        return "H.261 (Motion Estimation & Compensation)"
    
    def __init__(self, block_size: int = 16, search_range: int = 8):
        super().__init__()
        self.block_size = block_size
        self.search_range = search_range
        self.logger.info(f"Initialized H.261 Coder with block_size={block_size}, search_range={search_range}")

    def motion_estimation(self, current_frame: np.ndarray, reference_frame: np.ndarray) -> np.ndarray:
        height, width = current_frame.shape
        num_blocks_y = height // self.block_size
        num_blocks_x = width // self.block_size
        motion_vectors = np.zeros((num_blocks_y, num_blocks_x, 2), dtype=int)
        for y in range(0, num_blocks_y * self.block_size, self.block_size):
            for x in range(0, num_blocks_x * self.block_size, self.block_size):
                best_match = (0, 0)
                min_error = float('inf')
                current_block = current_frame[y:y + self.block_size, x:x + self.block_size]
                for dy in range(-self.search_range, self.search_range + 1):
                    for dx in range(-self.search_range, self.search_range + 1):
                        ref_x = x + dx
                        ref_y = y + dy
                        if (0 <= ref_x < width - self.block_size + 1 and 
                            0 <= ref_y < height - self.block_size + 1):
                            ref_block = reference_frame[ref_y:ref_y + self.block_size, ref_x:ref_x + self.block_size]
                            error = np.sum((current_block - ref_block) ** 2)
                            if error < min_error:
                                min_error = error
                                best_match = (dy, dx)
                motion_vectors[y // self.block_size, x // self.block_size] = best_match
        return motion_vectors

    def motion_compensation(self, reference_frame: np.ndarray, motion_vectors: np.ndarray) -> np.ndarray:
        height, width = reference_frame.shape
        num_blocks_y = height // self.block_size
        num_blocks_x = width // self.block_size
        compensated_frame = np.zeros_like(reference_frame)
        for y in range(0, num_blocks_y * self.block_size, self.block_size):
            for x in range(0, num_blocks_x * self.block_size, self.block_size):
                dy, dx = motion_vectors[y // self.block_size, x // self.block_size]
                ref_x = x + dx
                ref_y = y + dy
                if (0 <= ref_x < width - self.block_size + 1 and 
                    0 <= ref_y < height - self.block_size + 1):
                    compensated_frame[y:y + self.block_size, x:x + self.block_size] = \
                        reference_frame[ref_y:ref_y + self.block_size, ref_x:ref_x + self.block_size]
        return compensated_frame

    def encode(self, data: str) -> Tuple[Dict, Dict]:
        """Encode video file (data is the path to the video file)"""
        import cv2
        cap = cv2.VideoCapture(data)
        if not cap.isOpened():
            self.logger.error(f"Cannot open video file: {data}")
            raise ValueError("Cannot open video file")
        self.logger.info(f"Starting to encode video file: {data}")
        frames = []
        motion_vectors_list = []
        prev_frame = None
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        block_size = self.block_size
        search_range = self.search_range
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # Adjust dimensions to be multiples of block_size
        frame_width_adjusted = (frame_width // block_size) * block_size
        frame_height_adjusted = (frame_height // block_size) * block_size
        i = 0
        max_frames_to_process = 50 # Temporary limit for debugging
        self.logger.info(f"Processing up to {max_frames_to_process} frames for this test run.")
        while i < max_frames_to_process:
            ret, frame = cap.read()
            if not ret:
                self.logger.info("End of video file reached.")
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = gray_frame[:frame_height_adjusted, :frame_width_adjusted]
            if prev_frame is None:
                frames.append(gray_frame)
                motion_vectors_list.append(None)
            else:
                motion_vectors = self.motion_estimation(gray_frame, prev_frame)
                compensated_frame = self.motion_compensation(prev_frame, motion_vectors)
                residual = gray_frame.astype(int) - compensated_frame.astype(int)
                frames.append(residual)
                motion_vectors_list.append(motion_vectors)
            prev_frame = gray_frame
            i += 1
            if i % 10 == 0:
                self.logger.info(f"-> Processed frame {i}/{frame_count}")
        cap.release()
        self.logger.info(f"Finished encoding video file. Total frames processed: {len(frames)}")
        encoded_data = {
            'frames': frames,
            'motion_vectors': motion_vectors_list
        }
        metadata = {
            'frame_count': len(frames),
            'frame_shape': frames[0].shape if frames else (0, 0),
            'block_size': self.block_size,
            'search_range': self.search_range
        }
        return encoded_data, metadata

    def decode(self, encoded_data: Dict, metadata: Dict) -> List[np.ndarray]:
        """Decode video frames from encoded data and metadata"""
        frames = encoded_data['frames']
        motion_vectors_list = encoded_data['motion_vectors']
        decoded_frames = []
        prev_frame = None
        for i, (frame_data, motion_vectors) in enumerate(zip(frames, motion_vectors_list)):
            if motion_vectors is None:
                decoded_frame = frame_data
            else:
                compensated_frame = self.motion_compensation(prev_frame, motion_vectors)
                decoded_frame = compensated_frame.astype(int) + frame_data
                decoded_frame = np.clip(decoded_frame, 0, 255).astype(np.uint8)
            decoded_frames.append(decoded_frame)
            prev_frame = decoded_frame
        return decoded_frames
