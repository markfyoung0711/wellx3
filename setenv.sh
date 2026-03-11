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

# ── 4. Check Java is available (required for cb2xml) ─────────────────────────
echo ""
if command -v java &>/dev/null; then
    echo "Java: $(java -version 2>&1 | head -1)"
else
    echo "WARNING: Java not found. cb2xml requires Java to run."
    echo "         Install with: sudo apt-get install default-jre-headless"
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
