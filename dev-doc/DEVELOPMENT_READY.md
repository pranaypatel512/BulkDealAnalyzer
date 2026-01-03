# Development Readiness Checklist

## Branch Preparation Status

### Main Branch ✅
- [x] Sprint 0 foundation complete
- [x] All essential documentation in place
- [x] CI/CD workflows configured
- [x] Security scanning setup
- [x] Pre-commit hooks configured
- [x] Backend skeleton created
- [ ] Frontend structure created (Next.js)
- [ ] Environment configuration validated
- [ ] Database schema ready
- [ ] Development environment tested

### Dev Branch ✅
- [x] Created from main
- [x] Ready for feature development
- [ ] Initial frontend structure (if needed)
- [ ] Development setup validated

## Next Steps to Start Development

### 1. Frontend Setup (Sprint 1)
```bash
# Initialize Next.js frontend
cd frontend
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"
```

### 2. Backend Setup (Sprint 1)
```bash
# Install backend dependencies
cd backend
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy environment template
cp templates/env.example .env.development

# Fill in your credentials:
# - Supabase URL and keys
# - Database connection
# - API keys (if needed)
```

### 4. Database Setup
- [ ] Create Supabase project
- [ ] Run initial migrations
- [ ] Setup Row Level Security (RLS)
- [ ] Create test data (optional)

### 5. Development Server Setup
```bash
# Backend (Terminal 1)
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend
npm run dev
```

## Branch Workflow

### Starting New Feature
```bash
# From dev branch
git checkout dev
git pull origin dev

# Create feature branch
git checkout -b feature/auth-login-implementation

# Develop, commit, push
git add .
git commit -m "feat: implement login functionality"
git push -u origin feature/auth-login-implementation

# Create PR to dev branch
```

### Merging to Dev
```bash
# After PR approval, merge to dev
git checkout dev
git merge feature/auth-login-implementation
git push origin dev
```

### Releasing to Main
```bash
# After testing on dev, merge to main
git checkout main
git merge dev
git tag v0.1.0
git push origin main --tags
```

## Development Commands

### Backend
```bash
# Run tests
cd backend && pytest

# Run with hot reload
cd backend && uvicorn app.main:app --reload

# Check code quality
cd backend && ruff check .
cd backend && ruff format .
```

### Frontend
```bash
# Install dependencies
cd frontend && npm install

# Run development server
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Run tests (when configured)
cd frontend && npm test
```

## Validation Checklist

Before starting development, verify:
- [ ] All tools installed (run `./scripts/check_env.sh`)
- [ ] Environment variables configured
- [ ] Backend server starts successfully
- [ ] Frontend server starts successfully
- [ ] Database connection works
- [ ] Pre-commit hooks working
- [ ] CI/CD pipelines passing

## Ready to Start!

Once all checkboxes are complete, you're ready to begin Sprint 1 development.

