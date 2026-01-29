# REST API

A FastAPI-based REST API for running hazard simulations on distribution systems using the ERAD (Energy Resilience Analysis for Distribution Systems) framework.

## Features

- **Hazard Simulation**: Run simulations to compute asset survival probabilities and export results as SQLite database files
- **Scenario Generation**: Generate Monte Carlo scenarios with specific asset outages, exported as ZIP files with tracked changes and time series data
- **Distribution System Management**: Upload, list, retrieve, and delete distribution system models with persistent caching
- **Hazard Model Management**: Upload, list, retrieve, and delete hazard models with persistent caching
- **Persistent Cache**: Models are automatically stored in a standard system cache directory
- **File Downloads**: Simulation results and scenarios are returned as downloadable files (SQLite and ZIP)
- **Multiple Hazard Types**: Support for earthquakes, floods, wind, and fire hazards
- **Configurable Fragility Curves**: Use default or custom fragility curves for asset vulnerability

## Cache Directory

Models are persistently stored in platform-specific cache directories:

**Distribution Systems:**
- **Linux/macOS**: `~/.cache/erad/distribution_models/`
- **Windows**: `%LOCALAPPDATA%\erad\distribution_models\`

**Hazard Models:**
- **Linux/macOS**: `~/.cache/erad/hazard_models/`
- **Windows**: `%LOCALAPPDATA%\erad\hazard_models\`

Models persist across API restarts and are automatically loaded on startup.

## Installation

Install the required dependencies:

```bash
pip install -e ".[dev]"
```

Or install just the API dependencies:

```bash
pip install fastapi uvicorn[standard] python-multipart loguru
```

## Quick Start

### Running the API Server

Start the API server:

```bash
python -m erad.api
```

Or using uvicorn directly:

```bash
uvicorn erad.api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health & Info

- **GET /** - Root endpoint with basic API information
- **GET /health** - Health check endpoint

### Simulation

#### Run Simulation
**POST /simulate**

Run a hazard simulation and export results as a SQLite database file.

**Workflow:**
1. Loads the distribution system model from cache by name
2. Loads the hazard system model from cache by name
3. Runs the simulation using HazardSimulator
4. Exports results to a SQLite database
5. Returns the database file for download

**Request body:**
```json
{
  "distribution_system_name": "my_system",
  "hazard_system_name": "earthquake_scenario",
  "curve_set": "DEFAULT_CURVES"
}
```

**Response:** SQLite database file download
- **Content-Type:** `application/x-sqlite3`
- **Filename:** `{distribution_name}_{hazard_name}_results.sqlite`
- **File contains:** Complete simulation results including asset survival probabilities, hazard intensities, and timestamps

#### Generate Scenarios
**POST /generate-scenarios**

Generate Monte Carlo scenarios with specific asset outages and export as a ZIP file.

**Workflow:**
1. Loads the distribution system model from cache by name
2. Loads the hazard system model from cache by name
3. Generates scenarios using HazardScenarioGenerator
4. Creates a DistributionSystem with tracked_changes enabled
5. Exports tracked changes to JSON
6. Packages tracked_changes.json and time series folder into a ZIP file
7. Returns the ZIP file for download

**Request body:**
```json
{
  "distribution_system_name": "my_system",
  "hazard_system_name": "earthquake_scenario",
  "number_of_samples": 100,
  "seed": 42,
  "curve_set": "DEFAULT_CURVES"
}
```

**Response:** ZIP file download
- **Content-Type:** `application/zip`
- **Filename:** `{distribution_name}_scenarios_{num_samples}samples.zip`
- **ZIP contents:**
  - `tracked_changes.json` - JSON file with all scenario edits and metadata
  - `time_series/` - Folder containing time series data for each component

### Distribution System Management

#### Upload Distribution Model
**POST /distribution-models**

Upload a distribution system model as a JSON file to the persistent cache.

```bash
curl -X POST "http://localhost:8000/distribution-models" \
  -F "file=@system.json" \
  -F "name=my_system" \
  -F "description=My test system"
```

Response:
```json
{
  "status": "success",
  "message": "Distribution system 'my_system' uploaded successfully",
  "name": "my_system",
  "file_path": "/home/user/.cache/erad/distribution_models/my_system_123456.json"
}
```

#### List Distribution Models
**GET /distribution-models**

Get a list of all cached distribution system models.

Query parameters:
- `refresh` (boolean, optional): If true, refresh from cache directory before listing

```bash
# List without refresh
curl "http://localhost:8000/distribution-models"

# List with refresh from disk
curl "http://localhost:8000/distribution-models?refresh=true"
```

Response:
```json
[
  {
    "name": "my_system",
    "description": "My test system",
    "created_at": "2024-01-01T00:00:00",
    "file_path": "/home/user/.cache/erad/distribution_models/my_system_123456.json"
  }
]
```

#### Get Distribution Model
**GET /distribution-models/{model_name}**

Retrieve a specific distribution system model.

Response:
```json
{
  "name": "my_system",
  "description": "My test system",
  "created_at": "2024-01-01T00:00:00",
  "content": {
    "name": "my_system",
    "components": [],
    "properties": {}
  }
}
```

#### Delete Distribution Model
**DELETE /distribution-models/{model_name}**

Delete a distribution system model from cache.

Response:
```json
{
  "status": "success",
  "message": "Distribution system 'my_system' deleted successfully"
}
```

### Hazard Model Management

#### Upload Hazard Model
**POST /hazard-models**

Upload a hazard system model as a JSON file to the persistent cache.

```bash
curl -X POST "http://localhost:8000/hazard-models" \
  -F "file=@hazard.json" \
  -F "name=earthquake_scenario" \
  -F "description=Earthquake hazard scenario"
```

Response:
```json
{
  "status": "success",
  "message": "Hazard model 'earthquake_scenario' uploaded successfully",
  "name": "earthquake_scenario",
  "file_path": "/home/user/.cache/erad/hazard_models/earthquake_scenario_123456.json"
}
```

#### List Hazard Models
**GET /hazard-models**

Get a list of all cached hazard models.

Query parameters:
- `refresh` (boolean, optional): If true, refresh from cache directory before listing

Response:
```json
[
  {
    "name": "earthquake_scenario",
    "description": "Earthquake hazard scenario",
    "created_at": "2024-01-01T00:00:00",
    "file_path": "/home/user/.cache/erad/hazard_models/earthquake_scenario_123456.json"
  }
]
```

#### Get Hazard Model
**GET /hazard-models/{model_name}**

Retrieve a specific hazard model.

Response:
```json
{
  "name": "earthquake_scenario",
  "description": "Earthquake hazard scenario",
  "created_at": "2024-01-01T00:00:00",
  "content": {
    "models": [],
    "timestamps": []
  }
}
```

#### Delete Hazard Model
**DELETE /hazard-models/{model_name}**

Delete a hazard model from cache.

Response:
```json
{
  "status": "success",
  "message": "Hazard model 'earthquake_scenario' deleted successfully"
}
```

### Cache Management

#### Get Cache Info
**GET /cache-info**

Get information about the cache directory and stored models.

Response:
```json
{
  "cache_directory": "/home/user/.cache/erad/distribution_models",
  "metadata_file": "/home/user/.cache/erad/distribution_models/models_metadata.json",
  "total_models": 5,
  "total_files": 5,
  "total_size_bytes": 1048576,
  "total_size_mb": 1.0
}
```

#### Refresh Cache
**POST /refresh-cache**

Refresh the model list from the cache directory. This scans for new files and updates metadata.

Response:
```json
{
  "status": "success",
  "message": "Cache refreshed successfully",
  "total_models": 5,
  "models": ["model1", "model2", "model3", "model4", "model5"]
}
```

### Utility Endpoints

#### Get Supported Hazard Types
**GET /supported-hazard-types**

Get a list of supported hazard types.

Response:
```json
{
  "hazard_types": [
    "earthquake",
    "flood",
    "flood_area",
    "wind",
    "fire",
    "fire_area"
  ],
  "descriptions": {
    "earthquake": "Earthquake Model (EarthQuakeModel)",
    "flood": "Flood Model (FloodModel)",
    "flood_area": "Flood Area Model (FloodModelArea)",
    "wind": "Wind Model (WindModel)",
    "fire": "Fire Model (FireModel)",
    "fire_area": "Fire Area Model (FireModelArea)"
  }
}
```

#### Get Default Curve Sets
**GET /default-curve-sets**

Get information about available fragility curve sets.

Response:
```json
{
  "curve_sets": ["DEFAULT_CURVES"],
  "default": "DEFAULT_CURVES",
  "description": "Default fragility curves for various hazard types and assets"
}
```

## Usage Examples

### Python Client Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Upload a distribution system
with open("my_system.json", "rb") as f:
    files = {"file": ("my_system.json", f, "application/json")}
    data = {"name": "my_system", "description": "Test system"}
    response = requests.post(f"{BASE_URL}/distribution-models", files=files, data=data)
    print(response.json())

# 2. Upload a hazard model
with open("hazard.json", "rb") as f:
    files = {"file": ("hazard.json", f, "application/json")}
    data = {"name": "earthquake_scenario", "description": "Earthquake scenario"}
    response = requests.post(f"{BASE_URL}/hazard-models", files=files, data=data)
    print(response.json())

# 3. Run simulation and download SQLite results
simulation_request = {
    "distribution_system_name": "my_system",
    "hazard_system_name": "earthquake_scenario",
    "curve_set": "DEFAULT_CURVES"
}

response = requests.post(f"{BASE_URL}/simulate", json=simulation_request)
with open("simulation_results.sqlite", "wb") as f:
    f.write(response.content)
print("Simulation results saved to simulation_results.sqlite")

# 4. Generate scenarios and download ZIP file
scenario_request = {
    "distribution_system_name": "my_system",
    "hazard_system_name": "earthquake_scenario",
    "number_of_samples": 10,
    "seed": 42,
    "curve_set": "DEFAULT_CURVES"
}

response = requests.post(f"{BASE_URL}/generate-scenarios", json=scenario_request)
with open("scenarios.zip", "wb") as f:
    f.write(response.content)
print("Scenarios saved to scenarios.zip")

# 5. List all models
response = requests.get(f"{BASE_URL}/distribution-models")
models = response.json()
print(f"Available distribution models: {[m['name'] for m in models]}")

response = requests.get(f"{BASE_URL}/hazard-models")
models = response.json()
print(f"Available hazard models: {[m['name'] for m in models]}")
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Get supported hazard types
curl http://localhost:8000/supported-hazard-types

# Upload a distribution system
curl -X POST http://localhost:8000/distribution-models \
  -F "file=@system.json" \
  -F "name=test_system" \
  -F "description=Test system"

# Upload a hazard model
curl -X POST http://localhost:8000/hazard-models \
  -F "file=@hazard.json" \
  -F "name=earthquake_scenario" \
  -F "description=Earthquake scenario"

# List models
curl http://localhost:8000/distribution-models
curl http://localhost:8000/hazard-models

# Run simulation and save SQLite file
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "distribution_system_name": "test_system",
    "hazard_system_name": "earthquake_scenario",
    "curve_set": "DEFAULT_CURVES"
  }' \
  -o simulation_results.sqlite

# Generate scenarios and save ZIP file
curl -X POST http://localhost:8000/generate-scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "distribution_system_name": "test_system",
    "hazard_system_name": "earthquake_scenario",
    "number_of_samples": 5,
    "seed": 42,
    "curve_set": "DEFAULT_CURVES"
  }' \
  -o scenarios.zip

# Delete models
curl -X DELETE http://localhost:8000/distribution-models/test_system
curl -X DELETE http://localhost:8000/hazard-models/earthquake_scenario
```

## Testing

Run the API tests:

```bash
pytest tests/test_api.py -v
```

Run with coverage:

```bash
pytest tests/test_api.py --cov=erad.api --cov-report=html
```

Run only integration tests:

```bash
pytest tests/test_api.py -v -m integration
```

## Development

### Running in Development Mode

```bash
uvicorn erad.api:app --reload --log-level debug
```

### Code Quality

Format code:
```bash
black src/erad/api.py tests/test_api.py
```

Lint code:
```bash
ruff check src/erad/api.py tests/test_api.py
```

## Supported Hazard Types

| Hazard Type | Description | Model Class |
|------------|-------------|-------------|
| `earthquake` | Earthquake hazard model | `EarthQuakeModel` |
| `flood` | Flood hazard model | `FloodModel` |
| `flood_area` | Flood area hazard model | `FloodModelArea` |
| `wind` | Wind hazard model | `WindModel` |
| `fire` | Fire hazard model | `FireModel` |
| `fire_area` | Fire area hazard model | `FireModelArea` |

## Error Handling

The API uses standard HTTP status codes:

- **200 OK** - Successful request
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid request data
- **404 Not Found** - Resource not found
- **409 Conflict** - Resource conflict (e.g., duplicate name)
- **422 Unprocessable Entity** - Validation error
- **500 Internal Server Error** - Server error

Error responses include a `detail` field with a description of the error:

```json
{
  "detail": "Distribution system 'my_system' not found",
  "status_code": 404
}
```

## Production Deployment

For production deployment, consider:

1. **Use a production ASGI server**:
   ```bash
   gunicorn erad.api:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Add authentication/authorization** (e.g., OAuth2, API keys)

3. **Use a proper database** instead of in-memory storage

4. **Add rate limiting** to prevent abuse

5. **Enable CORS** if needed for web clients:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

6. **Set up logging and monitoring**

7. **Use environment variables** for configuration

## License

See LICENSE.txt for license information.

## Contributing

See [CONTRIBUTING.md](../community/contribute.md) for contribution guidelines.
