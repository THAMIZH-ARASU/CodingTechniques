# Audio Compression Algorithms

This module implements Linear Predictive Coding (LPC) for audio compression. Below is a detailed explanation of LPC, its theory, algorithm, and practical considerations.

---

## Linear Predictive Coding (LPC)

### Theory
Linear Predictive Coding (LPC) is a powerful method for representing the spectral envelope of a digital audio signal in compressed form. It is widely used in speech coding, audio synthesis, and telecommunication systems.

LPC models each audio sample as a linear combination of previous samples. The coefficients of this linear model are chosen to minimize the prediction error (the difference between the actual and predicted sample values).

Mathematically, for a signal x[n]:

    x[n] ≈ -a1*x[n-1] - a2*x[n-2] - ... - ap*x[n-p]

where a1, ..., ap are the LPC coefficients and p is the order of the model.

### Algorithm Steps
1. **Framing**: The audio signal is divided into short frames (not shown in this project; operates on the whole signal).
2. **Autocorrelation**: Compute the autocorrelation of the signal up to the desired order.
3. **Levinson-Durbin Recursion**: Solve the Yule-Walker equations to find the LPC coefficients efficiently.
4. **Encoding**: Store the LPC coefficients and the initial samples (for reconstruction).
5. **Decoding**: Reconstruct the signal by recursively applying the LPC model using the coefficients and initial samples.

### Levinson-Durbin Algorithm
The Levinson-Durbin recursion is an efficient method to solve the Toeplitz system of equations arising from the autocorrelation method. It computes the LPC coefficients in O(p^2) time, where p is the order.

**Steps:**
- Initialize the prediction error as the zero-lag autocorrelation.
- For each order from 1 to p:
  - Compute the reflection (PARCOR) coefficient.
  - Update the LPC coefficients.
  - Update the prediction error.
- Stop if the error becomes non-positive (unstable filter).

### Advantages
- Very efficient for speech and audio signals.
- Provides a compact representation (few coefficients per frame).
- Enables low-bitrate speech coding (used in GSM, vocoders, etc.).

### Disadvantages
- Sensitive to noise and non-speech signals.
- Requires careful handling of filter stability.
- Not suitable for music or complex audio.

### Practical Notes
- LPC is the basis for many speech codecs (e.g., GSM, LPC-10, CELP).
- In this project, the entire signal is modeled as one frame for simplicity.
- The order of the LPC model (number of coefficients) is user-selectable.
- The implementation uses the autocorrelation method and Levinson-Durbin recursion for stability and efficiency.

### References
- [LPC Wikipedia](https://en.wikipedia.org/wiki/Linear_predictive_coding)
- Rabiner & Schafer, "Digital Processing of Speech Signals"
- David Salomon, "Data Compression: The Complete Reference" 