import cv2
import webbrowser
import os
import json
import ws_server
from gesture_detector import GestureDetector
from key_mapper import KeyMapper

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "gesture_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "index_up":   "space",
        "two_fingers": "j",
        "horns":      "l",
        "open_hand":  "m",
        "fist":       "f",
        "thumb_up":   "up",
        "thumb_down": "down",
    }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

detector = GestureDetector()
mapper = KeyMapper()
mapper.gesture_key_map = load_config()

ws_server.run_in_background()

html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
webbrowser.open("file://" + os.path.abspath(html_path))

cap = cv2.VideoCapture(0)

print("🎬 YouTube Gesture Controller başlatıldı.")
print("🌐 Tarayıcı arayüzü açıldı.")
print("📷 Kamera aktif — çıkmak için 'q' tuşuna bas.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Tarayıcıdan gelen config güncellemelerini kontrol et
    if ws_server.pending_config:
        new_config = ws_server.pending_config
        ws_server.pending_config = None
        mapper.gesture_key_map = new_config
        save_config(new_config)
        print(f"\n✅ Config güncellendi: {new_config}")

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    landmarks = detector.detect(rgb)

    if landmarks:
        gesture = detector.classify_gesture(landmarks)

        if gesture:
            mapper.press(gesture)
            labels = {
                "index_up":   "OYNAT / DURAKLAT",
                "two_fingers":"10sn GERI",
                "horns":      "10sn ILERI",
                "open_hand":  "SES KAPAT",
                "fist":       "TAM EKRAN",
                "thumb_up":   "SES ARTIR",
                "thumb_down": "SES AZALT",
            }
            label = labels.get(gesture, gesture.replace("_", " ").upper())
            cv2.putText(frame, label, (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (93, 202, 165), 2)
        else:
            mapper.last_gesture = None
            cv2.putText(frame, "...", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)
    else:
        mapper.last_gesture = None

    cv2.imshow("YouTube Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()