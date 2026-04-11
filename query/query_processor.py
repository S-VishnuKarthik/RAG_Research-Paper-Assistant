import re

import query

class QueryProcessor:
    def __init__(self):
        self.section_keywords = {
        "abstract": ["abstract", "summary of paper"],
        "methodology": ["method", "approach", "algorithm"],
        "results": ["result", "evaluation"],
        "introduction": ["introduction", "background"],
    }

    def clean_query(self, query):
        query = query.lower().strip()
        query = re.sub(r'[^\w\s]', '', query)
        return query

    def detect_section(self, query):
        for section, keywords in self.section_keywords.items():
            for word in keywords:
                if word in query:
                    return section
        return None

    def extract_constraints(self, query):
        """
        Extract additional constraints like:
        - specific paper mention
        - section-based filtering
        """
        constraints = {
            "section": self.detect_section(query),
            "source": None
        }

        # Example: "paper1", "paper2"
        match = re.search(r'paper\s*(\d+)', query)
        if match:
            constraints["source"] = f"paper{match.group(1)}"

        return constraints
    
       
        sections_found = []


        for section, keywords in self.section_keywords.items():
            for word in keywords:
                if word in query:
                    sections.append(section)

        return {
             "sections": sections if sections else None,
            "source": None
        }
        
        

    def enhance_query(self, query, q_type):
        """
        Improve query for retrieval quality
        """
        if q_type == "comparison":
            return query + " compare differences similarities methods"
        elif q_type == "summary":
            return query + " key contributions overview summary"
        

        elif "methodology" in query:
            query += " method approach algorithm technique"

        elif "introduction" in query:
            query += " introduction background overview"
        else:
            return query
        

    def process(self, query, q_type):
        cleaned = self.clean_query(query)
        constraints = self.extract_constraints(cleaned)

        # 🔥 Intelligent default section handling
        if constraints["section"] is None:
            if q_type == "summary":
                constraints["section"] = "all"
            elif q_type == "comparison":
                constraints["section"] = "methodology"

        enhanced = self.enhance_query(cleaned, q_type)

        return {
            "original_query": query,
            "cleaned_query": cleaned,
            "enhanced_query": enhanced,
            "constraints": constraints
        }