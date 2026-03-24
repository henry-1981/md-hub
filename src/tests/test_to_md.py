"""Tests for to_md engine."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "md_hub"))

from md_hub.engines.to_md import convert


def test_convert_txt_file():
    """A plain .txt file should return its content."""
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False, encoding="utf-8") as f:
        f.write("Hello, world!\nThis is a test.")
        f.flush()
        result = convert(f.name)
    assert "Hello, world!" in result
    Path(f.name).unlink(missing_ok=True)


def test_convert_md_file():
    """A .md file should return its content."""
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("# Title\n\nSome **bold** text.")
        f.flush()
        result = convert(f.name)
    assert "Title" in result
    Path(f.name).unlink(missing_ok=True)


def test_convert_file_not_found():
    import pytest
    with pytest.raises(FileNotFoundError):
        convert("/nonexistent/file.txt")


def test_convert_unsupported_extension():
    import pytest
    with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
        pass
    with pytest.raises(ValueError, match="Unsupported"):
        convert(f.name)
    Path(f.name).unlink(missing_ok=True)
