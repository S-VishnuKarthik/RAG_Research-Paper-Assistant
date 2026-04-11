import hashlib
import time


class MetadataBuilder:
    def __init__(self):
        pass

    # 🔥 Unique ID generator
    def generate_id(self, source, page, chunk_index):
        return f"{source}_p{page}_c{chunk_index}"

    # 🔥 Hash for deduplication / tracking
    def generate_hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    # 🔥 Basic text stats
    def compute_stats(self, text):
        words = text.split()
        return {
            "char_length": len(text),
            "word_count": len(words),
            "avg_word_length": (len(text) / len(words)) if words else 0
        }

    # 🔥 Estimate tokens (approx)
    def estimate_tokens(self, text):
        return int(len(text.split()) * 1.3)

    # 🔥 Build full metadata object
    def build(
        self,
        content,
        source,
        page,
        section="unknown",
        chunk_index=0,
        start_index=0
    ):
        metadata = {}

        # Core
        metadata["id"] = self.generate_id(source, page, chunk_index)
        metadata["source"] = source
        metadata["page"] = page
        metadata["section"] = section

        # Content
        metadata["content"] = content

        # Position
        metadata["start_index"] = start_index
        metadata["end_index"] = start_index + len(content)

        # Stats
        stats = self.compute_stats(content)
        metadata.update(stats)

        # Tokens
        metadata["estimated_tokens"] = self.estimate_tokens(content)

        # Hash
        metadata["hash"] = self.generate_hash(content)

        # Timestamp
        metadata["created_at"] = time.time()

        return metadata

    # 🔥 Bulk processing
    def build_batch(self, chunks):
        enriched = []

        for i, c in enumerate(chunks):
            enriched.append(
                self.build(
                    content=c["content"],
                    source=c["source"],
                    page=c["page"],
                    section=c.get("section", "unknown"),
                    chunk_index=i,
                    start_index=c.get("start_index", 0)
                )
            )

        return enriched