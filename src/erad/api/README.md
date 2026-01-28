# ERAD API Module

This directory contains the modular REST API implementation for the ERAD Hazard Simulator.

## Structure

```
api/
├── __init__.py              # Package exports
├── main.py                  # FastAPI application and router setup
├── models.py                # Pydantic models for requests/responses
├── cache.py                 # Cache management for distribution and hazard models
├── helpers.py               # Helper functions for loading and creating systems
├── distribution_models.py   # Distribution model CRUD endpoints
├── hazard_models.py         # Hazard model CRUD endpoints
├── simulation.py            # Simulation and scenario generation endpoints
└── utility.py               # Utility endpoints (health, cache info, etc.)
```

## Key Features

### Distribution Model Management
- **POST /distribution-models** - Upload distribution system as ZIP file
- **GET /distribution-models** - List all uploaded distribution models
- **GET /distribution-models/{name}** - Get specific distribution model details
- **DELETE /distribution-models/{name}** - Delete a distribution model

### Hazard Model Management
- **POST /hazard-models** - Upload hazard model as ZIP file
- **GET /hazard-models** - List all uploaded hazard models  
- **GET /hazard-models/{name}** - Get specific hazard model details
- **DELETE /hazard-models/{name}** - Delete a hazard model

### Simulation
- **POST /simulate** - Run hazard simulation using cached models, returns SQLite results file
  - Loads both distribution and hazard models from cache by name
  - Runs simulation with specified fragility curve set
  - Exports results to SQLite database
  - Returns downloadable file: `{distribution_name}_{hazard_name}_results.sqlite`
  
- **POST /generate-scenarios** - Generate hazard scenarios, returns ZIP with tracked changes
  - Loads distribution and hazard models from cache
  - Generates specified number of scenario samples with random seed
  - Creates tracked changes showing asset state modifications
  - Packages results with time series data in ZIP file
  - Returns downloadable file: `{distribution_name}_scenarios_{num_samples}samples.zip`

### Utility
- **GET /** - API root information
- **GET /health** - Health check endpoint
- **GET /cache-info** - Information about cache directories
- **POST /refresh-cache** - Refresh model lists from cache
- **GET /supported-hazard-types** - List supported hazard types
- **GET /default-curve-sets** - Get default fragility curve sets

## Cache System

The API uses a persistent cache system for both distribution and hazard models:

- **Distribution Models**: `~/.cache/erad/distribution_models/` (Unix) or `%LOCALAPPDATA%\erad\distribution_models\` (Windows)
- **Hazard Models**: `~/.cache/erad/hazard_models/` (Unix) or `%LOCALAPPDATA%\erad\hazard_models\` (Windows)

Each cache includes:
- JSON model files (with original filenames preserved)
- Optional time series folders (`*_time_series/`)
- Metadata JSON file for tracking uploaded models

## File Upload Format

Both distribution and hazard models support ZIP file uploads with the following structure:

```
model.zip
├── model.json              # Main model definition
└── model_time_series/      # Optional time series data folder
    ├── file1.csv
    ├── file2.csv
    └── ...
```

The API preserves original filenames when extracting to cache.

## Usage

### Starting the API

```python
from erad.api import app
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
```

Or from command line:
```bash
python -m erad.api.main
```

### Example Workflow

1. **Upload a distribution model:**
```bash
curl -X POST "http://localhost:8000/distribution-models" \
  -F "file=@distribution_model.zip" \
  -F "name=power_grid_1" \
  -F "description=Main power grid"
```

2. **Upload a hazard model:**
```bash
curl -X POST "http://localhost:8000/hazard-models" \
  -F "file=@earthquake_model.zip" \
  -F "name=earthquake_2024" \
  -F "hazard_type=earthquake" \
  -F "description=Earthquake scenario"
```

3. **Run simulation:**
```bash
curl -X POST "http://localhost:8000/simulate" \
  -H "Content-Type: application/json" \
  -d '{
    "distribution_system_name": "power_grid_1",
    "hazard_system_name": "earthquake_2024",
    "curve_set": "DEFAULT_CURVES"
  }' \
  --output simulation_results.sqlite
```

4. **Generate scenarios:**
```bash
curl -X POST "http://localhost:8000/generate-scenarios" \
  -H "Content-Type: application/json" \
  -d '{
    "distribution_system_name": "power_grid_1",
    "hazard_system_name": "earthquake_2024",
    "number_of_samples": 100,
    "seed": 42,
    "curve_set": "DEFAULT_CURVES"
  }' \
  --output scenarios.zip
```

### API Documentation

Once running, access interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the API tests:
```bash
pytest tests/test_api.py -v
```

## Design Decisions

1. **Modular Structure**: Split monolithic `api.py` into logical modules for better maintainability
2. **Persistent Cache**: Store models on disk to survive API restarts
3. **ZIP-only Uploads**: Standardized on ZIP format to support time series data
4. **Filename Preservation**: Retain original filenames to maintain references in model data
5. **Shared Storage**: Use module-level dictionaries initialized from `main.py` for in-memory model tracking
6. **Cache-based Simulation**: Simulation endpoints reference models by name from cache rather than accepting inline data
7. **File Downloads**: Both simulation and scenario generation return downloadable files instead of JSON responses

## API Request/Response Formats

### Simulation Request
```json
{
  "distribution_system_name": "power_grid_1",
  "hazard_system_name": "earthquake_2024",
  "curve_set": "DEFAULT_CURVES"
}
```
**Response**: SQLite file download

### Scenario Generation Request
```json
{
  "distribution_system_name": "power_grid_1",
  "hazard_system_name": "earthquake_2024",
  "number_of_samples": 100,
  "seed": 42,
  "curve_set": "DEFAULT_CURVES"
}
```
**Response**: ZIP file containing:
- `tracked_changes.json` - Generated scenario data
- `tracked_changes_time_series/` - Time series data folder (if present)
