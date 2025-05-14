"""
Handlers for cryptocurrency-related Alpha Vantage MCP tools.

This module provides handler functions for cryptocurrency exchange rates,
time series data, and other crypto-related tools.
"""

import httpx
from typing import Dict, Any, List, Optional
import mcp.types as types

from ..api.client import make_alpha_request
from ..formatters.crypto import (
    format_crypto_rate, format_crypto_time_series,
    format_fx_rate, format_fx_time_series
)
from ..utils.validation import (
    validate_symbol, validate_enum, validate_required_params
)
from ..utils.error_handling import format_error_response

async def handle_crypto_exchange_rate(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle cryptocurrency exchange rate tool requests.
    
    Args:
        arguments: The tool arguments containing the crypto_symbol and market
        
    Returns:
        A list containing a single TextContent with the formatted cryptocurrency exchange rate
    """
    crypto_symbol = arguments.get("crypto_symbol")
    market = arguments.get("market", "USD")
    
    # Validate input
    if not crypto_symbol:
        return [types.TextContent(type="text", text=format_error_response("Missing crypto_symbol parameter"))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        crypto_data = await make_alpha_request(
            client,
            "CURRENCY_EXCHANGE_RATE",
            None,  # No symbol parameter
            {
                "from_currency": crypto_symbol.upper(),
                "to_currency": market.upper()
            }
        )
        
        # Check if crypto_data is an error message (string)
        if isinstance(crypto_data, str):
            return [types.TextContent(type="text", text=format_error_response(crypto_data))]
        
        # Format response
        formatted_response = format_crypto_rate(crypto_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_crypto_daily(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle daily cryptocurrency time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and market
        
    Returns:
        A list containing a single TextContent with the formatted daily crypto time series data
    """
    symbol = arguments.get("symbol")
    market = arguments.get("market", "USD")
    
    # Validate input
    if not symbol:
        return [types.TextContent(type="text", text=format_error_response("Missing symbol parameter"))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "DIGITAL_CURRENCY_DAILY",
            symbol.upper(),
            {"market": market.upper()}
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_crypto_time_series(time_series_data, 'daily')
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_crypto_weekly(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle weekly cryptocurrency time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and market
        
    Returns:
        A list containing a single TextContent with the formatted weekly crypto time series data
    """
    symbol = arguments.get("symbol")
    market = arguments.get("market", "USD")
    
    # Validate input
    if not symbol:
        return [types.TextContent(type="text", text=format_error_response("Missing symbol parameter"))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "DIGITAL_CURRENCY_WEEKLY",
            symbol.upper(),
            {"market": market.upper()}
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_crypto_time_series(time_series_data, 'weekly')
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_crypto_monthly(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle monthly cryptocurrency time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and market
        
    Returns:
        A list containing a single TextContent with the formatted monthly crypto time series data
    """
    symbol = arguments.get("symbol")
    market = arguments.get("market", "USD")
    
    # Validate input
    if not symbol:
        return [types.TextContent(type="text", text=format_error_response("Missing symbol parameter"))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "DIGITAL_CURRENCY_MONTHLY",
            symbol.upper(),
            {"market": market.upper()}
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_crypto_time_series(time_series_data, 'monthly')
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_fx_rate(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle foreign exchange rate tool requests.
    
    Args:
        arguments: The tool arguments containing the from_currency and to_currency
        
    Returns:
        A list containing a single TextContent with the formatted foreign exchange rate
    """
    from_currency = arguments.get("from_currency")
    to_currency = arguments.get("to_currency")
    
    # Validate input
    is_valid, error_message = validate_required_params(arguments, ["from_currency", "to_currency"])
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        fx_data = await make_alpha_request(
            client,
            "CURRENCY_EXCHANGE_RATE",
            None,  # No symbol parameter
            {
                "from_currency": from_currency.upper(),
                "to_currency": to_currency.upper()
            }
        )
        
        # Check if fx_data is an error message (string)
        if isinstance(fx_data, str):
            return [types.TextContent(type="text", text=format_error_response(fx_data))]
        
        # Format response
        formatted_response = format_fx_rate(fx_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_fx_daily(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle daily foreign exchange time series tool requests.
    
    Args:
        arguments: The tool arguments containing the from_symbol and to_symbol
        
    Returns:
        A list containing a single TextContent with the formatted daily FX time series data
    """
    from_symbol = arguments.get("from_symbol")
    to_symbol = arguments.get("to_symbol")
    
    # Validate input
    is_valid, error_message = validate_required_params(arguments, ["from_symbol", "to_symbol"])
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "FX_DAILY",
            None,  # No symbol parameter
            {
                "from_symbol": from_symbol.upper(),
                "to_symbol": to_symbol.upper()
            }
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_fx_time_series(time_series_data, 'daily')
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_fx_weekly(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle weekly foreign exchange time series tool requests.
    
    Args:
        arguments: The tool arguments containing the from_symbol and to_symbol
        
    Returns:
        A list containing a single TextContent with the formatted weekly FX time series data
    """
    from_symbol = arguments.get("from_symbol")
    to_symbol = arguments.get("to_symbol")
    
    # Validate input
    is_valid, error_message = validate_required_params(arguments, ["from_symbol", "to_symbol"])
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "FX_WEEKLY",
            None,  # No symbol parameter
            {
                "from_symbol": from_symbol.upper(),
                "to_symbol": to_symbol.upper()
            }
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_fx_time_series(time_series_data, 'weekly')
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_fx_monthly(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle monthly foreign exchange time series tool requests.
    
    Args:
        arguments: The tool arguments containing the from_symbol and to_symbol
        
    Returns:
        A list containing a single TextContent with the formatted monthly FX time series data
    """
    from_symbol = arguments.get("from_symbol")
    to_symbol = arguments.get("to_symbol")
    
    # Validate input
    is_valid, error_message = validate_required_params(arguments, ["from_symbol", "to_symbol"])
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "FX_MONTHLY",
            None,  # No symbol parameter
            {
                "from_symbol": from_symbol.upper(),
                "to_symbol": to_symbol.upper()
            }
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_fx_time_series(time_series_data, 'monthly')
        
        return [types.TextContent(type="text", text=formatted_response)]

# Export all handlers
__all__ = [
    'handle_crypto_exchange_rate',
    'handle_crypto_daily',
    'handle_crypto_weekly',
    'handle_crypto_monthly',
    'handle_fx_rate',
    'handle_fx_daily',
    'handle_fx_weekly',
    'handle_fx_monthly'
]