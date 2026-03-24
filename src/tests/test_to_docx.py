"""Tests for to_docx engine."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "md_hub"))

import pytest
from md_hub.engines.to_docx import convert


@pytest.fixture
def sample_md(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text("# Hello\n\nThis is a test document.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n", encoding="utf-8")
    return str(md_file)


def test_convert_produces_docx(sample_md, tmp_path):
    """Converting a .md file should produce a valid .docx."""
    output = str(tmp_path / "output.docx")
    convert(sample_md, output)
    output_path = Path(output)
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    # DOCX files are ZIP archives starting with PK
    with open(output, "rb") as f:
        magic = f.read(2)
    assert magic == b"PK"
