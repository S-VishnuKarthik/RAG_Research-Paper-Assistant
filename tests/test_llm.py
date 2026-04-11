from llm.generator import generate_answer

def test_llm_response():
    chunks = [
        {"content": "This paper uses CNN.", "page": 1, "source": "test.pdf"}
    ]

    response = generate_answer("What model is used?", chunks, "factual")

    assert isinstance(response, str)
    assert len(response) > 0