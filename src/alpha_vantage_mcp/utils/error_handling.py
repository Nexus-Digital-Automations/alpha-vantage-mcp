"""
Error handling utilities for Alpha Vantage MCP server.

This module provides functions for handling errors and exceptions.
"""

from typing import Any, Dict, Optional, Union
import httpx
import traceback
import logging
from ..config.settings import ERROR_MESSAGES

# Set up logger
logger = logging.getLogger("alpha_vantage_mcp")

class AlphaVantageError(Exception):
    """Base exception class for Alpha Vantage MCP errors."""
    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

def handle_api_error(response_data: Union[Dict[str, Any], str]) -> Optional[str]:
    """
    Check for and handle Alpha Vantage API errors in the response.
    
    Args:
        response_data: API response data (either dict for JSON or str for CSV)
        
    Returns:
        Error message if an error was detected, None otherwise
    """
    # Check for string error responses
    if isinstance(response_data, str):
        if "Error Message" in response_data:
            return f"Alpha Vantage API error: {response_data}"
        if "Thank you for using Alpha Vantage" in response_data and "API key" in response_data:
            return ERROR_MESSAGES["invalid_api_key"]
        if "higher API call frequency" in response_data:
            return ERROR_MESSAGES["rate_limit_exceeded"]
        
        # If it's a valid CSV response, it's probably not an error
        return None
        
    # Check for JSON error responses
    if isinstance(response_data, dict):
        # Check for explicit error messages
        if "Error Message" in response_data:
            return f"Alpha Vantage API error: {response_data['Error Message']}"
            
        # Check for Note field which often contains rate limiting warnings
        if "Note" in response_data:
            if "call frequency" in response_data["Note"]:
                return ERROR_MESSAGES["rate_limit_exceeded"]
            return f"Alpha Vantage API warning: {response_data['Note']}"
            
        # Check for empty response
        time_series_keys = [key for key in response_data.keys() if "Time Series" in key]
        if time_series_keys and not response_data[time_series_keys[0]]:
            return "No data available for the requested parameters."
            
    return None

def handle_request_exception(exception: Exception) -> str:
    """
    Handle exceptions that occur during API requests.
    
    Args:
        exception: The exception that occurred
        
    Returns:
        Formatted error message
    """
    # Log the exception
    logger.error(f"API request error: {str(exception)}")
    logger.debug(traceback.format_exc())
    
    # Handle specific exception types
    if isinstance(exception, httpx.TimeoutException):
        return ERROR_MESSAGES["timeout"]
    elif isinstance(exception, httpx.ConnectError):
        return ERROR_MESSAGES["connection_error"]
    elif isinstance(exception, httpx.RequestError):
        return f"Request error: {str(exception)}"
    elif isinstance(exception, AlphaVantageError):
        if exception.code:
            return f"{exception.code}: {exception.message}"
        return exception.message
    else:
        return ERROR_MESSAGES["unknown_error"].format(str(exception))

def format_error_response(error_message: str) -> str:
    """
    Format an error message for client display.
    
    Args:
        error_message: The error message
        
    Returns:
        Formatted error string
    """
    return f"Error: {error_message}"