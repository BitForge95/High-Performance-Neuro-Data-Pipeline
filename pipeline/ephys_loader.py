from pipeline.base_loader import BaseNeuroLoader


# Here Ephys stands for electrophysiology
class EphysLoader(BaseNeuroLoader):
    """
    A specialized loader for Electrophysiology data (like Neuropixels).
    and Inherits from BaseNeuroLoader.
    """

    def __init__(self, file_path, dataset_name, sampling_rate, num_channels):
        super().__init__(file_path, dataset_name)

        self.sampling_rate = sampling_rate
        self.num_channels = num_channels

    def display_ephys_info(self):
        print(
            f"[{self.dataset_name}] Ephys Data: {self.num_channels} channels: {self.sampling_rate}Hz"
        )

    def load_data(self):
        print(
            f"[{self.dataset_name}] High-Speed Load: Fetching {self.num_channels} channels using Zero-Copy Memory Mapping"
        )
