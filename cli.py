import argparse
import os
import numpy as np
from pipeline.ephys_loader import EphysLoader
from pipeline.video_loader import VideoLoader
from pipeline.synchronizer import DataSynchronizer


def main():
    parser = argparse.ArgumentParser(
        description="ExpAlign: High-Performance Neuro-Data Pipeline"
    )

    parser.add_argument(
        "--ephys",
        type=str,
        required=True,
        help="Path to the electrophysiology data file",
    )
    parser.add_argument(
        "--video", type=str, required=True, help="Path to the behavioral video file"
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

    if not os.path.exists(args.ephys):
        print(f"Generating dummy ephys data at {args.ephys} for CLI test...")
        np.random.rand(1000).astype(np.float32).tofile(args.ephys)

    print("\n" + "=" * 40)
    print(" EXPERANTO MULTIMODAL CLI PIPELINE")
    print("=" * 40)

    allen_ephys = EphysLoader(args.ephys, "CLI_Ephys_Dataset", 30000, 384)
    behavior_cam = VideoLoader(args.video, "CLI_Video_Dataset", 60, "1920x1080")

    allen_ephys.load_data(filter_rule=args.filter)
    behavior_cam.load_data()

    sync_engine = DataSynchronizer(allen_ephys, behavior_cam)
    sync_engine.get_data_at_time(args.time)

    print("=" * 40 + "\n")


if __name__ == "__main__":
    main()
