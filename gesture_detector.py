import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

class GestureDetector:
    def __init__(self):
        model_path = "hand_landmarker.task"
        
        # Modeli indir (yoksa)
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

    def classify_gesture(self, landmarks):
        index_up = landmarks[8].y < landmarks[6].y
        middle_up = landmarks[12].y < landmarks[10].y

        if index_up and not middle_up:
            return "index_up"
        elif not index_up and not middle_up:
            return "fist"
        elif index_up and middle_up:
            return "two_fingers"
        else:
            return "open_hand"