# md-hub

조직의 암묵지를 명시지로 바꾸는 첫걸음.

흩어진 문서(PDF, DOCX, PPTX...)를 마크다운으로 모으고, 마크다운에서 필요한 포맷으로 내보내는 MCP 서버입니다. AI 채팅에서 자연어로 문서를 변환할 수 있습니다.

```
기존 문서 (PDF, DOCX, PPTX, XLSX, HTML...)
        │
        ▼  convert_to_md
    Markdown (.md)  ← 중심 허브
        │             분석 · 검색 · LLM 활용 · 버전 관리
        │
   ┌────┼────────┬────────┐
   ▼    ▼        ▼        ▼
 DOCX  PDF      HWP     PPTX
```

## 설치

```bash
pip install markdown-hub
playwright install chromium
```

외부 의존성 자동 설치:
```bash
bash setup.sh
```

## MCP 설정

`.mcp.json` 또는 AI 클라이언트 설정에 추가:

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

### convert_to_md — 기존 문서 → Markdown

PDF, DOCX, PPTX, XLSX, HTML 등 대부분의 문서 포맷을 마크다운으로 변환합니다.

- 디지털 PDF: markitdown으로 텍스트 추출
- 스캔 PDF: AI Vision API 필요 (자동 감지)
- 그 외: markitdown 범용 변환

### convert_to_docx — Markdown → Word

마크다운을 DOCX로 변환합니다. 템플릿으로 스타일(폰트, 색상, 번호매기기 등)을 제어합니다.

- pandoc + python-docx 기반
- 템플릿별 커버 병합, heading 번호매기기, 테이블 스타일 자동 적용
- **필수**: pandoc

### convert_to_pdf — Markdown → PDF (다이렉트)

마크다운을 DOCX를 거치지 않고 직접 PDF로 변환합니다.

- HTML + CSS 렌더링 → Playwright(Chromium)로 PDF 생성
- 동일한 템플릿 시스템으로 스타일 제어
- **필수**: Playwright + Chromium (`playwright install chromium`)

### convert_to_hwp — Markdown → 한글

마크다운을 HWP(한글) 문서로 변환합니다.

- 한컴오피스 COM 자동화 방식
- **필수**: Windows + 한컴오피스 설치
- 비-Windows 환경에서는 사용 불가 (에러 메시지로 안내)

### convert_to_pptx — Markdown → 발표자료

마크다운을 PPTX 발표자료로 변환합니다.

- HTML 슬라이드 생성 → Playwright 렌더링 → pptxgenjs 조립
- **필수**: Node.js + presentation 프로젝트 설치
- 현재 별도 설치 필요 (통합 예정)

## 사용 예시

AI 채팅에서 자연어로:

```
"이 PDF를 마크다운으로 변환해줘"
"report.md를 PDF로 만들어줘"
"이 문서를 docx로 변환해"
"한글 파일로 만들어줘"
```

## 지원 플랫폼

MCP(Model Context Protocol)를 지원하는 모든 AI 클라이언트에서 사용 가능합니다:

| 플랫폼 | 지원 |
|--------|------|
| Claude Desktop / Claude Code | ✅ |
| ChatGPT (Team/Business/Enterprise) | ✅ |
| Gemini (Google Cloud MCP) | ✅ |
| Cursor, Windsurf, VS Code | ✅ |
| 기타 MCP 호환 클라이언트 | ✅ |

## 환경별 도구 가용성

모든 도구가 모든 환경에서 동작하지는 않습니다:

| 도구 | Windows | macOS | Linux | 추가 요구사항 |
|------|---------|-------|-------|--------------|
| convert_to_md | ✅ | ✅ | ✅ | — |
| convert_to_docx | ✅ | ✅ | ✅ | pandoc |
| convert_to_pdf | ✅ | ✅ | ✅ | Playwright + Chromium |
| convert_to_hwp | ✅ | — | — | 한컴오피스 |
| convert_to_pptx | ✅ | ✅ | ✅ | Node.js (별도 설치) |

## 템플릿

기본 템플릿(Malgun Gothic, A4)이 내장되어 있습니다.
커스텀 템플릿은 YAML 파일로 추가할 수 있습니다:

```yaml
templates:
  my-style:
    extends: default
    font:
      heading: Arial
    colors:
      heading: "#0066CC"
      table_header_bg: "#E8F0FE"
```

DOCX와 PDF 모두 동일한 템플릿을 공유합니다.

## 의존성

**필수:**
- Python 3.10+

**도구별 (사용하는 도구만 설치하면 됨):**
- pandoc — DOCX 변환 (`convert_to_docx`)
- Playwright + Chromium — PDF 변환 (`convert_to_pdf`)
- 한컴오피스 — HWP 변환 (`convert_to_hwp`, Windows 전용)
- Java — 디지털 PDF 고품질 변환 (선택)

## 라이선스

MIT
