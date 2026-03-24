#!/usr/bin/env bash
# md-hub setup — document ecosystem one-click setup
# Usage: ./setup.sh [--mcp-target <path>]
#
# --mcp-target: .mcp.json merge target (default: ~/.claude/.mcp.json)

set +e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MCP_TARGET="${HOME}/.claude/.mcp.json"
SUMMARY=()

while [[ $# -gt 0 ]]; do
    case $1 in
        --mcp-target) MCP_TARGET="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

info()  { echo "[INFO]  $1"; }
warn()  { echo "[WARN]  $1"; }
ok()    { echo "[OK]    $1"; SUMMARY+=("✓ $1"); }
skip()  { echo "[SKIP]  $1"; SUMMARY+=("- $1 (skipped)"); }
fail()  { echo "[FAIL]  $1"; SUMMARY+=("✗ $1"); }

is_windows() {
    [[ "$(uname -s)" == *"MINGW"* || "$(uname -s)" == *"MSYS"* || "$(uname -s)" == *"NT"* ]]
}

step_migrate() {
    if command -v md-hub &>/dev/null; then
        warn "md-hub v0.1.0 MCP server detected. Removing..."
        pip uninstall -y markdown-hub 2>/dev/null
        ok "markdown-hub PyPI package removed"
        warn "If your .mcp.json has an 'md-hub' key, please remove it manually."
    fi
}

step_system_tools() {
    info "Checking system tools..."
    if command -v pandoc &>/dev/null; then
        ok "pandoc $(pandoc --version | head -1)"
    else
        fail "pandoc not found — MD→DOCX will not work. Install: https://pandoc.org/installing.html"
    fi
    if command -v java &>/dev/null; then
        ok "Java $(java -version 2>&1 | head -1)"
    else
        skip "Java not found — digital PDF→MD will use Claude Vision fallback"
    fi
    if command -v pdftoppm &>/dev/null; then
        ok "poppler (pdftoppm found)"
    else
        skip "poppler not found — pymupdf fallback for PDF→image"
    fi
}

step_python() {
    info "Installing Python dependencies..."
    if pip install -r "$SCRIPT_DIR/requirements.txt"; then
        ok "Python dependencies installed"
    else
        fail "pip install failed"
        return
    fi
    info "Installing Chromium for Playwright..."
    if python -m playwright install chromium; then
        ok "Chromium installed"
    else
        fail "Chromium install failed — MD→PDF and MD→PPTX will not work"
    fi
}

step_nodejs() {
    if ! command -v node &>/dev/null; then
        fail "Node.js not found — presentation (PPTX) will not work"
        return
    fi
    info "Installing Node.js dependencies for presentation..."
    if (cd "$SCRIPT_DIR/presentation" && npm install); then
        ok "Node.js dependencies installed"
    else
        fail "npm install failed"
        return
    fi
    info "Building presentation TypeScript..."
    if (cd "$SCRIPT_DIR/presentation" && ./node_modules/.bin/tsc); then
        ok "presentation built"
    else
        fail "TypeScript build failed — presentation PPTX will not work"
    fi
}

step_hwp() {
    if ! is_windows; then
        skip "HWP — Windows only (current: $(uname -s))"
        return
    fi
    if [ -d "/c/Program Files (x86)/HNC" ] || [ -d "/c/Program Files/HNC" ]; then
        info "한컴오피스 detected"
        if [ ! -d "$HOME/tools/hwp-mcp" ]; then
            info "Cloning hwp-mcp..."
            git clone https://github.com/jkf87/hwp-mcp.git "$HOME/tools/hwp-mcp"
            (cd "$HOME/tools/hwp-mcp" && python -m venv .venv && .venv/Scripts/pip install -r requirements.txt)
        fi
        ok "HWP MCP ready"
    else
        skip "HWP — 한컴오피스 not detected"
    fi
}

step_skills() {
    info "Registering skills to ~/.claude/skills/..."
    mkdir -p "$HOME/.claude/skills"
    for skill_dir in "$SCRIPT_DIR"/skills/*/; do
        skill_name=$(basename "$skill_dir")
        target="$HOME/.claude/skills/$skill_name"
        if [ -e "$target" ]; then
            skip "Skill '$skill_name' already exists at $target"
        else
            if is_windows; then
                if ln -s "$skill_dir" "$target" 2>/dev/null; then
                    ok "Skill '$skill_name' linked"
                else
                    cp -r "$skill_dir" "$target"
                    ok "Skill '$skill_name' copied (symlink unavailable)"
                fi
            else
                ln -s "$skill_dir" "$target"
                ok "Skill '$skill_name' linked"
            fi
        fi
    done
}

step_mcp() {
    info "Merging MCP config into $MCP_TARGET..."
    if [ ! -f "$MCP_TARGET" ]; then
        mkdir -p "$(dirname "$MCP_TARGET")"
        python -c "
import json
data = {'mcpServers': {'word': {'command': 'uvx', 'args': ['--from', 'office-word-mcp-server==1.1.11', 'word_mcp_server']}}}
with open('$MCP_TARGET', 'w') as f:
    json.dump(data, f, indent=2)
"
        ok ".mcp.json created with word MCP"
    else
        if python -c "import json; d=json.load(open('$MCP_TARGET')); exit(0 if 'word' in d.get('mcpServers',{}) else 1)" 2>/dev/null; then
            skip "word MCP already registered in $MCP_TARGET"
        else
            python -c "
import json
with open('$MCP_TARGET') as f:
    data = json.load(f)
data.setdefault('mcpServers', {})
data['mcpServers']['word'] = {'command': 'uvx', 'args': ['--from', 'office-word-mcp-server==1.1.11', 'word_mcp_server']}
with open('$MCP_TARGET', 'w') as f:
    json.dump(data, f, indent=2)
"
            ok "word MCP added to $MCP_TARGET"
        fi
    fi
    if [ -d "$HOME/tools/hwp-mcp" ]; then
        HWP_PYTHON="$(cd "$HOME/tools/hwp-mcp" && pwd)/.venv/Scripts/python.exe"
        HWP_SCRIPT="$(cd "$HOME/tools/hwp-mcp" && pwd)/hwp_mcp_stdio_server.py"
        if python -c "import json; d=json.load(open('$MCP_TARGET')); exit(0 if 'hwp' in d.get('mcpServers',{}) else 1)" 2>/dev/null; then
            skip "hwp MCP already registered"
        else
            python -c "
import json
with open('$MCP_TARGET') as f:
    data = json.load(f)
data['mcpServers']['hwp'] = {
    'command': '${HWP_PYTHON}'.replace('\\\\', '/'),
    'args': ['${HWP_SCRIPT}'.replace('\\\\', '/')]
}
with open('$MCP_TARGET', 'w') as f:
    json.dump(data, f, indent=2)
"
            ok "hwp MCP added to $MCP_TARGET"
        fi
    fi
}

step_env() {
    info "Setting MD_HUB_HOME environment variable..."
    SHELL_RC=""
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        SHELL_RC="$HOME/.bash_profile"
    fi
    if [ -z "$SHELL_RC" ]; then
        SHELL_RC="$HOME/.bashrc"
        touch "$SHELL_RC"
    fi
    if grep -q "MD_HUB_HOME" "$SHELL_RC" 2>/dev/null; then
        skip "MD_HUB_HOME already set in $SHELL_RC"
    else
        echo "" >> "$SHELL_RC"
        echo "# md-hub document ecosystem" >> "$SHELL_RC"
        echo "export MD_HUB_HOME=\"$SCRIPT_DIR\"" >> "$SHELL_RC"
        ok "MD_HUB_HOME=$SCRIPT_DIR added to $SHELL_RC"
    fi
    export MD_HUB_HOME="$SCRIPT_DIR"
}

echo "========================================"
echo "  md-hub setup — document ecosystem"
echo "========================================"
echo ""

step_migrate
step_system_tools
step_python
step_nodejs
step_hwp
step_skills
step_mcp
step_env

echo ""
echo "========================================"
echo "  Setup Summary"
echo "========================================"
for line in "${SUMMARY[@]}"; do
    echo "  $line"
done
echo ""
echo "Run 'source ~/.bashrc' (or restart terminal) to activate MD_HUB_HOME."
echo "Done."
