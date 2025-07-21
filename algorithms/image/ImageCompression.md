# Image Compression Algorithms

This module implements JPEG image compression, supporting both lossy and lossless modes. Below is a detailed explanation of the JPEG algorithm, its theory, steps, and practical considerations.

---

## JPEG Compression (Lossy and Lossless)

### Theory
JPEG (Joint Photographic Experts Group) is the most widely used image compression standard for photographs and natural images. It is a lossy compression algorithm, meaning some information is discarded to achieve higher compression ratios. JPEG can also operate in a lossless mode (using PNG in this project for demonstration), but its main strength is in lossy compression.

### Steps in JPEG Compression (Lossy)
1. **Color Space Conversion**: Convert the image from RGB to YCbCr (luminance and chrominance channels). (In this project, images are converted to RGB for simplicity.)
2. **Block Splitting**: Divide the image into 8x8 blocks.
3. **Discrete Cosine Transform (DCT)**: Apply the DCT to each block to convert spatial pixel values into frequency coefficients.
4. **Quantization**: Divide each DCT coefficient by a quantization value and round. This step discards less visually important information and is the main source of loss.
5. **Zigzag Scan and Run-Length Encoding**: Reorder coefficients and compress runs of zeros.
6. **Entropy Coding**: Apply Huffman or arithmetic coding to the quantized coefficients.
7. **File Packaging**: Store the compressed data along with metadata (quantization tables, Huffman tables, etc.).

### Lossless JPEG (PNG in this Project)
- Instead of quantization and DCT, lossless JPEG (or PNG) uses predictive coding and entropy coding without discarding any information.
- In this project, selecting "lossless" uses PNG compression via Pillow, which is a true lossless format.

### Advantages
- High compression ratios for photographic images.
- Adjustable quality (trade-off between size and fidelity).
- Supported by virtually all image viewers and editors.

### Disadvantages
- Lossy: Repeated saves degrade quality.
- Not suitable for images with sharp edges, text, or graphics (use PNG for those).
- Blocking artifacts may appear at high compression.

### Practical Notes
- JPEG is the standard for digital cameras, web images, and photo storage.
- Lossless mode (PNG) is used for images where fidelity is critical (e.g., medical, scientific, graphics).
- The implementation in this project uses Pillow for DCT, quantization, and file handling, and allows you to select quality and lossless options.

### References
- [JPEG Wikipedia](https://en.wikipedia.org/wiki/JPEG)
- [DCT Wikipedia](https://en.wikipedia.org/wiki/Discrete_cosine_transform)
- David Salomon, "Data Compression: The Complete Reference" 