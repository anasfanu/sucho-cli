# File: sucho-cli/core/parser.py
from bs4 import BeautifulSoup
import extruct
import json

def parse_html(html: str, url: str):
    """
    Extracts structured data from raw HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    data = {
        'url': url,
        'title': '',
        'meta_description': '',
        'headings': [],
        'images_count': 0,
        'links_internal': 0,
        'links_external': 0,
        'json_ld': [],
        'has_llms_txt': False, # Nanti dicek terpisah, default False
        'semantic_tags': []
    }

    # 1. Basic Meta
    if soup.title and soup.title.string:
        data['title'] = soup.title.string.strip()
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        data['meta_description'] = meta_desc['content'].strip()

    # 2. Headings (H1-H3)
    for i in range(1, 4):
        tags = soup.find_all(f'h{i}')
        for tag in tags:
            if tag.text.strip():
                data['headings'].append({f'h{i}': tag.text.strip()})

    # 3. Images & Links
    data['images_count'] = len(soup.find_all('img'))
    links = soup.find_all('a', href=True)
    for link in links:
        if url in link['href']:
            data['links_internal'] += 1
        else:
            data['links_external'] += 1

    # 4. Structured Data (JSON-LD) menggunakan extruct
    try:
        extracted = extruct.extract(html, url=url, syntaxes=['json-ld'])
        if 'json-ld' in extracted:
            data['json_ld'] = extracted['json-ld']
    except Exception:
        pass # Abaikan jika HTML terlalu rusak

    # 5. Semantic HTML Check (Penting untuk AI)
    semantic_tags = ['article', 'main', 'nav', 'footer', 'aside', 'section']
    for tag in semantic_tags:
        if soup.find(tag):
            data['semantic_tags'].append(tag)

    return data