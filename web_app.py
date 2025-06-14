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

# Classe para simular os argumentos
class Args:
    def __init__(self):
        self.offset_threshold = 10
        self.time_threshold = 5
        self.neck_angle_threshold = 30
        self.torso_angle_threshold = 20

# Variáveis globais para controle da câmera
camera = None
camera_thread = None
is_camera_running = False
args = Args()

def generate_frames():
    global camera, is_camera_running
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
            frame, status = analyze_posture(
                frame, results.pose_landmarks, w, h, args, font, fps, good_frames, bad_frames
            )
            good_frames, bad_frames = status

            if (bad_frames / fps) > args.time_threshold:
                send_warning()

        # Converte o frame para base64 para transmissão via WebSocket
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('video_frame', {'frame': frame_base64})

        time.sleep(1/30)  # Limita a 30 FPS

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

if __name__ == '__main__':
    socketio.run(app, debug=True) 