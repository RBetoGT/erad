# Cache Functionality Enhancement - Summary

## Overview

Enhanced the ERAD REST API with persistent cache functionality for distribution system models. Models are now stored in a standard system cache directory and automatically loaded on API startup.

## New Features

### 1. Standard Cache Directory
- **Location**: Platform-specific cache directory
  - Linux/macOS: `~/.cache/erad/distribution_models/`
  - Windows: `%LOCALAPPDATA%\erad\distribution_models\`
- **Automatic creation**: Directory is created automatically if it doesn't exist
- **Persistence**: Models persist across API restarts

### 2. Metadata Management
- **Metadata file**: `models_metadata.json` stores model information
- **Auto-save**: Metadata is automatically saved when models are uploaded or deleted
- **Auto-load**: Metadata is loaded on API startup

### 3. New API Endpoints

#### GET /cache-info
Get information about the cache directory:
```json
{
  "cache_directory": "/Users/user/.cache/erad/distribution_models",
  "metadata_file": "/Users/user/.cache/erad/distribution_models/models_metadata.json",
  "total_models": 3,
  "total_files": 3,
  "total_size_bytes": 524288,
  "total_size_mb": 0.5
}
```

#### POST /refresh-cache
Manually refresh the model list from disk:
```json
{
  "status": "success",
  "message": "Cache refreshed successfully",
  "total_models": 3,
  "models": ["model1", "model2", "model3"]
}
```

#### GET /distribution-models?refresh=true
List models with optional auto-refresh from disk:
```bash
curl "http://localhost:8000/distribution-models?refresh=true"
```

### 4. Enhanced Existing Endpoints

#### POST /distribution-models
- Now saves to cache directory instead of local `uploaded_models/` folder
- Persists metadata to disk
- Returns full cache path in response

#### DELETE /distribution-models/{name}
- Updates metadata file after deletion
- Ensures cache consistency

### 5. Automatic Cache Loading
- On API startup, models are automatically loaded from cache
- Scans cache directory for existing model files
- Validates files and updates metadata

## Implementation Details

### Key Functions

1. **get_cache_directory()**: Returns platform-specific cache directory
2. **get_metadata_file()**: Returns metadata file path
3. **load_metadata()**: Loads metadata from disk
4. **save_metadata()**: Saves metadata to disk
5. **scan_cache_directory()**: Scans directory for model files
6. **refresh_models_from_cache()**: Refreshes in-memory models from disk

### Startup Behavior

```python
@app.on_event("startup")
async def startup_event():
    """Load models from cache on startup."""
    logger.info("Starting ERAD API...")
    refresh_models_from_cache()
    logger.info(f"API ready with {len(uploaded_models)} cached models")
```

## Testing

### Test Coverage
- **28 tests** total, all passing ✅
- **New tests** added for cache functionality:
  - `test_get_cache_info`: Tests cache info endpoint
  - `test_refresh_cache`: Tests manual cache refresh
  - `test_list_models_with_refresh`: Tests listing with refresh parameter
  - `test_cache_directory_creation`: Tests cache directory creation

### Test Results
```
======================== 28 passed, 4 warnings in 0.80s ========================
```

## Usage Examples

### Python Example

```python
import requests

# Get cache information
response = requests.get("http://localhost:8000/cache-info")
print(response.json())

# Upload model (auto-saved to cache)
with open("model.json", "rb") as f:
    files = {"file": ("model.json", f, "application/json")}
    data = {"name": "my_model", "description": "My model"}
    response = requests.post(
        "http://localhost:8000/distribution-models",
        files=files,
        data=data
    )

# List models with refresh
response = requests.get("http://localhost:8000/distribution-models?refresh=true")
models = response.json()

# Manually refresh cache
response = requests.post("http://localhost:8000/refresh-cache")
```

### cURL Examples

```bash
# Get cache info
curl http://localhost:8000/cache-info

# Refresh cache
curl -X POST http://localhost:8000/refresh-cache

# List models with refresh
curl "http://localhost:8000/distribution-models?refresh=true"
```

## Files Modified

1. **src/erad/api.py**:
   - Added cache directory management functions
   - Added metadata persistence
   - Added new cache endpoints
   - Added startup event handler
   - Updated upload/delete endpoints

2. **tests/test_api.py**:
   - Added 4 new tests for cache functionality
   - Updated fixtures to work with cache

3. **docs/api/rest_api.md**:
   - Added cache directory documentation
   - Added new endpoint documentation
   - Updated existing endpoint examples

4. **examples/cache_demo.py**:
   - New demo script showcasing cache functionality

5. **test_cache.py**:
   - Standalone test script for cache functions

## Benefits

1. **Persistence**: Models survive API restarts
2. **Standard Location**: Uses OS-specific cache directories
3. **Automatic Loading**: No manual intervention needed
4. **Cache Management**: Built-in tools to inspect and manage cache
5. **Flexibility**: Can refresh from disk or manually manage files
6. **Backwards Compatible**: Existing endpoints still work the same way

## Migration Notes

- Old uploads in `uploaded_models/` directory are not automatically migrated
- New uploads will go to the cache directory
- To migrate old models, manually copy JSON files to cache directory and run `/refresh-cache`

## Future Enhancements

Potential improvements:
1. Add cache cleanup/pruning based on age or size
2. Add cache export/import functionality
3. Add model versioning
4. Add cache statistics and analytics
5. Add support for model tags/categories
