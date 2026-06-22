// Eklenti yüklendiğinde content script'i aktifleştir
chrome.runtime.onInstalled.addListener(() => {
  console.log('[Gesture] Eklenti yüklendi');
});