"""
Alpha Vantage API client module.

This module provides functions for making requests to the Alpha Vantage API
and handling common API operations.
"""

from typing import Any, Dict, Optional, Union
import httpx
import csv
import io
from ..config.settings import (
    ALPHA_VANTAGE_BASE_URL,
    API_KEY,
    DEFAULT_TIMEOUT,
    ERROR_MESSAGES
)

async def make_alpha_request(
    client: httpx.AsyncClient,
    function: str,
    symbol: Optional[str] = None,
    additional_params: Optional[Dict[str, Any]] = None,
    expected_datatype: str = "json"
) -> Union[Dict[str, Any], str]:
    """
    Make a request to the Alpha Vantage API with proper error handling.
    
    Args:
        client: An httpx AsyncClient instance
        function: The Alpha Vantage API function to call
        symbol: The stock/crypto symbol (can be None for some endpoints)
        additional_params: Additional parameters to include in the request
        expected_datatype: 'json' or 'csv' to determine parsing
        
    Returns:
        Either a dictionary (for JSON) or string (for CSV, or error message)
    """
    # Validate API key
    if not API_KEY:
        return ERROR_MESSAGES["missing_api_key"]
    
    # Build request parameters
    params = {
        "function": function,
        "apikey": API_KEY
    }
    
    if symbol:
        params["symbol"] = symbol
        
    if additional_params:
        params.update(additional_params)
    
    # If requesting CSV, ensure 'datatype=csv' is in params for Alpha Vantage
    if expected_datatype == "csv" and "datatype" not in params:
        # Many AV CSV endpoints default to CSV if no datatype is specified, 
        # but we'll set it explicitly to be sure
        params["datatype"] = "csv"

    try:
        response = await client.get(
            ALPHA_VANTAGE_BASE_URL,
            params=params,
            timeout=DEFAULT_TIMEOUT
        )
        
        # Check for common API errors in the response
        if "Error Message" in response.text:
            if "Invalid API call" in response.text:
                return f"Invalid API call. Please check the function name and parameters."
            elif "Thank you for using Alpha Vantage" in response.text or "API key" in response.text.lower():
                return ERROR_MESSAGES["invalid_api_key"]
            elif "higher API call frequency" in response.text.lower():
                return ERROR_MESSAGES["rate_limit_exceeded"]
            else:
                return f"Alpha Vantage API error: {response.text}"
        
        # Check for "Note" in response which often indicates rate limit issues
        if expected_datatype == "json":
            json_data = response.json()
            if "Note" in json_data and "API call frequency" in json_data["Note"]:
                return ERROR_MESSAGES["rate_limit_exceeded"]
            return json_data
        else:
            # For CSV responses
            return response.text
            
    except httpx.TimeoutException:
        return ERROR_MESSAGES["timeout"]
    except httpx.ConnectError:
        return ERROR_MESSAGES["connection_error"]
    except httpx.RequestError as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return ERROR_MESSAGES["unknown_error"].format(str(e))

def parse_csv_response(csv_data: str) -> list[Dict[str, str]]:
    """
    Parse a CSV response from Alpha Vantage into a list of dictionaries.
    
    Args:
        csv_data: CSV data as a string
        
    Returns:
        List of dictionaries, each representing a row in the CSV
    """
    if not csv_data or len(csv_data.strip()) == 0:
        return []
        
    try:
        # Parse CSV data
        reader = csv.reader(io.StringIO(csv_data))
        rows = list(reader)
        
        if not rows or len(rows) < 2:  # Need at least header + 1 data row
            return []
            
        headers = rows[0]
        result = []
        
        for row in rows[1:]:
            # Convert each row to a dictionary using the headers as keys
            row_dict = {headers[i]: row[i] for i in range(min(len(headers), len(row)))}
            result.append(row_dict)
            
        return result
    except Exception as e:
        # If parsing fails, return empty list
        return []

async def check_api_health() -> Dict[str, Any]:
    """
    Check the health of the Alpha Vantage API connection.
    
    Returns:
        Dictionary with status information
    """
    async with httpx.AsyncClient() as client:
        try:
            # Make a simple request to check if the API is responding
            result = await make_alpha_request(
                client,
                "TIME_SERIES_INTRADAY",
                symbol="IBM",
                additional_params={"interval": "5min", "outputsize": "compact"}
            )
            
            if isinstance(result, dict) and "Meta Data" in result:
                return {
                    "status": "healthy",
                    "message": "Alpha Vantage API is responding normally"
                }
            else:
                return {
                    "status": "degraded",
                    "message": f"Alpha Vantage API response format unexpected: {result}"
                }
        except Exception as e:
            return {
                "status": "down",
                "message": f"Alpha Vantage API connection failed: {str(e)}"
            }