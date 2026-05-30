// OriginX Background Service Worker

chrome.runtime.onInstalled.addListener(() => {
  console.log("OriginX extension installed.");
});

// Handle messages from content script or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "CHECK_URL") {
    const apiUrl = `http://localhost:8000/api/cases?q=${encodeURIComponent(request.url)}`;
    fetch(apiUrl)
      .then((r) => r.json())
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true; // keep message channel open for async
  }
});
