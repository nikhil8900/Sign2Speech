import pyttsx3
import threading

def _speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

def speak(text):
    thread = threading.Thread(target=_speak, args=(text,))
    thread.daemon = True
    thread.start()