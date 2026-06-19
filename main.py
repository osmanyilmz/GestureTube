import cv2
import webbrowser
import os
import json
import ws_server
from gesture_detector import GestureDetector
from key_mapper import KeyMapper

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "gesture_config.json")

DEFAULT_CONFIG = {
    "index_up":    "space",
    "two_fingers": "j",
    "horns":       "l",
    "open_hand":   "m",
    "fist":        "f",
    "thumb_up":    "up",
    "thumb_down":  "down",
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

detector = GestureDetector()
mapper = KeyMapper()
config = load_config()
mapper.gesture_key_map = config
ws_server.set_config(config)

ws_server.run_in_background()

html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
webbrowser.open("file://" + os.path.abspath(html_path))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # ← küçük çözünürlük
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)            # ← FPS sabitle

print("🎬 YouTube Gesture Controller başlatıldı.")
print("🌐 Tarayıcı arayüzü açıldı.")
print("📷 Kamera aktif — çıkmak için 'q' tuşuna bas.\n")

frame_skip = 0  # Her frame'i değil, atlamalı işle

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if ws_server.pending_config:
        new_config = ws_server.pending_config
        ws_server.pending_config = None
        mapper.gesture_key_map = new_config
        ws_server.set_config(new_config)
        save_config(new_config)
        print(f"\n✅ Config güncellendi: {new_config}")

    frame = cv2.flip(frame, 1)

    # Her 2 frame'den birini işle — CPU yükünü yarıya indirir
    frame_skip += 1
    if frame_skip % 2 == 0:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks = detector.detect(rgb)

        if landmarks:
            gesture = detector.classify_gesture(landmarks)
            if gesture:
                mapper.press(gesture)
            else:
                mapper.last_gesture = None
        else:
            mapper.last_gesture = None

    cv2.imshow("YouTube Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()