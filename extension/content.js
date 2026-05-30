// OriginX Content Script
// Scans Facebook feed for known fake-context videos and overlays warnings.

const ORIGINX_API = "http://localhost:3000";

// Known fake video signatures (URL fragments or identifiers)
// Update this list with your demo video IDs before the hackathon
const KNOWN_FAKE_SIGNATURES = [
  "1001", "1002", "1003", "1004", "1005",
  "1006", "1007", "1008", "1009", "1010",
];

const PROCESSED = new WeakSet();

function isFakeVideo(url) {
  if (!url) return false;
  return KNOWN_FAKE_SIGNATURES.some((sig) => url.includes(sig));
}

function createWarningOverlay(investigationId) {
  const overlay = document.createElement("div");
  overlay.dataset.originxOverlay = "true";
  overlay.style.cssText = `
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(255, 59, 92, 0.92);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    backdrop-filter: blur(4px);
    cursor: pointer;
  `;

  overlay.innerHTML = `
    <div style="font-size:24px;margin-bottom:6px">⚠️</div>
    <div style="
      color: white;
      font-weight: 900;
      font-size: 13px;
      font-family: monospace;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    ">মিথ্যা প্রসঙ্গ সনাক্ত</div>
    <div style="
      color: rgba(255,255,255,0.85);
      font-size: 10px;
      font-family: monospace;
      margin-bottom: 8px;
    ">FALSE CONTEXT DETECTED</div>
    <div style="
      background: rgba(255,255,255,0.2);
      color: white;
      font-size: 10px;
      font-family: monospace;
      padding: 3px 8px;
      border-radius: 100px;
      border: 1px solid rgba(255,255,255,0.4);
    ">Powered by OriginX ✕</div>
  `;

  if (investigationId) {
    overlay.addEventListener("click", (e) => {
      e.stopPropagation();
      window.open(`${ORIGINX_API}/investigation/${investigationId}`, "_blank");
    });
    const badge = document.createElement("div");
    badge.style.cssText = `
      margin-top: 6px;
      color: rgba(255,255,255,0.7);
      font-size: 9px;
      font-family: monospace;
    `;
    badge.textContent = "Click to view investigation →";
    overlay.appendChild(badge);
  } else {
      overlay.addEventListener("click", (e) => {
        e.stopPropagation();
        overlay.style.display = "none";
      });
  }

  return overlay;
}

function createCheckButton(videoElement, url) {
  const btn = document.createElement("button");
  btn.style.cssText = `
    position: absolute;
    bottom: 8px;
    right: 8px;
    background: rgba(13, 25, 42, 0.9);
    border: 1px solid #3D8BFF;
    color: #3D8BFF;
    font-family: monospace;
    font-size: 10px;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 100px;
    cursor: pointer;
    z-index: 9998;
    letter-spacing: 0.05em;
    backdrop-filter: blur(4px);
  `;
  btn.textContent = "ORIGINX CHECK";
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const encodedUrl = encodeURIComponent(url || window.location.href);
    window.open(`${ORIGINX_API}/?url=${encodedUrl}`, "_blank");
  });
  return btn;
}

function processVideoContainers() {
  // Find video elements
  const videos = document.querySelectorAll("video");

  videos.forEach((video) => {
    if (PROCESSED.has(video)) return;
    PROCESSED.add(video);

    // Find parent container to overlay on
    let container = video.closest('[data-video-id]') ||
                    video.closest('.x1cy8zhl') ||   // FB video container class
                    video.parentElement?.parentElement;

    if (!container) return;

    // Make container relative for absolute positioning
    const existingPosition = window.getComputedStyle(container).position;
    if (existingPosition === "static") {
      container.style.position = "relative";
    }

    // Check current page URL and video src for known fakes
    const pageUrl = window.location.href;
    const videoSrc = video.src || video.currentSrc || "";

    if (isFakeVideo(pageUrl) || isFakeVideo(videoSrc)) {
      const overlay = createWarningOverlay(null);
      container.appendChild(overlay);
    } else {
      // Add "Check with OriginX" button
      const btn = createCheckButton(video, pageUrl);
      container.appendChild(btn);
    }
  });
}

// Initial scan
processVideoContainers();

// Watch for dynamically loaded videos (infinite scroll)
const observer = new MutationObserver(() => {
  processVideoContainers();
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});
