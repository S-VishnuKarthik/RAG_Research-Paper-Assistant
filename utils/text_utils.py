import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_text(text):
    return text.lower()

def remove_special_chars(text):
    return re.sub(r'[^\w\s]', '', text)

def truncate_text(text, max_len=500):
    return text[:max_len]