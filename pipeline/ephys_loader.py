import mmap
import numpy as np
import os
from pipeline.base_loader import BaseNeuroLoader
from pipeline.filter_engine import StringFilterEngine


class EphysLoader(BaseNeuroLoader):
    def __init__(self, file_path, dataset_name, sampling_rate, num_channels):
        super().__init__(file_path, dataset_name)
        self.sampling_rate = sampling_rate
        self.num_channels = num_channels
        self._mmap_obj = None

        # COMPOSITION: We plug the FilterEngine into this loader!
        self.filter_engine = StringFilterEngine()

    def load_data(self, filter_rule=None):
        print(f"[{self.dataset_name}] Initializing Zero-Copy Memory Mapping...")

        if not os.path.exists(self.file_path):
            print(f"[{self.dataset_name}] Error: File not found at {self.file_path}")
            return

        with open(self.file_path, "rb") as f:
            self._mmap_obj = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

            raw_bytes = self._mmap_obj[:400]
            data_array = np.frombuffer(raw_bytes, dtype=np.float32)
            self.is_loaded = True

            print(f"[{self.dataset_name}] Raw data preview: {data_array[:5]}")

            if filter_rule:
                data_array = self.filter_engine.apply_filter(data_array, filter_rule)
                print(f"[{self.dataset_name}] Filtered data preview: {data_array[:5]}")

            self._mmap_obj.close()
