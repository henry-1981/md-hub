# md-hub

조직의 암묵지를 명시지로 바꾸는 첫걸음.

흩어진 문서(PDF, DOCX, PPTX...)를 마크다운으로 모으고, 마크다운에서 필요한 포맷으로 내보내는 MCP 서버입니다.

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

## 지원 환경

md-hub는 MCP(Model Context Protocol) 서버입니다. **MCP 클라이언트가 있는 로컬 에이전트 환경**에서 동작합니다.

| 환경 | 지원 | 비고 |
|------|------|------|
| **Claude Code** (CLI) | ✅ | `.mcp.json` 설정 |
| **Claude Desktop** | ✅ | 설정 파일에서 MCP 서버 등록 |
| **Cursor, Windsurf** 등 AI IDE | ✅ | MCP 설정 지원 |
| **Codex CLI** (OpenAI) | ✅ | MCP 지원 |
| ChatGPT 웹/앱 | ❌ | 사용자 정의 MCP 연결 불가 (폐쇄형) |
| Gemini 웹/앱 | ❌ | 사용자 정의 MCP 연결 불가 |

> ChatGPT/Gemini 웹 채팅은 MCP를 지원하지 않습니다.
> 이 도구는 로컬에서 MCP 클라이언트를 실행할 수 있는 환경에서 사용합니다.

## 설치

### Step 1: 패키지 설치

```bash
pip install markdown-hub
```

### Step 2: 외부 의존성 (사용할 도구에 따라)

```bash
# PDF 변환을 사용하려면
playwright install chromium

# DOCX 변환을 사용하려면
# pandoc 설치: https://pandoc.org/installing.html
# Windows: winget install JohnMacFarlane.Pandoc
# macOS: brew install pandoc

# HWP 변환을 사용하려면 (Windows 전용)
# 한컴오피스 설치 필요
pip install pywin32
```

### Step 3: MCP 서버 등록

설치만으로는 동작하지 않습니다. AI 클라이언트에 MCP 서버를 등록해야 합니다.

**Claude Code** — 프로젝트 루트의 `.mcp.json`에 추가:

```json
{
  "mcpServers": {
    "md-hub": {
      "command": "md-hub"
    }
  }
}
```

**Claude Desktop** — 설정 파일(`claude_desktop_config.json`)에 추가:

```json
{
  "mcpServers": {
    "md-hub": {
      "command": "md-hub"
    }
  }
}
```

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Cursor** — Settings → MCP Servers → Add Server:

```
Name: md-hub
Command: md-hub
```

등록 후 AI 클라이언트를 **재시작**하면 도구가 활성화됩니다.

### Step 4: 동작 확인

AI 채팅에서:
```
"convert_to_md 도구가 보이나요?"
```

또는 터미널에서 직접:
```bash
md-hub  # MCP 서버 실행 (클라이언트가 자동으로 호출하므로 수동 실행은 불필요)
```

## 도구

### convert_to_md — 기존 문서 → Markdown

PDF, DOCX, PPTX, XLSX, HTML 등 대부분의 문서 포맷을 마크다운으로 변환합니다.

- 디지털 PDF: markitdown으로 텍스트 추출
- 스캔 PDF: AI Vision API 필요 (자동 감지 후 안내)
- 그 외: markitdown 범용 변환

### convert_to_docx — Markdown → Word

마크다운을 DOCX로 변환합니다. 템플릿으로 스타일을 제어합니다.

- pandoc + python-docx 기반
- 템플릿별 커버 병합, heading 번호매기기, 테이블 스타일 자동 적용
- **필수**: pandoc

### convert_to_pdf — Markdown → PDF (다이렉트)

마크다운을 DOCX를 거치지 않고 직접 PDF로 변환합니다.

- HTML + CSS 렌더링 → Playwright(Chromium)로 PDF 생성
- 동일한 템플릿 시스템으로 스타일 제어
- **필수**: Playwright + Chromium

### convert_to_hwp — Markdown → 한글

마크다운을 HWP(한글) 문서로 변환합니다.

- 한컴오피스 COM 자동화 방식
- **필수**: Windows + 한컴오피스
- 비-Windows 환경에서는 사용 불가

### convert_to_pptx — Markdown → 발표자료

마크다운을 PPTX 발표자료로 변환합니다.

- HTML 슬라이드 → Playwright 렌더링 → pptxgenjs 조립
- **필수**: Node.js (별도 설치 필요, 통합 예정)

## 환경별 도구 가용성

| 도구 | Windows | macOS | Linux | 추가 요구사항 |
|------|---------|-------|-------|--------------|
| convert_to_md | ✅ | ✅ | ✅ | — |
| convert_to_docx | ✅ | ✅ | ✅ | pandoc |
| convert_to_pdf | ✅ | ✅ | ✅ | Playwright + Chromium |
| convert_to_hwp | ✅ | — | — | 한컴오피스 |
| convert_to_pptx | ✅ | ✅ | ✅ | Node.js (별도 설치) |

## 사용 예시

MCP 클라이언트(Claude Code, Claude Desktop 등)에서 자연어로:

```
"이 PDF를 마크다운으로 변환해줘"
"report.md를 PDF로 만들어줘"
"이 문서를 docx로 변환해"
"한글 파일로 만들어줘"
```

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

## 라이선스

MIT
