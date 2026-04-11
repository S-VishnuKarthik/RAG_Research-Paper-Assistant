from config.constants import SECTIONS
from utils.text_utils import normalize_text
from utils.logger import setup_logger

import re

logger = setup_logger()


class SectionParser:
    def __init__(self):
        #  Expand section synonyms (VERY IMPORTANT)
        self.section_map = {
            "abstract": ["abstract", "summary"],
            "introduction": ["introduction", "background"],
            "methodology": ["method", "methods", "approach", "algorithm", "framework"],
            "results": ["results", "evaluation", "performance"],
            "discussion": ["discussion", "analysis"],
            "conclusion": ["conclusion", "future work", "closing"]
        }

        #  Priority (for conflict resolution)
        self.priority = {
            "abstract": 1,
            "introduction": 2,
            "methodology": 3,
            "results": 4,
            "discussion": 5,
            "conclusion": 6
        }

    #  Detect headings (strong signal)
    def detect_heading(self, text):
        lines = text.split("\n")[:5]  # check first few lines

        for line in lines:
            clean_line = line.strip().lower()

            if len(clean_line) < 50:  # likely heading
                for section, keywords in self.section_map.items():
                    for kw in keywords:
                        if kw in clean_line:
                            return section

        return None

    #  Score-based matching
    def score_sections(self, text):
        scores = {sec: 0 for sec in self.section_map}

        for section, keywords in self.section_map.items():
            for kw in keywords:
                matches = len(re.findall(rf"\b{kw}\b", text))
                scores[section] += matches

        return scores

    #  Select best section
    def select_best(self, scores):
        # Remove zero scores
        valid = {k: v for k, v in scores.items() if v > 0}

        if not valid:
            return "unknown"

        # Sort by score + priority
        return sorted(
            valid,
            key=lambda x: (-valid[x], self.priority.get(x, 99))
        )[0]

    #  Confidence calculation
    def compute_confidence(self, scores, selected):
        total = sum(scores.values())
        if total == 0:
            return 0.0
        return scores[selected] / total

    #  Main detection
    def detect(self, text):
        text = normalize_text(text)

        # 1️⃣ Heading-based detection (highest priority)
        heading_section = self.detect_heading(text)
        if heading_section:
            return {
                "section": heading_section,
                "confidence": 0.95,
                "method": "heading"
            }

        # 2️⃣ Score-based detection
        scores = self.score_sections(text)
        selected = self.select_best(scores)
        confidence = self.compute_confidence(scores, selected)

        return {
            "section": selected,
            "confidence": round(confidence, 2),
            "method": "scoring"
        }


#  Wrapper function (for compatibility)
def detect_section(text):
    parser = SectionParser()
    result = parser.detect(text)
    return result["section"]