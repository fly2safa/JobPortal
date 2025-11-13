# Contributing to TalentNest Job Portal

Thank you for your interest in contributing to TalentNest! This document provides guidelines and best practices for contributing to the project.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Branch Strategy](#branch-strategy)
3. [Development Workflow](#development-workflow)
4. [Pull Request Guidelines](#pull-request-guidelines)
5. [Code Standards](#code-standards)
6. [Commit Message Guidelines](#commit-message-guidelines)
7. [Testing Requirements](#testing-requirements)
8. [Documentation](#documentation)

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.11+** (backend)
- **Node.js 18+** and **npm** (frontend)
- **MongoDB Atlas** account (or local MongoDB)
- **Git** for version control

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/fly2safa/JobPortal.git
   cd JobPortal
   ```

2. **Set up the backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Configure your environment variables
   ```

3. **Set up the frontend:**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local  # Configure your environment variables
   ```

4. **Read the documentation:**
   - [README.md](README.md) - Project overview and setup
   - [ERD.md](docs/ERD.md) - Database schema
   - [docker/README.md](docker/README.md) - Docker deployment

---

## Branch Strategy

We follow a **Git Flow-inspired** branching strategy with `main`, `dev`, and feature branches.

### Branch Types

| Branch Type | Naming Convention | Purpose | Base Branch |
|-------------|-------------------|---------|-------------|
| **Main** | `main` | Production-ready code | - |
| **Development** | `dev` | Integration branch for features | `main` |
| **Feature** | `feat/<feature-name>` | New features | `dev` |
| **Bug Fix** | `fix/<bug-name>` | Bug fixes | `dev` |
| **Documentation** | `docs/<doc-name>` | Documentation updates | `dev` |
| **Hotfix** | `hotfix/<issue>` | Critical production fixes | `main` |

### Branch Naming Examples

✅ **Good:**
- `feat/job-search-filters`
- `feat/ai-cover-letter`
- `fix/login-validation`
- `docs/api-endpoints`
- `hotfix/security-patch`

❌ **Bad:**
- `my-feature` (no type prefix)
- `feat/MyFeature` (use kebab-case, not PascalCase)
- `feature/new-stuff` (too vague)

---

## Development Workflow

### 1. Start a New Feature

Always branch from the latest `dev`:

```bash
# Ensure you're on dev and up to date
git checkout dev
git pull origin dev

# Create and switch to your feature branch
git checkout -b feat/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the [Code Standards](#code-standards)
- Test your changes locally
- Commit frequently with meaningful messages

### 3. Keep Your Branch Updated

Regularly sync with `dev` to avoid conflicts:

```bash
# Fetch latest changes
git fetch origin dev

# Rebase your branch on top of dev
git rebase origin/dev

# Or merge if you prefer (less clean history)
git merge origin/dev
```

### 4. Push Your Branch

```bash
# First time pushing the branch
git push -u origin feat/your-feature-name

# Subsequent pushes
git push
```

### 5. Create a Pull Request

1. Go to GitHub and create a PR from your branch to `dev`
2. Fill out the PR template (see [PR Guidelines](#pull-request-guidelines))
3. Request at least **1 reviewer**
4. Address any feedback from code review
5. Once approved, **squash and merge** to keep history clean

---

## Pull Request Guidelines

### PR Title Format

Use conventional commit format:

```
<type>(<scope>): <description>

Examples:
feat(jobs): add advanced search filters
fix(auth): resolve token expiration issue
docs(readme): update setup instructions
```

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issue
Closes #<issue-number> (if applicable)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Backend tests pass (`pytest`)
- [ ] Frontend builds successfully (`npm run build`)
- [ ] Manually tested locally
- [ ] No linter errors

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No new warnings or errors
```

### PR Review Process

1. **Automated Checks:** Ensure all CI/CD checks pass
2. **Code Review:** At least 1 team member must approve
3. **Testing:** Reviewer should test changes locally if significant
4. **Feedback:** Address all comments and requested changes
5. **Approval:** Once approved, the PR can be merged

### Merging Strategy

- **Squash and Merge:** Default for feature branches to `dev`
  - Keeps history clean
  - Combines all commits into one
  
- **Merge Commit:** For `dev` → `main` releases
  - Preserves full history
  - Creates a clear release point

---

## Code Standards

### Backend (Python/FastAPI)

#### Style Guide
- Follow **PEP 8** style guide
- Use **type hints** for all function parameters and return values
- Maximum line length: **100 characters**
- Use **docstrings** for all classes and functions

#### Example:
```python
from typing import Optional, List
from pydantic import BaseModel

async def get_user_jobs(
    user_id: str,
    status: Optional[str] = None,
    limit: int = 10
) -> List[Job]:
    """
    Retrieve jobs for a specific user.
    
    Args:
        user_id: The user's unique identifier
        status: Optional status filter (active, closed, etc.)
        limit: Maximum number of jobs to return
        
    Returns:
        List of Job objects matching the criteria
    """
    # Implementation here
    pass
```

#### Linting
```bash
# Run linter
flake8 app/

# Run type checker
mypy app/

# Auto-format code
black app/
```

### Frontend (TypeScript/React/Next.js)

#### Style Guide
- Follow **Airbnb JavaScript Style Guide**
- Use **TypeScript** for all new code
- Use **functional components** with hooks
- Maximum line length: **100 characters**
- Use **named exports** for components

#### Example:
```typescript
import { useState, useEffect } from 'react';
import { Job } from '@/types';

interface JobListProps {
  userId: string;
  status?: string;
}

export const JobList: React.FC<JobListProps> = ({ userId, status }) => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch jobs
  }, [userId, status]);

  return (
    <div className="job-list">
      {/* Component JSX */}
    </div>
  );
};
```

#### Linting
```bash
# Run linter
npm run lint

# Auto-fix issues
npm run lint:fix

# Type check
npm run type-check
```

### General Best Practices

1. **DRY (Don't Repeat Yourself):** Extract reusable logic into functions/components
2. **Single Responsibility:** Each function/component should do one thing well
3. **Meaningful Names:** Use descriptive variable and function names
4. **Error Handling:** Always handle errors gracefully
5. **Security:** Never commit secrets, API keys, or sensitive data
6. **Comments:** Explain *why*, not *what* (code should be self-explanatory)

---

## Commit Message Guidelines

We follow the **Conventional Commits** specification.

### Format

```
<type>(<scope>): <subject>

<body> (optional)

<footer> (optional)
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(jobs): add salary range filter` |
| `fix` | Bug fix | `fix(auth): resolve login redirect issue` |
| `docs` | Documentation | `docs(readme): update installation steps` |
| `style` | Code style (formatting, no logic change) | `style(backend): format with black` |
| `refactor` | Code refactoring | `refactor(api): simplify job query logic` |
| `test` | Adding/updating tests | `test(jobs): add unit tests for search` |
| `chore` | Maintenance tasks | `chore(deps): update dependencies` |
| `perf` | Performance improvement | `perf(db): optimize job search query` |

### Scope (Optional)

The scope specifies what part of the codebase is affected:
- `auth` - Authentication/authorization
- `jobs` - Job posting/searching
- `applications` - Job applications
- `ai` - AI features (assistant, resume parsing)
- `ui` - User interface
- `api` - API endpoints
- `db` - Database/models

### Examples

✅ **Good:**
```
feat(jobs): add remote work filter to job search

- Add is_remote field to search parameters
- Update frontend filter UI
- Add backend query logic
```

```
fix(auth): prevent token expiration during active session

Tokens were expiring even when user was active. Now refresh
token automatically when user is active within 5 minutes of expiration.

Closes #123
```

❌ **Bad:**
```
update stuff
```

```
Fixed bug
```

```
WIP - working on feature (don't commit WIP to shared branches)
```

---

## Testing Requirements

### Backend Testing

All new features and bug fixes must include tests.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_jobs.py

# Run specific test
pytest tests/test_jobs.py::test_create_job
```

#### Test Structure
```python
import pytest
from app.models.job import Job

@pytest.mark.asyncio
async def test_create_job(test_client, test_user):
    """Test job creation endpoint."""
    job_data = {
        "title": "Software Engineer",
        "description": "Build amazing things",
        # ... other fields
    }
    
    response = await test_client.post(
        "/api/v1/jobs",
        json=job_data,
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    
    assert response.status_code == 201
    assert response.json()["title"] == job_data["title"]
```

### Frontend Testing

```bash
# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Manual Testing Checklist

Before submitting a PR, manually test:
- ✅ Feature works as expected
- ✅ No console errors
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Error states handled gracefully
- ✅ Loading states displayed
- ✅ Accessibility (keyboard navigation, screen readers)

---

## Documentation

### When to Update Documentation

Update documentation when you:
- Add a new feature
- Change existing functionality
- Add/modify API endpoints
- Change environment variables
- Update dependencies
- Fix a significant bug

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, setup, features |
| `docs/ERD.md` | Database schema and relationships |
| `docker/README.md` | Docker setup and deployment |
| `CONTRIBUTING.md` | This file - contribution guidelines |
| `backend/app/api/v1/routes/*.py` | API endpoint docstrings |

### API Documentation

All API endpoints should include docstrings:

```python
@router.post("/jobs", response_model=JobResponse, status_code=201)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_employer)
) -> Job:
    """
    Create a new job posting.
    
    **Required Role:** Employer
    
    **Request Body:**
    - title: Job title (required)
    - description: Job description (required)
    - location: Job location (required)
    - ... (other fields)
    
    **Returns:**
    - 201: Job created successfully
    - 400: Invalid job data
    - 401: Unauthorized (not logged in)
    - 403: Forbidden (not an employer)
    
    **Example:**
    ```json
    {
      "title": "Senior Python Developer",
      "description": "We're looking for...",
      "location": "San Francisco, CA",
      "salary_min": 120000,
      "salary_max": 180000
    }
    ```
    """
    # Implementation
```

---

## Code Review Guidelines

### For Authors

When submitting a PR:
1. **Self-review first:** Review your own code before requesting review
2. **Keep it focused:** One feature/fix per PR
3. **Provide context:** Explain *why* the change is needed
4. **Test thoroughly:** Ensure all tests pass
5. **Be responsive:** Address feedback promptly

### For Reviewers

When reviewing a PR:
1. **Be constructive:** Provide helpful, actionable feedback
2. **Ask questions:** If something is unclear, ask for clarification
3. **Test locally:** For significant changes, pull and test locally
4. **Check for:**
   - Code quality and readability
   - Proper error handling
   - Security concerns
   - Performance implications
   - Test coverage
   - Documentation updates

---

## Common Scenarios

### Scenario 1: Fixing Merge Conflicts

```bash
# Update your branch with latest dev
git checkout dev
git pull origin dev

# Go back to your feature branch
git checkout feat/your-feature

# Rebase on dev (recommended)
git rebase dev

# Resolve conflicts in your editor
# After resolving each file:
git add <resolved-file>
git rebase --continue

# Force push (rebase rewrites history)
git push --force-with-lease
```

### Scenario 2: Updating a PR After Review

```bash
# Make the requested changes
# ... edit files ...

# Commit the changes
git add .
git commit -m "fix: address PR feedback"

# Push to update the PR
git push
```

### Scenario 3: Syncing Fork with Upstream

```bash
# Add upstream remote (one time)
git remote add upstream https://github.com/fly2safa/JobPortal.git

# Fetch upstream changes
git fetch upstream

# Update your dev branch
git checkout dev
git merge upstream/dev
git push origin dev
```

---

## Release Process

### Creating a Release

1. **Ensure `dev` is stable:**
   - All tests pass
   - No known critical bugs
   - All features complete

2. **Create release PR:**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b release/v1.0.0
   
   # Update version numbers, CHANGELOG, etc.
   git commit -m "chore: prepare release v1.0.0"
   git push -u origin release/v1.0.0
   ```

3. **Create PR from `release/v1.0.0` to `main`**

4. **After merge, tag the release:**
   ```bash
   git checkout main
   git pull origin main
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

5. **Merge back to `dev`:**
   ```bash
   git checkout dev
   git merge main
   git push origin dev
   ```

---

## Getting Help

### Resources

- **Documentation:** [README.md](README.md), [ERD.md](docs/ERD.md)
- **Issues:** Check [GitHub Issues](https://github.com/fly2safa/JobPortal/issues)
- **Discussions:** Use [GitHub Discussions](https://github.com/fly2safa/JobPortal/discussions)

### Contact

- **Project Lead:** [Your Name]
- **Email:** [your-email@example.com]
- **Slack/Discord:** [Link to team chat]

---

## License

By contributing to TalentNest, you agree that your contributions will be licensed under the same license as the project.

---

## Acknowledgments

Thank you to all contributors who help make TalentNest better! 🎉

---

**Last Updated:** November 2024  
**Version:** 1.0  
**Maintained By:** TalentNest Development Team

