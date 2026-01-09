# GitHub Project Setup - Step-by-Step Guide

## Creating the Project Board

When you create a new GitHub Project, you'll see the "Bulk import items" option. **This is exactly what we want!**

### Step 1: Start Project Creation
1. Go to: https://github.com/pranaypatel512/BulkDealAnalyzer/projects/new
2. Choose **"Board"** template
3. Name it: **"BulkDeal Analyzer Development"**

### Step 2: Bulk Import Items (Important!)

When you see:
> "Bulk import items - All new and existing items from the selected source will be added to this project."

**DO THIS:**
1. ✅ **Select "Repository"** as the source
2. ✅ **Select your repository**: `pranaypatel512/BulkDealAnalyzer`
3. This will automatically add:
   - All existing issues (including #9, #10, #11, #12)
   - Future issues and PRs

**Benefits:**
- All Sprint 1 issues will automatically appear in the project
- Future issues will automatically be added
- PRs linked to issues will automatically appear

### Step 3: Configure Project Columns

After import, you'll have default columns. **Configure them to match this workflow:**

1. 📋 **Backlog** - Planned features and tasks (not started)
2. 📝 **TODO** - Tasks ready to start, assigned to developer
3. 🔄 **In Progress** - Active development
4. 👀 **Review** - PRs open and being reviewed
5. 🧪 **Testing** - Code merged, undergoing testing
6. ✅ **Done** - Complete and verified

**To configure columns:**
- **Rename**: Click column header (three dots) → "Edit column" → Rename → Save
- **Add new column**: Click "+ Add column" → Enter name → Create
- **Reorder**: Drag column headers to reorder

### Step 4: Add Custom Fields (Optional but Recommended)

Add custom fields to track Sprint, Priority, and Module:

1. Click **"+"** in the top right of the project
2. Select **"Field"**
3. Add these fields:

**Sprint Field:**
- Type: **Single select**
- Name: **Sprint**
- Options:
  - Sprint 1 - Core Infrastructure
  - Sprint 2 - Authentication
  - Sprint 3 - NSE Data Fetching

**Priority Field:**
- Type: **Single select**
- Name: **Priority**
- Options:
  - High
  - Medium
  - Low

**Module Field:**
- Type: **Single select**
- Name: **Module**
- Options:
  - Database
  - Backend
  - Frontend
  - Auth
  - User
  - Admin

**Estimate Field:**
- Type: **Number**
- Name: **Estimate** (in days)

### Step 5: Organize Sprint 1 Issues

After bulk import, your Sprint 1 issues will be in the project. **Update them:**

1. **Open each issue card** (#9, #10, #11, #12)
2. **Set the custom fields:**
   - Sprint: "Sprint 1 - Core Infrastructure"
   - Priority: "High"
   - Module: (Database, Backend, Frontend, Auth respectively)
   - Estimate: 2-3 (days)

3. **Move cards to appropriate columns:**
   - Initially, all should be in "Backlog"
   - When ready to start, move to "TODO"
   - When actively coding, move to "In Progress"
   - When PR is created, move to "Review"
   - After merge, move to "Testing"
   - After testing complete, move to "Done"

## Automatic Features

Once set up, the project will automatically:

✅ **Add new issues** to the project (if bulk import enabled)
✅ **Link PRs** when they reference issues ("Closes #123")
✅ **Update status** based on PR labels and status

## Quick Verification

After setup, verify:

1. ✅ All 4 Sprint 1 issues are in the project
2. ✅ Issues are in "Backlog" column
3. ✅ All 6 columns exist: Backlog, TODO, In Progress, Review, Testing, Done
4. ✅ Custom fields are set correctly
5. ✅ Labels match (sprint-1, backend, frontend, etc.)

## Next Steps

Once the project is set up:

1. ✅ Issues are tracked in the project
2. ✅ Move issue from "Backlog" to "TODO" when ready to start
3. ✅ Start development: `git checkout -b feature/database-schema-complete`
4. ✅ Move card to "In Progress" when actively coding
5. ✅ Create PR with "Closes #9" when ready
6. ✅ Move card to "Review" when PR is created
7. ✅ Move to "Testing" after PR merge
8. ✅ Move to "Done" after testing complete

---

**Note:** If you didn't use bulk import, you can still add issues manually:
- Open each issue → Right sidebar → "Projects" → Add to "BulkDeal Analyzer Development"

