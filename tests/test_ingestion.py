from ingestion.pdf_loader import extract_text_from_pdf

def test_pdf_loading():
    data = extract_text_from_pdf("data/Bayesian_Optimization.pdf")
    assert len(data) > 0
    assert "text" in data[0]