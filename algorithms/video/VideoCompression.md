# Video Compression Algorithms

This module implements H.261-style video compression, focusing on block-based motion estimation and compensation. Below is a detailed explanation of the algorithm, its theory, steps, and practical considerations.

---

## H.261 Video Compression (Motion Estimation & Compensation)

### Theory
H.261 is one of the earliest digital video compression standards, designed for video conferencing and telephony. Its core idea is to exploit temporal redundancy between successive frames using motion estimation and compensation, combined with block-based transform coding.

### Steps in H.261-style Compression
1. **Frame Partitioning**: Each video frame is divided into fixed-size blocks (e.g., 16x16 pixels).
2. **Motion Estimation**: For each block in the current frame, search for the most similar block in a reference (previous) frame within a search window. The offset (motion vector) is stored.
3. **Motion Compensation**: Use the motion vectors to construct a predicted frame from the reference frame.
4. **Residual Calculation**: Subtract the predicted (compensated) frame from the current frame to obtain the residual (difference) frame.
5. **Encoding**: Store the motion vectors and the residuals. (In full H.261, the residuals are further transformed and quantized, but this project focuses on the core motion estimation/compensation.)
6. **Decoding**: Reconstruct each frame by adding the residual to the motion-compensated prediction from the previous frame.

### Block-based Motion Estimation
- Each block in the current frame is compared to candidate blocks in the reference frame within a search range.
- The best match is found by minimizing the sum of squared differences (SSD).
- The displacement (dy, dx) is stored as the motion vector for that block.

### Motion Compensation
- The reference frame is shifted according to the motion vectors to create a prediction of the current frame.
- The residual (difference) is encoded instead of the full frame, reducing temporal redundancy.

### Advantages
- Significantly reduces the amount of data needed to represent video by exploiting temporal redundancy.
- Forms the basis for all modern video codecs (MPEG, H.26x, H.264, H.265, AV1, etc.).

### Disadvantages
- Computationally intensive (especially for large search ranges and high-resolution video).
- Sensitive to scene changes and fast motion.
- Blocking artifacts may appear at block boundaries.

### Practical Notes
- H.261 is the ancestor of all modern block-based video codecs.
- Modern codecs add DCT, quantization, entropy coding, and more advanced motion models.
- The implementation in this project is educational and omits transform coding for clarity.
- For real-world use, further compression (DCT, quantization, entropy coding) is needed.

### References
- [H.261 Wikipedia](https://en.wikipedia.org/wiki/H.261)
- [Motion Estimation Wikipedia](https://en.wikipedia.org/wiki/Motion_estimation)
- David Salomon, "Data Compression: The Complete Reference" 