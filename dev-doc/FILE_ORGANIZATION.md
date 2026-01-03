# File Organization Guide

## Directory Structure

### Root Directory
Essential project files that should remain in root:
- `README.md` - Project overview and quick start
- `PRD.md` - Product Requirements Document
- `RELEASE.md` - Release management process
- `SECURITY.md` - Security policies

### dev-doc/ Directory
**AI-generated task documentation ONLY:**
- Files created when resolving/performing tasks
- Task checklists generated during work
- Sprint notes created during sprints
- Internal task notes
- Repository setup notes
- **NOT for user/API documentation**

### docs/ Directory
**User-facing and project documentation:**
- API documentation
- User guides
- Architecture documentation
- Database schemas
- Technical decisions
- Tool setup guides (for end users)
- Tutorials

## Rules for Creating .md Files

1. **Always ask before creating new .md files**
2. **Development/task docs** → `dev-doc/`
3. **User-facing docs** → `docs/`
4. **Essential project docs** → Root (with approval)

## File Categories

### Development Documentation (dev-doc/)
- Setup guides
- Task checklists
- Sprint documentation
- Tool configuration
- Internal notes

### Project Documentation (Root)
- README
- PRD
- Release process
- Security policies

### User Documentation (docs/)
- API docs
- User guides
- Tutorials

