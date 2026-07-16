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

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Camera opened:", cap.isOpened())
success, frame = cap.read()
print("Frame:", success)

# -----------------------------
# Gesture Stability Variables
# -----------------------------
current_gesture = ""
last_spoken = ""

gesture_start_time = 0

STABILITY_TIME = 0.5

while True:

    success, frame = cap.read()

    if not success:
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

    # -----------------------------
    # Display Gesture
    # -----------------------------
    cv2.putText(
        frame,
        f"Gesture : {current_gesture}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        3
    )

    cv2.imshow("Sign to Speech", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()