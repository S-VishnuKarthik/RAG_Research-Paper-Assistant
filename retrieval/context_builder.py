def build_context(chunks):
    context = ""

    for c in chunks:
        context += f"[{c['source']} - Page {c['page']} - {c['section']}]\n{c['content']}\n\n"

    return context