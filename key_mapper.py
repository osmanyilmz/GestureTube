import pyautogui
import time
import ws_server

class KeyMapper:
    def __init__(self):
        self.last_gesture = None
        self.last_press_time = 0
        self.cooldown = 1.5  # jest başına bekleme süresi (saniye)

    def press(self, gesture):
        now = time.time()

        # Cooldown dolmadan hiçbir jest kabul etme (aynı veya farklı)
        if now - self.last_press_time < self.cooldown:
            return

        # Aynı jest tekrar gelirse basma
        if gesture == self.last_gesture:
            return

        self.last_gesture = gesture
        self.last_press_time = now
        key = self.gesture_key_map.get(gesture)

        if key:
            pyautogui.press(key)
            ws_server.broadcast(gesture, key)
            print(f"\r{gesture}  →  [{key.upper()}] basıldı   ", end="", flush=True)