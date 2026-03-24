"""MD→HWP engine. Wraps hwp-mcp COM automation (Windows + 한컴오피스 required)."""

import platform
from pathlib import Path
from markdown_it import MarkdownIt


def convert(md_path: str, output_path: str) -> None:
    """Convert MD file to HWP using COM automation.

    Requires Windows + 한컴오피스 installed.
    """
    if platform.system() != "Windows":
        raise EnvironmentError(
            "HWP 변환은 Windows에서만 지원됩니다 (한컴오피스 COM 자동화)"
        )

    try:
        import win32com.client
    except ImportError:
        raise EnvironmentError(
            "pywin32가 필요합니다: pip install pywin32"
        )

    md_text = Path(md_path).read_text(encoding="utf-8")
    mdi = MarkdownIt("commonmark").enable("table")
    tokens = mdi.parse(md_text)

    try:
        hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
    except Exception:
        raise EnvironmentError(
            "한컴오피스가 설치되어 있지 않거나 COM 등록이 안 되어 있습니다"
        )

    hwp.XHwpWindows.Item(0).Visible = False
    hwp.HAction.GetDefault("FileNew", hwp.HParameterSet.HFileOpenSave.HSet)
    hwp.HAction.Execute("FileNew", hwp.HParameterSet.HFileOpenSave.HSet)

    for token in tokens:
        if token.type == "heading_open":
            level = int(token.tag[1])  # h1→1, h2→2
            # HWP outline level
            hwp.HAction.GetDefault("Style", hwp.HParameterSet.HCharShape.HSet)
            act = hwp.CreateAction("Style")
            pset = act.CreateSet()
            act.GetDefault(pset)
            # Heading styles vary by HWP version; use outline level
        elif token.type == "inline" and token.content:
            _insert_text(hwp, token.content)
        elif token.type == "paragraph_close":
            _insert_paragraph(hwp)
        elif token.type == "heading_close":
            _insert_paragraph(hwp)

    # Save
    save_set = hwp.HParameterSet.HFileOpenSave
    hwp.HAction.GetDefault("FileSaveAs_S", save_set.HSet)
    save_set.filename = str(Path(output_path).resolve())
    save_set.Format = "HWP"
    hwp.HAction.Execute("FileSaveAs_S", save_set.HSet)
    hwp.Clear(1)  # close without save prompt


def _insert_text(hwp, text: str) -> None:
    """Insert text at current cursor position."""
    act = hwp.CreateAction("InsertText")
    pset = act.CreateSet()
    act.GetDefault(pset)
    pset.SetItem("Text", text)
    act.Execute(pset)


def _insert_paragraph(hwp) -> None:
    """Insert a paragraph break."""
    hwp.HAction.Run("BreakPara")
