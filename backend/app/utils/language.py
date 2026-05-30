from typing import Optional
from datetime import date as date_type


# Bengali digit → ASCII digit mapping
_BENGALI_TO_ASCII = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')


def normalize_bengali_numerals(text: str) -> str:
    """Convert Bengali digit characters (০-৯) to ASCII digits (0-9)."""
    return text.translate(_BENGALI_TO_ASCII)


def extract_claimed_date(text: str) -> Optional[date_type]:
    """
    Extract a claimed date from user-supplied context text.
    Handles Bengali numerals, standalone 4-digit years, and common separators.
    Returns a date or None.
    """
    import re
    if not text:
        return None

    normalized = normalize_bengali_numerals(text)

    # Full date: YYYY-MM-DD or YYYY/MM/DD
    m = re.search(r'(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})', normalized)
    if m:
        try:
            return date_type(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass

    # Full date: DD/MM/YYYY or DD-MM-YYYY
    m = re.search(r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})', normalized)
    if m:
        try:
            return date_type(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass

    # Standalone 4-digit year in range 1900-2099 (e.g., "২০২৬" → "2026")
    m = re.search(r'\b((?:19|20)\d{2})\b', normalized)
    if m:
        try:
            return date_type(int(m.group(1)), 1, 1)
        except ValueError:
            pass

    return None


# Unicode range → script name
SCRIPT_RANGES = [
    (0x0980, 0x09FF, "Bengali"),
    (0x0600, 0x06FF, "Arabic/Urdu"),
    (0x0750, 0x077F, "Arabic/Urdu"),
    (0xFB50, 0xFDFF, "Arabic/Urdu"),
    (0xFE70, 0xFEFF, "Arabic/Urdu"),
    (0x0900, 0x097F, "Devanagari"),
    (0x0041, 0x007A, "Latin"),
    (0x0400, 0x04FF, "Cyrillic"),
    (0x0E00, 0x0E7F, "Thai"),
    (0x0B80, 0x0BFF, "Tamil"),
    (0x4E00, 0x9FFF, "Chinese/CJK"),
    (0x3040, 0x30FF, "Japanese"),
    (0xAC00, 0xD7AF, "Korean"),
]

# Script → most likely country/region
SCRIPT_TO_COUNTRY: dict[str, str] = {
    "Bengali": "Bangladesh or West Bengal, India",
    "Arabic/Urdu": "Pakistan, Middle East, or Afghanistan",
    "Devanagari": "India or Nepal",
    "Latin": "Western country or international",
    "Thai": "Thailand",
    "Tamil": "Tamil Nadu, India or Sri Lanka",
}

# Script → NOT Bangladesh flag (high-weight geo signal)
SCRIPTS_NOT_BANGLADESH = {"Arabic/Urdu", "Devanagari", "Thai", "Chinese/CJK", "Japanese", "Korean", "Cyrillic"}


def detect_scripts(text: str) -> list[str]:
    """Return list of script names detected in the given text string."""
    found = set()
    for char in text:
        cp = ord(char)
        for start, end, script in SCRIPT_RANGES:
            if start <= cp <= end:
                found.add(script)
                break
    return list(found)


def infer_country_from_scripts(scripts: list[str]) -> Optional[dict]:
    """
    Given a list of detected scripts, infer the most likely country.

    Returns:
    {
        "country": str,
        "confidence": float,
        "reasoning": str,
        "not_bangladesh": bool,
    }
    or None if scripts list is empty.
    """
    if not scripts:
        return None

    not_bd_scripts = [s for s in scripts if s in SCRIPTS_NOT_BANGLADESH]

    if not_bd_scripts:
        primary = not_bd_scripts[0]
        return {
            "country": SCRIPT_TO_COUNTRY.get(primary, "Unknown"),
            "confidence": 0.80,
            "reasoning": f"Script '{primary}' detected — not used in Bangladesh",
            "not_bangladesh": True,
        }

    if "Bengali" in scripts and len(scripts) == 1:
        return {
            "country": "Bangladesh or West Bengal, India",
            "confidence": 0.50,
            "reasoning": "Only Bengali script detected — consistent with BD but not conclusive",
            "not_bangladesh": False,
        }

    return {
        "country": "Unknown",
        "confidence": 0.20,
        "reasoning": f"Scripts detected: {scripts}",
        "not_bangladesh": False,
    }


NON_BD_CHANNELS: dict[str, str] = {
    "Geo News": "Pakistan", "GEO NEWS": "Pakistan",
    "ARY News": "Pakistan", "ARY NEWS": "Pakistan",
    "Samaa": "Pakistan", "SAMAA TV": "Pakistan",
    "Dawn News": "Pakistan", "DAWN NEWS": "Pakistan",
    "Express News": "Pakistan", "Aaj News": "Pakistan",
    "Hum News": "Pakistan", "BOL News": "Pakistan",
    "India Today": "India", "INDIA TODAY": "India",
    "NDTV": "India", "Zee News": "India", "ZEE NEWS": "India",
    "ABP News": "India", "Republic TV": "India",
    "Times Now": "India", "TIMES NOW": "India",
    "Aaj Tak": "India", "AAJ TAK": "India",
    "News18": "India", "CNN-News18": "India",
    "WION": "India", "Wion": "India",
}


def scan_channel_names(text: str) -> Optional[dict]:
    """
    Scan OCR text for known non-Bangladesh news channel names.
    Returns match info or None.
    """
    if not text:
        return None
    text_upper = text.upper()
    for channel, country in NON_BD_CHANNELS.items():
        if channel.upper() in text_upper:
            return {
                "channel": channel,
                "country": country,
                "confidence": 0.95,
                "reasoning": f"Non-BD news channel '{channel}' detected in on-screen text — this video is from {country}",
                "not_bangladesh": True,
            }
    return None


def extract_date_patterns(text: str) -> list[str]:
    """
    Extract date-like strings from OCR text using simple regex patterns.
    Bengali numerals are normalized to ASCII before matching.
    Returns list of potential date strings for Chronologist to parse.
    """
    import re
    normalized = normalize_bengali_numerals(text)
    patterns = [
        r"\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}",
        r"\d{4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2}",
        r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}",
        r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}",
        r"\b(?:19|20)\d{2}\b",  # standalone 4-digit year
    ]
    found = []
    for pattern in patterns:
        found.extend(re.findall(pattern, normalized, re.IGNORECASE))
    return list(set(found))
