from pipeline.base_loader import BaseNeuroLoader


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
