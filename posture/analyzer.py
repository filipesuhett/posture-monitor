import cv2
from utils.geometry import find_distance, find_angle
import mediapipe as mp

def analyze_posture(frame, landmarks, w, h, args, font, fps, good_frames, bad_frames, base_neck_angle=None, base_torso_angle=None):
    pose_landmark = mp.solutions.pose.PoseLandmark

    def get_coords(point):
        return int(landmarks.landmark[point].x * w), int(landmarks.landmark[point].y * h)

    l_shldr_x, l_shldr_y = get_coords(pose_landmark.LEFT_SHOULDER)
    r_shldr_x, r_shldr_y = get_coords(pose_landmark.RIGHT_SHOULDER)
    l_ear_x, l_ear_y = get_coords(pose_landmark.LEFT_EAR)
    l_hip_x, l_hip_y = get_coords(pose_landmark.LEFT_HIP)

    offset = find_distance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
    
    neck_angle = find_angle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
    torso_angle = find_angle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

    good = False
    
    # Verifica se a postura base foi capturada
    if base_neck_angle is not None and base_torso_angle is not None:
        # Define a faixa de tolerância para o pescoço (base +/- 10)
        neck_threshold_min = base_neck_angle - 10
        neck_threshold_max = base_neck_angle + 10
        
        # Define a faixa de tolerância para o tronco (base +/- 10)
        torso_threshold_min = base_torso_angle - 10
        torso_threshold_max = base_torso_angle + 10

        # A postura é "boa" se ambos os ângulos estiverem dentro de suas respectivas faixas
        if (neck_threshold_min < neck_angle < neck_threshold_max) and \
           (torso_threshold_min < torso_angle < torso_threshold_max):
            good = True
    else:
        # Lógica original se nenhuma postura base for definida, usando os valores fixos
        if neck_angle < args.neck_angle_threshold and torso_angle < args.torso_angle_threshold:
            good = True

    color = (127, 233, 100) if good else (0, 0, 255)

    good_frames = good_frames + 1 if good else 0
    bad_frames = bad_frames + 1 if not good else 0

    cv2.putText(frame, f"Neck Inclination: {neck_angle}", (10, 30), font, 0.6, color, 2)
    cv2.putText(frame, f"Torso Inclination: {torso_angle}", (10, 60), font, 0.6, color, 2)
    cv2.putText(frame, f"{'Good' if good else 'Bad'} Posture Time: {round((good_frames if good else bad_frames)/fps, 1)}s",
                (10, h - 20), font, 0.9, color, 2)

    cv2.putText(frame, f"{int(offset)} Shoulder " + ("aligned" if offset < args.offset_threshold else "not aligned"),
                (w - 280, 30), font, 0.6, (0, 255, 0) if offset < args.offset_threshold else (0, 0, 255), 2)

    return frame, (good_frames, bad_frames), neck_angle, torso_angle