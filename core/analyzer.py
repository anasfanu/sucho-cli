# File: sucho-cli/core/analyzer.py

def calculate_score(data: dict):
    """
    Calculates Sucho Score (0-100) based on AI-friendly factors.
    """
    score = 0
    gaps = []
    max_score = 0

    # 1. Title & Meta (Max 20)
    max_score += 20
    if data.get('title'):
        score += 10
    else:
        gaps.append("Missing <title> tag")
        
    if data.get('meta_description'):
        score += 10
    else:
        gaps.append("Missing meta description")

    # 2. Structured Data (Max 40) - SANGAT PENTING UNTUK AI
    max_score += 40
    if data.get('json_ld'):
        score += 40
    else:
        gaps.append("No JSON-LD Structured Data found (Critical for AI)")

    # 3. Semantic HTML (Max 20)
    max_score += 20
    semantic_count = len(data.get('semantic_tags', []))
    if semantic_count >= 3:
        score += 20
    elif semantic_count > 0:
        score += 10
        gaps.append("Low semantic HTML usage (add <article>, <main>, etc.)")
    else:
        gaps.append("No semantic HTML tags found")

    # 4. Content Structure (Max 20)
    max_score += 20
    if len(data.get('headings', [])) > 0:
        score += 10
    else:
        gaps.append("No headings (H1-H3) found")
        
    if data.get('images_count', 0) > 0:
        score += 10
    else:
        gaps.append("No images found")

    # Normalize score to 100
    final_score = int((score / max_score) * 100) if max_score > 0 else 0

    return final_score, gaps