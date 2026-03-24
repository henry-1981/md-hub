"""PDF engine: MD -> HTML -> Playwright -> PDF."""

from pathlib import Path

from markdown_it import MarkdownIt


def md_to_html(md_text: str) -> str:
    """Convert markdown text to HTML using markdown-it-py with table support."""
    md = MarkdownIt().enable("table")
    return md.render(md_text)


def build_css(config: dict) -> str:
    """Generate CSS from template config dict."""
    font = config.get("font", {})
    margin = config.get("margin", {})
    colors = config.get("colors", {})

    heading_font = font.get("heading", "sans-serif")
    body_font = font.get("body", "sans-serif")
    font_size = font.get("size", "11pt")
    fallback = f"'{heading_font}', 'NanumGothic', sans-serif"

    return f"""
@page {{
    margin: {margin.get('top', '2.54cm')} {margin.get('right', '3.17cm')} {margin.get('bottom', '2.54cm')} {margin.get('left', '3.17cm')};
}}
body {{
    font-family: {fallback};
    font-size: {font_size};
    color: {colors.get('body', '#333')};
    line-height: 1.6;
}}
h1, h2, h3, h4, h5, h6 {{
    font-family: {fallback};
    color: {colors.get('heading', '#000')};
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
}}
th, td {{
    border: 1px solid #ccc;
    padding: 0.4em 0.6em;
}}
th {{
    background: {colors.get('table_header_bg', '#F2F2F2')};
}}
"""


def convert(md_path: str, output_path: str, template_name: str = "default") -> None:
    """Full pipeline: read MD, convert to HTML, render PDF via Playwright."""
    from engines.template_loader import load_template
    config = load_template(template_name)

    md_text = Path(md_path).read_text(encoding="utf-8")
    html_body = md_to_html(md_text)
    css = build_css(config)

    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{html_body}</body></html>"""

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(full_html, wait_until="networkidle")
        page.pdf(path=output_path)
        browser.close()
