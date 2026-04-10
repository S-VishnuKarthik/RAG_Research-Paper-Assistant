def get_prompt(q_type, context, query):
    if q_type == "comparison":
        return f"""
Compare the research papers.

Context:
{context}

Question: {query}
"""
    elif q_type == "summary":
        return f"""
Summarize the research papers.

Context:
{context}

Question: {query}
"""
    else:
        return f"""
Answer the question with citations.

Context:
{context}

Question: {query}
"""