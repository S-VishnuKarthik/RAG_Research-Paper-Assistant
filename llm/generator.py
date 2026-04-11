'''
from openai import OpenAI
from llm.prompts import build_messages

client = OpenAI()

from retrieval.context_builder import ContextBuilder

builder = ContextBuilder()
context = builder.build_context(chunks)

def generate_answer(query, chunks, q_type):
    # Build context with strong citations
    context = ""

    for c in chunks:
        context += f"[{c['source']} - Page {c['page']}]\n{c['content']}\n\n"

    # Build messages
    messages = build_messages(q_type, context, query)

    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2  # low → less hallucination
    )

    return response.choices[0].message.content'''
    
from openai import OpenAI
from llm.prompts import build_messages
from retrieval.context_builder import ContextBuilder
from utils.logger import setup_logger
import time

# Initialize components
client = OpenAI()
logger = setup_logger()
context_builder = ContextBuilder()

# Config
MAX_RETRIES = 3
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.2
MAX_CONTEXT_CHARS = 12000


def generate_answer(query, chunks, q_type, stream=False):
    """
    Advanced LLM generation pipeline:
    - Builds optimized context
    - Applies strict prompting
    - Handles retries
    - Logs execution
    """

    start_time = time.time()

    try:
        # 🔥 Step 1: Build optimized context
        context = context_builder.build_context(chunks)

        if len(context) > MAX_CONTEXT_CHARS:
            context = context[:MAX_CONTEXT_CHARS]

        # 🔥 Step 2: Build messages (system + user)
        messages = build_messages(q_type, context, query)

        logger.info(f"Query: {query}")
        logger.info(f"Query Type: {q_type}")
        logger.info(f"Context Length: {len(context)}")

        # 🔥 Step 3: Retry mechanism
        for attempt in range(MAX_RETRIES):
            try:
                if stream:
                    # 🔥 Streaming response (optional)
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        temperature=TEMPERATURE,
                        stream=True
                    )

                    full_response = ""
                    for chunk in response:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            full_response += delta
                    answer = full_response

                else:
                    # 🔥 Standard response
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        temperature=TEMPERATURE
                    )

                    answer = response.choices[0].message.content

                # 🔥 Step 4: Guardrails check
                if not answer or len(answer.strip()) == 0:
                    raise ValueError("Empty response from model")

                # 🔥 Step 5: Post-processing
                answer = post_process_answer(answer)

                end_time = time.time()
                logger.info(f"Response generated in {end_time - start_time:.2f}s")

                return answer

            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed: {e}")
                time.sleep(1)

        # 🔥 If all retries fail
        return "⚠️ Unable to generate response at the moment. Please try again."

    except Exception as e:
        logger.error(f"Critical error: {e}")
        return "⚠️ System error occurred."


# 🔥 POST-PROCESSING FUNCTION
def post_process_answer(answer):
    """
    Clean and enhance LLM output
    """
    # Remove unnecessary whitespace
    answer = answer.strip()

    # Optional: enforce citation presence
    if "[" not in answer:
        answer += "\n\n(Note: No citations found in response.)"

    return answer