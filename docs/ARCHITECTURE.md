# NeuroAlign Architecture & System Design

This document outlines the core architectural decisions, memory management strategies, and mathematical synchronization systems that power the NeuroAlign pipeline.

## System Overview

NeuroAlign is designed to solve the out-of-core memory bottleneck inherent in modern neuroinformatics. The system is built on a rigid object-oriented contract that separates data loading, data filtering, temporal synchronization, and serialization into distinct, highly optimized modules.

The pipeline follows a strict unidirectional data flow:
1. Lazy Initialization (Zero-Copy Mappings)
2. Dynamic Pre-Filtering
3. Temporal Index Calculation
4. Array Slicing
5. HDF5 Serialization

## Core Components

### 1. The Zero-Copy Data Loaders
Standard Python data pipelines fail when attempting to load terabyte-scale electrophysiology data into RAM. NeuroAlign mitigates this through OS-level memory management.

All data loaders inherit from the `BaseNeuroLoader` Abstract Base Class, ensuring a unified interface for the synchronizer.

* **EphysLoader (Neuropixels):** Utilizes `numpy.memmap` to create a virtual pointer to binary `.dat` files on the hard drive. Data is never loaded into RAM until an explicit temporal slice is requested.
* **VideoLoader:** Leverages chunked decoding to read frames on demand, bypassing the need to hold entire `.mp4` arrays in memory.
* **BidsNiftiLoader (fMRI):** Implements `nibabel` proxy objects to lazily load 4D NIfTI arrays. It includes an automated JSON parser to extract the `RepetitionTime` (TR) metadata required for temporal math.

### 2. The Dynamic Filter Engine
To further reduce the memory footprint before synchronization, NeuroAlign implements an object composition pattern for dynamic filtering.

Instead of writing custom Python loops, users pass a string-based rule (e.g., `signal > 0.8`). The `StringFilterEngine` dynamically parses this condition and applies it directly to the memory-mapped arrays using vectorized NumPy operations. Irrelevant data points are dropped immediately, reducing the array size passed to the synchronizer.

### 3. The Temporal Synchronizer
The `DataSynchronizer` is the mathematical core of the pipeline. It maps disparate hardware sampling rates onto a unified, continuous event timeline.

Given a target time `T` (in seconds):
* **Ephys Index Calculation:** `target_index = int(T * ephys_sample_rate)` (e.g., 2.5s * 30,000 Hz = Index 75,000).
* **Video Frame Calculation:** `target_frame = int(T * video_fps)` (e.g., 2.5s * 60 FPS = Frame 150).
* **fMRI Volume Calculation:** `target_volume = int(T / TR_time)` (e.g., 2.5s / 2.0s TR = Volume 1).

The synchronizer calculates these overlaps in milliseconds and requests only the specific array slices from the zero-copy loaders.

### 4. Handling BIDS Edge Cases
The pipeline includes strict safety constraints for neuroimaging metadata. Standard continuous alignment relies heavily on a fixed TR. However, in sparse acquisition paradigms, the `RepetitionTime` may be undefined. 

The `BidsNiftiLoader` explicitly checks for missing TR values during initialization. If a sparse acquisition is detected, the pipeline safely halts and raises a descriptive `ValueError` to prevent silent mathematical drift downstream, adhering to BIDS Specification 1.11.1.

### 5. HDF5 Serialization
Deep learning frameworks like PyTorch and TensorFlow require highly structured, serialized data. Once the multimodal slices are aligned, the `Hdf5Exporter` groups them into a single, compressed `.h5` file. 

This creates a seamless bridge between raw, unstructured laboratory hardware data and high-performance ML ingestion pipelines like OmniMouse.