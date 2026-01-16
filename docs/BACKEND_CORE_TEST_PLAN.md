# Backend Core Module - Test Plan

## Overview
Test plan for the backend core module structure, covering configuration, database, responses, exceptions, and API endpoints.

## Test Categories

### 1. Configuration Tests (`test_core_config.py`)

#### Unit Tests
- [x] **test_settings_defaults**: Verify default values
  - App name, version, debug mode
  - Environment defaults to development
  - API prefix defaults to `/api/v1`
  - CORS origins include localhost:3000

- [x] **test_settings_from_env**: Verify environment variable loading
  - Supabase URL and keys
  - Secret key
  - Debug flag parsing
  - Environment setting

- [x] **test_settings_cors_origins**: Verify CORS origins
  - Default includes localhost:3000
  - Can be configured via env

#### Additional Tests Needed
- [ ] **test_settings_validation**: Test invalid values rejected
- [ ] **test_settings_caching**: Verify settings are cached
- [ ] **test_settings_required_fields**: Test required fields raise errors
- [ ] **test_settings_optional_fields**: Test optional fields work

### 2. Response Tests (`test_core_responses.py`)

#### Unit Tests
- [x] **test_success_response**: Test success response creation
  - Success flag is True
  - Data and message set correctly
  - Errors field is None

- [x] **test_success_response_defaults**: Test defaults
  - Default message is "Success"
  - Data can be None

- [x] **test_error_response**: Test error response creation
  - Success flag is False
  - Message and errors set correctly

- [x] **test_api_response_inheritance**: Test class inheritance
  - SuccessResponse is APIResponse
  - ErrorResponse is APIResponse

#### Additional Tests Needed
- [ ] **test_response_serialization**: Test JSON serialization
- [ ] **test_response_validation**: Test Pydantic validation
- [ ] **test_response_with_nested_data**: Test complex data structures

### 3. Database Tests (To Be Created: `test_core_database.py`)

#### Unit Tests
- [ ] **test_get_supabase_client**: Test client creation
  - Client is created successfully
  - Client is cached
  - Uses correct URL and key

- [ ] **test_get_supabase_admin_client**: Test admin client
  - Admin client created with service role key
  - Raises error if service role key not configured

- [ ] **test_database_initialization**: Test Database class
  - Can be instantiated with default client
  - Can be instantiated with custom client

#### Integration Tests (Requires Supabase)
- [ ] **test_database_connection**: Test actual connection
  - Can connect to Supabase
  - Can query tables
  - Handles connection errors

- [ ] **test_execute_query_select**: Test SELECT operations
  - Can query table
  - Filters work correctly
  - Returns expected data

- [ ] **test_execute_query_insert**: Test INSERT operations
  - Can insert data
  - Returns created record
  - Handles validation errors

- [ ] **test_execute_query_update**: Test UPDATE operations
  - Can update records
  - Filters work correctly
  - Returns updated records

- [ ] **test_execute_query_delete**: Test DELETE operations
  - Can delete records
  - Filters work correctly

- [ ] **test_get_table**: Test table query builder
  - Returns table query object
  - Can chain operations

### 4. Exception Tests (To Be Created: `test_core_exceptions.py`)

#### Unit Tests
- [ ] **test_bulk_deal_analyzer_exception**: Test base exception
  - Inherits from HTTPException
  - Has default status code
  - Has default detail message

- [ ] **test_not_found_error**: Test NotFoundError
  - Status code is 404
  - Custom message works
  - Default message works

- [ ] **test_validation_error**: Test ValidationError
  - Status code is 422
  - Custom message works

- [ ] **test_authentication_error**: Test AuthenticationError
  - Status code is 401
  - Custom message works

- [ ] **test_authorization_error**: Test AuthorizationError
  - Status code is 403
  - Custom message works

- [ ] **test_database_error**: Test DatabaseError
  - Status code is 500
  - Custom message works

### 5. API Endpoint Tests (To Be Created: `test_api_v1_health.py`)

#### Integration Tests
- [ ] **test_health_check**: Test health endpoint
  - Returns 200 status
  - Returns correct response format
  - Includes app name and version

- [ ] **test_readiness_check**: Test ready endpoint
  - Returns 200 status
  - Returns ready status
  - Can check database connection (future)

- [ ] **test_liveness_check**: Test live endpoint
  - Returns 200 status
  - Returns alive status

- [ ] **test_root_endpoint**: Test root endpoint
  - Returns API information
  - Includes docs URL
  - Includes API prefix

### 6. Module Structure Tests (To Be Created: `test_module_structure.py`)

#### Integration Tests
- [ ] **test_modules_importable**: Test all modules can be imported
  - Auth module imports
  - User module imports
  - Admin module imports
  - Shared module imports

- [ ] **test_constants_accessible**: Test shared constants
  - SubscriptionTier constants
  - DealType constants
  - UserRole constants
  - APILimits constants
  - FileLimits constants

### 7. Main Application Tests (To Be Created: `test_main.py`)

#### Integration Tests
- [ ] **test_app_initialization**: Test FastAPI app
  - App is created
  - Title and version set correctly
  - Debug mode configured

- [ ] **test_cors_middleware**: Test CORS
  - CORS middleware configured
  - Origins set correctly
  - Methods and headers configured

- [ ] **test_api_routers_included**: Test routers
  - API routers are included
  - Health router included
  - Bulk deals router included

- [ ] **test_openapi_docs**: Test API documentation
  - OpenAPI schema generated
  - Docs accessible at /docs
  - ReDoc accessible at /redoc

## Test Coverage Goals

### Minimum Coverage
- **Core modules**: 80%+
- **API endpoints**: 70%+
- **Exception handling**: 90%+
- **Configuration**: 90%+

### Priority Tests (Must Have)
1. Configuration tests ✅ (Done)
2. Response format tests ✅ (Done)
3. Database connection tests (Mocked)
4. Exception tests
5. Health endpoint tests

### Nice to Have (Future)
1. Database integration tests (requires Supabase)
2. Performance tests
3. Load tests
4. Security tests

## Test Execution

### Run All Tests
```bash
cd backend
python3 -m pytest tests/ -v --cov=app --cov-report=html
```

### Run Specific Test Suite
```bash
# Config tests
python3 -m pytest tests/test_core_config.py -v

# Response tests
python3 -m pytest tests/test_core_responses.py -v

# Database tests (when created)
python3 -m pytest tests/test_core_database.py -v

# Exception tests (when created)
python3 -m pytest tests/test_core_exceptions.py -v

# API tests (when created)
python3 -m pytest tests/test_api_v1_health.py -v
```

### Run with Coverage
```bash
python3 -m pytest tests/ --cov=app --cov-report=term-missing
```

## Mocking Strategy

### Database Mocks
- Mock Supabase client for unit tests
- Use real client only for integration tests
- Mock connection errors and timeouts

### Settings Mocks
- Use environment variable patches
- Mock file reading for .env files
- Clear cache between tests

### HTTP Client Mocks
- Mock httpx for API tests
- Mock responses for external services

## Continuous Integration

### CI Test Pipeline
1. Lint code (ruff)
2. Run unit tests
3. Run integration tests (if credentials available)
4. Generate coverage report
5. Check coverage threshold

### Test Requirements
- All tests must pass
- Coverage must meet minimum thresholds
- No linting errors
- Type checking passes (if enabled)

## Test Data Management

### Fixtures
- Create test fixtures for database
- Create test fixtures for API responses
- Create test fixtures for configuration

### Test Environment
- Use separate test database (if available)
- Use test environment variables
- Clean up after tests

## Future Enhancements

### Property-Based Testing
- Use Hypothesis for property-based tests
- Test edge cases automatically
- Generate test data

### Contract Testing
- Test API contracts
- Test database schema contracts
- Test configuration contracts

### Performance Testing
- Load testing for endpoints
- Stress testing for database
- Benchmark critical paths

## Notes

- Some tests require Supabase credentials (integration tests)
- Mock external dependencies for unit tests
- Use pytest fixtures for test setup/teardown
- Keep tests fast and independent
- Use descriptive test names

