"""
Input validation utilities for Alpha Vantage MCP tools.

This module provides functions for validating user input before making API requests.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import re
from datetime import datetime
from ..config.settings import ERROR_MESSAGES

def validate_symbol(symbol: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate a stock or cryptocurrency symbol.
    
    Args:
        symbol: The symbol to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not symbol:
        return False, ERROR_MESSAGES["missing_parameter"].format("symbol")
    
    # Remove any whitespace and convert to uppercase
    symbol = symbol.strip().upper()
    
    # Basic validation - symbols are usually 1-5 alphanumeric characters
    # Some may include dots (e.g., BRK.A) or hyphens
    if not re.match(r'^[A-Z0-9\.\-]{1,5}$', symbol):
        return False, ERROR_MESSAGES["invalid_parameter"].format("symbol", symbol)
    
    return True, None

def validate_date(date_str: Optional[str], format_str: str = "%Y-%m-%d") -> Tuple[bool, Optional[str]]:
    """
    Validate a date string.
    
    Args:
        date_str: The date string to validate
        format_str: Expected date format
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_str:
        return True, None  # Date is optional
    
    try:
        datetime.strptime(date_str, format_str)
        return True, None
    except ValueError:
        return False, ERROR_MESSAGES["invalid_parameter"].format(
            "date", f"{date_str} (expected format: {format_str})"
        )

def validate_enum(value: Optional[str], valid_values: List[str], 
                 param_name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a value is one of a set of valid values.
    
    Args:
        value: The value to validate
        valid_values: List of valid values
        param_name: Name of the parameter (for error message)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return True, None  # Assume parameter is optional
    
    if value not in valid_values:
        return False, ERROR_MESSAGES["invalid_parameter"].format(
            param_name, f"{value} (expected one of: {', '.join(valid_values)})"
        )
    
    return True, None

def validate_number(value: Optional[Union[int, float, str]], 
                   min_value: Optional[float] = None,
                   max_value: Optional[float] = None,
                   param_name: str = "value") -> Tuple[bool, Optional[str]]:
    """
    Validate that a value is a number within specified range.
    
    Args:
        value: The value to validate
        min_value: Minimum acceptable value (optional)
        max_value: Maximum acceptable value (optional)
        param_name: Name of the parameter (for error message)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if value is None:
        return True, None  # Assume parameter is optional
    
    # Convert string to number if needed
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return False, ERROR_MESSAGES["invalid_parameter"].format(
                param_name, f"{value} (not a valid number)"
            )
    
    # Check range if specified
    if min_value is not None and value < min_value:
        return False, ERROR_MESSAGES["invalid_parameter"].format(
            param_name, f"{value} (less than minimum: {min_value})"
        )
    
    if max_value is not None and value > max_value:
        return False, ERROR_MESSAGES["invalid_parameter"].format(
            param_name, f"{value} (greater than maximum: {max_value})"
        )
    
    return True, None

def validate_interval(interval: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate a time interval parameter.
    
    Args:
        interval: The interval to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_intervals = [
        "1min", "5min", "15min", "30min", "60min",
        "daily", "weekly", "monthly"
    ]
    
    return validate_enum(interval, valid_intervals, "interval")

def validate_output_size(output_size: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate an output size parameter.
    
    Args:
        output_size: The output size to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_sizes = ["compact", "full"]
    
    return validate_enum(output_size, valid_sizes, "outputsize")

def validate_required_params(params: Dict[str, Any], 
                            required_params: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate that all required parameters are present.
    
    Args:
        params: Dictionary of parameter values
        required_params: List of required parameter names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    missing_params = []
    
    for param in required_params:
        if param not in params or params[param] is None or params[param] == "":
            missing_params.append(param)
    
    if missing_params:
        return False, ERROR_MESSAGES["missing_parameter"].format(
            ", ".join(missing_params)
        )
    
    return True, None