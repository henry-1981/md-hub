"""md-hub MCP server — document conversion with Markdown as the hub."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("md-hub")


@mcp.tool()
async def convert_to_md(file_path: str) -> str:
    """Convert a document (PDF, DOCX, PPTX, XLSX, HTML...) to Markdown."""
    from md_hub.engines.to_md import convert
    return convert(file_path)


@mcp.tool()
async def convert_to_docx(md_path: str, output_path: str, template: str = "default", doc_code: str = "") -> str:
    """Convert a Markdown file to DOCX."""
    from md_hub.engines.to_docx import convert
    kwargs = {"doc_code": doc_code} if doc_code else {}
    convert(md_path, output_path, template, **kwargs)
    return output_path


@mcp.tool()
async def convert_to_pdf(md_path: str, output_path: str, template: str = "default") -> str:
    """Convert a Markdown file directly to PDF (no DOCX intermediate)."""
    from md_hub.engines.to_pdf import convert
    convert(md_path, output_path, template)
    return output_path


@mcp.tool()
async def convert_to_hwp(md_path: str, output_path: str) -> str:
    """Convert a Markdown file to HWP (한글). Requires Windows + 한컴오피스."""
    from md_hub.engines.to_hwp import convert
    convert(md_path, output_path)
    return output_path


@mcp.tool()
async def convert_to_pptx(md_path: str, output_path: str, slide_count: int = 8, mood: str = "") -> str:
    """Convert a Markdown file to PPTX presentation."""
    from md_hub.engines.to_pptx import convert
    convert(md_path, output_path, slide_count=slide_count, mood=mood)
    return output_path


def main():
    mcp.run()
