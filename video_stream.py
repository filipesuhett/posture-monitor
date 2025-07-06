import cv2
import mediapipe as mp
from utils.geometry import find_distance, find_angle
from utils.notifier import send_warning
from posture.analyzer import analyze_posture

def run_posture_monitor(args):
    cap = cv2.VideoCapture(int(args.video) if args.video is not None and args.video.isdigit() else args.video or 0)
    pose = mp.solutions.pose.Pose()
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    good_frames = bad_frames = 0
    font = cv2.FONT_HERSHEY_SIMPLEX

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or cannot access webcam.")
            break

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            frame, status = analyze_posture(
                frame, results.pose_landmarks, w, h, args, font, fps, good_frames, bad_frames
            )
            good_frames, bad_frames = status

            if (bad_frames / fps) >= args.time_threshold:
                send_warning()

        cv2.imshow("Posture Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
