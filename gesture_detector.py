import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

class GestureDetector:
    def __init__(self):
        model_path = "hand_landmarker.task"
        if not os.path.exists(model_path):
            print("📥 Model indiriliyor...")
            urllib.request.urlretrieve(
                "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
                model_path
            )
            print("✅ Model indirildi!")

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.7
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        result = self.detector.detect(mp_image)
        if result.hand_landmarks:
            return result.hand_landmarks[0]
        return None

    def is_finger_up(self, landmarks, tip, dip, pip):
        return landmarks[tip].y < landmarks[dip].y and landmarks[tip].y < landmarks[pip].y

    def classify_gesture(self, landmarks):
        index_up  = self.is_finger_up(landmarks, 8,  7,  6)
        middle_up = self.is_finger_up(landmarks, 12, 11, 10)
        ring_up   = self.is_finger_up(landmarks, 16, 15, 14)
        pinky_up  = self.is_finger_up(landmarks, 20, 19, 18)

        thumb_tip  = landmarks[4]
        thumb_ip   = landmarks[3]
        thumb_mcp  = landmarks[2]
        index_mcp  = landmarks[5]
        middle_mcp = landmarks[9]

        fingers_up_count = sum([index_up, middle_up, ring_up, pinky_up])

        # Başparmak yönü — diğer parmaklardan bağımsız net kontrol
        thumb_up_clear   = (thumb_tip.y < thumb_mcp.y - 0.08)
        thumb_down_clear = (thumb_tip.y > thumb_mcp.y + 0.08)

        # Yumruk — tüm parmaklar kapalı VE başparmak yatay/içeride
        # başparmak ucu orta parmak MCP'sinden aşağıda olmalı
        thumb_tucked = thumb_tip.y > index_mcp.y

        # 👍 Başparmak yukarı — sadece 4 parmak kapalı ve başparmak net yukarı
        if thumb_up_clear and fingers_up_count == 0:
            return "thumb_up"

        # 👎 Başparmak aşağı — sadece 4 parmak kapalı ve başparmak net aşağı
        if thumb_down_clear and fingers_up_count == 0:
            return "thumb_down"

        # ✊ Yumruk — tüm parmaklar kapalı VE başparmak içeride/yatay
        if fingers_up_count == 0 and thumb_tucked and not thumb_up_clear and not thumb_down_clear:
            return "fist"

        # 🖐️ Açık el — 4 parmak açık
        if fingers_up_count >= 4:
            return "open_hand"

        # ☝️ Sadece işaret parmağı
        if index_up and not middle_up and not ring_up and not pinky_up:
            return "index_up"

        # ✌️ İki parmak
        if index_up and middle_up and not ring_up and not pinky_up:
            return "two_fingers"

        # 🤘 Horns (işaret + serçe) — call me yerine
        if index_up and pinky_up and not middle_up and not ring_up:
            return "horns"

        return None