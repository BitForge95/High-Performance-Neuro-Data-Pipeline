import numpy as np
import os
from pipeline.ephys_loader import EphysLoader
from pipeline.video_loader import VideoLoader

# --- SETUP: GENERATE A FAKE NEUROPIXELS DATASET ---
print("--- GENERATING FAKE NEUROPIXELS DATA ---")
fake_file_path = "fake_neuropixels.dat"
# Generate 1000 random floating-point numbers (simulating brain signals)
fake_data = np.random.rand(1000).astype(np.float32)
fake_data.tofile(fake_file_path)  # Save directly to disk
print(f"Created {fake_file_path} ({os.path.getsize(fake_file_path)} bytes)\n")


# --- RUN THE PIPELINE ---
# 1. Instantiate loaders (pointing EphysLoader to our new real file)
allen_ephys = EphysLoader(
    file_path=fake_file_path,
    dataset_name="Neuropixels_Probe_A",
    sampling_rate=30000,
    num_channels=384,
)

behavior_cam = VideoLoader(
    file_path="/data/mouse_treadmill.mp4",  # We leave this fake for now
    dataset_name="Treadmill_Camera",
    fps=60,
    resolution="1920x1080",
)

experiment_datasets = [allen_ephys, behavior_cam]

for dataset in experiment_datasets:
    dataset.load_data()
    print("-" * 30)
