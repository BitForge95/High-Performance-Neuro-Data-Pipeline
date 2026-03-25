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

##Usage (Command Line Interface)

Installing the package exposes the neuro-align global command. You can align any combination of Electrophysiology, Video, and fMRI data.

**Standard Alignment with Export :**

```bash
neuro-align --ephys neuropixels.dat --video behavior.mp4 --fmri sub-01_bold.nii.gz --time 2.5
```

**Applying Data Filters:**

Isolate specific signals during initialization to drop low-value data from RAM early:

```bash
neuro-align --ephys neuropixels.dat --video behavior.mp4 --time 2.5 --filter "signal > 0.8"
```

## Testing

This project enforces strict validation for its synchronization logic. Run the automated test suite locally:

```bash
pytest tests/
```

```bash
neuro-align --help
```
