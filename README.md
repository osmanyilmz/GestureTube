# 🎮 YouTube Gesture Controller

Control YouTube with your hand gestures using your webcam! Play, pause, adjust volume, and more — all without touching your keyboard.

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
git clone https://github.com/YOUR_USERNAME/CameraMotion.git
cd CameraMotion

# Install dependencies
pip install opencv-python mediapipe==0.10.33 pyautogui pynput websockets

# Run
python main.py
```

### Build EXE yourself

```bash
pip install pyinstaller

python -m PyInstaller --onefile --noconsole --name GestureController \
  --add-data "templates;templates" \
  --add-data "gesture_config.json;." \
  --add-data "hand_landmarker.task;." \
  main.py
```

---

## 📁 Project Structure
CameraMotion/

├── main.py               # Main application

├── gesture_detector.py   # Hand gesture detection (MediaPipe)

├── key_mapper.py         # Gesture → Key mapping

├── ws_server.py          # WebSocket server

├── gesture_config.json   # Saved settings

├── templates/

│   └── index.html        # Browser dashboard

└── chrome-extension/     # Chrome extension

├── manifest.json

├── content.js

├── background.js

├── popup.html

└── popup.js

//TURKCE
# 🎮 YouTube Gesture Controller

Elinizin hareketlerini kullanarak YouTube'u kontrol edin! Kamera karşısında el jestleri yaparak video oynatma, durdurma, ses ayarlama ve daha fazlasını yapabilirsiniz.

---

## 🎯 Özellikler

| Jest | Eylem |
|------|-------|
| ☝️ İşaret parmağı | Oynat / Duraklat |
| ✌️ İki parmak | 10sn Geri Al |
| 🤘 Horns | 10sn İleri Al |
| 🖐️ Açık el | Sesi Kapat |
| ✊ Yumruk | Tam Ekran |
| 👍 Başparmak yukarı | Sesi Artır |
| 👎 Başparmak aşağı | Sesi Azalt |

---

## 📦 Kurulum

### 1. GestureController.exe'yi İndir

Sağ taraftaki **Releases** bölümünden `GestureController.exe` dosyasını indirin.

### 2. Chrome Eklentisini Kur

1. Bu repoyu ZIP olarak indirin → **Code → Download ZIP**
2. ZIP'i çıkartın
3. Chrome'da `chrome://extensions` adresine gidin
4. Sağ üstten **Geliştirici modu**'nu açın
5. **Paketlenmemiş öğe yükle** butonuna tıklayın
6. İndirdiğiniz klasörün içindeki `chrome-extension` klasörünü seçin

---

## 🚀 Kullanım

1. `GestureController.exe` dosyasını çalıştırın
2. Kamera penceresi ve tarayıcı arayüzü otomatik açılır
3. Chrome'da bir YouTube videosu açın
4. El hareketlerinizi kameraya gösterin!

> ⚠️ GestureController.exe çalışırken YouTube sekmesi aktif olmalıdır.

---

## ⚙️ Jest Ayarları

Tarayıcıda açılan arayüzden **⚙️ Ayarlar** sekmesine giderek:
- Jestlere farklı tuşlar atayabilirsiniz
- İstemediğiniz jestleri kaldırabilirsiniz  
- Yeni jest ekleyebilirsiniz
- Değişiklikler otomatik kaydedilir

---

## 🛠️ Geliştirici Kurulumu

Kodu kendiniz çalıştırmak istiyorsanız:

### Gereksinimler

- Python 3.10+
- Webcam

### Kurulum

```bash
# Repoyu klonlayın
git clone https://github.com/osmanyilmz/CameraMotion.git
cd CameraMotion

# Kütüphaneleri kurun
pip install opencv-python mediapipe==0.10.33 pyautogui pynput websockets

# Çalıştırın
python main.py
```

---

