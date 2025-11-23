#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

print_usage() {
  cat <<EOF
Usage: $(basename "$0") [--yes]

Builds the package and uploads to PyPI using the PYPI_API_TOKEN found in .env at the repo root.

Options:
  --yes    Run non-interactively (no confirmation prompt)

Security: Do NOT commit your token. Keep it in .env or an environment variable.
EOF
}

CONFIRM=yes
if [ "${1:-}" = "--yes" ]; then
  CONFIRM=no
fi

if [ ! -f .env ]; then
  echo "Error: .env file not found in repo root ($REPO_ROOT). Create .env with PYPI_API_TOKEN." >&2
  exit 1
fi

# Extract PYPI_API_TOKEN robustly (handles quotes and = in value)
PYPI_API_TOKEN=$(awk -F'=' '/^PYPI_API_TOKEN/ { $1=""; sub(/^=/,""); val=$0; gsub(/^\s+|\s+$/,"",val); gsub(/^\"|\"$/,"",val); print val; exit }' .env)

if [ -z "$PYPI_API_TOKEN" ]; then
  echo "Error: PYPI_API_TOKEN not found or empty in .env" >&2
  exit 1
fi

echo "Found PYPI token in .env (will not display it)."

if [ "$CONFIRM" = "yes" ]; then
  read -r -p "Build package and upload to PyPI? (y/N): " resp
  case "$resp" in
    [yY][eE][sS]|[yY]) ;;
    *) echo "Aborted"; exit 1;;
  esac
fi


# Find a usable python executable
if command -v python3 >/dev/null 2>&1; then
  PY_CMD=python3
elif command -v python >/dev/null 2>&1; then
  PY_CMD=python
else
  echo "Error: neither 'python3' nor 'python' is available on PATH. Please install Python 3 (eg. 'brew install python') and retry." >&2
  exit 127
fi

echo "Installing build dependencies..."
$PY_CMD -m pip install --upgrade pip build twine >/dev/null

echo "Building package..."
$PY_CMD -m build

echo "Uploading to PyPI via twine..."
# Use twine non-interactively with __token__ username
TWINE_USERNAME=__token__ TWINE_PASSWORD="$PYPI_API_TOKEN" $PY_CMD -m twine upload dist/* --non-interactive

echo "Upload finished. You may want to tag/release the repo if not already done."
