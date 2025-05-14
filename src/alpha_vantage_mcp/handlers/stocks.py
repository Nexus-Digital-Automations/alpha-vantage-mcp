"""
Handlers for stock-related Alpha Vantage MCP tools.

This module provides handler functions for stock quotes, company information,
time series data, and other stock-related tools.
"""

import httpx
from typing import Dict, Any, List, Optional
import mcp.types as types

from ..api.client import make_alpha_request
from ..formatters.stocks import (
    format_quote, format_company_info, format_time_series,
    format_time_series_weekly, format_time_series_monthly,
    format_time_series_daily_adjusted, format_time_series_weekly_adjusted,
    format_time_series_monthly_adjusted, format_market_status,
    format_listing_status, format_historical_options,
    format_intraday_time_series, format_symbol_search,
    format_etf_profile, format_ipo_calendar,
    format_earnings_calendar, format_earnings_call_transcript,
    format_insider_transactions, format_gainers_losers
)
from ..utils.validation import (
    validate_symbol, validate_date, validate_enum, 
    validate_number, validate_output_size
)
from ..utils.error_handling import format_error_response

async def handle_stock_quote(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle stock quote tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted stock quote
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        quote_data = await make_alpha_request(
            client,
            "GLOBAL_QUOTE",
            symbol.upper()
        )
        
        # Check if quote_data is an error message (string)
        if isinstance(quote_data, str):
            return [types.TextContent(type="text", text=format_error_response(quote_data))]
        
        # Format response
        formatted_response = f"Stock quote for {symbol.upper()}:\n\n{format_quote(quote_data)}"
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_company_info(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle company information tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted company information
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        company_data = await make_alpha_request(
            client,
            "OVERVIEW",
            symbol.upper()
        )
        
        # Check if company_data is an error message (string)
        if isinstance(company_data, str):
            return [types.TextContent(type="text", text=format_error_response(company_data))]
        
        # Format response
        formatted_response = format_company_info(company_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_time_series(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and outputsize
        
    Returns:
        A list containing a single TextContent with the formatted time series data
    """
    symbol = arguments.get("symbol")
    outputsize = arguments.get("outputsize", "compact")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(outputsize, ["compact", "full"], "outputsize")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "TIME_SERIES_DAILY",
            symbol.upper(),
            {"outputsize": outputsize}
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_time_series(time_series_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_time_series_weekly(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle weekly time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted weekly time series data
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "TIME_SERIES_WEEKLY",
            symbol.upper()
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_time_series_weekly(time_series_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_time_series_monthly(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle monthly time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted monthly time series data
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "TIME_SERIES_MONTHLY",
            symbol.upper()
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_time_series_monthly(time_series_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_time_series_daily_adjusted(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle daily adjusted time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and outputsize
        
    Returns:
        A list containing a single TextContent with the formatted daily adjusted time series data
    """
    symbol = arguments.get("symbol")
    outputsize = arguments.get("outputsize", "compact")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(outputsize, ["compact", "full"], "outputsize")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "TIME_SERIES_DAILY_ADJUSTED",
            symbol.upper(),
            {"outputsize": outputsize}
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_time_series_daily_adjusted(time_series_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_time_series_weekly_adjusted(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle weekly adjusted time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted weekly adjusted time series data
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "TIME_SERIES_WEEKLY_ADJUSTED",
            symbol.upper()
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_time_series_weekly_adjusted(time_series_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_time_series_monthly_adjusted(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle monthly adjusted time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted monthly adjusted time series data
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        time_series_data = await make_alpha_request(
            client,
            "TIME_SERIES_MONTHLY_ADJUSTED",
            symbol.upper()
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_time_series_monthly_adjusted(time_series_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_intraday_time_series(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle intraday time series tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, adjusted, extended_hours, and outputsize
        
    Returns:
        A list containing a single TextContent with the formatted intraday time series data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "15min")
    adjusted = arguments.get("adjusted", True)
    extended_hours = arguments.get("extended_hours", True)
    outputsize = arguments.get("outputsize", "compact")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(interval, ["1min", "5min", "15min", "30min", "60min"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(outputsize, ["compact", "full"], "outputsize")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        additional_params = {
            "interval": interval,
            "outputsize": outputsize,
            "adjusted": "true" if adjusted else "false",
            "extended_hours": "true" if extended_hours else "false"
        }
        
        time_series_data = await make_alpha_request(
            client,
            "TIME_SERIES_INTRADAY",
            symbol.upper(),
            additional_params
        )
        
        # Check if time_series_data is an error message (string)
        if isinstance(time_series_data, str):
            return [types.TextContent(type="text", text=format_error_response(time_series_data))]
        
        # Format response
        formatted_response = format_intraday_time_series(time_series_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_market_status(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle market status tool requests.
    
    Args:
        arguments: The tool arguments (empty in this case)
        
    Returns:
        A list containing a single TextContent with the formatted market status information
    """
    # Make API request
    async with httpx.AsyncClient() as client:
        market_data = await make_alpha_request(
            client,
            "MARKET_STATUS",
            None  # No symbol needed
        )
        
        # Check if market_data is an error message (string)
        if isinstance(market_data, str):
            return [types.TextContent(type="text", text=format_error_response(market_data))]
        
        # Format response
        formatted_response = format_market_status(market_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_listing_status(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle listing status tool requests.
    
    Args:
        arguments: The tool arguments containing the date and state
        
    Returns:
        A list containing a single TextContent with the formatted listing status information
    """
    date = arguments.get("date", "")  # Optional date
    state = arguments.get("state", "active")  # Default to 'active'
    
    # Validate input
    if date:
        is_valid, error_message = validate_date(date)
        if not is_valid:
            return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(state, ["active", "delisted"], "state")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        additional_params = {"state": state}
        if date:
            additional_params["date"] = date
            
        # This endpoint returns CSV data
        listing_data = await make_alpha_request(
            client,
            "LISTING_STATUS",
            None,  # No symbol needed
            additional_params,
            expected_datatype="csv"
        )
        
        # Check if listing_data is an error message (string)
        if isinstance(listing_data, str) and "Error" in listing_data:
            return [types.TextContent(type="text", text=format_error_response(listing_data))]
        
        # Format response
        formatted_response = format_listing_status(listing_data, state)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_historical_options(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle historical options tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, date, limit, sort_by, and sort_order
        
    Returns:
        A list containing a single TextContent with the formatted historical options information
    """
    symbol = arguments.get("symbol")
    date = arguments.get("date", "")  # Optional date
    limit = arguments.get("limit", 10)
    sort_by = arguments.get("sort_by", "strike")
    sort_order = arguments.get("sort_order", "asc")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    if date:
        is_valid, error_message = validate_date(date)
        if not is_valid:
            return [types.TextContent(type="text", text=format_error_response(error_message))]
            
    valid_sort_fields = ["strike", "expiration", "volume", "open_interest", "implied_volatility", 
                        "delta", "gamma", "theta", "vega", "rho", "last", "bid", "ask"]
    is_valid, error_message = validate_enum(sort_by, valid_sort_fields, "sort_by")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
        
    is_valid, error_message = validate_enum(sort_order, ["asc", "desc"], "sort_order")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
        
    is_valid, error_message = validate_number(limit, min_value=-1, param_name="limit")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        additional_params = {}
        if date:
            additional_params["date"] = date
            
        options_data = await make_alpha_request(
            client,
            "HISTORICAL_OPTIONS",
            symbol.upper(),
            additional_params
        )
        
        # Check if options_data is an error message (string)
        if isinstance(options_data, str):
            return [types.TextContent(type="text", text=format_error_response(options_data))]
        
        # Format response
        formatted_response = format_historical_options(options_data, limit, sort_by, sort_order)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_symbol_search(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle symbol search tool requests.
    
    Args:
        arguments: The tool arguments containing the keywords
        
    Returns:
        A list containing a single TextContent with the formatted symbol search results
    """
    keywords = arguments.get("keywords")
    
    # Validate input
    if not keywords:
        return [types.TextContent(type="text", text=format_error_response("Missing keywords parameter"))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        search_data = await make_alpha_request(
            client,
            "SYMBOL_SEARCH",
            None,  # No symbol needed
            {"keywords": keywords}
        )
        
        # Check if search_data is an error message (string)
        if isinstance(search_data, str):
            return [types.TextContent(type="text", text=format_error_response(search_data))]
        
        # Format response
        formatted_response = format_symbol_search(search_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_etf_profile(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle ETF profile tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted ETF profile information
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        etf_data = await make_alpha_request(
            client,
            "ETF_PROFILE",
            symbol.upper()
        )
        
        # Check if etf_data is an error message (string)
        if isinstance(etf_data, str):
            return [types.TextContent(type="text", text=format_error_response(etf_data))]
        
        # Format response
        formatted_response = format_etf_profile(etf_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_ipo_calendar(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle IPO calendar tool requests.
    
    Args:
        arguments: The tool arguments (empty in this case)
        
    Returns:
        A list containing a single TextContent with the formatted IPO calendar information
    """
    # Make API request
    async with httpx.AsyncClient() as client:
        # This endpoint returns CSV data
        ipo_data = await make_alpha_request(
            client,
            "IPO_CALENDAR",
            None,  # No symbol needed
            {},
            expected_datatype="csv"
        )
        
        # Check if ipo_data is an error message (string)
        if isinstance(ipo_data, str) and "Error" in ipo_data:
            return [types.TextContent(type="text", text=format_error_response(ipo_data))]
        
        # Format response
        formatted_response = format_ipo_calendar(ipo_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_earnings_calendar(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle earnings calendar tool requests.
    
    Args:
        arguments: The tool arguments containing symbol and horizon
        
    Returns:
        A list containing a single TextContent with the formatted earnings calendar information
    """
    symbol = arguments.get("symbol", "")  # Optional symbol
    horizon = arguments.get("horizon", "3month")  # Default to 3 months
    
    # Validate input
    if symbol:
        is_valid, error_message = validate_symbol(symbol)
        if not is_valid:
            return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(horizon, ["3month", "6month", "12month"], "horizon")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        additional_params = {"horizon": horizon}
        if symbol:
            additional_params["symbol"] = symbol.upper()
            
        # This endpoint returns CSV data
        earnings_data = await make_alpha_request(
            client,
            "EARNINGS_CALENDAR",
            None,  # No symbol needed in main parameter
            additional_params,
            expected_datatype="csv"
        )
        
        # Check if earnings_data is an error message (string)
        if isinstance(earnings_data, str) and "Error" in earnings_data:
            return [types.TextContent(type="text", text=format_error_response(earnings_data))]
        
        # Format response
        formatted_response = format_earnings_calendar(earnings_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_earnings_call_transcript(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle earnings call transcript tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and quarter
        
    Returns:
        A list containing a single TextContent with the formatted earnings call transcript information
    """
    symbol = arguments.get("symbol")
    quarter = arguments.get("quarter")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    if not quarter or not quarter.startswith("20") or not quarter[4] == "Q" or not quarter[5] in "1234":
        return [types.TextContent(type="text", text=format_error_response(
            "Invalid quarter format. Expected YYYYQN format (e.g., 2023Q1)"))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        transcript_data = await make_alpha_request(
            client,
            "EARNINGS_CALL_TRANSCRIPT",
            symbol.upper(),
            {"quarter": quarter}
        )
        
        # Check if transcript_data is an error message (string)
        if isinstance(transcript_data, str):
            return [types.TextContent(type="text", text=format_error_response(transcript_data))]
        
        # Format response
        formatted_response = format_earnings_call_transcript(transcript_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_insider_transactions(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle insider transactions tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted insider transactions information
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        transactions_data = await make_alpha_request(
            client,
            "INSIDER_TRANSACTIONS",
            symbol.upper()
        )
        
        # Check if transactions_data is an error message (string)
        if isinstance(transactions_data, str):
            return [types.TextContent(type="text", text=format_error_response(transactions_data))]
        
        # Format response
        formatted_response = format_insider_transactions(transactions_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_gainers_losers(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle top gainers/losers tool requests.
    
    Args:
        arguments: The tool arguments (empty in this case)
        
    Returns:
        A list containing a single TextContent with the formatted gainers/losers information
    """
    # Make API request
    async with httpx.AsyncClient() as client:
        gainers_losers_data = await make_alpha_request(
            client,
            "TOP_GAINERS_LOSERS",
            None  # No symbol needed
        )
        
        # Check if gainers_losers_data is an error message (string)
        if isinstance(gainers_losers_data, str):
            return [types.TextContent(type="text", text=format_error_response(gainers_losers_data))]
        
        # Format response
        formatted_response = format_gainers_losers(gainers_losers_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

# Export all handlers
__all__ = [
    'handle_stock_quote',
    'handle_company_info',
    'handle_time_series',
    'handle_time_series_weekly',
    'handle_time_series_monthly',
    'handle_time_series_daily_adjusted',
    'handle_time_series_weekly_adjusted',
    'handle_time_series_monthly_adjusted',
    'handle_intraday_time_series',
    'handle_market_status',
    'handle_listing_status',
    'handle_historical_options',
    'handle_symbol_search',
    'handle_etf_profile',
    'handle_ipo_calendar',
    'handle_earnings_calendar',
    'handle_earnings_call_transcript',
    'handle_insider_transactions',
    'handle_gainers_losers'
]