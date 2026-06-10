import cv2
from gesture_detector import GestureDetector
from key_mapper import KeyMapper

detector = GestureDetector()
mapper = KeyMapper()

cap = cv2.VideoCapture(0)  # 0 = varsayılan kamera

print("🎯 Gesture Controller başlatıldı. Çıkmak için 'q'")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Ayna görüntüsü
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    landmarks = detector.detect(rgb)
    
    if landmarks:
        gesture = detector.classify_gesture(landmarks)
        mapper.press(gesture)
        cv2.putText(frame, f"Jest: {gesture}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()