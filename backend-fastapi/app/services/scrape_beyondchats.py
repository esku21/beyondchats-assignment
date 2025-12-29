import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import urljoin

BASE_URL = "https://beyondchats.com"

def get_last_page_url(list_url: str = f"{BASE_URL}/blogs/") -> str:
    resp = requests.get(list_url, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Strategy: find pagination container, pick last page link
    # Adjust selectors based on actual DOM
    pagination = soup.select("nav.pagination a") or soup.select(".pagination a")
    if pagination:
        last = pagination[-1].get("href")
        return urljoin(BASE_URL, last)
    # If no pagination, assume single page
    return list_url

def scrape_list_page(page_url: str) -> List[Dict]:
    resp = requests.get(page_url, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    items = []
    # Adjust selectors based on the blog card layout
    for card in soup.select("article, .blog-card, .post"):
        title_el = card.select_one("h2 a, h3 a, .title a")
        if not title_el:
            title_el = card.select_one("h2, h3, .title")
        title = title_el.get_text(strip=True) if title_el else None

        href = None
        if title_el and title_el.name == "a":
            href = title_el.get("href")
        else:
            link_el = card.select_one("a")
            href = link_el.get("href") if link_el else None

        if title and href:
            items.append({
                "title": title,
                "url": urljoin(BASE_URL, href)
            })
    return items

def scrape_article_content(article_url: str) -> Dict[str, Optional[str]]:
    resp = requests.get(article_url, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Attempt to find main content container
    main = soup.select_one("article") or soup.select_one("main") or soup.select_one(".post-content")
    content_html = str(main) if main else soup.prettify()
    content_text = main.get_text("\n", strip=True) if main else soup.get_text("\n", strip=True)
    return {"content_html": content_html, "content_text": content_text}
