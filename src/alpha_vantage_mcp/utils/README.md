# Utils Module

This module contains utility functions and helpers used throughout the application.

## Structure

- `error_handling.py`: Functions for handling and formatting errors
- `validation.py`: Functions for validating input parameters
- `__init__.py`: Initializes the utils module

## Error Handling

The `error_handling.py` module provides functions for:

1. Handling exceptions from the Alpha Vantage API
2. Formatting error messages for users
3. Logging errors for debugging
4. Providing consistent error responses

Common functions include:

- `handle_api_error`: Converts API exceptions to user-friendly messages
- `format_error_message`: Creates a formatted error message for users
- `handle_validation_error`: Handles input validation errors

Example usage:

```python
try:
    # Code that might raise an exception
    result = do_something_risky()
    return result
except Exception as e:
    error_message = handle_api_error(e)
    return TextContent(error_message)
```

## Validation

The `validation.py` module provides functions for:

1. Validating input parameters before making API requests
2. Checking parameter types, ranges, and formats
3. Ensuring required parameters are provided
4. Converting parameters to the correct format

Common validation functions include:

- `validate_symbol`: Checks that a stock symbol is valid
- `validate_interval`: Validates the time interval parameter
- `validate_time_period`: Ensures the time period is a positive integer
- `validate_date`: Checks that a date string has the correct format

Example usage:

```python
def handle_request(symbol, interval="daily", time_period=14):
    # Validate parameters
    validate_symbol(symbol)
    validate_interval(interval)
    validate_time_period(time_period)
    
    # Continue with the request...
```

## Adding New Utility Functions

To add a new utility function:

1. Identify the appropriate category file (or create a new one if needed)
2. Create a function with clear parameters and return values
3. Add proper docstrings explaining the function's purpose
4. Add unit tests for the function
5. Import and use the function where needed

Example:

```python
def validate_parameter(param, allowed_values, param_name="parameter"):
    """
    Validate that a parameter is in the list of allowed values.
    
    Args:
        param: The parameter value to validate
        allowed_values: List of allowed values
        param_name: Name of the parameter (for error messages)
        
    Raises:
        ValueError: If the parameter is not in the allowed values
    """
    if param not in allowed_values:
        allowed_str = ", ".join(str(v) for v in allowed_values)
        raise ValueError(f"Invalid {param_name}: '{param}'. Must be one of: {allowed_str}")
```