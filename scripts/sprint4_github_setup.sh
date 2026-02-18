#!/usr/bin/env bash
# Sprint 4 – Create milestone and issues in GitHub
# Prerequisite: gh auth login
# Usage: ./scripts/sprint4_github_setup.sh

set -e
REPO="${GITHUB_REPO:-pranaypatel512/BulkDealAnalyzer}"

echo "1. Creating Sprint 4 milestone..."
gh milestone create "Sprint 4 - Analytics Polish" --repo "$REPO" || true

echo "2. Creating issues..."
gh issue create --repo "$REPO" --title "Analytics: Add pagination to Bulk Deals table" \
  --body "Add Previous/Next and page indicator to the Bulk Deals table. Use \`page\` and \`page_size\` query params.
Branch: \`feature/analytics-pagination\`
Sprint: Sprint 4" \
  --label "enhancement" 2>/dev/null || gh issue create --repo "$REPO" --title "Analytics: Add pagination to Bulk Deals table" --body "Add Previous/Next and page indicator. Branch: feature/analytics-pagination"

gh issue create --repo "$REPO" --title "Analytics: Add CSV upload to Bulk Deals tab" \
  --body "Add Upload CSV on Analytics Bulk Deals tab. Call POST /api/v1/bulk-deals/upload-csv; refresh table after.
Branch: \`feature/analytics-csv-upload\`
Sprint: Sprint 4" \
  --label "enhancement" 2>/dev/null || gh issue create --repo "$REPO" --title "Analytics: Add CSV upload to Bulk Deals tab" --body "Upload CSV in Analytics. Branch: feature/analytics-csv-upload"

gh issue create --repo "$REPO" --title "Export filtered Bulk Deals to CSV" \
  --body "Export current filtered Bulk Deals from Analytics to CSV.
Branch: \`feature/export-csv\`
Sprint: Sprint 4" \
  --label "enhancement" 2>/dev/null || gh issue create --repo "$REPO" --title "Export filtered Bulk Deals to CSV" --body "Export to CSV. Branch: feature/export-csv"

echo "Done. In GitHub: Issues → edit each issue → set milestone to 'Sprint 4 - Analytics Polish'."
