# File: sucho-cli/core/crawler.py
import httpx
from bs4 import BeautifulSoup

def crawl_website(url: str):
    """Fetches HTML content with robust anti-timeout and browser-like headers."""
    if not url.startswith('http'):
        url = 'https://' + url

    # Headers yang lebih mirip browser Chrome asli untuk menghindari blokir WAF dasar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Connection': 'keep-alive',
    }

    try:
        # Timeout diperpanjang jadi 15 detik, follow_redirects wajib
        with httpx.Client(follow_redirects=True, timeout=15.0) as client:
            response = client.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.text, response.status_code
            else:
                return None, response.status_code
                
    except httpx.TimeoutException:
        print("⚠️ Request timed out. The website might be blocking automated requests (WAF).")
        return None, 0
    except httpx.RequestError as e:
        print(f"⚠️ Network Error: {e}")
        return None, 0
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return None, 0

def discover_from_sitemap(base_url: str):
    """Silently attempts to find a sitemap to understand site structure."""
    if not base_url.endswith('/'):
        base_url += '/'
        
    sitemap_urls = [
        f"{base_url}sitemap.xml",
        f"{base_url}sitemap_index.xml",
        f"{base_url}post-sitemap.xml",
        f"{base_url}product-sitemap.xml"
    ]

    headers = {'User-Agent': 'Mozilla/5.0 (compatible; SuchoBot/1.0)'}

    try:
        with httpx.Client(follow_redirects=True, timeout=5.0) as client:
            for sitemap_url in sitemap_urls:
                response = client.get(sitemap_url, headers=headers)
                if response.status_code == 200 and 'xml' in response.headers.get('content-type', ''):
                    soup = BeautifulSoup(response.text, 'xml')
                    urls = soup.find_all('loc')
                    if urls:
                        return [url.text for url in urls[:5]] # Ambil 5 sampel
    except Exception:
        pass # Gagal? Tidak apa-apa, fallback ke analisis URL tunggal
        
    return []