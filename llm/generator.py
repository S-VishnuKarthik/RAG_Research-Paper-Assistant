from openai import OpenAI
from llm.prompts import get_prompt

client = OpenAI()

def generate_answer(query, chunks, q_type):
    context = ""

    for c in chunks:
        context += f"[{c['source']} Page {c['page']}]: {c['content']}\n\n"

    prompt = get_prompt(q_type, context, query)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content