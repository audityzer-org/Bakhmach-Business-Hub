# Bakhmach Business Hub - Integration Test Suite

## Overview

Comprehensive testing framework for the Bakhmach Business Hub integration service, covering unit tests, integration tests, end-to-end tests, and performance benchmarks.

## Test Structure

```
tests/
├── unit/
│   ├── test_sync_orchestrator.py
│   ├── test_webhook_receiver.py
│   ├── test_oauth_handler.py
│   └── test_data_transformer.py
├── integration/
│   ├── test_github_integration.py
│   ├── test_ai_studio_sync.py
│   ├── test_database_operations.py
│   └── test_api_endpoints.py
├── e2e/
│   ├── test_complete_workflow.py
│   ├── test_user_flows.py
│   └── test_error_scenarios.py
├── performance/
│   ├── test_load_handling.py
│   ├── test_sync_performance.py
│   └── test_api_latency.py
└── fixtures/
    ├── mock_github_data.py
    ├── mock_ai_studio_data.py
    └── test_helpers.py
```

## Running Tests

### All Tests
```bash
pytest tests/ -v --cov=services --cov-report=html
```

### Unit Tests Only
```bash
pytest tests/unit/ -v
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### End-to-End Tests
```bash
pytest tests/e2e/ -v -m e2e
```

### Performance Tests
```bash
pytest tests/performance/ -v --benchmark
```

### Specific Test File
```bash
pytest tests/unit/test_sync_orchestrator.py -v
```

## Test Coverage Requirements

- **Minimum Overall Coverage**: 85%
- **Critical Services Coverage**: 95%
  - sync_orchestrator.py
  - webhook_receiver.py
  - oauth_handler.py
- **Integration Points**: 90%

## Unit Test Examples

### Sync Orchestrator Tests
```python
import pytest
from services.integration.sync_orchestrator import SyncOrchestrator

class TestSyncOrchestrator:
    @pytest.fixture
    def orchestrator(self):
        return SyncOrchestrator()
    
    def test_github_sync_success(self, orchestrator):
        result = orchestrator.sync_github()
        assert result['status'] == 'success'
        assert result['items_synced'] > 0
    
    def test_ai_studio_sync_with_error(self, orchestrator):
        with pytest.raises(SyncException):
            orchestrator.sync_ai_studio(retry=False)
    
    def test_conflict_resolution(self, orchestrator):
        result = orchestrator.resolve_conflict(
            source='github',
            target='ai-studio',
            conflict_type='version_mismatch'
        )
        assert result['resolved'] is True
```

### Webhook Receiver Tests
```python
class TestWebhookReceiver:
    def test_github_push_webhook(self, client):
        payload = {"action": "push", "repository": "test-repo"}
        response = client.post('/webhooks/github', json=payload)
        assert response.status_code == 200
    
    def test_ai_studio_update_webhook(self, client):
        payload = {"type": "model_update", "model_id": "123"}
        response = client.post('/webhooks/ai-studio', json=payload)
        assert response.status_code == 200
    
    def test_invalid_webhook_signature(self, client):
        response = client.post('/webhooks/github', 
                              json={}, 
                              headers={'X-Hub-Signature': 'invalid'})
        assert response.status_code == 401
```

## Integration Tests

### Database Operations
```python
class TestDatabaseOperations:
    @pytest.fixture(autouse=True)
    def setup_db(self, db_session):
        # Setup test data
        yield
        # Cleanup
        db_session.rollback()
    
    def test_sync_record_creation(self, db_session):
        sync = SyncRecord(
            source='github',
            target='ai-studio',
            status='completed'
        )
        db_session.add(sync)
        db_session.commit()
        
        assert sync.id is not None
        assert SyncRecord.query.count() > 0
    
    def test_concurrent_sync_handling(self, db_session):
        # Test multiple syncs don't create conflicts
        for i in range(5):
            sync = SyncRecord(source='github')
            db_session.add(sync)
        db_session.commit()
        
        assert db_session.query(SyncRecord).count() == 5
```

## End-to-End Tests

```python
class TestCompleteWorkflow:
    def test_full_sync_workflow(self, app_client):
        # 1. Trigger GitHub webhook
        webhook_response = app_client.post(
            '/webhooks/github',
            json={"action": "push", "repository": "test-repo"}
        )
        assert webhook_response.status_code == 200
        
        # 2. Verify sync started
        time.sleep(1)  # Allow async processing
        sync_status = app_client.get('/api/sync/status')
        assert sync_status.json()['status'] == 'in_progress'
        
        # 3. Verify completion
        time.sleep(5)  # Wait for sync
        final_status = app_client.get('/api/sync/status')
        assert final_status.json()['status'] == 'completed'
        assert final_status.json()['error_count'] == 0
    
    def test_conflict_resolution_workflow(self, app_client):
        # Create conflicting changes
        app_client.post('/webhooks/github', json={...})
        app_client.post('/webhooks/ai-studio', json={...})
        
        # Verify conflict detection and resolution
        conflicts = app_client.get('/api/conflicts')
        assert len(conflicts.json()) > 0
        
        # Verify resolution
        resolution = app_client.post(
            '/api/conflicts/resolve',
            json={"strategy": "prefer_latest"}
        )
        assert resolution.json()['resolved'] is True
```

## Performance Tests

```python
class TestPerformance:
    def test_sync_performance(self, benchmark):
        orchestrator = SyncOrchestrator()
        result = benchmark(
            orchestrator.sync_github,
            min_time=0.1,
            min_rounds=5
        )
        assert result['time'] < 5  # Should complete in < 5 seconds
    
    def test_api_latency(self, benchmark, client):
        result = benchmark(client.get, '/api/sync/status')
        assert result.elapsed.total_seconds() < 0.1  # < 100ms
    
    def test_concurrent_requests(self):
        import concurrent.futures
        
        def make_request():
            return requests.get('http://localhost:8000/api/health')
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        assert all(r.status_code == 200 for r in results)
        assert len(results) == 100
```

## Continuous Integration

### GitHub Actions Workflow
Tests run automatically on:
- Push to main branch
- All pull requests
- Scheduled daily at 2 AM UTC

### Coverage Thresholds
- New code: minimum 80% coverage
- Existing code: maintain or improve current coverage
- Branches fail if coverage decreases > 2%

## Mocking and Fixtures

### Mock GitHub API
```python
@pytest.fixture
def mock_github_api(monkeypatch):
    def mock_list_repos(*args, **kwargs):
        return [
            {"name": "test-repo", "url": "https://github.com/test/test-repo"},
            {"name": "test-repo-2", "url": "https://github.com/test/test-repo-2"},
        ]
    
    monkeypatch.setattr("services.github.list_repos", mock_list_repos)
    return mock_list_repos
```

### Mock AI Studio API
```python
@pytest.fixture
def mock_ai_studio_api(monkeypatch):
    def mock_get_models(*args, **kwargs):
        return {
            "models": [
                {"id": "model-1", "name": "Test Model"},
                {"id": "model-2", "name": "Test Model 2"},
            ]
        }
    
    monkeypatch.setattr("services.ai_studio.get_models", mock_get_models)
    return mock_get_models
```

## Test Reporting

### HTML Coverage Report
```bash
pytest tests/ --cov=services --cov-report=html
# Open htmlcov/index.html in browser
```

### JUnit XML for CI
```bash
pytest tests/ --junit-xml=test-results.xml
```

### Allure Report
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

## Test Data Management

### Database Fixtures
- Use pytest-factoryboy for model factories
- Each test gets isolated database transaction
- Automatic rollback after test completion

### Test Credentials
- Stored in `.env.test` (not version controlled)
- Use separate test API keys
- Mock external services in unit tests

## Debugging Tests

### Running with Print Output
```bash
pytest tests/ -v -s
```

### Running with PDB
```bash
pytest tests/ --pdb
# or
pytest tests/ --pdbcls=IPython.terminal.debugger:TerminalPdb
```

### Running Specific Test
```bash
pytest tests/unit/test_sync_orchestrator.py::TestSyncOrchestrator::test_github_sync_success -v
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Meaningful Names**: Test names should describe what they test
3. **Arrange-Act-Assert**: Follow AAA pattern
4. **Mock External Calls**: Don't make real API calls in tests
5. **Use Fixtures**: Share common setup code
6. **Test Both Success and Failure**: Include error cases
7. **Avoid Test Interdependence**: Don't rely on test execution order
8. **Clean Up Resources**: Close connections, delete temp files

## Maintenance

- Review test coverage monthly
- Update tests with new features
- Refactor tests when code changes
- Keep test data current
- Monitor test execution time
- Remove obsolete tests

## Support and Issues

For test-related issues:
- Check test logs in GitHub Actions
- Review coverage reports
- Enable verbose output with `-vv`
- Contact: @romanchaa997
