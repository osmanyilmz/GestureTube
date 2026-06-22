let ws = null;
let connected = false;
let reconnectTimer = null;

function connect() {
  ws = new WebSocket('ws://localhost:5678');

  ws.onopen = () => {
    connected = true;
    console.log('[Gesture] Bağlandı');
    chrome.runtime.sendMessage({ type: 'connection', status: true }).catch(() => {});
  };

  ws.onclose = () => {
    connected = false;
    console.log('[Gesture] Bağlantı kesildi, yeniden deneniyor...');
    chrome.runtime.sendMessage({ type: 'connection', status: false }).catch(() => {});
    clearTimeout(reconnectTimer);
    reconnectTimer = setTimeout(connect, 2000);
  };

  ws.onerror = () => {
    ws.close();
  };

  ws.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);

      if (!window.location.href.includes('youtube.com/watch')) return;

      if (data.type === 'gesture' && data.key) {
        pressKey(data.key);
        console.log(`[Gesture] ${data.gesture} → ${data.key}`);
      }
    } catch (err) {
      console.error('[Gesture] Mesaj hatası:', err);
    }
  };
}

function pressKey(key) {
  const keyMap = {
    'space': ' ',
    'up':    'ArrowUp',
    'down':  'ArrowDown',
    'left':  'ArrowLeft',
    'right': 'ArrowRight',
    'f':     'f',
    'j':     'j',
    'k':     'k',
    'l':     'l',
    'm':     'm',
    'c':     'c',
    'esc':   'Escape',
  };

  const mappedKey = keyMap[key.toLowerCase()] || key;

  const player = document.querySelector('.html5-video-player');
  if (player) player.focus();

  const event = new KeyboardEvent('keydown', {
    key: mappedKey,
    code: mappedKey,
    bubbles: true,
    cancelable: true,
  });

  document.dispatchEvent(event);

  const video = document.querySelector('video');
  if (video) video.dispatchEvent(event);
}

// Popup'tan gelen mesajları dinle — Promise döndür
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'get_status') {
    sendResponse({ connected });
    return true; // ← async response için gerekli
  }
});

connect();