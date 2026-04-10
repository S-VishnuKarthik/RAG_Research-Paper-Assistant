def classify_query(query):
    q = query.lower()

    if "compare" in q:
        return "comparison"
    elif "summarize" in q or "summary" in q:
        return "summary"
    else:
        return "factual"