import subprocess
import sys

def start_recognition():
    subprocess.Popen([sys.executable, "hand_detection.py"])