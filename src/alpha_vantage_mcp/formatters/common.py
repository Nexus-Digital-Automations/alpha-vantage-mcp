"""
Common formatting utilities for Alpha Vantage API responses.

This module provides utility functions used across different formatter modules
to maintain consistent formatting of financial data.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import re
from ..config.settings import MAX_DISPLAY_ITEMS

def format_number(value: Union[float, int, str], is_currency: bool = False, 
                  decimal_places: int = 2) -> str:
    """
    Format a number with proper formatting.
    
    Args:
        value: The number to format
        is_currency: Whether to format as currency with $ symbol
        decimal_places: Number of decimal places to show
        
    Returns:
        Formatted number string
    """
    if value is None or value == "":
        return "N/A"
        
    # Convert string to float if needed
    if isinstance(value, str):
        # Remove any existing commas
        value = value.replace(",", "")
        try:
            value = float(value)
        except ValueError:
            return value  # Return original if conversion fails
    
    # Format the number
    if is_currency:
        return f"${value:,.{decimal_places}f}"
    else:
        return f"{value:,.{decimal_places}f}"

def format_percentage(value: Union[float, int, str], include_sign: bool = True) -> str:
    """
    Format a value as a percentage.
    
    Args:
        value: The value to format (0.05 = 5%)
        include_sign: Whether to include + sign for positive values
        
    Returns:
        Formatted percentage string
    """
    if value is None or value == "":
        return "N/A"
    
    # Convert string to float if needed
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return value  # Return original if conversion fails
    
    # Ensure value is in decimal form (e.g., 0.05 for 5%)
    if abs(value) > 1 and abs(value) < 100:
        # Value might already be in percentage form (e.g., 5 instead of 0.05)
        value = value / 100
    
    # Format with sign
    if include_sign and value > 0:
        return f"+{value:.2%}"
    else:
        return f"{value:.2%}"

def format_date(date_str: str, input_format: str = "%Y-%m-%d", 
                output_format: str = "%Y-%m-%d") -> str:
    """
    Format a date string.
    
    Args:
        date_str: The date string to format
        input_format: The format of the input date
        output_format: The desired output format
        
    Returns:
        Formatted date string
    """
    if not date_str:
        return "N/A"
    
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return date_str  # Return original if conversion fails

def format_volume(volume: Union[int, str]) -> str:
    """
    Format a volume number with commas.
    
    Args:
        volume: The volume number
        
    Returns:
        Formatted volume string
    """
    if volume is None or volume == "":
        return "N/A"
    
    # Convert string to int if needed
    if isinstance(volume, str):
        try:
            volume = int(float(volume))
        except ValueError:
            return volume  # Return original if conversion fails
    
    return f"{int(volume):,}"

def truncate_list(items: List[Any], max_items: Optional[int] = None) -> List[Any]:
    """
    Truncate a list to the specified maximum number of items.
    
    Args:
        items: List of items to truncate
        max_items: Maximum number of items to return, defaults to MAX_DISPLAY_ITEMS
        
    Returns:
        Truncated list
    """
    if max_items is None:
        max_items = MAX_DISPLAY_ITEMS
        
    if not items or len(items) <= max_items:
        return items
    else:
        return items[:max_items]

def clean_key(key: str) -> str:
    """
    Clean up API response keys for better display.
    
    Args:
        key: The key to clean
        
    Returns:
        Cleaned key string
    """
    # Replace periods, underscores, and camelCase with spaces
    key = re.sub(r'([a-z])([A-Z])', r'\1 \2', key)  # Insert space before capital letters
    key = key.replace('.', ' ').replace('_', ' ')
    
    # Clean up specific abbreviations
    key = key.replace('Pct', 'Percentage')
    key = key.replace('Num', 'Number')
    key = key.replace('Amt', 'Amount')
    key = key.replace('Avg', 'Average')
    key = key.replace('Vol', 'Volume')
    
    # Capitalize each word
    return key.title()

def extract_metadata(data: Dict[str, Any], metadata_key: str = "Meta Data") -> Dict[str, str]:
    """
    Extract metadata from Alpha Vantage API response.
    
    Args:
        data: The API response data
        metadata_key: The key containing metadata in the response
        
    Returns:
        Dictionary with metadata information
    """
    metadata = {}
    
    if metadata_key in data:
        # Extract common metadata fields
        meta = data[metadata_key]
        
        if "1. Information" in meta:
            metadata["information"] = meta["1. Information"]
            
        if "2. Symbol" in meta:
            metadata["symbol"] = meta["2. Symbol"]
            
        if "3. Last Refreshed" in meta:
            metadata["last_refreshed"] = meta["3. Last Refreshed"]
            
        if "4. Interval" in meta:
            metadata["interval"] = meta["4. Interval"]
            
        if "4. Output Size" in meta:
            metadata["output_size"] = meta["4. Output Size"]
            
        if "5. Time Zone" in meta:
            metadata["timezone"] = meta["5. Time Zone"]
            
    return metadata

def format_error_message(error: str) -> str:
    """
    Format an error message for display.
    
    Args:
        error: The error message
        
    Returns:
        Formatted error message
    """
    return f"Error: {error}"