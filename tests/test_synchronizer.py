from pipeline.ephys_loader import EphysLoader
from pipeline.video_loader import VideoLoader
from pipeline.synchronizer import DataSynchronizer


def test_synchronizer_math():
    """
    Tests if the DataSynchronizer accurately aligns timestamps
    between disparate sampling rates.
    """
    # 1. SETUP: Create "dummy" objects just for their metadata
    dummy_ephys = EphysLoader(
        "dummy.dat", "Ephys", sampling_rate=30000, num_channels=384
    )
    dummy_video = VideoLoader("dummy.mp4", "Video", fps=60, resolution="1920x1080")

    # Pass them into our manager
    sync_engine = DataSynchronizer(dummy_ephys, dummy_video)

    # 2. EXECUTE: Run the method we want to test at T = 1.5 seconds
    ephys_idx, video_frame = sync_engine.get_data_at_time(1.5)

    # 3. ASSERT: Demand that the math is perfectly accurate
    # 30,000 * 1.5 = 45,000
    assert ephys_idx == 45000, f"Math failed! Expected 45000, got {ephys_idx}"

    # 60 * 1.5 = 90
    assert video_frame == 90, f"Math failed! Expected 90, got {video_frame}"
