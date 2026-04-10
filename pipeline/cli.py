import argparse
import os
import logging
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ExpAlignCLI")

from .ephys_loader import EphysLoader
from .video_loader import VideoLoader
from .synchronizer import DataSynchronizer
from .nifti_loader import BidsNiftiLoader
from .exporter import NumpyExporter


def main():
    parser = argparse.ArgumentParser(
        description="NeuroAlign: High-Performance Neuro-Data Pipeline"
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

    logger.info("Starting NeuroAlign Multimodal Pipeline")

    ephys_loader = None
    video_loader = None

    if args.ephys:
        if not os.path.exists(args.ephys):
            logger.warning(
                f"Generating dummy ephys data at {args.ephys} for CLI test..."
            )
            np.random.rand(1000).astype(np.float32).tofile(args.ephys)
        ephys_loader = EphysLoader(args.ephys, "CLI_Ephys_Dataset", 30000, 384)
        ephys_loader.load_data(filter_rule=args.filter)

    if args.video:
        video_loader = VideoLoader(args.video, "CLI_Video_Dataset", 60, "1920x1080")
        video_loader.load_data()

    if args.fmri:
        logger.info("Initializing BIDS fMRI Pipeline")
        bids_scan = BidsNiftiLoader(args.fmri, "CLI_fMRI_Dataset")
        bids_scan.load_data(filter_rule=args.filter)

    if ephys_loader and video_loader:
        sync_engine = DataSynchronizer(ephys_loader, video_loader)
        ephys_idx, video_frame = sync_engine.get_data_at_time(args.time)

        exporter = NumpyExporter()
        exporter.export_sync_data(
            time_sec=args.time, ephys_idx=ephys_idx, video_frame=video_frame
        )

    logger.info("Pipeline Execution Finished Successfully.")


if __name__ == "__main__":
    main()
