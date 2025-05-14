# API Module

This module handles communication with the Alpha Vantage API, providing a consistent interface for making requests and handling responses.

## Structure

- `client.py`: Contains the API client for making requests to Alpha Vantage
- `__init__.py`: Initializes the API module

## API Client

The API client is responsible for:

1. Building request URLs with the appropriate parameters
2. Managing the API key for authentication
3. Handling HTTP requests and responses
4. Implementing rate limiting and error handling
5. Providing a consistent interface for the handler functions

## Making API Requests

The primary function used for API requests is `make_alpha_vantage_request`, which:

1. Takes a dictionary of query parameters
2. Adds the API key from configuration
3. Makes an HTTP request to the Alpha Vantage API
4. Returns the parsed JSON response
5. Handles errors, retries, and rate limiting

Example usage:

```python
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "MSFT",
    "outputsize": "compact"
}

response_data = await make_alpha_vantage_request(params)
```

## Rate Limiting

The Alpha Vantage API has the following rate limits:

- Free API key: 5 requests per minute, 500 requests per day
- Premium API keys: Various limits based on subscription level

The API client implements rate limiting to avoid exceeding these limits by:

1. Adding delays between requests when necessary
2. Handling rate limit exceeded errors gracefully
3. Providing meaningful error messages when rate limits are reached

## Error Handling

The API client handles various error scenarios:

1. Network errors (timeout, connection failed)
2. Rate limiting errors (HTTP 429)
3. Invalid API key errors
4. Not found errors (HTTP 404)
5. API response format errors
6. JSON parsing errors

## Configuration

The API client uses configuration from the `config` module, specifically:

1. API key from environment variables or configuration file
2. Base URL for the Alpha Vantage API
3. Timeout settings
4. Retry settings

## Adding New Endpoints

The API client is designed to work with any Alpha Vantage endpoint. To use a new endpoint:

1. Use the same `make_alpha_vantage_request` function
2. Specify the appropriate function name in the parameters
3. Handle the specific response format in your formatter function

Example for a new endpoint:

```python
async def request_new_endpoint(param1, param2):
    params = {
        "function": "NEW_ENDPOINT",
        "param1": param1,
        "param2": param2
    }
    
    return await make_alpha_vantage_request(params)
```