'''def build_context(chunks):
    context = ""

    for c in chunks:
        context += f"[{c['source']} - Page {c['page']} - {c['section']}]\n{c['content']}\n\n"

    return context'''
    
import hashlib

class ContextBuilder:
    def __init__(self, max_chars=20000):
        self.max_chars = max_chars

    def _hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def deduplicate(self, chunks):
        seen = set()
        unique = []

        for c in chunks:
            h = self._hash(c["content"])
            if h not in seen:
                seen.add(h)
                unique.append(c)

        return unique

    def sort_by_priority(self, chunks):
        # Example: prioritize methodology > abstract > others
        priority_map = {
            "abstract": 1,
            "methodology": 2,
            "results": 3,
            "introduction": 4,
            "conclusion": 5
        }

        return sorted(
            chunks,
            key=lambda x: priority_map.get(x.get("section", ""), 99)
        )

    def build_context(self, chunks):
        chunks = self.deduplicate(chunks)
        chunks = self.sort_by_priority(chunks)

        context = ""
        total_len = 0

        for c in chunks:
            block = f"[{c['source']} - Page {c['page']} - {c.get('section','unknown')}]\n{c['content']}\n\n"

            if total_len + len(block) > self.max_chars:
                break

            context += block
            total_len += len(block)

        return context