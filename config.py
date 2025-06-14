import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description="Posture Monitor with MediaPipe")
    parser.add_argument("--video", type=str, default=None, help="Video path or webcam index (default webcam).")
    parser.add_argument("--offset-threshold", type=int, default=100, help="Shoulder alignment threshold.")
    parser.add_argument("--neck-angle-threshold", type=int, default=32, help="Neck angle threshold.")
    parser.add_argument("--torso-angle-threshold", type=int, default=32, help="Torso angle threshold.")
    parser.add_argument("--time-threshold", type=int, default=180, help="Bad posture alert threshold (s).")
    return parser.parse_args()
