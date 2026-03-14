from pipeline.base_loader import BaseNeuroLoader
from pipeline.ephys_loader import EphysLoader
from pipeline.video_loader import VideoLoader


allen_data = BaseNeuroLoader(
    file_path="/simulated/path/mouse_visual_cortex.nwb",
    dataset_name="Allen_Neuropixels_Probe_A",
)

bwm_data = BaseNeuroLoader(
    file_path="/simulated/path/brain_wide_map_subject1.h5",
    dataset_name="Brain_Wide_Map_Trial_1",
)

print("\nLoading First Dataset")
allen_data.display_info()

print("\nLoading Second Dataset")
bwm_data.display_info()

allen_ephys = EphysLoader(
    file_path="/simulated/path/mouse_visual_cortex.nwb",
    dataset_name="Allen_Neuropixels_Probe_A",
    sampling_rate=30000,
    num_channels=384,
)

allen_ephys.display_info()

allen_ephys.display_ephys_info()

behaviour_cam = VideoLoader(
    file_path="/data/mouse_threadmill.mp4",
    dataset_name="Threadmill_Cam_recordings",
    fps=60,
    resolution="1920x1080",
)

experiment_datasets = [behaviour_cam, allen_ephys]

print("Start Pipleine")

for dataset in experiment_datasets:
    dataset.load_data()

print("ENd Pipeline")
