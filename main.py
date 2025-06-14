from config import get_arguments
from video_stream import run_posture_monitor

if __name__ == "__main__":
    args = get_arguments()
    run_posture_monitor(args)
