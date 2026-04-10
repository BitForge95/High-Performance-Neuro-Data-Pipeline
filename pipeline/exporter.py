import os
import json
import logging
import numpy as np


class NumpyExporter:
    """
    Serializes synchronized multimodal data chunks into thread-safe .npy format
    for downstream machine learning pipelines (e.g., PyTorch/TensorFlow).
    """

    def __init__(self, output_dir="neuro_sync_output"):
        self.output_dir = output_dir
        self.logger = logging.getLogger("NumpyExporter")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export_sync_data(self, time_sec, ephys_idx, video_frame, fmri_tr=None):
        self.logger.info(
            f"Exporting synchronized slice at T={time_sec}s to {self.output_dir}/"
        )

        # 1. Save timestamps as a separate .npy file (Sensorium standard)
        timestamp_array = np.array([time_sec], dtype=np.float32)
        np.save(os.path.join(self.output_dir, "timestamps.npy"), timestamp_array)

        # 2. Save the data pointers as parallel-friendly .npy arrays
        np.save(
            os.path.join(self.output_dir, "ephys_sync_index.npy"),
            np.array([ephys_idx], dtype=np.int64),
        )
        np.save(
            os.path.join(self.output_dir, "video_sync_frame.npy"),
            np.array([video_frame], dtype=np.int64),
        )

        # 3. Create a metadata group for the JSON manifest
        meta_dict = {"sync_time_seconds": time_sec}

        if fmri_tr is not None:
            np.save(
                os.path.join(self.output_dir, "fmri_sync_volume.npy"),
                np.array([fmri_tr], dtype=np.int64),
            )
            meta_dict["fmri_sync_volume"] = fmri_tr

        # Save JSON manifest
        with open(os.path.join(self.output_dir, "manifest.json"), "w") as f:
            json.dump(meta_dict, f, indent=4)

        self.logger.info("Export complete. Data is ready for downstream AI ingestion.")
