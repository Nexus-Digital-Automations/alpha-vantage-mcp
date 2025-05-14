# Models Module

This module contains JSON schemas for validating input parameters to Alpha Vantage API endpoints and other data models used throughout the system.

## Structure

- `schemas.py`: Contains JSON schema definitions for all Alpha Vantage API endpoints
- `__init__.py`: Initializes the models module

## JSON Schemas

The `schemas.py` file contains JSON schema definitions that serve several purposes:

1. Validate input parameters for MCP tools
2. Document the available parameters for each endpoint
3. Define default values for optional parameters
4. Specify required parameters
5. Enable consistent parameter validation across the application

## Schema Structure

Each schema follows a consistent structure:

```python
ENDPOINT_SCHEMA = {
    "type": "object",
    "properties": {
        "param1": {
            "type": "string", 
            "description": "Description of parameter 1",
            "enum": ["value1", "value2", "value3"],  # Optional: limited set of values
            "default": "value1"  # Optional: default value
        },
        "param2": {
            "type": "integer",
            "description": "Description of parameter 2",
            "default": 14  # Optional: default value
        }
    },
    "required": ["param1"]  # List of required parameters
}
```

## Adding a New Schema

To add a new schema for an Alpha Vantage endpoint:

1. Create a schema definition in `schemas.py` following the pattern above
2. Add the schema to the `__all__` list in `schemas.py`
3. Import the schema in `server.py` for use in the MCP tool definition

## Example

Here's an example of a schema for a technical indicator:

```python
TECHNICAL_INDICATOR_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string", 
            "description": "Stock symbol (e.g., IBM)"
        },
        "interval": {
            "type": "string", 
            "description": "Time interval between data points.",
            "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
            "default": "daily"
        },
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each indicator value. Positive integers are accepted.",
            "default": 14
        },
        "series_type": {
            "type": "string",
            "description": "The desired price type in the time series",
            "enum": ["close", "open", "high", "low"],
            "default": "close"
        }
    },
    "required": ["symbol"]
}
```

## Schema Validation

Schemas are used in the MCP server to validate input parameters before making API requests. This ensures that:

1. All required parameters are provided
2. Parameter values are of the correct type
3. Enum parameters contain only allowed values
4. Default values are applied when parameters are omitted

The schemas serve as both documentation and runtime validation for the MCP tools.