#!/usr/bin/env bash
set -e

echo "🔍 Running pre-commit checks..."
echo ""

errors=0

# Check for .env files
if find . -name ".env*" -not -name ".env.example" -not -name "templates/env.example" | grep -q .; then
    echo "❌ ERROR: Found .env files (should not be committed)"
    find . -name ".env*" -not -name ".env.example" -not -name "templates/env.example"
    errors=$((errors+1))
else
    echo "✅ No .env files found"
fi

# Check for secrets using gitleaks
if command -v gitleaks >/dev/null 2>&1; then
    echo ""
    echo "Running gitleaks secret scan..."
    if gitleaks detect --source . --verbose --no-git 2>&1 | grep -q "No leaks found"; then
        echo "✅ gitleaks: No secrets found"
    else
        echo "⚠️  gitleaks: Potential secrets detected (review output above)"
        gitleaks detect --source . --verbose --no-git 2>&1 | head -10
    fi
else
    echo "⚠️  gitleaks not installed - skipping secret scan"
    echo "   Install: https://github.com/gitleaks/gitleaks#installation"
fi

# Check Python syntax
if command -v python3 >/dev/null 2>&1; then
    echo ""
    echo "Checking Python syntax..."
    if python3 -m py_compile backend/app/main.py backend/app/core/parser.py backend/app/core/models.py 2>&1; then
        echo "✅ Python syntax check passed"
    else
        echo "❌ ERROR: Python syntax errors found"
        errors=$((errors+1))
    fi
else
    echo "⚠️  python3 not found - skipping syntax check"
fi

# Check for large files
if find . -type f -size +1M -not -path "./.git/*" -not -path "./node_modules/*" | grep -q .; then
    echo "⚠️  WARNING: Large files found (>1MB)"
    find . -type f -size +1M -not -path "./.git/*" -not -path "./node_modules/*" | head -5
else
    echo "✅ No large files found"
fi

echo ""
if [ $errors -gt 0 ]; then
    echo "❌ Pre-commit checks failed with $errors error(s)"
    exit 1
else
    echo "✅ All pre-commit checks passed"
    exit 0
fi

