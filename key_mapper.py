import pyautogui
from config import GESTURE_KEY_MAP

class KeyMapper:
    def __init__(self):
        self.last_gesture = None

    def press(self, gesture):
        if gesture == self.last_gesture:
            return  # Aynı jesti tekrar tetikleme
        
        self.last_gesture = gesture
        key = GESTURE_KEY_MAP.get(gesture)
        
        if key:
            pyautogui.press(key)
            print(f"✅ Jest: {gesture} → Tuş: {key}")