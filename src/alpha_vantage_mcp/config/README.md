# Configuration Module

This module handles application configuration, including API keys, settings, and environment variables.

## Structure

- `settings.py`: Contains configuration settings and validation logic
- `__init__.py`: Initializes the configuration module

## API Key Management

The Alpha Vantage API requires an API key for authentication. The configuration module handles:

1. Loading the API key from environment variables
2. Validating the API key format
3. Providing the API key to other components
4. Handling missing or invalid API keys

The API key is retrieved from the `ALPHA_VANTAGE_API_KEY` environment variable.

## Configuration Settings

The configuration module manages several settings:

1. API base URL
2. Request timeout values
3. Rate limiting settings
4. Retry settings for failed requests
5. Default values for common parameters

## Environment Variables

The following environment variables are supported:

| Variable | Description | Default |
|----------|-------------|---------|
| ALPHA_VANTAGE_API_KEY | Your Alpha Vantage API key (required) | None |
| ALPHA_VANTAGE_BASE_URL | Base URL for the Alpha Vantage API | "https://www.alphavantage.co/query" |
| ALPHA_VANTAGE_TIMEOUT | Request timeout in seconds | 30 |
| ALPHA_VANTAGE_MAX_RETRIES | Maximum number of retries for failed requests | 3 |

## Validation

The `validate_api_key` function checks that:

1. The API key is provided
2. The API key has the expected format
3. The API key is not a placeholder value

Example usage:

```python
from .config.settings import validate_api_key

# Validate API key at startup
api_key = validate_api_key()
```

## Configuration at Startup

The MCP server validates the configuration at startup to ensure:

1. The API key is present and valid
2. Required environment variables are set
3. The application can connect to the Alpha Vantage API

If configuration validation fails, the server will fail to start with a helpful error message.

## Adding New Configuration Settings

To add a new configuration setting:

1. Add the setting to `settings.py`
2. Create a getter function that retrieves the setting
3. Add validation if necessary
4. Document the setting in this README