"""
Handlers for economic and fundamental data Alpha Vantage MCP tools.

This module provides handler functions for economic indicators, treasury yields,
fundamental company data, news sentiment, and commodity prices.
"""

import httpx
from typing import Dict, Any, List, Optional
import mcp.types as types

from ..api.client import make_alpha_request
from ..formatters.economic import (
    format_economic_indicator, format_treasury_yield,
    format_fundamental_data, format_news_sentiment,
    format_commodity_data, format_metal_commodity,
    format_agricultural_commodity, format_real_gdp_per_capita, 
    format_federal_funds_rate, format_retail_sales, format_durables,
    format_unemployment, format_nonfarm_payroll
)
from ..utils.validation import (
    validate_symbol, validate_enum, validate_required_params
)
from ..utils.error_handling import format_error_response

async def handle_real_gdp(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Real GDP indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Real GDP data
    """
    interval = arguments.get("interval", "annual")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["annual", "quarterly"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "REAL_GDP",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_economic_indicator(indicator_data, "Real GDP")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_cpi(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Consumer Price Index (CPI) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted CPI data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "semiannual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "CPI",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_economic_indicator(indicator_data, "Consumer Price Index (CPI)")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_inflation(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Inflation indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Inflation data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "INFLATION",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_economic_indicator(indicator_data, "Inflation")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_treasury_yield(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Treasury Yield indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval and maturity
        
    Returns:
        A list containing a single TextContent with the formatted Treasury Yield data
    """
    interval = arguments.get("interval", "monthly")
    maturity = arguments.get("maturity", "10year")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["daily", "weekly", "monthly"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(
        maturity, 
        ["3month", "2year", "5year", "7year", "10year", "30year"], 
        "maturity"
    )
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "TREASURY_YIELD",
            None,  # No symbol needed
            {
                "interval": interval,
                "maturity": maturity
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_treasury_yield(indicator_data, maturity)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_income_statement(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Income Statement fundamental data tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and period
        
    Returns:
        A list containing a single TextContent with the formatted Income Statement data
    """
    symbol = arguments.get("symbol")
    period = arguments.get("period", "annual")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(period, ["annual", "quarterly"], "period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        fundamental_data = await make_alpha_request(
            client,
            "INCOME_STATEMENT",
            symbol.upper()
        )
        
        # Check if fundamental_data is an error message (string)
        if isinstance(fundamental_data, str):
            return [types.TextContent(type="text", text=format_error_response(fundamental_data))]
        
        # Format response
        report_type = "income" if period == "annual" else "income_quarterly"
        formatted_response = format_fundamental_data(fundamental_data, report_type)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_balance_sheet(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Balance Sheet fundamental data tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and period
        
    Returns:
        A list containing a single TextContent with the formatted Balance Sheet data
    """
    symbol = arguments.get("symbol")
    period = arguments.get("period", "annual")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(period, ["annual", "quarterly"], "period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        fundamental_data = await make_alpha_request(
            client,
            "BALANCE_SHEET",
            symbol.upper()
        )
        
        # Check if fundamental_data is an error message (string)
        if isinstance(fundamental_data, str):
            return [types.TextContent(type="text", text=format_error_response(fundamental_data))]
        
        # Format response
        report_type = "balance" if period == "annual" else "balance_quarterly"
        formatted_response = format_fundamental_data(fundamental_data, report_type)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_cash_flow(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Cash Flow fundamental data tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and period
        
    Returns:
        A list containing a single TextContent with the formatted Cash Flow data
    """
    symbol = arguments.get("symbol")
    period = arguments.get("period", "annual")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(period, ["annual", "quarterly"], "period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        fundamental_data = await make_alpha_request(
            client,
            "CASH_FLOW",
            symbol.upper()
        )
        
        # Check if fundamental_data is an error message (string)
        if isinstance(fundamental_data, str):
            return [types.TextContent(type="text", text=format_error_response(fundamental_data))]
        
        # Format response
        report_type = "cash" if period == "annual" else "cash_quarterly"
        formatted_response = format_fundamental_data(fundamental_data, report_type)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_earnings(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Earnings fundamental data tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol
        
    Returns:
        A list containing a single TextContent with the formatted Earnings data
    """
    symbol = arguments.get("symbol")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        fundamental_data = await make_alpha_request(
            client,
            "EARNINGS",
            symbol.upper()
        )
        
        # Check if fundamental_data is an error message (string)
        if isinstance(fundamental_data, str):
            return [types.TextContent(type="text", text=format_error_response(fundamental_data))]
        
        # Format response
        formatted_response = format_fundamental_data(fundamental_data, "earnings_quarterly")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_news_sentiment(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle News Sentiment tool requests.
    
    Args:
        arguments: The tool arguments containing tickers, topics, time filters, etc.
        
    Returns:
        A list containing a single TextContent with the formatted News Sentiment data
    """
    tickers = arguments.get("tickers", "")
    topics = arguments.get("topics", "")
    time_from = arguments.get("time_from", "")
    time_to = arguments.get("time_to", "")
    limit = arguments.get("limit", 10)
    sort = arguments.get("sort", "LATEST")
    
    # At least one of tickers or topics must be provided
    if not tickers and not topics:
        return [types.TextContent(type="text", text=format_error_response(
            "At least one of 'tickers' or 'topics' parameters must be provided"))]
    
    # Validate time format if provided
    if time_from and not (len(time_from) == 12 and time_from[8] == 'T'):
        return [types.TextContent(type="text", text=format_error_response(
            "Invalid time_from format. Expected YYYYMMDDTHHMM format"))]
    
    if time_to and not (len(time_to) == 12 and time_to[8] == 'T'):
        return [types.TextContent(type="text", text=format_error_response(
            "Invalid time_to format. Expected YYYYMMDDTHHMM format"))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        additional_params = {}
        
        if tickers:
            additional_params["tickers"] = tickers
        if topics:
            additional_params["topics"] = topics
        if time_from:
            additional_params["time_from"] = time_from
        if time_to:
            additional_params["time_to"] = time_to
        if limit:
            additional_params["limit"] = limit
        if sort:
            additional_params["sort"] = sort
            
        news_data = await make_alpha_request(
            client,
            "NEWS_SENTIMENT",
            None,  # No symbol needed
            additional_params
        )
        
        # Check if news_data is an error message (string)
        if isinstance(news_data, str):
            return [types.TextContent(type="text", text=format_error_response(news_data))]
        
        # Format response
        formatted_response = format_news_sentiment(news_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_wti(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle WTI Crude Oil price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted WTI price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["daily", "weekly", "monthly"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "WTI",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_commodity_data(commodity_data, "WTI")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_brent(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Brent Crude Oil price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Brent price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["daily", "weekly", "monthly"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "BRENT",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_commodity_data(commodity_data, "BRENT")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_natural_gas(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Natural Gas price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Natural Gas price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["daily", "weekly", "monthly"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "NATURAL_GAS",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_commodity_data(commodity_data, "NATURAL_GAS")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_copper(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Copper price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Copper price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "quarterly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "COPPER",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_metal_commodity(commodity_data, "COPPER")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_real_gdp_per_capita(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Real GDP Per Capita indicator tool requests.
    
    Args:
        arguments: The tool arguments (no parameters required)
        
    Returns:
        A list containing a single TextContent with the formatted Real GDP Per Capita data
    """
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "REAL_GDP_PER_CAPITA",
            None,  # No symbol needed
            {}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_real_gdp_per_capita(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_federal_funds_rate(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Federal Funds Rate indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Federal Funds Rate data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["daily", "weekly", "monthly"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "FEDERAL_FUNDS_RATE",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_federal_funds_rate(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_aluminum(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Aluminum price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Aluminum price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "quarterly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "ALUMINUM",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_metal_commodity(commodity_data, "ALUMINUM")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_wheat(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Wheat price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Wheat price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "quarterly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "WHEAT",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_agricultural_commodity(commodity_data, "WHEAT")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_corn(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Corn price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Corn price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "quarterly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "CORN",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_agricultural_commodity(commodity_data, "CORN")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_retail_sales(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Retail Sales indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Retail Sales data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "RETAIL_SALES",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_retail_sales(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_durables(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Durable Goods Orders indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Durable Goods Orders data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "DURABLES",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_durables(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_unemployment(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Unemployment Rate indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Unemployment Rate data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "UNEMPLOYMENT",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_unemployment(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_nonfarm_payroll(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Nonfarm Payroll indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Nonfarm Payroll data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "NONFARM_PAYROLL",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_nonfarm_payroll(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_cotton(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Cotton price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Cotton price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "quarterly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "COTTON",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_agricultural_commodity(commodity_data, "COTTON")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_sugar(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Sugar price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Sugar price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "quarterly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "SUGAR",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_agricultural_commodity(commodity_data, "SUGAR")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_coffee(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Coffee price tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted Coffee price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "quarterly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "COFFEE",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response
        formatted_response = format_agricultural_commodity(commodity_data, "COFFEE")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_all_commodities(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle All Commodities (Global Price Index) tool requests.
    
    Args:
        arguments: The tool arguments containing the interval
        
    Returns:
        A list containing a single TextContent with the formatted All Commodities price data
    """
    interval = arguments.get("interval", "monthly")
    
    # Validate input
    is_valid, error_message = validate_enum(interval, ["monthly", "quarterly", "annual"], "interval")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        commodity_data = await make_alpha_request(
            client,
            "ALL_COMMODITIES",
            None,  # No symbol needed
            {"interval": interval}
        )
        
        # Check if commodity_data is an error message (string)
        if isinstance(commodity_data, str):
            return [types.TextContent(type="text", text=format_error_response(commodity_data))]
        
        # Format response using commodity_data formatter since it's a general price index
        formatted_response = format_commodity_data(commodity_data, "ALL_COMMODITIES")
        
        return [types.TextContent(type="text", text=formatted_response)]

# Export all handlers
__all__ = [
    'handle_real_gdp',
    'handle_cpi',
    'handle_inflation',
    'handle_treasury_yield',
    'handle_income_statement',
    'handle_balance_sheet',
    'handle_cash_flow',
    'handle_earnings',
    'handle_news_sentiment',
    'handle_wti',
    'handle_brent',
    'handle_natural_gas',
    'handle_copper',
    'handle_wheat',
    'handle_corn',
    'handle_real_gdp_per_capita',
    'handle_federal_funds_rate',
    'handle_aluminum',
    'handle_retail_sales',
    'handle_durables',
    'handle_unemployment',
    'handle_nonfarm_payroll',
    'handle_cotton',
    'handle_sugar',
    'handle_coffee',
    'handle_all_commodities'
]