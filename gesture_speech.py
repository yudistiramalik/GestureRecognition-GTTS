import cv2
import mediapipe as mp
from gtts import gTTS
from io import BytesIO
import pygame
import time
import threading

# Inisialisasi pygame mixer
pygame.mixer.init()

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Setup kamera dengan resolusi default (ukuran penuh webcam)
cap = cv2.VideoCapture(0)

gesture_dict = {
    "halo": "Halo!",
    "perkenalan": "Perkenalkan, saya Yudistira",
    "salam": "Salam kenal",
    "terima": "Terimakasih, sampai jumpa"
}

last_gesture = None
last_speak_time = 0
speak_interval = 5  # detik waktu minimal bicara ulang gesture sama
frame_count = 0
last_hand_landmarks = None

def count_fingers(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tips_ids[i]].y < hand_landmarks.landmark[tips_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def speak_thread(text, lang='id'):
    def run():
        try:
            mp3_fp = BytesIO()
            tts = gTTS(text=text, lang=lang)
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            pygame.mixer.music.load(mp3_fp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"Error during speech synthesis: {e}")

    threading.Thread(target=run, daemon=True).start()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_count += 1
    gesture_text = None

    # Deteksi gesture tiap 3 frame agar performa optimal
    if frame_count % 3 == 0:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            last_hand_landmarks = result.multi_hand_landmarks[0]

            finger_count = count_fingers(last_hand_landmarks)
            if finger_count == 1:
                gesture_text = "halo"
            elif finger_count == 2:
                gesture_text = "perkenalan"
            elif finger_count == 5:
                gesture_text = "terima"
            else:
                gesture_text = "salam"
        else:
            last_hand_landmarks = None
            gesture_text = None

    # Gambar garis jari di semua frame dari hasil landmark terakhir
    if last_hand_landmarks:
        mp_draw.draw_landmarks(frame, last_hand_landmarks, mp_hands.HAND_CONNECTIONS)

    current_time = time.time()

    if gesture_text:
        print("Gesture terdeteksi:", gesture_text)

    # Bicara dan update gesture terakhir jika gesture baru atau waktu interval tercapai
    if gesture_text is not None and ((gesture_text != last_gesture) or (current_time - last_speak_time > speak_interval)):
        if gesture_text in gesture_dict:
            print("Mengucapkan:", gesture_dict[gesture_text])
            speak_thread(gesture_dict[gesture_text])
            last_gesture = gesture_text
            last_speak_time = current_time

    # Tampilkan teks gesture terakhir agar teks tampil stabil tanpa kedap-kedip
    if last_gesture in gesture_dict:
        cv2.putText(frame, gesture_dict[last_gesture], (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Speech", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
