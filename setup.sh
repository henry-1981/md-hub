#!/usr/bin/env bash
# md-hub setup — install all dependencies
set -e
cd "$(dirname "$0")"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }

echo "=== md-hub setup ==="

# pandoc
if command -v pandoc &>/dev/null; then
  ok "pandoc"
else
  echo "pandoc 설치 중..."
  winget install --id JohnMacFarlane.Pandoc -e --accept-source-agreements --accept-package-agreements 2>/dev/null \
    && ok "pandoc" || fail "pandoc — 수동 설치: https://pandoc.org/installing.html"
fi

# Java
if command -v java &>/dev/null; then
  ok "java"
else
  echo "Java 설치 중..."
  winget install --id Microsoft.OpenJDK.21 -e --accept-source-agreements --accept-package-agreements 2>/dev/null \
    && ok "java (터미널 재시작 필요)" || fail "java — 수동 설치: https://adoptium.net"
fi

# Python package
echo "md-hub 패키지 설치 중..."
python -m pip install -e . --quiet \
  && ok "md-hub" || fail "md-hub pip install"

# Playwright
echo "Playwright Chromium 설치 중..."
python -m playwright install chromium 2>/dev/null \
  && ok "playwright chromium" || fail "playwright — python -m playwright install chromium"

# Verify
echo ""
echo "=== 검증 ==="
python -c "from md_hub.server import mcp; print('server OK')" 2>/dev/null && ok "MCP server" || fail "MCP server"
python -c "from md_hub.engines.to_md import convert; print('to_md OK')" 2>/dev/null && ok "to_md engine" || fail "to_md"
python -c "from md_hub.engines.to_docx import convert; print('to_docx OK')" 2>/dev/null && ok "to_docx engine" || fail "to_docx"
python -c "from md_hub.engines.to_pdf import convert; print('to_pdf OK')" 2>/dev/null && ok "to_pdf engine" || fail "to_pdf"

echo ""
echo "=== 사용법 ==="
echo '.mcp.json에 추가:'
echo '  { "mcpServers": { "md-hub": { "command": "md-hub" } } }'
