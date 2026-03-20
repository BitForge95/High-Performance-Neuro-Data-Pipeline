# High-Performance-Neuro-Data-Pipeline

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A high-performance, object-oriented data infrastructure prototype designed to align large-scale neuronal recordings with high-dimensional behavioral stimuli. 

Built as an architectural proof-of-concept for the Experanto framework, this pipeline demonstrates scalable methods for loading, filtering, and temporally synchronizing massive, out-of-core multimodal datasets.

## Core Architecture

* **Zero-Copy Memory Mapping:** Bypasses standard memory limitations using OS-level `mmap` and NumPy buffers, enabling instant partial access to multi-gigabyte data files (e.g., Neuropixels recordings).
* **Multimodal Time Alignment:** Mathematically synchronizes disparate sampling frequencies (e.g., 30,000 Hz electrophysiology and 60 FPS behavioral video) to a unified event timeline.
* **Dynamic String Filtering:** Implements object composition to parse and apply conditional string rules (e.g., "signal > 0.5") directly to memory-mapped arrays during load operations.
* **Extensible OOP Design:** Utilizes Python Abstract Base Classes (ABCs) to enforce strict methodological contracts across all data loaders, maximizing modularity and code reuse.
* **Automated Testing & CI/CD:** Integrated with GitHub Actions and a comprehensive `pytest` suite to ensure mathematical accuracy and system stability upon every commit.

## Installation

Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/BitForge95/High-Performance-Neuro-Data-Pipeline.git](https://github.com/BitForge95/High-Performance-Neuro-Data-Pipeline.git)
cd High-Performance-Neuro-Data-Pipeline
pip install -r requirements.txt
```

## Usage

The pipeline includes a Command Line Interface (CLI) for rapid execution and alignment testing.

**Standard Alignment:**

```bash
python cli.py --ephys path/to/neuropixels.dat --video path/to/behavior.mp4 --time 2.5
```

**Applying Data Filters:**

Conditional thresholding can be applied during initialization to isolate specific signals:

```bash
python cli.py --ephys path/to/neuropixels.dat --video path/to/behavior.mp4 --time 2.5 --filter "signal > 0.8"
```

## Testing

This project enforces strict validation for its synchronization logic. Run the automated test suite locally:

```bash
pytest tests/
```

## Repository Structure

```text
├── pipeline/
│   ├── base_loader.py      # Abstract Base Class defining loader contracts
│   ├── ephys_loader.py     # Memory-mapped loader for high-density electrophysiology
│   ├── video_loader.py     # Standard loader for behavioral camera frames
│   ├── filter_engine.py    # String-parsing composition module
│   └── synchronizer.py     # Core temporal alignment engine
├── tests/
│   └── test_synchronizer.py # Automated test suite for alignment mathematics
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline configuration
├── cli.py                  # Command Line Interface execution script
└── requirements.txt        # System dependencies
```
