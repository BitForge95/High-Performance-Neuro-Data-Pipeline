import os
import json
import nibabel as nib
from pipeline.base_loader import BaseNeuroLoader
from pipeline.filter_engine import StringFilterEngine


class BidsNiftiLoader(BaseNeuroLoader):
    """
    A specialized loader for BIDS-compliant fMRI NIfTI datasets.
    """

    def __init__(self, file_path, dataset_name):
        super().__init__(file_path, dataset_name)
        self.tr_time = None  # Repetition Time (fMRI's version of sampling rate)

        # COMPOSITION: Plug in the filter engine we built earlier!
        self.filter_engine = StringFilterEngine()

    def _parse_bids_metadata(self):
        """
        Automatically extracts RepetitionTime (TR) from the BIDS sidecar JSON.
        This proves domain expertise in the Brain Imaging Data Structure (BIDS) standard.
        """
        # A valid BIDS NIfTI (sub-01_task-rest_bold.nii.gz) always has a matching JSON
        base_name = self.file_path.replace(".nii.gz", "").replace(".nii", "")
        json_path = f"{base_name}.json"

        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                metadata = json.load(f)
                # Safely extract the TR time
                self.tr_time = metadata.get("RepetitionTime", None)
                print(
                    f"[{self.dataset_name}] BIDS Metadata automatically parsed. TR = {self.tr_time}s"
                )
        else:
            print(
                f"[{self.dataset_name}] Warning: No BIDS sidecar JSON found at {json_path}"
            )

    def load_data(self, filter_rule=None):
        if not os.path.exists(self.file_path):
            print(f"[{self.dataset_name}] Error: File not found at {self.file_path}")
            return

        # 1. Auto-extract the sampling rate from the JSON sidecar
        self._parse_bids_metadata()

        # 2. Load the data using Nibabel's memory-efficient proxy objects
        print(
            f"[{self.dataset_name}] Loading NIfTI image via Nibabel proxy to save RAM..."
        )
        img = nib.load(self.file_path)

        # fMRI is 4D data: (X, Y, Z, Time)
        print(f"[{self.dataset_name}] 4D Image shape (X, Y, Z, Time): {img.shape}")
        self.is_loaded = True

        # 3. Apply the custom Experanto string filter if provided
        if filter_rule:
            print(
                f"[{self.dataset_name}] Fetching full data array into RAM for filtering..."
            )
            # Note: getting full data of a 4D fMRI is heavy, but required for global filtering
            data_array = img.get_fdata()
            filtered_data = self.filter_engine.apply_filter(data_array, filter_rule)
            print(
                f"[{self.dataset_name}] Filtered data size: {filtered_data.size} points."
            )
