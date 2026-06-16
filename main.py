import cv2
import webbrowser
import os
import ws_server
from gesture_detector import GestureDetector
from key_mapper import KeyMapper

detector = GestureDetector()
mapper = KeyMapper()

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

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    landmarks = detector.detect(rgb)

    if landmarks:
        gesture = detector.classify_gesture(landmarks)

        if gesture:
            mapper.press(gesture)
            labels = {
                "index_up":   "OYNAT / DURAKLAT",
                "thumb_up":   "OYNAT / DURAKLAT",
                "two_fingers":"10sn GERI",
                "horns":      "10sn ILERI",
                "open_hand":  "SES KAPAT",
                "fist":       "TAM EKRAN",
                "thumb_down": "CIKIS",
            }
            label = labels.get(gesture, gesture.replace("_", " "))
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