# MCP Server

A Model Context Protocol (MCP) server for integrating ERAD hazard simulation capabilities with AI assistants like Claude, GitHub Copilot, and other MCP-compatible clients.

## Overview

The ERAD MCP server exposes distribution system models and hazard models through the standardized MCP protocol, enabling AI assistants to:

- Access cached distribution system models and hazard models as resources
- Run hazard simulations using cached models
- Generate Monte Carlo scenarios for risk analysis
- Query hazard type information and cache status
- Manage distribution and hazard model caches

## Installation

Install ERAD with MCP support:

```bash
pip install -e ".[dev]"
```

Or install just the MCP dependency:

```bash
pip install mcp>=1.0.0
```

## Running the Server

### Using the Entry Point

```bash
erad-mcp
```

### Using Python Module

```bash
python -m erad.mcp
```

## VS Code Integration

### Configuration

Add the following to your `.vscode/mcp.json` file:

```json
{
  "mcpServers": {
    "erad": {
      "command": "python",
      "args": ["-m", "erad.mcp"]
    }
  }
}
```

Or if using a conda environment:

```json
{
  "mcpServers": {
    "erad": {
      "command": "conda",
      "args": ["run", "-n", "erad", "python", "-m", "erad.mcp"]
    }
  }
}
```

## Resources

The MCP server exposes the following resources:

### Cache Info
**URI:** `erad://cache/info`

Returns information about the cache directory and stored models.

```json
{
  "cache_directory": "/home/user/.cache/erad/distribution_models",
  "metadata_file": "/home/user/.cache/erad/distribution_models/models_metadata.json",
  "total_models": 3
}
```

### Hazard Types
**URI:** `erad://hazards/types`

Returns supported hazard types and descriptions.

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

### Model Data
**URI:** `erad://models/{model_name}`

Returns the full JSON data for a specific distribution system model.

### Model Summary
**URI:** `erad://models/{model_name}/summary`

Returns a summary of a distribution system model including component counts.

### Hazard Model Data
**URI:** `erad://hazards/{model_name}`

Returns the full JSON data for a specific hazard system model.

### Hazard Model Summary
**URI:** `erad://hazards/{model_name}/summary`

Returns a summary of a hazard system model including hazard counts and timestamps.

## Tools

The MCP server provides the following tools:

### run_simulation

Run a hazard simulation using cached distribution and hazard system models.

**Parameters:**
- `distribution_system_name` (string, required): Name of the cached distribution system model
- `hazard_system_name` (string, required): Name of the cached hazard system model
- `curve_set` (string, optional): Fragility curve set to use (default: "DEFAULT_CURVES")

**Example:**
```json
{
  "distribution_system_name": "my_system",
  "hazard_system_name": "earthquake_scenario",
  "curve_set": "DEFAULT_CURVES"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Simulation completed successfully",
  "distribution_system_name": "my_system",
  "hazard_system_name": "earthquake_scenario",
  "asset_count": 10,
  "hazard_count": 3,
  "timestamps": ["2024-01-01T00:00:00"],
  "curve_set": "DEFAULT_CURVES"
}
```

### generate_scenarios

Generate Monte Carlo scenarios using cached distribution and hazard system models.

**Parameters:**
- `distribution_system_name` (string, required): Name of the cached distribution system model
- `hazard_system_name` (string, required): Name of the cached hazard system model
- `number_of_samples` (integer, optional): Number of scenarios to generate (default: 1)
- `seed` (integer, optional): Random seed for reproducibility
- `curve_set` (string, optional): Fragility curve set to use (default: "DEFAULT_CURVES")

**Example:**
```json
{
  "distribution_system_name": "my_system",
  "hazard_system_name": "earthquake_scenario",
  "number_of_samples": 100,
  "seed": 42,
  "curve_set": "DEFAULT_CURVES"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Scenarios generated successfully",
  "distribution_system_name": "my_system",
  "hazard_system_name": "earthquake_scenario",
  "number_of_samples": 100,
  "seed": 42,
  "total_scenarios": 100,
  "scenarios": [
    {
      "scenario_name": "sample_0",
      "timestamp": "2024-01-01T00:00:00",
      "edits": [
        {
          "component_uuid": "asset_1_uuid",
          "name": "in_service",
          "value": false
        }
      ]
    }
  ]
}
```

### list_cached_models

List all distribution system models available in the cache.

**Parameters:** None

**Returns:**
```json
{
  "models": [
    {
      "name": "model1",
      "description": "Test model",
      "created_at": "2024-01-01T00:00:00",
      "file_path": "/path/to/model.json"
    }
  ],
  "total_count": 1
}
```

### get_model_info

Get detailed information about a specific cached model.

**Parameters:**
- `model_name` (string, required): Name of the model to retrieve info for

### refresh_cache

Refresh the model list from the cache directory.

**Parameters:** None

### get_cache_info

Get information about the cache directory.

**Parameters:** None

**Returns:**
```json
{
  "cache_directory": "/home/user/.cache/erad/distribution_models",
  "metadata_file": "/home/user/.cache/erad/distribution_models/models_metadata.json",
  "total_models": 3,
  "total_files": 3,
  "total_size_bytes": 1024000,
  "total_size_mb": 1.0
}
```

### list_cached_hazard_models

List all hazard system models available in the cache.

**Parameters:** None

**Returns:**
```json
{
  "total_models": 2,
  "models": [
    {
      "name": "earthquake_scenario",
      "description": "Earthquake hazard model",
      "created_at": "2024-01-01T00:00:00"
    },
    {
      "name": "flood_scenario",
      "description": "Flood hazard model",
      "created_at": "2024-01-02T00:00:00"
    }
  ]
}
```

### get_hazard_model_info

Get detailed information about a specific cached hazard model.

**Parameters:**
- `model_name` (string, required): Name of the hazard model to retrieve info for

**Returns:**
```json
{
  "name": "earthquake_scenario",
  "description": "Earthquake hazard model",
  "created_at": "2024-01-01T00:00:00",
  "file_path": "/home/user/.cache/erad/hazard_models/earthquake_scenario.json",
  "file_size_bytes": 2048,
  "content_keys": ["models", "timestamps"],
  "hazard_model_count": 3,
  "timestamp_count": 1
}
```

## Prompts

The MCP server provides template prompts for common tasks:

### simulate_hazard

Generate a prompt for running a hazard simulation.

**Arguments:**
- `model_name` (string, required): Name of the distribution system model
- `hazard_type` (string, required): Type of hazard (earthquake, flood, wind, fire, etc.)

### analyze_vulnerability

Generate a prompt for analyzing system vulnerability to hazards.

**Arguments:**
- `model_name` (string, required): Name of the distribution system model

## Supported Hazard Types

| Hazard Type | Description | Model Class |
|------------|-------------|-------------|
| `earthquake` | Earthquake hazard model | `EarthQuakeModel` |
| `flood` | Flood hazard model | `FloodModel` |
| `flood_area` | Flood area hazard model | `FloodModelArea` |
| `wind` | Wind hazard model | `WindModel` |
| `fire` | Fire hazard model | `FireModel` |
| `fire_area` | Fire area hazard model | `FireModelArea` |

## Cache Directory

Models are stored in platform-specific cache directories:

**Distribution Systems:**
- **Linux/macOS:** `~/.cache/erad/distribution_models/`
- **Windows:** `%LOCALAPPDATA%\erad\distribution_models\`

**Hazard Models:**
- **Linux/macOS:** `~/.cache/erad/hazard_models/`
- **Windows:** `%LOCALAPPDATA%\erad\hazard_models\`

Models uploaded via the REST API are automatically available to the MCP server.

## Example Usage with AI Assistants

Once configured, you can interact with the ERAD MCP server through your AI assistant:

**Listing available models:**
> "What distribution system models are available in ERAD?"

> "List all cached hazard models"

**Running a simulation:**
> "Run an earthquake simulation using the 'test_system' distribution model and 'earthquake_scenario' hazard model"

**Generating scenarios:**
> "Generate 100 Monte Carlo scenarios using 'distribution_grid_1' and 'flood_scenario' with seed 42"

**Getting hazard information:**
> "What hazard types does ERAD support?"

**Model information:**
> "Get details about the 'earthquake_scenario' hazard model"

## Testing

Run the MCP server tests:

```bash
pytest tests/test_mcp.py -v
```

## Architecture

The MCP server shares the same cache directories and model management functionality as the REST API, ensuring consistency between both interfaces:

```
┌─────────────────┐     ┌─────────────────┐
│   REST API      │     │   MCP Server    │
│   (api.py)      │     │   (mcp.py)      │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   Cache Directory     │
         │ ~/.cache/erad/        │
         │ ├── distribution_     │
         │ │   models/           │
         │ └── hazard_models/    │
         └───────────────────────┘
```

**Key Features:**
- **Unified Cache:** Both REST API and MCP server use the same cache
- **Model Persistence:** Models uploaded via REST API are accessible through MCP
- **Cross-Interface Compatibility:** Changes in one interface are immediately available in the other

## See Also

- [REST API Documentation](rest_api.md)
- [Data Models](data_models.md)
- [ERAD Documentation](../intro.md)
