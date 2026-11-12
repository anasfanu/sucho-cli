# File: sucho-cli/core/reporter.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def print_report(url: str, score: int, data: dict, gaps: list):
    """
    Prints a beautiful report in the terminal.
    """
    console.print() # Empty line
    
    # Header Panel
    color = "red" if score < 50 else "yellow" if score < 80 else "green"
    header = Panel(
        f"[bold white]URL:[/] {url}\n"
        f"[bold white]Type:[/] {data.get('page_type', 'Unknown')}\n"
        f"[bold white]Score:[/] [{color}]{score}/100[/]",
        title="🤖 SUCHO ANALYSIS REPORT",
        border_style=color
    )
    console.print(header)

    # Details Table
    table = Table(title="📊 Page Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Title Length", f"{len(data.get('title', ''))} chars")
    table.add_row("Meta Desc Length", f"{len(data.get('meta_description', ''))} chars")
    table.add_row("JSON-LD Blocks", f"{len(data.get('json_ld', []))}")
    table.add_row("Semantic Tags", ", ".join(data.get('semantic_tags', [])) or "None")
    table.add_row("Headings Count", str(len(data.get('headings', []))))
    table.add_row("Images", str(data.get('images_count', 0)))

    console.print(table)

    # Gaps/Recommendations
    if gaps:
        console.print("\n[bold red]⚠️ Areas for Improvement (AI Gaps):[/]")
        for gap in gaps:
            console.print(f"  - {gap}")
    else:
        console.print("\n[bold green]✅ Great job! This page looks very AI-friendly.[/]")
        
    console.print() # Empty line