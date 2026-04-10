from config.constants import SECTIONS

def detect_section(text):
    text_lower = text.lower()
    for sec in SECTIONS:
        if sec in text_lower:
            return sec
    return "unknown"