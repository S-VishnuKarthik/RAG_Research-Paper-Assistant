from utils.text_utils import clean_text
from ingestion.section_parser import detect_section
from config.settings import CHUNK_SIZE

def chunk_text(data, source):
    chunks = []

    for item in data:
        text = clean_text(item["text"])

        for i in range(0, len(text), CHUNK_SIZE):
            chunk = text[i:i+CHUNK_SIZE]

            chunks.append({
                "content": chunk,
                "page": item["page"],
                "source": source,
                "section": detect_section(chunk)
            })

    return chunks