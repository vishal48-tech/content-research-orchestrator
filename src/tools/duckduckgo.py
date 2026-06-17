import requests
from bs4 import BeautifulSoup
import urllib.parse

def search(query: str, max_results: int = 3):
    url = "https://html.duckduckgo.com/html/"
    response = requests.post(url, data={"q": query}, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    soup = BeautifulSoup(response.text, "lxml")
    
    results = []
    for result in soup.find_all("div", class_="result")[:max_results]:
        a = result.find("a", class_="result__a")
        if not a:
            continue
            
        href = a.get("href", "")
        if href.startswith("/l/?uddg="):
            real_url = urllib.parse.unquote(href.replace("/l/?uddg=", ""))
        elif href.startswith("//"):
            real_url = f"https:{href}"
        else:
            real_url = href
            
        try:
            final_url = requests.head(real_url, allow_redirects=True, timeout=10).url
        except Exception:
            final_url = real_url
            
        results.append({"title": a.get_text(strip=True), "url": final_url})
    
    return results