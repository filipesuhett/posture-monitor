from playsound import playsound

def send_warning():
    print("⚠️ Warning: Bad posture detected for extended period.")
    playsound("utils\chime-alert-demo-309545.mp3")


