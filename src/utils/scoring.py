def score_source(url: str, length: int):
    domain = url.split("/")[2] if "//" in url else url
    score = 0.9 if any(d in domain for d in [".edu", ".gov", "arxiv", "ieee", "nature"]) else \
            0.7 if any(d in domain for d in ["github", "docs."]) else 0.5
    if length > 2000: score += 0.1
    elif length > 1000: score += 0.05
    return min(round(score, 2), 1.0)