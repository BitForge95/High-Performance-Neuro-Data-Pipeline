import os
import json
import logging
import torch
import numpy as np
from torch.utils.data import Dataset

logger = logging.getLogger("NeuroAlignDataset")


class NeuroAlignDataset(Dataset):
    """
    Native PyTorch Dataset for Experanto and OmniMouse ingestion.
    Reads thread-safe .npy pointers using zero-copy memory mapping
    to bypass RAM limits and libhdf5 locks.
    """

    def __init__(self, data_dir="neuro_sync_output"):
        self.data_dir = data_dir

        # We need this to ensure the downstream ML model knows the global state (like fMRI TRs)
        manifest_path = os.path.join(data_dir, "manifest.json")
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(
                f"Oops! No manifest found at {manifest_path}. Did the exporter run?"
            )

        with open(manifest_path, "r") as f:
            self.metadata = json.load(f)

        # By using mmap_mode='r' (read-only), we tell the OS: "Don't load this file into RAM, just give me a map to the hard drive." This is exactly what prevents the pipeline from crashing when dealing with massive datasets, and allows PyTorch multiprocessing.
        try:
            self.timestamps = np.load(
                os.path.join(data_dir, "timestamps.npy"), mmap_mode="r"
            )
            self.ephys_indices = np.load(
                os.path.join(data_dir, "ephys_sync_index.npy"), mmap_mode="r"
            )
            self.video_frames = np.load(
                os.path.join(data_dir, "video_sync_frame.npy"), mmap_mode="r"
            )

            # Safely handle fMRI if it exists in the output folder (since it was optional in the CLI)
            self.fmri_volumes = None
            fmri_path = os.path.join(data_dir, "fmri_sync_volume.npy")
            if os.path.exists(fmri_path):
                self.fmri_volumes = np.load(fmri_path, mmap_mode="r")

        except Exception as e:
            logger.error(f"Failed to memory-map the .npy arrays: {e}")
            raise

        logger.info(
            f"Dataset initialized successfully with {len(self.timestamps)} synchronized slices."
        )

    def __len__(self):
        # PyTorch DataLoaders call this function to know exactly how many batches they can create. It just returns the total number of timestamps.
        return len(self.timestamps)

    def __getitem__(self, idx):
        """
        Fetches the synchronized data pointers for a specific time index.
        Returns a dictionary of PyTorch tensors ready for the GPU.
        """
        # PyTorch's background CPU workers will call this function thousands of times a second.
        # We slice the memory-mapped arrays at the exact index [idx], and instantly cast them into PyTorch Tensors so OmniMouse can read them.

        sample = {
            # float32 is the standard for PyTorch neural network inputs
            "timestamp": torch.tensor(self.timestamps[idx], dtype=torch.float32),
            # Indices/pointers are always integers, so we use torch.long
            "ephys_index": torch.tensor(self.ephys_indices[idx], dtype=torch.long),
            "video_frame": torch.tensor(self.video_frames[idx], dtype=torch.long),
        }

        if self.fmri_volumes is not None:
            sample["fmri_volume"] = torch.tensor(
                self.fmri_volumes[idx], dtype=torch.long
            )

        return sample
