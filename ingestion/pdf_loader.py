import fitz

def extract_text_from_pdf(file):
    doc = fitz.open(file)
    data = []

    for i, page in enumerate(doc):
        data.append({
            "text": page.get_text(),
            "page": i + 1
        })

    return data