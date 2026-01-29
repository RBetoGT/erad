# ERAD REST API - Installation and Usage Guide

## Quick Setup

1. **Install dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

2. **Start the API server**:
   ```bash
   python -m erad.api
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn erad.api:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Running Tests

```bash
# Run all API tests
pytest tests/test_api.py -v

# Run with coverage
pytest tests/test_api.py --cov=erad.api --cov-report=html

# Run specific test
pytest tests/test_api.py::test_health_check -v
```

## Example Usage

```bash
# Run the example script (make sure API is running first)
python examples/api_example.py
```

## What's Included

### API Features (`src/erad/api.py`)
- **Simulation Endpoints**: Run hazard simulations and generate scenarios
- **Model Management**: Upload, list, retrieve, and delete distribution systems
- **Utility Endpoints**: Get supported hazard types and curve sets
- **Health Checks**: Monitor API status
- **Error Handling**: Comprehensive error responses

### Tests (`tests/test_api.py`)
- **Unit Tests**: Test individual endpoints
- **Integration Tests**: Test full workflows
- **Mock Tests**: Test with mocked dependencies
- **Error Tests**: Test error handling

### Documentation (`docs/api/rest_api.md`)
- Complete API reference
- Usage examples (Python & cURL)
- Development guide
- Production deployment tips

### Examples (`examples/api_example.py`)
- End-to-end usage demonstration
- Upload, simulate, and generate scenarios
- Model management operations

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/simulate` | Run simulation |
| POST | `/generate-scenarios` | Generate scenarios |
| POST | `/distribution-models` | Upload model |
| GET | `/distribution-models` | List models |
| GET | `/distribution-models/{name}` | Get model |
| DELETE | `/distribution-models/{name}` | Delete model |
| GET | `/supported-hazard-types` | List hazard types |
| GET | `/default-curve-sets` | List curve sets |

## Next Steps

1. Install the dependencies: `pip install -e ".[dev]"`
2. Start the API server: `python -m erad.api`
3. Visit http://localhost:8000/docs to explore the interactive API documentation
4. Run the tests: `pytest tests/test_api.py -v`
5. Try the example: `python examples/api_example.py`

## Troubleshooting

**Problem**: Import errors for FastAPI
**Solution**: Run `pip install -e ".[dev]"` to install all dependencies

**Problem**: API won't start
**Solution**: Check if port 8000 is already in use: `lsof -i :8000`

**Problem**: Tests fail with connection errors
**Solution**: Tests use TestClient and don't require a running server

**Problem**: Example script fails
**Solution**: Make sure the API server is running before running the example
