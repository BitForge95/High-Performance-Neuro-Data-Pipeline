# NeuroAlign (High-Performance-Neuro-Data-Pipeline)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A high-performance, object-oriented data infrastructure library designed to mathematically align large-scale neuronal recordings with high-dimensional behavioral stimuli. 

As neuroscience datasets scale to the terabyte level (e.g., Allen Neuropixels, Brain Wide Map), standard procedural data loaders act as severe memory bottlenecks. **NeuroAlign** solves this by utilizing OS-level memory mapping and proxy objects to load, filter, and temporally synchronize massive, out-of-core multimodal datasets without exceeding standard RAM limitations.

## Core Architecture

* **Zero-Copy Memory Mapping:** Bypasses standard memory limits using `mmap` and NumPy buffers, enabling instant partial access to multi-gigabyte binary files.
* **BIDS-Compliant fMRI Support:** Automatically parses JSON sidecars for Repetition Times (TR) and uses `nibabel` proxy objects to handle 4D NIfTI scans efficiently.
* **Multimodal Time Alignment:** Synchronizes disparate sampling frequencies (e.g., 30,000 Hz electrophysiology vs. 60 FPS video) to a unified event timeline.
* **Dynamic String Filtering:** Uses object composition to parse conditional string rules (e.g., "signal > 0.5") directly onto memory-mapped arrays.
* **HDF5 Serialization:** Exports synchronized multimodal slices directly to `.h5` files for immediate downstream ingestion by PyTorch/TensorFlow.

## Installation

Clone the repository and install the package globally in editable mode:

```bash
git clone [https://github.com/BitForge95/High-Performance-Neuro-Data-Pipeline.git](https://github.com/BitForge95/High-Performance-Neuro-Data-Pipeline.git)
cd High-Performance-Neuro-Data-Pipeline
pip install -e .

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
