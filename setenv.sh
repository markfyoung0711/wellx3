#!/usr/bin/env bash
# setup-dev.sh — Bootstrap the wellx3 development environment using uv.
#
# Usage:
#   bash setup-dev.sh
#
# After running, activate the venv and work normally:
#   source .venv/bin/activate
#   pytest
#   python3 build.py
#   jupyter lab

set -euo pipefail

# ── 1. Ensure uv is available ─────────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
    echo "Installing uv …"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for the rest of this script
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "uv $(uv --version)"

# ── 2. Create virtualenv (reuse if exists) and install/update dependencies ────
echo ""
if [ -d ".venv" ]; then
    echo "Reusing existing .venv, checking for updates …"
else
    echo "Creating .venv …"
    uv venv
fi
uv pip install -e ".[dev]" --upgrade

# ── 3. Verify key tools are importable ────────────────────────────────────────
echo ""
echo "Verifying installation …"
uv run python -c "import pandas, geopandas, sklearn, xgboost, pytest; print('  All packages OK')"

# ── 4. Ensure Java is available (required for cb2xml) ────────────────────────
echo ""
if command -v java &>/dev/null; then
    echo "Java: $(java -version 2>&1 | head -1)"
else
    echo "Java not found. Installing default-jre-headless …"
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y default-jre-headless
    elif command -v brew &>/dev/null; then
        brew install --cask temurin
    else
        echo "ERROR: Cannot install Java automatically. Install a JRE manually and re-run."
        exit 1
    fi
    echo "Java: $(java -version 2>&1 | head -1)"
fi

# ── 5. Ensure cb2xml is present ───────────────────────────────────────────────
echo ""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CB2XML_JAR="$SCRIPT_DIR/cb2xml/lib/cb2xml.jar"
CB2XML_VERSION="1.01.6"
CB2XML_URL="https://sourceforge.net/projects/cb2xml/files/cb2xml/${CB2XML_VERSION}/cb2xml_Version_${CB2XML_VERSION}.zip/download"
CB2XML_ZIP="/tmp/cb2xml_${CB2XML_VERSION}.zip"

if [ -f "$CB2XML_JAR" ]; then
    echo "cb2xml: $CB2XML_JAR (already present)"
else
    echo "cb2xml not found. Downloading cb2xml ${CB2XML_VERSION} from SourceForge …"
    curl -L --fail --show-error -o "$CB2XML_ZIP" "$CB2XML_URL"
    echo "Extracting …"
    unzip -q "$CB2XML_ZIP" -d "$SCRIPT_DIR/cb2xml"
    rm -f "$CB2XML_ZIP"
    if [ ! -f "$CB2XML_JAR" ]; then
        echo "ERROR: Extraction succeeded but $CB2XML_JAR still missing. Check zip structure."
        exit 1
    fi
    echo "cb2xml installed to $(dirname "$CB2XML_JAR")"
fi

echo ""
echo "Done. Activate the environment with:"
echo "  source .venv/bin/activate"
echo ""
echo "Then run the pipeline:"
echo "  python3 build.py"
echo ""
echo "Or run tests:"
echo "  pytest"
