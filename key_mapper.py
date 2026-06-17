import pyautogui
import time
import ws_server

class KeyMapper:
    def __init__(self):
        self.last_gesture = None
        self.last_press_time = 0
        self.cooldown = 1.0
        self.gesture_key_map = {}

    def press(self, gesture):
        now = time.time()

        if gesture == self.last_gesture:
            return
        if now - self.last_press_time < self.cooldown:
            return

        self.last_gesture = gesture
        self.last_press_time = now
        key = self.gesture_key_map.get(gesture)

        if key:
            pyautogui.press(key)
            ws_server.broadcast(gesture, key)
            print(f"\r{gesture}  →  [{key.upper()}] basıldı   ", end="", flush=True)