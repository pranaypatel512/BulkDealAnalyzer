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

# Get download URL from GitHub API
echo "Fetching download URL..."
DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/gitleaks/gitleaks/releases/latest" | grep "browser_download_url.*linux.*${ARCH}" | cut -d '"' -f 4)

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

# Install to /usr/local/bin (requires sudo)
if [ -w /usr/local/bin ]; then
    mv gitleaks /usr/local/bin/
    chmod +x /usr/local/bin/gitleaks
else
    echo "⚠️  /usr/local/bin is not writable. Using sudo..."
    sudo mv gitleaks /usr/local/bin/
    sudo chmod +x /usr/local/bin/gitleaks
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

