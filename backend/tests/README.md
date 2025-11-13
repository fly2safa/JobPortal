# Backend Testing Guide

## Overview

This directory contains automated tests for the TalentNest Job Portal backend API.

---

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_auth.py             # Authentication tests
├── test_jobs.py             # Job posting tests
├── test_applications.py     # Job application tests
└── README.md                # This file
```

---

## Prerequisites

Before running tests, ensure you have:

1. **Python 3.11+** installed
2. **Virtual environment** activated
3. **Dependencies** installed:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-asyncio pytest-cov httpx
   ```
4. **MongoDB** connection configured in `.env`
5. **Test database** (tests use a separate database with `_test` suffix)

---

## Running Tests

### Run All Tests

```bash
# From backend directory
cd backend
pytest
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
pytest tests/test_jobs.py
pytest tests/test_applications.py
```

### Run Specific Test Function

```bash
pytest tests/test_auth.py::test_register_job_seeker
pytest tests/test_jobs.py::test_create_job_as_employer
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage Report

```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

### Run with Output (print statements)

```bash
pytest -s
```

### Run Tests Matching Pattern

```bash
pytest -k "auth"      # Run all tests with "auth" in name
pytest -k "create"    # Run all tests with "create" in name
```

---

## Test Fixtures

### Database Fixtures

- **`db_client`**: MongoDB client with test database
- **`test_client`**: HTTP client for making API requests

### User Fixtures

- **`test_user`**: Job seeker user
- **`test_employer`**: Employer user
- **`auth_headers`**: Authentication headers for job seeker
- **`employer_auth_headers`**: Authentication headers for employer

### Data Fixtures

- **`test_company`**: Test company
- **`test_job`**: Test job posting
- **`test_application`**: Test job application
- **`test_resume`**: Test resume

---

## Test Coverage

### Authentication Tests (`test_auth.py`)

- ✅ User registration (job seeker)
- ✅ User registration (employer)
- ✅ Duplicate email handling
- ✅ Invalid email validation
- ✅ Login with valid credentials
- ✅ Login with invalid credentials
- ✅ Get current user
- ✅ Unauthorized access

### Job Tests (`test_jobs.py`)

- ✅ Get jobs (public)
- ✅ Get job by ID
- ✅ Get nonexistent job
- ✅ Search jobs by keyword
- ✅ Filter jobs by location
- ✅ Filter jobs by remote option
- ✅ Create job (employer)
- ✅ Create job (job seeker - forbidden)
- ✅ Update job (owner)
- ✅ Delete job (owner)
- ✅ Get employer's jobs

### Application Tests (`test_applications.py`)

- ✅ Create application
- ✅ Duplicate application prevention
- ✅ Get my applications
- ✅ Get application by ID
- ✅ Get job applications (employer)
- ✅ Update application status (employer)
- ✅ Shortlist application
- ✅ Reject application with reason
- ✅ Withdraw application (applicant)
- ✅ Filter applications by status

---

## Writing New Tests

### Test Function Template

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_feature_name(test_client: AsyncClient, auth_headers: dict):
    """Test description."""
    # Arrange
    test_data = {"key": "value"}
    
    # Act
    response = await test_client.post(
        "/api/v1/endpoint",
        headers=auth_headers,
        json=test_data
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "value"
```

### Best Practices

1. **Use descriptive test names**: `test_<action>_<expected_result>`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Test one thing per test**: Keep tests focused
4. **Use fixtures**: Reuse common setup code
5. **Test edge cases**: Invalid input, missing data, etc.
6. **Clean up**: Fixtures handle cleanup automatically
7. **Document**: Add docstrings to explain what's being tested

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Backend Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    
    - name: Run tests
      env:
        MONGODB_URL: ${{ secrets.MONGODB_URL }}
        SECRET_KEY: test-secret-key
      run: |
        cd backend
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

---

## Troubleshooting

### Tests Fail with Database Connection Error

**Problem**: Cannot connect to MongoDB

**Solution**:
1. Check `.env` file has correct `MONGODB_URL`
2. Ensure MongoDB Atlas allows connections from your IP
3. Verify network connectivity

### Tests Fail with Import Errors

**Problem**: Cannot import modules

**Solution**:
1. Ensure virtual environment is activated
2. Install all dependencies: `pip install -r requirements.txt`
3. Install test dependencies: `pip install pytest pytest-asyncio`

### Tests Pass Locally but Fail in CI

**Problem**: Environment differences

**Solution**:
1. Check environment variables in CI
2. Ensure same Python version
3. Verify all dependencies are installed
4. Check for hardcoded paths or URLs

### Slow Tests

**Problem**: Tests take too long

**Solution**:
1. Use test database (not production)
2. Mock external API calls
3. Run tests in parallel: `pytest -n auto` (requires pytest-xdist)
4. Optimize database queries

---

## Test Database

Tests use a separate database with `_test` suffix to avoid affecting production data.

**Example**:
- Production DB: `talentnest`
- Test DB: `talentnest_test`

The test database is automatically:
- Created before tests run
- Populated with fixtures
- Dropped after tests complete

---

## Code Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| Models | 90%+ |
| API Routes | 85%+ |
| Services | 80%+ |
| Utilities | 75%+ |
| Overall | 80%+ |

---

## Additional Testing

### Manual Testing

See [docs/MANUAL_TESTING_GUIDE.md](../../docs/MANUAL_TESTING_GUIDE.md) for comprehensive manual testing procedures.

### Integration Testing

Integration tests verify that different components work together:
- Database operations
- External API calls
- Email sending
- File uploads

### Performance Testing

Use tools like:
- **Locust**: Load testing
- **Apache JMeter**: Performance testing
- **pytest-benchmark**: Benchmark tests

---

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [HTTPX](https://www.python-httpx.org/)

---

**Last Updated:** November 2024  
**Version:** 1.0  
**Maintained By:** TalentNest QA Team

