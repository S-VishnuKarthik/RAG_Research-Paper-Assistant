'''def classify_query(query):
    q = query.lower()

    if "compare" in q:
        return "comparison"
    elif "summarize" in q or "summary" in q:
        return "summary"
    else:
        return "factual"
'''
class QueryClassifier:
    def __init__(self):
        self.rules = {
            "comparison": ["compare", "difference", "vs", "similarities"],
            "summary": ["summarize", "summary", "overview", "brief"],
            "factual": ["what", "which", "who", "when", "where", "how"]
        }

    def classify(self, query):
        query = query.lower()

        scores = {
            "comparison": 0,
            "summary": 0,
            "factual": 0
        }

        for label, keywords in self.rules.items():
            for word in keywords:
                if word in query:
                    scores[label] += 1

        # fallback logic
        if max(scores.values()) == 0:
            return "factual"

        return max(scores, key=scores.get)


# simple wrapper (for compatibility)
def classify_query(query):
    classifier = QueryClassifier()
    return classifier.classify(query)