import mmap
import numpy as np
import os
from pipeline.base_loader import BaseNeuroLoader


class EphysLoader(BaseNeuroLoader):
    """
    A specialized loader for Electrophysiology data using high-speed Memory Mapping.
    """

    def __init__(self, file_path, dataset_name, sampling_rate, num_channels):
        super().__init__(file_path, dataset_name)
        self.sampling_rate = sampling_rate
        self.num_channels = num_channels
        self._mmap_obj = None  # We will store the memory map here

    def load_data(self):
        print(f"[{self.dataset_name}] Initializing Zero-Copy Memory Mapping...")

        # 1. Safety Check: Does the file exist?
        if not os.path.exists(self.file_path):
            print(f"[{self.dataset_name}] Error: File not found at {self.file_path}")
            return

        # 2. Open the file in Read-Binary ("rb") mode
        with open(self.file_path, "rb") as f:
            # 3. Create the Memory Map! (length=0 means map the whole file)
            self._mmap_obj = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

            # 4. Zero-Copy Magic: We tell NumPy to look at the first 400 bytes
            # of the memory map and treat them as 100 32-bit floats.
            # NumPy does NOT copy this data; it just points to the mmap!
            raw_bytes = self._mmap_obj[:400]
            data_array = np.frombuffer(raw_bytes, dtype=np.float32)

            self.is_loaded = True
            print(
                f"[{self.dataset_name}] Successfully mapped {len(self._mmap_obj)} bytes to virtual memory."
            )
            print(
                f"[{self.dataset_name}] Zero-copy preview of first 5 signals: {data_array[:5]}"
            )

            # Close it up when we are done previewing
            self._mmap_obj.close()
