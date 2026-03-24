"""to_md engine — convert any supported document to Markdown text."""

from pathlib import Path

SUPPORTED_EXTENSIONS: set[str] = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls",
    ".csv", ".json", ".xml", ".html", ".epub",
    ".txt", ".md",
}


def convert(file_path: str) -> str:
    """Convert any supported document to Markdown text.

    - Non-PDF files: use markitdown directly
    - Digital PDF: use markitdown
    - Scanned PDF: return message that Claude Vision is needed
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {ext}. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if ext == ".pdf":
        return _convert_pdf(path)

    # Non-PDF: use markitdown
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(path))
    return result.text_content


def _convert_pdf(path: Path) -> str:
    """Handle PDF conversion with scan detection."""
    import pymupdf

    doc = pymupdf.open(str(path))
    scanned_pages = 0
    total_pages = len(doc)

    for page in doc:
        raw_text = page.get_text("text").strip()
        text_blocks = [b for b in page.get_text("dict").get("blocks", []) if b["type"] == 0]
        if len(text_blocks) < 3 and len(raw_text) < 50:
            scanned_pages += 1
    doc.close()

    if scanned_pages == total_pages:
        return (
            f"[스캔 PDF 감지] {path.name} ({total_pages}페이지)\n"
            "이 PDF는 스캔 이미지로 구성되어 있어 텍스트 추출이 불가합니다.\n"
            "Claude Vision API를 사용한 OCR 변환이 필요합니다."
        )

    # Digital or mixed: try markitdown
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(path))

    if scanned_pages > 0:
        warning = (
            f"\n\n---\n[주의] {total_pages}페이지 중 {scanned_pages}페이지가 "
            "스캔 이미지입니다. 해당 페이지는 변환되지 않았을 수 있습니다.\n"
        )
        return result.text_content + warning

    return result.text_content
