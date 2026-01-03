#!/usr/bin/env bash
set -e

echo "🚀 Bootstrapping BulkDeal Analyzer development environment..."
echo ""

# Check if template exists
if [ ! -f templates/env.example ]; then
  echo "❌ Missing templates/env.example. Create one or contact maintainers"
  exit 1
fi

# Create .env.development if it doesn't exist
if [ ! -f .env.development ]; then
  cp templates/env.example .env.development
  echo "✅ Created .env.development from .env.example"
  echo "⚠️  Please edit .env.development with your dev credentials"
else
  echo "ℹ️  .env.development already exists"
fi

# Check if docker-compose is available
if command -v docker-compose >/dev/null 2>&1; then
  echo ""
  echo "🐳 Starting local containers (supabase emulator, local db)..."
  if [ -f docker-compose.yml ]; then
    docker-compose up -d || echo "⚠️  Could not start containers. Please check docker-compose.yml"
  else
    echo "ℹ️  docker-compose.yml not found. Skipping container startup."
  fi
else
  echo "⚠️  docker-compose not found — please start required services manually"
fi

# Seed test data if available
if [ -d ./tests/fixtures ]; then
  echo ""
  echo "📦 Test fixtures found in tests/fixtures/"
  if [ -f scripts/seed_test_data.sh ]; then
    echo "🌱 Seeding test data..."
    ./scripts/seed_test_data.sh || echo "⚠️  Could not seed test data"
  else
    echo "ℹ️  Seed script not found. Skipping test data seeding."
  fi
fi

echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env.development with your credentials"
echo "2. Run ./scripts/check_env.sh to validate your environment"
echo "3. Install dependencies:"
echo "   - Backend: cd backend && pip install -r requirements.txt"
echo "   - Frontend: cd frontend && npm install"
echo "4. Start development servers"

