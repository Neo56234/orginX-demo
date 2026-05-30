import logging
import os
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from app.config import get_settings

logger = logging.getLogger("originx.services.card_generator")

CARD_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;700&family=Inter:wght@400;700&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1080px; height: 1080px; background: #0A0E1A; color: #E8ECF7; font-family: 'Inter', sans-serif; overflow: hidden; }
  .top { position: relative; height: 540px; }
  .thumbnail { width: 100%; height: 100%; object-fit: cover; opacity: 0.6; }
  .false-label {
    position: absolute; top: 32px; left: 32px;
    background: #FF3B5C; color: white;
    font-size: 28px; font-weight: 700;
    padding: 8px 24px; border-radius: 6px;
    font-family: 'Noto Sans Bengali', sans-serif;
  }
  .bottom { padding: 40px; height: 540px; display: flex; flex-direction: column; gap: 24px; background: #13192A; }
  .headline { font-family: 'Noto Sans Bengali', sans-serif; font-size: 36px; font-weight: 700; color: #FF3B5C; line-height: 1.3; }
  .subheadline { font-family: 'Noto Sans Bengali', sans-serif; font-size: 24px; color: #E8ECF7; line-height: 1.5; }
  .evidence { font-family: 'Noto Sans Bengali', sans-serif; font-size: 18px; color: #8B95A9; line-height: 1.5; border-left: 3px solid #3D8BFF; padding-left: 16px; }
  .footer { margin-top: auto; display: flex; align-items: center; justify-content: space-between; }
  .brand { font-size: 20px; font-weight: 700; color: #3D8BFF; letter-spacing: 0.05em; }
  .tagline { font-family: 'Noto Sans Bengali', sans-serif; font-size: 14px; color: #5A6378; }
</style>
</head>
<body>
  <div class="top">
    {% if thumbnail_url %}
    <img class="thumbnail" src="{{ thumbnail_url }}" />
    {% endif %}
    <div class="false-label">মিথ্যা প্রসঙ্গ</div>
  </div>
  <div class="bottom">
    <div class="headline">{{ headline_bn }}</div>
    <div class="subheadline">{{ subheadline_bn }}</div>
    <div class="evidence">{{ evidence_snippet_bn }}</div>
    <div class="footer">
      <div>
        <div class="brand">OriginX</div>
        <div class="tagline">প্রতিটি ভিডিওর আসল উৎস আছে। আমরা খুঁজে দিই।</div>
      </div>
    </div>
  </div>
</body>
</html>"""


def generate_card(
    investigation_id: str,
    headline_bn: str,
    subheadline_bn: str,
    evidence_snippet_bn: str,
    thumbnail_url: Optional[str] = None,
) -> Optional[str]:
    """
    Generate a 1080×1080 counter-narrative card PNG using Playwright.
    Returns absolute path to the PNG file, or None on failure.

    Phase 1 implementation:
    - Render CARD_TEMPLATE to HTML string with Jinja2
    - Launch Playwright Chromium headless
    - Set viewport 1080×1080
    - Screenshot → save to {DATA_DIR}/cards/{investigation_id}.png
    - Return file path
    """
    settings = get_settings()
    os.makedirs(settings.cards_dir, exist_ok=True)
    out_path = os.path.join(settings.cards_dir, f"{investigation_id}.png")

    # ── Phase 1: uncomment and test ────────────────────────────────────────
    try:
        from playwright.sync_api import sync_playwright
        from jinja2 import Template
    
        html = Template(CARD_TEMPLATE).render(
            headline_bn=headline_bn,
            subheadline_bn=subheadline_bn,
            evidence_snippet_bn=evidence_snippet_bn,
            thumbnail_url=thumbnail_url,
        )
    
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path="/usr/bin/chromium")
            page = browser.new_page(viewport={"width": 1080, "height": 1080})
            page.set_content(html, wait_until="networkidle")
            page.screenshot(path=out_path, full_page=False)
            browser.close()
    
        logger.info("Counter card generated: %s", out_path)
        return out_path
    except Exception as e:
        logger.error("Card generation failed: %s", e)
        return None
    # ──────────────────────────────────────────────────────────────────────
