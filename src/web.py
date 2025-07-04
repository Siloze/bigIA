from duckduckgo_search import DDGS
import trafilatura
import time

def search_duckduckgo(query, max_results=5):
    print("Recherche DuckDuckGo (sans clé API)")
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        urls = [r["href"] for r in results if "href" in r]
    return urls

def extract_text_from_url(url):
    print("Téléchargement et extraction propre du contenu d'une page web")
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
            return extracted
    except Exception as e:
        print(f"Erreur extraction {url} : {e}")
    return None

def web_search_and_extract(query, max_results=5):
    urls = search_duckduckgo(query, max_results)
    documents = []
    for url in urls:
        if "youtube.com" in url:
            print(f"Skip {url}")
            continue
        print(f"🔗 Récupération : {url}")
        text = extract_text_from_url(url)
        if text:
            documents.append({"url": url, "content": text})
        time.sleep(0.5)  # éviter de spammer les sites
    return documents
