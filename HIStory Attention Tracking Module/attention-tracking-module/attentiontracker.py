import threading
import time
import dlib
import cv2
from PIL import Image
from imutils import face_utils
from facepose import Facepose
from utils import *
from utils import rec_to_roi_box

#Model
p = "../model/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

LOST_FOCUS_THRESHOLD = 10 #Time threshold in seconds to increment the count of being distracted
MINIGAME_THRESHOLD = 3 #Threshold for distraction counts to trigger minigame
POWERUP_THRESHOLD = 3 #Threshold for focused counts to trigger power-up

_state = {
    'lostFocusCount': 0,
    'lostFocusDuration': 0.0,
    'focusedCount': 0,
    'isDistracted': False,
    'facePresent': False,
    'facePos': None,
    'triggerMinigame': False,
    'triggerPowerup': False,
    'frame': None,
}
_running = False

#Return webcam frame
def get_frame():
    return _state['frame']

#Read and clear the current attention state every loop
def get_attention_state():
    state = _state.copy()
    _state['triggerMinigame'] = False
    _state['triggerPowerup'] = False
    return state

#Start attention tracking
def start_attention_monitor():
    global _running
    _running = True
    threading.Thread(target=_monitor_loop, daemon=True).start()

#Stop attention tracking
def stop_attention_monitor():
    global _running
    _running = False

#Attention tracking based on face angle detection
def _monitor_loop():
    cap = cv2.VideoCapture(0)

    lostFocusDuration = 0.0
    focusedTime = 0.0
    focusTimer = None
    focusedTimer = None
    lostFocusCount = 0
    focusedCount = 0

    frame_rate_use = 5
    prev = 0
    yaw_predicted = None
    facepose = Facepose()

    while cap.isOpened() and _running:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        _state['frame'] = frame

        time_elapsed = time.time() - prev
        if time_elapsed < 1. / frame_rate_use:
            continue

        prev = time.time()
        facePresent = False
        facePos = None

        rects = detector(gray, 0)
        for (_, rect) in enumerate(rects):
            facePresent = True
            facePos = (rect.left(), rect.top(), rect.width(), rect.height())
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            roi_box, _, _ = rec_to_roi_box(rect)
            roi_img = crop_img(frame, roi_box)
            (yaw_predicted, _, _) = facepose.predict(Image.fromarray(roi_img))

        isDistracted = (not facePresent) or (
            yaw_predicted is not None and
            (yaw_predicted.item() < -30 or yaw_predicted.item() > 30)
        )

        if isDistracted:
            if focusTimer is None:
                focusTimer = time.time()
            lostFocusDuration += time.time() - focusTimer
            focusTimer = time.time()
            focusedTimer = None

            if lostFocusDuration >= LOST_FOCUS_THRESHOLD:
                lostFocusCount += 1
                lostFocusDuration = 0.0

                if lostFocusCount >= MINIGAME_THRESHOLD:
                    _state['triggerMinigame'] = True
                    lostFocusCount = 0

        else:
            focusTimer = None
            lostFocusDuration = 0.0
            if focusedTimer is None:
                focusedTimer = time.time()
            focusedTime += time.time() - focusedTimer
            focusedTimer = time.time()

            if focusedTime >= LOST_FOCUS_THRESHOLD:
                focusedCount += 1
                focusedTime = 0.0
                if lostFocusCount > 0:
                    lostFocusCount -= 1
                if focusedCount % POWERUP_THRESHOLD == 0:
                    _state['triggerPowerup'] = True

        #Sync all states
        _state['lostFocusCount'] = lostFocusCount
        _state['lostFocusDuration'] = lostFocusDuration
        _state['focusedCount'] = focusedCount
        _state['isDistracted'] = isDistracted
        _state['facePresent'] = facePresent
        _state['facePos'] = facePos

    cap.release()