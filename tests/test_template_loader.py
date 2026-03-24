"""Tests for template_loader: deep_merge and load_template."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "md_hub"))

from engines.template_loader import deep_merge, load_template


def test_deep_merge_basic():
    base = {"a": 1, "b": {"x": 10, "y": 20}}
    override = {"b": {"y": 99}, "c": 3}
    result = deep_merge(base, override)
    assert result["a"] == 1
    assert result["b"]["x"] == 10
    assert result["b"]["y"] == 99
    assert result["c"] == 3


def test_deep_merge_override_replaces_list():
    base = {"items": [1, 2, 3]}
    override = {"items": [4, 5]}
    result = deep_merge(base, override)
    assert result["items"] == [4, 5]


def test_load_template_default():
    config = load_template("default")
    assert config["font"]["heading"] == "Malgun Gothic"
    assert config["font"]["body"] == "Malgun Gothic"
    assert config["font"]["size"] == "11pt"
    assert config["colors"]["heading"] == "#1A1A1A"
    assert config["colors"]["body"] == "#333333"
    assert config["colors"]["table_header_bg"] == "#F2F2F2"
    assert config["page"] == "A4"
    assert config["margin"]["top"] == "2.54cm"


def test_load_template_invalid():
    import pytest
    with pytest.raises(KeyError, match="템플릿을 찾을 수 없습니다"):
        load_template("nonexistent")
