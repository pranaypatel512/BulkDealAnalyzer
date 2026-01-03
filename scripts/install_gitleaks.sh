#!/usr/bin/env bash
set -e

echo "🔍 Installing gitleaks for secret scanning..."
echo ""

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    ARCH="amd64"
elif [ "$ARCH" = "aarch64" ]; then
    ARCH="arm64"
else
    echo "❌ Unsupported architecture: $ARCH"
    exit 1
fi

# Get latest version
echo "Fetching latest gitleaks version..."
GITLEAKS_VERSION=$(curl -s https://api.github.com/repos/gitleaks/gitleaks/releases/latest | grep "tag_name" | cut -d '"' -f 4)

if [ -z "$GITLEAKS_VERSION" ]; then
    echo "❌ Failed to fetch latest version"
    exit 1
fi

echo "Latest version: $GITLEAKS_VERSION"
echo "Architecture: $ARCH"
echo ""

# Map architecture to gitleaks naming
if [ "$ARCH" = "amd64" ] || [ "$ARCH" = "x86_64" ]; then
    GITLEAKS_ARCH="x64"
elif [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ]; then
    GITLEAKS_ARCH="arm64"
else
    echo "❌ Unsupported architecture: $ARCH"
    exit 1
fi

# Get download URL from GitHub API
echo "Fetching download URL for linux_${GITLEAKS_ARCH}..."
DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/gitleaks/gitleaks/releases/latest" | python3 -c "import sys, json; data=json.load(sys.stdin); [print(asset['browser_download_url']) for asset in data['assets'] if f'linux_{GITLEAKS_ARCH}' in asset['name']]" 2>/dev/null | head -1)

if [ -z "$DOWNLOAD_URL" ]; then
    echo "❌ Failed to fetch download URL"
    exit 1
fi

echo "Downloading from: $DOWNLOAD_URL"
cd /tmp

# Download and extract
curl -L -o gitleaks.tar.gz "$DOWNLOAD_URL" || {
    echo "❌ Failed to download gitleaks"
    exit 1
}

tar -xzf gitleaks.tar.gz gitleaks || {
    echo "❌ Failed to extract gitleaks"
    exit 1
}

# Install to ~/.local/bin (user directory, no sudo needed)
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"
mv gitleaks "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/gitleaks"

# Add to PATH if not already there
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo ""
    echo "⚠️  Adding $INSTALL_DIR to PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
    echo "✅ Added to ~/.bashrc (restart terminal or run: source ~/.bashrc)"
fi

# Cleanup
rm -f gitleaks.tar.gz

# Verify installation
if command -v gitleaks >/dev/null 2>&1; then
    echo ""
    echo "✅ gitleaks installed successfully!"
    echo "Version: $(gitleaks version)"
    echo ""
    echo "You can now run: gitleaks detect --source ."
else
    echo "❌ Installation failed - gitleaks not found in PATH"
    exit 1
fi

