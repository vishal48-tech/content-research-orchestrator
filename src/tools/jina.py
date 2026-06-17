import requests

def extract(url: str):
    try:
        r = requests.get(f"https://r.jina.ai/http://{url}", timeout=30)
        lines = r.text.strip().split("\n")
        content = "\n".join(lines[1:]).strip()
        return {
            "title": lines[0] if lines else "",
            "content": content,
            "word_count": len(content.split())
        }
    except Exception:
        return {"title": "", "content": "", "word_count": 0}