from pipeline.base_loader import BaseNeuroLoader


class VideoLoader(BaseNeuroLoader):
    """
    A specialized loader for behavioural video data.
    """

    def __init__(self, file_path, dataset_name, fps, resolution):
        super().__init__(file_path, dataset_name)
        self.fps = fps
        self.resolution = resolution

    def load_data(self):
        print(
            f"[{self.dataset_name}] Video Load: Decoding {self.resolution} frames at {self.fps} FPS..."
        )
