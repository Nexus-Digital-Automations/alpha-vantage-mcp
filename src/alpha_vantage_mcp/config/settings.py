"""
Configuration settings for the Alpha Vantage MCP server.

This module contains configuration variables and settings used throughout the application.
"""

import os
from typing import Optional

# Alpha Vantage API settings
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

# Data type settings
DEFAULT_DATA_TYPE = "json"  # Default data type for API requests (json or csv)

# Request settings
DEFAULT_TIMEOUT = 30  # Default timeout for API requests in seconds

# Rate limiting
MAX_REQUESTS_PER_MINUTE = 5  # Alpha Vantage free tier limit

# Response limits
MAX_DISPLAY_ITEMS = 10  # Maximum number of items to display in formatted responses
MAX_TIME_SERIES_POINTS = 5   # Maximum number of time series data points to display

# Error messages
ERROR_MESSAGES = {
    "missing_api_key": "Alpha Vantage API key is missing. Please set the ALPHA_VANTAGE_API_KEY environment variable.",
    "invalid_api_key": "Invalid Alpha Vantage API key. Please check your API key.",
    "rate_limit_exceeded": "Alpha Vantage API rate limit exceeded. Please try again later.",
    "missing_parameter": "Required parameter is missing: {}",
    "invalid_parameter": "Invalid parameter value for {}: {}",
    "api_error": "Alpha Vantage API error: {}",
    "timeout": "Request to Alpha Vantage API timed out.",
    "connection_error": "Failed to connect to Alpha Vantage API.",
    "unknown_error": "An unknown error occurred: {}",
}

def validate_api_key() -> Optional[str]:
    """
    Validate that the API key is set.
    
    Returns:
        Optional[str]: An error message if validation fails, None if validation passes
    """
    if not API_KEY:
        return ERROR_MESSAGES["missing_api_key"]
    return None