
def build_messages(q_type, context, query):
    system_prompt = """
You are an expert AI Research Assistant.

STRICT RULES:
1. Answer ONLY using the provided context.
2. DO NOT use external knowledge.
3. If answer is not in context, say:
   "The answer is not available in the provided documents."
4. Always include citations in this format:
   [source - page number]
5. Be precise, structured, and academic.
6. Do NOT hallucinate.
"""

    if q_type == "comparison":
        user_prompt = f"""
You are given multiple research paper excerpts.

TASK:
Compare the methodologies across papers.

INSTRUCTIONS:
- Highlight similarities and differences
- Mention paper names and pages
- Keep it structured (bullet points)

CONTEXT:
{context}

QUESTION:
{query}
"""

    elif q_type == "summary":
        user_prompt = f"""
You are given research paper content.

TASK:
Provide a clear and structured summary.

INSTRUCTIONS:
- Include key contributions
- Include methodology overview
- Keep it concise

CONTEXT:
{context}

QUESTION:
{query}
"""

    else:  # factual
        user_prompt = f"""
You are given research paper excerpts.

TASK:
Answer the question strictly from the context.

INSTRUCTIONS:
- Be precise
- Include citations
- If not found, say it's unavailable

CONTEXT:
{context}

QUESTION:
{query}
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]