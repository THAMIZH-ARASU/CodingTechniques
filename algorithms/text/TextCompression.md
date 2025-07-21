# Text Compression Algorithms

This module implements several classic text compression algorithms. Each algorithm is explained in detail below, including its theory, steps, advantages, disadvantages, and practical notes.

---

## 1. Shannon-Fano Coding

**Theory:**
Shannon-Fano coding is an early entropy encoding technique based on the probability of occurrence of each symbol. It builds a binary tree by recursively dividing the set of symbols into two groups with as close to equal total probabilities as possible.

**Algorithm Steps:**
1. Calculate the frequency/probability of each symbol in the input.
2. Sort the symbols in descending order of probability.
3. Recursively divide the list into two parts with (almost) equal total probabilities.
4. Assign '0' to one part and '1' to the other at each split.
5. Repeat until each symbol has a unique binary code.

**Advantages:**
- Simple to implement.
- Provides prefix-free codes.

**Disadvantages:**
- Not always optimal; may produce longer codes than Huffman for some distributions.
- Sensitive to symbol probability distribution.

**Practical Notes:**
- Used mainly for educational purposes; rarely used in modern compressors.

---

## 2. Huffman Coding

**Theory:**
Huffman coding is a widely used entropy encoding algorithm that produces an optimal prefix code for a set of symbols based on their frequencies. It builds a binary tree by repeatedly merging the two least probable symbols.

**Algorithm Steps:**
1. Calculate the frequency of each symbol.
2. Create a leaf node for each symbol and build a min-heap.
3. While there is more than one node in the heap:
   - Remove the two nodes with the lowest frequency.
   - Merge them into a new node with their combined frequency.
   - Insert the new node back into the heap.
4. Assign binary codes by traversing the tree (left = '0', right = '1').

**Advantages:**
- Produces optimal prefix codes for known symbol frequencies.
- Simple and fast for static data.

**Disadvantages:**
- Requires two passes: one to build the frequency table, one to encode.
- Not adaptive (unless using Adaptive Huffman).

**Practical Notes:**
- Used in many file formats (e.g., DEFLATE, JPEG, MP3, PNG).

---

## 3. Arithmetic Coding

**Theory:**
Arithmetic coding encodes an entire message into a single fractional number between 0 and 1. It achieves compression rates close to the theoretical entropy limit by representing the message as a subinterval of [0,1) based on symbol probabilities.

**Algorithm Steps:**
1. Calculate the probability of each symbol.
2. Start with the interval [0,1).
3. For each symbol in the message:
   - Subdivide the current interval according to the symbol probabilities.
   - Select the subinterval corresponding to the current symbol.
4. The final interval uniquely represents the message; any number within it is a valid encoding.

**Advantages:**
- Achieves compression rates very close to entropy.
- Can handle fractional bits per symbol.

**Disadvantages:**
- More complex to implement than Huffman.
- Susceptible to floating-point precision issues.
- Slower for short messages.

**Practical Notes:**
- Used in advanced codecs (e.g., JPEG2000, H.264/AVC, Bzip2).

---

## 4. Run Length Encoding (RLE)

**Theory:**
RLE is a simple lossless compression method that replaces sequences of repeated symbols with a single symbol and a count.

**Algorithm Steps:**
1. Scan the input for runs of the same symbol.
2. Replace each run with the symbol and the run length.

**Advantages:**
- Extremely simple and fast.
- Very effective for data with long runs (e.g., bitmap images, simple text).

**Disadvantages:**
- Ineffective for data without runs; can increase size.
- Not suitable for most natural language text.

**Practical Notes:**
- Used in fax, bitmap images, and as a preprocessing step in other algorithms.

---

## 5. Lempel-Ziv-Welch (LZW) Coding

**Theory:**
LZW is a dictionary-based compression algorithm that replaces repeated sequences with references to a dynamically built dictionary.

**Algorithm Steps:**
1. Initialize the dictionary with all possible single-symbol strings.
2. Scan the input for the longest string that exists in the dictionary.
3. Output the dictionary index for that string.
4. Add the new string (current + next symbol) to the dictionary.
5. Repeat until the input is exhausted.

**Advantages:**
- No need to transmit the dictionary; both encoder and decoder build it on the fly.
- Good for data with repeated patterns.

**Disadvantages:**
- Dictionary can grow large; may need to reset or limit size.
- Not optimal for all data types.

**Practical Notes:**
- Used in GIF, TIFF, and early Unix compress utility.

---

## References
- David Salomon, "Data Compression: The Complete Reference"
- Wikipedia: [Shannon-Fano](https://en.wikipedia.org/wiki/Shannon%E2%80%93Fano_coding), [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding), [Arithmetic coding](https://en.wikipedia.org/wiki/Arithmetic_coding), [Run-length encoding](https://en.wikipedia.org/wiki/Run-length_encoding), [LZW](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch) 