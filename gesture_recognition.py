def recognize_gesture(landmarks):

    # ---------- Finger States ----------
    thumb_up = landmarks[4].x < landmarks[3].x

    index_up = landmarks[8].y < landmarks[6].y
    middle_up = landmarks[12].y < landmarks[10].y
    ring_up = landmarks[16].y < landmarks[14].y
    pinky_up = landmarks[20].y < landmarks[18].y

    # ---------- STOP ----------
    if index_up and middle_up and ring_up and pinky_up:
        return "STOP"

    # ---------- HELP ----------
    if index_up and not middle_up and not ring_up and not pinky_up:
        return "HELP"

    # ---------- PEACE ----------
    if index_up and middle_up and not ring_up and not pinky_up:
        return "PEACE"

    # ---------- YES ----------
    if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        return "YES"

    # ---------- THANK YOU ----------
    if not thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        return "THANK YOU"

    return "Unknown"