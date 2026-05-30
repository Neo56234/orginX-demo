// Query active tab for flagged video count
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const tab = tabs[0];
  if (tab?.url?.includes("facebook.com")) {
    // Count overlays injected by content script
    chrome.scripting
      .executeScript({
        target: { tabId: tab.id },
        func: () =>
          document.querySelectorAll('[data-originx-overlay]').length,
      })
      .then((results) => {
        const count = results?.[0]?.result ?? 0;
        const el = document.getElementById("flaggedCount");
        if (el) {
          el.textContent = count > 0 ? `${count} ভিডিও` : "কোনোটা নয়";
          el.className = count > 0 ? "status-value" : "status-value green";
        }
      })
      .catch(() => {
        const el = document.getElementById("flaggedCount");
        if (el) el.textContent = "N/A";
      });
  } else {
    const el = document.getElementById("flaggedCount");
    if (el) el.textContent = "FB only";
  }
});
