# CodingTechniques

A comprehensive Python application for learning, visualizing, and experimenting with classic information coding and compression algorithms for text, image, audio, and video data. The project features a modern GUI, robust logging, and modular algorithm implementations for educational and research purposes.

---

## Table of Contents
- [CodingTechniques](#codingtechniques)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Clone the Repository](#clone-the-repository)
    - [Install Dependencies](#install-dependencies)
  - [Usage](#usage)
    - [Run the Application](#run-the-application)
    - [Workflow](#workflow)
    - [Example (Text Compression)](#example-text-compression)
    - [Example (Image Compression)](#example-image-compression)
  - [Graphical User Interface (GUI)](#graphical-user-interface-gui)
  - [Algorithms Overview](#algorithms-overview)
  - [Logging and Troubleshooting](#logging-and-troubleshooting)
  - [Example Use Cases](#example-use-cases)
  - [FAQ](#faq)
  - [Directory Structure](#directory-structure)
  - [Contributing](#contributing)
  - [License](#license)

---

## Introduction

**CodingTechniques** is an interactive, educational platform for exploring the theory and practice of data compression. It provides hands-on experience with foundational algorithms in text, image, audio, and video compression, making it ideal for students, educators, and researchers. The application is built with modularity and extensibility in mind, allowing you to experiment, visualize, and compare different coding techniques in a unified environment.

---

## Features
- **Text Compression**: Shannon-Fano, Huffman, Arithmetic, Run Length Encoding, LZW
- **Image Compression**: JPEG (Lossy and Lossless)
- **Audio Compression**: LPC (Linear Predictive Coding)
- **Video Compression**: H.261 (Motion Estimation & Compensation)
- **Modern Tkinter GUI**: Interactive tabs for each data type
- **Logging**: All operations are logged to both terminal and file
- **Modular Design**: Easily extend or swap algorithms
- **Educational Documentation**: In-depth explanations for every algorithm
- **Cross-platform**: Works on Windows, macOS, and Linux

---

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Clone the Repository
```bash
git clone <repo-url>
cd CodingTechniques
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages include:**
- numpy
- pillow
- opencv-python
- tkinter (usually included with Python)

---

## Usage

### Run the Application
```bash
python main.py
```

### Workflow
1. **Launch the GUI**: The main window will open with tabs for Text, Image, Audio, and Video.
2. **Select a Tab**: Choose the type of data you want to compress/decompress.
3. **Choose an Algorithm**: Each tab provides a dropdown to select the algorithm.
4. **Load or Enter Data**: Use the provided controls to load files or enter data manually.
5. **Encode/Decode**: Click the Encode or Decode buttons to perform operations. Results and statistics are displayed in the output area.
6. **Save/Load Results**: You can save encoded results to JSON and load them back for decoding.

### Example (Text Compression)
1. Go to the **Text Coding** tab.
2. Enter or load a text file.
3. Select "Huffman" from the algorithm dropdown.
4. Click **Encode** to compress, then **Decode** to reconstruct the original text.
5. View compression statistics and save results if desired.

### Example (Image Compression)
1. Go to the **Image Coding** tab.
2. Load an image (JPEG, PNG, BMP, etc.).
3. Adjust quality or select lossless mode.
4. Click **Compress** to encode, then **Decompress** to view the result.
5. Save the compressed image if needed.

---

## Graphical User Interface (GUI)

The GUI is built with Tkinter and provides an intuitive, tabbed interface:

- **Text Coding Tab**: Encode/decode text using various algorithms. View statistics and save/load results.
- **Image Coding Tab**: Compress/decompress images with adjustable quality. Preview results.
- **Audio Coding Tab**: Encode/decode audio using LPC. View and edit sample data, save/load encoded JSON.
- **Video Coding Tab**: Encode/decode video using H.261-style motion estimation. View progress and statistics.

**Screenshot Example:**
<div align='center'>
  <img src="images/ui_example.png.png" alt="UI Example">
</div>

---

## Algorithms Overview

- **Text**: See [algorithms/text/TextCompression.md](algorithms/text/TextCompression.md)
- **Image**: See [algorithms/image/ImageCompression.md](algorithms/image/ImageCompression.md)
- **Audio**: See [algorithms/audio/AudioCompression.md](algorithms/audio/AudioCompression.md)
- **Video**: See [algorithms/video/VideoCompression.md](algorithms/video/VideoCompression.md)

Each algorithm is explained in detail, including theory, steps, advantages/disadvantages, and practical notes.

---

## Logging and Troubleshooting

- All operations are logged at INFO/DEBUG level to both the terminal and `coding_techniques.log`.
- If you encounter issues:
  - Check the terminal for real-time logs.
  - Review `coding_techniques.log` for a persistent record.
  - Use the logs to trace errors, performance bottlenecks, or unexpected behavior.
- For further debugging, increase the log level in `core/logger.py`.

---

## Example Use Cases

- **Educational Demos**: Show students how classic compression algorithms work step-by-step.
- **Algorithm Comparison**: Compare compression ratios and speed for different data types.
- **Research Prototyping**: Quickly test new ideas by adding or modifying algorithms.
- **Visualization**: Visualize motion vectors in video, code trees in text, or quantization in images.
- **Data Forensics**: Analyze how different algorithms affect data integrity and size.

---

## FAQ

**Q: Can I add my own algorithm?**
A: Yes! The codebase is modular. Add your algorithm in the appropriate `algorithms/` subfolder and register it in `main.py`.

**Q: Where are logs stored?**
A: All logs are written to both the terminal and `coding_techniques.log` in the project root.

**Q: What file formats are supported?**
A: Text: .txt; Image: .jpg, .jpeg, .png, .bmp, .tiff, .gif; Audio: .wav, .txt; Video: .avi, .mp4, .mov, .mkv, .flv

**Q: Why is video encoding slow?**
A: Block-based motion estimation is computationally intensive. Try using a smaller video or reducing the search range/block size for faster results.

**Q: Can I use this for real-world compression?**
A: This project is for educational and research purposes. For production use, refer to optimized libraries like ffmpeg and codecs.

---

## Directory Structure
```
CodingTechniques/
  algorithms/
    text/      # Text compression algorithms
    image/     # Image compression algorithms
    audio/     # Audio compression algorithms
    video/     # Video compression algorithms
  core/        # Core framework, utilities, logger
  ui/          # GUI components
  main.py      # Application entry point
  README.md    # This file
```

---

## Contributing
Pull requests and suggestions are welcome! Please open an issue or submit a PR. For major changes, please open an issue first to discuss what you would like to change.

---

## License
This project is licesned under MIT License 