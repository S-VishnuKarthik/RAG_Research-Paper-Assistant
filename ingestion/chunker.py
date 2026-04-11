from utils.text_utils import clean_text
from ingestion.section_parser import detect_section
from config.settings import CHUNK_SIZE
from utils.logger import setup_logger

import hashlib

logger = setup_logger()

# 🔥 Config
OVERLAP_SIZE = int(CHUNK_SIZE * 0.2)  # 20% overlap
MIN_CHUNK_LENGTH = 50


def _hash(text):
    return hashlib.md5(text.encode()).hexdigest()


def _create_chunk(content, page, source, section, chunk_id, start_idx):
    return {
        "id": chunk_id,
        "content": content,
        "page": page,
        "source": source,
        "section": section,
        "start_index": start_idx,
        "length": len(content)
    }


def chunk_text(data, source):
    """
    Advanced chunking:
    - Overlapping chunks
    - Metadata enrichment
    - Section-aware splitting
    """

    chunks = []
    seen_hashes = set()

    chunk_counter = 0

    for item in data:
        text = clean_text(item.get("content") or item.get("text", ""))

        if not text or len(text) < MIN_CHUNK_LENGTH:
            continue

        page = item["page"]

        # 🔥 Use section from PDF loader if available
        base_section = item.get("section", "unknown")

        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + CHUNK_SIZE
            chunk = text[start:end]

            # 🔥 Skip very small chunks
            if len(chunk.strip()) < MIN_CHUNK_LENGTH:
                start += CHUNK_SIZE
                continue

            # 🔥 Section detection (fallback or refine)
            section = base_section if base_section != "unknown" else detect_section(chunk)

            # 🔥 Deduplication
            h = _hash(chunk)
            if h in seen_hashes:
                start += CHUNK_SIZE
                continue

            seen_hashes.add(h)

            chunk_id = f"{source}_p{page}_c{chunk_counter}"

            chunks.append(
                _create_chunk(
                    content=chunk,
                    page=page,
                    source=source,
                    section=section,
                    chunk_id=chunk_id,
                    start_idx=start
                )
            )

            chunk_counter += 1

            # 🔥 Move with overlap
            start += (CHUNK_SIZE - OVERLAP_SIZE)

    logger.info(f"Total chunks created: {len(chunks)}")

    return chunks