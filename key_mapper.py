import pyautogui
import time
from config import GESTURE_KEY_MAP
import ws_server

class KeyMapper:
    def __init__(self):
        self.last_gesture = None
        self.last_press_time = 0
        self.cooldown = 1.0

    def press(self, gesture):
        now = time.time()

        if gesture == self.last_gesture:
            return
        if now - self.last_press_time < self.cooldown:
            return

        self.last_gesture = gesture
        self.last_press_time = now
        key = GESTURE_KEY_MAP.get(gesture)

        if key:
            pyautogui.press(key)
            ws_server.broadcast(gesture, key)

            symbols = {
                "index_up":   "☝️  işaret parmağı  → Oynat/Duraklat",
                "thumb_up":   "👍  başparmak yukarı → Oynat/Duraklat",
                "two_fingers":"✌️  iki parmak       → 10sn Geri",
                "horns":      "🤘  horns            → 10sn İleri",
                "open_hand":  "🖐️  açık el          → Ses Kapat",
                "fist":       "✊  yumruk           → Tam Ekran",
                "thumb_down": "👎  başparmak aşağı  → Tam Ekrandan Çık",
            }
            label = symbols.get(gesture, gesture)
            print(f"\r{label}   ", end="", flush=True)