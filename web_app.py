from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import base64
import mediapipe as mp
from utils.geometry import find_distance, find_angle
from utils.notifier import send_warning
from posture.analyzer import analyze_posture
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

class Args:
    def __init__(self):
        self.offset_threshold = 10
        self.time_threshold = 3
        self.neck_angle_threshold = 30
        self.torso_angle_threshold = 20

camera = None
camera_thread = None
is_camera_running = False
args = Args()

base_neck_angle = None
base_torso_angle = None
last_known_neck_angle = None
last_known_torso_angle = None
capture_lock = threading.Lock()

def generate_frames():
    global camera, is_camera_running, base_neck_angle, base_torso_angle
    global last_known_neck_angle, last_known_torso_angle
    
    pose = mp.solutions.pose.Pose()
    good_frames = bad_frames = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    fps = 30

    while is_camera_running:
        ret, frame = camera.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            analyzed_frame, status, current_neck_angle, current_torso_angle = analyze_posture(
                frame, results.pose_landmarks, w, h, args, font, fps, good_frames, bad_frames, base_neck_angle, base_torso_angle
            )
            good_frames, bad_frames = status

            with capture_lock:
                last_known_neck_angle = current_neck_angle
                last_known_torso_angle = current_torso_angle

            if (bad_frames / fps) >= args.time_threshold:
                send_warning()
            
            frame_to_send = analyzed_frame
        else:
            frame_to_send = frame

        _, buffer = cv2.imencode('.jpg', frame_to_send)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('video_frame', {'frame': frame_base64})

        time.sleep(1/30) 

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global camera, camera_thread, is_camera_running
    
    if camera is None:
        camera = cv2.VideoCapture(0)
        is_camera_running = True
        camera_thread = threading.Thread(target=generate_frames)
        camera_thread.start()

@socketio.on('disconnect')
def handle_disconnect():
    global camera, is_camera_running
    
    is_camera_running = False
    if camera is not None:
        camera.release()
        camera = None

@socketio.on('capture_base_posture')
def capture_base_posture():
    """
    Captura a postura base usando os últimos ângulos conhecidos pelo
    loop de geração de frames, garantindo consistência com o que o usuário vê.
    """
    global base_neck_angle, base_torso_angle, last_known_neck_angle, last_known_torso_angle
    
    with capture_lock:
        if last_known_neck_angle is not None and last_known_torso_angle is not None:
            base_neck_angle = last_known_neck_angle
            base_torso_angle = last_known_torso_angle

            socketio.emit('base_posture_set', {'neck_angle': base_neck_angle, 'torso_angle': base_torso_angle})
            print(f"Base posture set: Neck Angle={base_neck_angle}, Torso Angle={base_torso_angle}")

if __name__ == '__main__':
    socketio.run(app, debug=True)