"""Tests for to_pdf engine."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "md_hub"))

import pytest
from engines.to_pdf import convert, md_to_html, build_css


def test_md_to_html():
    html = md_to_html("# Hello\n\nWorld")
    assert "<h1>" in html
    assert "Hello" in html


def test_build_css_defaults():
    config = {"font": {"heading": "Arial"}, "margin": {}, "colors": {}}
    css = build_css(config)
    assert "Arial" in css
    assert "@page" in css


@pytest.fixture
def sample_md(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# PDF Test\n\nHello PDF world.\n", encoding="utf-8")
    return str(md_file)


def test_convert_produces_pdf(sample_md, tmp_path):
    """Converting a .md file should produce a valid PDF with %%PDF magic bytes."""
    output = str(tmp_path / "output.pdf")
    try:
        convert(sample_md, output)
    except Exception as e:
        if "playwright" in str(e).lower() or "browser" in str(e).lower():
            pytest.skip("Playwright browsers not installed")
        raise
    output_path = Path(output)
    assert output_path.exists()
    with open(output, "rb") as f:
        magic = f.read(4)
    assert magic == b"%PDF"
