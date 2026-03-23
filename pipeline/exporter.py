import h5py
import os
import logging


class Hdf5Exporter:
    """
    Serializes synchronized multimodal data chunks into HDF5 format
    for downstream machine learning pipelines (e.g., PyTorch/TensorFlow).
    """

    def __init__(self, output_filename="neuro_sync_output.h5"):
        self.output_filename = output_filename
        self.logger = logging.getLogger("Hdf5Exporter")

    def export_sync_data(self, time_sec, ephys_idx, video_frame, fmri_tr=None):
        self.logger.info(
            f"Exporting synchronized slice at T={time_sec}s to {self.output_filename}"
        )

        # Open an HDF5 file in write ('w') mode
        with h5py.File(self.output_filename, "w") as hf:
            # 1. Create a metadata group
            meta_group = hf.create_group("metadata")
            meta_group.create_dataset("sync_time_seconds", data=time_sec)

            # 2. Create the data pointers
            hf.create_dataset("ephys_sync_index", data=ephys_idx)
            hf.create_dataset("video_sync_frame", data=video_frame)

            if fmri_tr is not None:
                hf.create_dataset("fmri_sync_volume", data=fmri_tr)

        self.logger.info("Export complete. Data is ready for downstream AI ingestion.")
