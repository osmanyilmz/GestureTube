# 🎮 YouTube Gesture Controller

Control YouTube with your hand gestures using your webcam! Play, pause, adjust volume, and more — all without touching your keyboard.

> 🇹🇷 Türkçe açıklama aşağıda bulunmaktadır.

---

## 🎯 Gestures

| Gesture | Action |
|---------|--------|
| ☝️ Index finger | Play / Pause |
| ✌️ Two fingers | Rewind 10s |
| 🤘 Horns | Forward 10s |
| 🖐️ Open hand | Mute |
| ✊ Fist | Fullscreen |
| 👍 Thumbs up | Volume Up |
| 👎 Thumbs down | Volume Down |

---

## 📦 Installation

### 1. Download GestureController.exe

Go to the **Releases** section on the right and download `GestureController.exe`.

### 2. Install the Chrome Extension

1. Download this repo as ZIP → **Code → Download ZIP**
2. Extract the ZIP
3. Open Chrome and go to `chrome://extensions`
4. Enable **Developer mode** in the top right
5. Click **Load unpacked**
6. Select the `chrome-extension` folder from the extracted files

---

## 🚀 How to Use

1. Run `GestureController.exe`
2. The camera window and browser dashboard will open automatically
3. Open a YouTube video in Chrome
4. Show your hand gestures to the camera!

> ⚠️ GestureController.exe must be running while you use YouTube.

---

## ⚙️ Customizing Gestures

In the browser dashboard, go to the **⚙️ Settings** tab to:
- Assign different keys to gestures
- Remove gestures you don't need
- Add new gesture mappings
- Changes are saved automatically

---

## 🛠️ Developer Setup

If you want to run the source code directly:

### Requirements

- Python 3.10+
- Webcam

### Setup

```bash
# Clone the repo
git clone https://github.com/osmanyilmz/CameraMotion.git
cd CameraMotion

# Install dependencies
pip install opencv-python mediapipe==0.10.33 pyautogui pynput websockets

# Run
python main.py
```

### Build EXE yourself

```bash
pip install pyinstaller

python -m PyInstaller --onefile --noconsole --name GestureController --add-data "templates;templates" --add-data "gesture_config.json;." --add-data "hand_landmarker.task;." main.py
```

---

## 📁 Project Structure