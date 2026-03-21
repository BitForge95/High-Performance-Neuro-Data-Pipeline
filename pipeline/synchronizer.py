class DataSynchronizer:
    """
    Aligns multimodal datasets (e.g., High-speed Ephys and Behavioral Video)
    based on a common time axis.
    """

    def __init__(self, ephys_loader, video_loader):
        # We pass the ENTIRE objects into this manager
        self.ephys = ephys_loader
        self.video = video_loader

    def get_data_at_time(self, time_in_seconds):
        """
        Calculates the exact array index and video frame for a given timestamp.
        """
        print(f"\n--- [Synchronizer] Aligning data at T = {time_in_seconds}s ---")

        # 1. Calculate the Ephys Index
        # If sampling at 30,000 Hz, 2 seconds in is index 60,000
        ephys_index = int(time_in_seconds * self.ephys.sampling_rate)

        # 2. Calculate the Video Frame
        # If recording at 60 FPS, 2 seconds in is frame 120
        video_frame = int(time_in_seconds * self.video.fps)

        print(f" -> {self.ephys.dataset_name} Index: {ephys_index}")
        print(f" -> {self.video.dataset_name} Frame: {video_frame}")

        return ephys_index, video_frame
