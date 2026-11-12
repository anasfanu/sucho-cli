# File: sucho-cli/sucho.py
import click
from core.crawler import crawl_website, discover_from_sitemap
from core.parser import parse_html
from core.detector import detect_page_type
from core.analyzer import calculate_score
from core.reporter import print_report

@click.group()
def cli():
    """Sucho: Your Agentic AI SEO Analyzer"""
    pass

@cli.command()
@click.argument('url')
def analyze(url):
    """Analyze a website URL for Agentic AI readiness."""
    click.echo(f"🔍 Starting analysis for: {url}")
    
    # 1. Deep Discovery (Otomatis, diam-diam di latar belakang)
    sample_urls = discover_from_sitemap(url)
    site_context = ""
    if sample_urls:
        site_context = f" (Sitemap detected, sampled {len(sample_urls)} pages for context)"
    
    # 2. Crawl Main URL
    with click.progressbar(length=100, label='Crawling main page') as bar:
        html, status = crawl_website(url)
        bar.update(50)
        if not html:
            click.echo(f"❌ Failed to crawl {url} (Status: {status}). Website mungkin memblokir bot.")
            return
        bar.update(50)

    # 3. Parse
    click.echo("🧩 Parsing HTML structure...")
    data = parse_html(html, url)
    
    # 4. Detect (Content-based + Schema)
    click.echo("🧠 Detecting page type...")
    page_type = detect_page_type(data, url)
    data['page_type'] = page_type + site_context

    # 5. Analyze
    click.echo("📊 Calculating Sucho Score...")
    score, gaps = calculate_score(data)

    # 6. Report
    print_report(url, score, data, gaps)

if __name__ == '__main__':
    cli()