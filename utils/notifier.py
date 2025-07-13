# utils/notifier.py
from playsound import playsound
from pathlib import Path
import threading

def _play_sound_async():
    """Função interna para tocar o som em uma thread separada."""
    try:
        # Constroi o caminho do arquivo de som de forma compatível com múltiplos sistemas
        sound_file = Path(__file__).parent / "chime-alert-demo-309545.mp3"
        playsound(str(sound_file))
    except Exception as e:
        print(f"Erro ao tocar o som: {e}")

def send_warning():
    """
    Inicia a reprodução do som de alerta em uma nova thread para não bloquear
    o programa principal.
    """
    print("⚠️ Alerta: Postura inadequada detectada por um período prolongado.")
    # Cria e inicia uma nova thread para tocar o som
    sound_thread = threading.Thread(target=_play_sound_async)
    sound_thread.start()