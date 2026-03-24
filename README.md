# md-hub

마크다운을 허브로 한 문서 변환 생태계. Claude Code에서 자연어로 문서를 변환합니다.

## 지원 변환

| 입력 → 출력 | 엔진 | 필수 도구 |
|-------------|------|----------|
| 기존 문서 → MD | markitdown | - |
| 디지털 PDF → MD | opendataloader | Java 21 |
| 스캔 PDF → MD | Claude Vision | Anthropic API key |
| MD → DOCX | python-docx + pandoc | pandoc |
| MD → PDF | Playwright HTML→PDF | Chromium |
| MD → PPTX | pptxgenjs | Node.js + Chromium |
| MD → HWP | COM 자동화 | Windows + 한컴오피스 |

## 설치

```bash
git clone https://github.com/henry-1981/md-hub.git
cd md-hub
./setup.sh
source ~/.bashrc
```

setup.sh가 자동으로:
1. 기존 md-hub v0.1.0 감지 시 마이그레이션
2. 시스템 도구 확인 (pandoc, Java, Chromium 등)
3. Python + Node.js 의존성 설치
4. HWP 지원 설정 (Windows + 한컴오피스 감지 시)
5. Claude Code 스킬 등록 (`~/.claude/skills/`)
6. word MCP 서버 설정 (`.mcp.json` 병합)
7. `MD_HUB_HOME` 환경 변수 설정

## 사용법

Claude Code에서 자연어로:

- "이 PDF를 마크다운으로 변환해줘"
- "report.md를 DOCX로 만들어줘"
- "이 문서 PDF로 변환해"
- "발표자료 만들어줘"

## 요구사항

- Python 3.10+
- Node.js 18+ (presentation용)
- Claude Code
- pandoc (DOCX 변환)
- Chromium (setup.sh가 자동 설치)

## v0.1.0에서 전환

이전에 `pip install markdown-hub`로 MCP 서버를 설치했다면, setup.sh가 자동으로 감지하여 제거합니다. 수동 전환:

```bash
pip uninstall markdown-hub
# .mcp.json에서 "md-hub" 키 제거
```

## 라이선스

MIT
