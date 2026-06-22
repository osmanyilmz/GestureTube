const GESTURE_INFO = {
  'index_up':   '☝️ işaret parmağı',
  'two_fingers':'✌️ iki parmak',
  'horns':      '🤘 horns',
  'open_hand':  '🖐️ açık el',
  'fist':       '✊ yumruk',
  'thumb_up':   '👍 başparmak yukarı',
  'thumb_down': '👎 başparmak aşağı',
};

// Varsayılan config'i hemen göster
const defaultConfig = {
  'index_up':    'space',
  'two_fingers': 'j',
  'horns':       'l',
  'open_hand':   'm',
  'fist':        'f',
  'thumb_up':    'up',
  'thumb_down':  'down',
};
renderList(defaultConfig);

// Storage'dan config yükle
chrome.storage.local.get('gesture_config', (data) => {
  if (data.gesture_config) renderList(data.gesture_config);
});

// YouTube sekmesine bağlantı durumunu sor
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  if (!tabs[0]) {
    setStatus(false);
    return;
  }

  // Sekme YouTube değilse direkt false göster
  if (!tabs[0].url || !tabs[0].url.includes('youtube.com')) {
    setStatus(false, 'YouTube sekmesi açık değil');
    return;
  }

  chrome.tabs.sendMessage(tabs[0].id, { type: 'get_status' }, (res) => {
    if (chrome.runtime.lastError || !res) {
      setStatus(false);
      return;
    }
    setStatus(res.connected);
  });
});

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'connection') setStatus(msg.status);
});

function setStatus(active, customText) {
  document.getElementById('dot').classList.toggle('active', active);
  const text = document.getElementById('status-text');
  if (customText) {
    text.textContent = customText;
  } else {
    text.textContent = active ? "Python'a bağlı ✓" : 'Python çalışmıyor';
  }
  text.classList.toggle('active', active);
}

function renderList(config) {
  const list = document.getElementById('gesture-list');
  list.innerHTML = Object.entries(config).map(([gesture, key]) => `
    <div class="gesture-item">
      <span class="gesture-name">${GESTURE_INFO[gesture] || gesture}</span>
      <span class="gesture-key">${key.toUpperCase()}</span>
    </div>
  `).join('');
}