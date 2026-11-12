# File: sucho-cli/core/detector.py

def detect_page_type(data: dict, url: str) -> str:
    """
    Advanced rule-based detector using Content Heuristics + Schema + URL.
    Prioritas: JSON-LD Schema > Konten HTML > Pola URL.
    """
    url_lower = url.lower()
    
    # Gabungkan semua teks dari headings dan meta untuk dicari polanya
    text_content = str(data.get('headings', [])).lower() + " " + data.get('meta_description', '').lower()
    
    # 1. CEK JSON-LD SCHEMA (Paling Akurat untuk AI)
    json_ld_types = []
    for schema in data.get('json_ld', []):
        if isinstance(schema, dict):
            schema_type = schema.get('@type', '')
            if isinstance(schema_type, list):
                json_ld_types.extend([t.lower() for t in schema_type])
            else:
                json_ld_types.append(schema_type.lower())
    
    if any(t in json_ld_types for t in ['product', 'offer']):
        return "E-commerce / Product Page"
    if any(t in json_ld_types for t in ['article', 'blogposting', 'newsarticle']):
        return "Article / Blog Post"
    if any(t in json_ld_types for t in ['faqpage']):
        return "FAQ / Support Page"
    if any(t in json_ld_types for t in ['website', 'organization', 'localbusiness']):
        return "Homepage / Corporate"

    # 2. CEK HEURISTIK KONTEN (Jika Schema tidak ada/tidak jelas)
    # Indikator E-commerce
    ecommerce_keywords = ['harga', 'rp', 'idr', 'usd', 'add to cart', 'beli', 'stok', 'sku', 'keranjang']
    if any(kw in text_content for kw in ecommerce_keywords):
        return "E-commerce / Product Page"
    
    # Indikator Artikel/Blog
    article_keywords = ['dipublikasikan', 'published', 'penulis', 'author', 'baca juga', 'komentar', 'comments']
    if any(kw in text_content for kw in article_keywords):
        return "Article / Blog Post"
        
    # Indikator FAQ
    if 'faq' in url_lower or 'pertanyaan' in text_content or 'jawaban' in text_content:
        return "FAQ / Support Page"

    # 3. CEK POLA URL (Fallback terakhir)
    if '/product/' in url_lower or '/item/' in url_lower or '/shop/' in url_lower or '/p/' in url_lower:
        return "E-commerce / Product Page"
    if '/blog/' in url_lower or '/article/' in url_lower or '/news/' in url_lower or '/post/' in url_lower:
        return "Article / Blog Post"
    
    # 4. DEFAULT
    if url_lower.endswith('/') or url_lower.count('/') <= 3:
        return "Homepage / General Corporate"
    
    return "General Web Page"