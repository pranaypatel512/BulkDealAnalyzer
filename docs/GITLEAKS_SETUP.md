# Gitleaks Setup Guide

## What is Gitleaks?

Gitleaks is a secret scanning tool that detects hardcoded secrets, API keys, passwords, and other sensitive information in your codebase.

## Installation

### Option 1: Using the Installation Script (Recommended)

```bash
./scripts/install_gitleaks.sh
```

This script will:
- Detect your system architecture
- Download the latest gitleaks release
- Install it to `/usr/local/bin`
- Verify the installation

### Option 2: Manual Installation

1. **Download the latest release**:
   ```bash
   # For Linux AMD64
   curl -L https://github.com/gitleaks/gitleaks/releases/download/v8.30.0/gitleaks_8.30.0_linux_amd64.tar.gz -o gitleaks.tar.gz
   
   # Extract
   tar -xzf gitleaks.tar.gz
   
   # Install
   sudo mv gitleaks /usr/local/bin/
   sudo chmod +x /usr/local/bin/gitleaks
   ```

2. **Verify installation**:
   ```bash
   gitleaks version
   ```

### Option 3: Using Package Managers

**Homebrew (macOS/Linux)**:
```bash
brew install gitleaks
```

**Snap (Linux)**:
```bash
sudo snap install gitleaks
```

## Usage

### Run Secret Scan

```bash
# Scan current directory
gitleaks detect --source . --verbose

# Scan without git history (faster)
gitleaks detect --source . --verbose --no-git
```

### Integration with Pre-commit

The `scripts/pre_commit_check.sh` script automatically uses gitleaks if installed:

```bash
./scripts/pre_commit_check.sh
```

### CI/CD Integration

Gitleaks is already configured in `.github/workflows/security-scan.yml` to run on pull requests.

## What Gitleaks Detects

- API keys (AWS, Google, GitHub, etc.)
- Passwords and credentials
- Database connection strings
- Private keys
- Tokens and secrets
- And more...

## Configuration

Gitleaks uses default rules, but you can customize detection by creating a `.gitleaksignore` file or `gitleaks.toml` configuration file.

## Troubleshooting

### "gitleaks not found"

1. Check if gitleaks is in PATH:
   ```bash
   which gitleaks
   ```

2. If not found, ensure `/usr/local/bin` is in your PATH:
   ```bash
   echo $PATH | grep /usr/local/bin
   ```

3. Reinstall using the installation script:
   ```bash
   ./scripts/install_gitleaks.sh
   ```

### False Positives

If gitleaks detects false positives, you can:
- Add patterns to `.gitleaksignore`
- Configure custom rules in `gitleaks.toml`
- Review and whitelist specific findings

## Resources

- [Gitleaks GitHub](https://github.com/gitleaks/gitleaks)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks#documentation)
- [Latest Releases](https://github.com/gitleaks/gitleaks/releases)

