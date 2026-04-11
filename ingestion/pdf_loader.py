import fitz  # PyMuPDF
import os
from utils.logger import setup_logger
from utils.text_utils import clean_text

logger = setup_logger()


class PDFLoader:
    def __init__(self):
        self.section_keywords = {
            "abstract": ["abstract"],
            "introduction": ["introduction"],
            "methodology": ["method", "approach", "algorithm"],
            "results": ["result", "evaluation", "performance"],
            "conclusion": ["conclusion", "future work"]
        }

    # 🔥 Detect section from text
    def detect_section(self, text):
        text_lower = text.lower()

        for section, keywords in self.section_keywords.items():
            for word in keywords:
                if word in text_lower[:500]:  # check beginning of page
                    return section

        return "unknown"

    # 🔥 Validate file
    def validate_file(self, file):
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")

        if not file.lower().endswith(".pdf"):
            raise ValueError("Invalid file type. Only PDF allowed.")

    # 🔥 Extract text safely
    def extract(self, file):
        self.validate_file(file)

        try:
            doc = fitz.open(file)
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            raise

        data = []

        for i, page in enumerate(doc):
            try:
                text = page.get_text()

                # 🔥 OCR fallback (if no text)
                if not text.strip():
                    text = page.get_text("text")  # fallback attempt

                text = clean_text(text)

                if not text:
                    continue

                section = self.detect_section(text)

                data.append({
                    "content": text,
                    "page": i + 1,
                    "section": section,
                    "source": os.path.basename(file)
                })

            except Exception as e:
                logger.warning(f"Error processing page {i+1}: {e}")

        doc.close()

        logger.info(f"Processed {len(data)} pages from {file}")

        return data


# 🔥 Wrapper function (for compatibility with your existing code)
def extract_text_from_pdf(file):
    loader = PDFLoader()
    return loader.extract(file)