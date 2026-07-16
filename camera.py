import cv2
import mediapipe as mp
import time

from speech import speak
from gesture_recognition import recognize_gesture

# -----------------------------
# Initialize MediaPipe
# -----------------------------
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# -----------------------------
# Gesture Variables
# -----------------------------
current_gesture = ""
last_spoken = ""
gesture_start_time = 0

STABILITY_TIME = 0.5


def generate_frames():

    global current_gesture
    global last_spoken
    global gesture_start_time

    # Open camera every time streaming starts
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Unable to open camera")
        return

    while True:

        success, frame = cap.read()

        if not success:
            print("❌ Failed to read frame")
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        detected_gesture = "Unknown"

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                landmarks = hand_landmarks.landmark

                detected_gesture = recognize_gesture(landmarks)

        # -----------------------------
        # Gesture Stability
        # -----------------------------
        if detected_gesture != current_gesture:

            current_gesture = detected_gesture
            gesture_start_time = time.time()

        else:

            elapsed = time.time() - gesture_start_time

            if (
                elapsed >= STABILITY_TIME
                and current_gesture != "Unknown"
                and current_gesture != last_spoken
            ):

                speak(current_gesture)
                last_spoken = current_gesture

        if detected_gesture == "Unknown":
            last_spoken = ""

        # Display Gesture
        cv2.putText(
            frame,
            f"Gesture : {current_gesture}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

    cap.release()