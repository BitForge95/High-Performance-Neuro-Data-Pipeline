import argparse
import os
import numpy as np
from pipeline.ephys_loader import EphysLoader
from pipeline.video_loader import VideoLoader
from pipeline.synchronizer import DataSynchronizer
from pipeline.nifti_loader import BidsNiftiLoader


def main():
    parser = argparse.ArgumentParser(
        description="ExpAlign: High-Performance Neuro-Data Pipeline"
    )

    parser.add_argument(
        "--ephys",
        type=str,
        required=False,
        help="Path to the electrophysiology data file",
    )
    parser.add_argument(
        "--video", type=str, required=False, help="Path to the behavioral video file"
    )
    parser.add_argument(
        "--fmri", type=str, required=False, help="Path to the BIDS NIfTI file"
    )

    parser.add_argument(
        "--time", type=float, required=True, help="Timestamp in seconds to align"
    )
    parser.add_argument(
        "--filter",
        type=str,
        default=None,
        help="Optional string-based filter (e.g., 'signal > 0.5')",
    )

    args = parser.parse_args()

    print("\n" + "=" * 40)
    print(" EXPERANTO MULTIMODAL CLI PIPELINE")
    print("=" * 40)

    ephys_loader = None
    video_loader = None

    if args.ephys:
        if not os.path.exists(args.ephys):
            print(f"Generating dummy ephys data at {args.ephys} for CLI test...")
            np.random.rand(1000).astype(np.float32).tofile(args.ephys)

        ephys_loader = EphysLoader(args.ephys, "CLI_Ephys_Dataset", 30000, 384)
        ephys_loader.load_data(filter_rule=args.filter)

    if args.video:
        video_loader = VideoLoader(args.video, "CLI_Video_Dataset", 60, "1920x1080")
        video_loader.load_data()

    if args.fmri:
        print("\n--- Initializing BIDS fMRI Pipeline ---")
        bids_scan = BidsNiftiLoader(args.fmri, "CLI_fMRI_Dataset")
        bids_scan.load_data(filter_rule=args.filter)

    if ephys_loader and video_loader:
        sync_engine = DataSynchronizer(ephys_loader, video_loader)
        sync_engine.get_data_at_time(args.time)

    print("=" * 40 + "\n")


if __name__ == "__main__":
    main()
