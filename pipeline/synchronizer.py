class DataSynchronizer:
    """
    Aligns multimodal datasets based on a common time axis.

    This manager coordinates between high-frequency electrophysiology
    loaders and lower-frequency behavioral video loaders to find
    corresponding data indices for specific events.

    Parameters
    ----------
    ephys_loader : EphysLoader
        An instantiated loader containing electrophysiology data.
    video_loader : VideoLoader
        An instantiated loader containing behavioral video data.
    """

    def __init__(self, ephys_loader, video_loader):
        self.ephys = ephys_loader
        self.video = video_loader

    def get_data_at_time(self, time_in_seconds):
        """
        Calculates the exact array index and video frame for a given timestamp.

        Parameters
        ----------
        time_in_seconds : float
            The timestamp of the event to align, measured in seconds from
            the start of the recording.

        Returns
        -------
        tuple of int
            A tuple containing (ephys_index, video_frame).
            - ephys_index: The array index in the electrophysiology data.
            - video_frame: The corresponding frame number in the video data.
        """
        print(f"\n--- [Synchronizer] Aligning data at T = {time_in_seconds}s ---")

        ephys_index = int(time_in_seconds * self.ephys.sampling_rate)
        video_frame = int(time_in_seconds * self.video.fps)

        print(f" -> {self.ephys.dataset_name} Index: {ephys_index}")
        print(f" -> {self.video.dataset_name} Frame: {video_frame}")

        return ephys_index, video_frame
