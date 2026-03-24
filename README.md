# md-hub

문서 변환 MCP 서버. 마크다운을 허브로 양방향 변환합니다.

```
기존 문서 (PDF, DOCX, PPTX, XLSX, HTML...)
        │
        ▼  convert_to_md
    Markdown (.md)
        │
   ┌────┼────────┐
   ▼    ▼        ▼
 DOCX  PDF     PPTX
```

## 설치

```bash
pip install markdown-hub
playwright install chromium
```

외부 의존성 (자동 설치 스크립트 제공):
```bash
bash setup.sh
```

## MCP 설정

`.mcp.json` 또는 Claude Desktop 설정에 추가:

```json
{
  "mcpServers": {
    "md-hub": {
      "command": "md-hub"
    }
  }
}
```

## 도구

| 도구 | 설명 | 입력 | 출력 |
|------|------|------|------|
| `convert_to_md` | 기존 문서 → Markdown | PDF, DOCX, PPTX, XLSX, HTML... | MD 텍스트 |
| `convert_to_docx` | Markdown → Word | .md 파일 + 템플릿 | .docx |
| `convert_to_pdf` | Markdown → PDF (다이렉트) | .md 파일 + 템플릿 | .pdf |
| `convert_to_pptx` | Markdown → 발표자료 | .md 파일 | .pptx |

## 사용 예시

AI 채팅에서 자연어로:

- "이 PDF를 마크다운으로 변환해줘"
- "report.md를 PDF로 만들어줘"
- "이 문서를 docx로 변환해"

## 지원 플랫폼

MCP를 지원하는 모든 AI 클라이언트:

- Claude Desktop / Claude Code
- ChatGPT (Team/Business/Enterprise)
- Gemini (Google Cloud MCP)
- Cursor, Windsurf, VS Code
- 기타 MCP 호환 클라이언트

## 템플릿

기본 템플릿(Malgun Gothic, A4)이 내장되어 있습니다.
커스텀 템플릿은 `templates/` 디렉토리에 YAML 파일로 추가할 수 있습니다.

```yaml
# templates/my-template.yaml
templates:
  my-style:
    extends: default
    font:
      heading: Arial
    colors:
      heading: "#0066CC"
```

## 의존성

- Python 3.10+
- pandoc (DOCX 변환용)
- Playwright + Chromium (PDF 변환용)
- Java (디지털 PDF 변환 시 opendataloader 사용, 선택)

## 라이선스

MIT
