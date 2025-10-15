from duckduckgo_search import DDGS
from playwright.sync_api import sync_playwright
import trafilatura
import time
import urllib.parse

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

def web_search_and_extract_duck(query, max_results=5):
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

from playwright.sync_api import sync_playwright
import trafilatura

def web_search_and_extract(query, max_resultats=5):
    liens = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()


        search_url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}&t=h_&ia=web"
        page.goto(search_url)
        page.wait_for_timeout(3000)

        # Pas d'attente inutile → récupération directe des <a> visibles avec class js-result-title
        results = page.locator("a[data-testid='result-title-a']")
        count = results.count()

        print(f"[DEBUG] Résultats visibles : {count}")

        for i in range(min(count, max_resultats)):
            href = results.nth(i).get_attribute("href")
            if href and href.startswith("http"):
                liens.append(href)

        browser.close()

    print(f"[+] Liens trouvés : {liens}")

    # Extraction de texte avec trafilatura
    textes = []
    for url in liens:
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                texte = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
                if texte:
                    textes.append({"url": url, "content": texte})
        except Exception as e:
            print(f"Erreur pour {url}: {e}")

    return textes