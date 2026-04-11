def filter_chunks(chunks, constraints):
    """
    Filters chunks based on:
    - section
    - source (paper)
    """

    filtered = []

    for chunk in chunks:
        keep = True

       # 🔥 Section filtering (only if not "all")
        if constraints.get("section") and constraints["section"] != "all":
            if chunk.get("section") != constraints["section"]:
                keep = False
                
        if constraints.get("sections"):
            if chunk.get("section") not in constraints["sections"]:
                keep = False

        # 🔥 Source filtering
        if constraints.get("source"):
            if constraints["source"] not in chunk.get("source", "").lower():
                keep = False

        if keep:
            filtered.append(chunk)

    return filtered



    
    

def fallback_filter(original_chunks, filtered_chunks):
    """
    If filtering removes too many chunks,
    fallback to original results
    """
    if len(filtered_chunks) < 2:
        return original_chunks
    return filtered_chunks