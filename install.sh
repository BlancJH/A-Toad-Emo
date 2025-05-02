set -e

REQUIRED_PYTHON_VERSION="3.11"
CLI_NAME="a-toad-emo"
PYPI_PACKAGE="a-toad-emo"

# 1. Check if Python is installed
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 is not installed."
  echo "➡️  Install it from https://www.python.org/downloads/"
  exit 1
fi

# 2. Check Python version
version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(printf '%s\n' "$REQUIRED_PYTHON_VERSION" "$version" | sort -V | head -n1) != "$REQUIRED_PYTHON_VERSION" ]]; then
  echo "❌ Python >= $REQUIRED_PYTHON_VERSION is required (found: $version)"
  exit 1
fi

echo "✅ Python $version detected."

# 3. Check if pipx is installed
if ! command -v pipx &>/dev/null; then
  echo "ℹ️ pipx not found. Installing pipx..."
  python3 -m pip install --user pipx
  python3 -m pipx ensurepath
  echo "✅ pipx installed. Please restart your shell if command not found."
fi

# 4. Install or upgrade the CLI
if pipx list | grep -q "$CLI_NAME"; then
  echo "🔄 Updating $CLI_NAME via pipx..."
  pipx upgrade "$PYPI_PACKAGE"
else
  echo "⬇️ Installing $CLI_NAME via pipx..."
  pipx install "$PYPI_PACKAGE"
fi

echo "🎉 Installation complete. Run with: $CLI_NAME --help"
