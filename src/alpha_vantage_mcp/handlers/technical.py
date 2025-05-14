"""
Handlers for technical indicator Alpha Vantage MCP tools.

This module provides handler functions for technical indicators like
SMA, MACD, BBANDS, STOCH, and others.
"""

import httpx
from typing import Dict, Any, List, Optional
import mcp.types as types

from ..api.client import make_alpha_request
from ..formatters.technical import (
    format_technical_indicator, format_bbands, format_macd,
    format_stoch, format_stochf, format_willr, format_adx,
    format_stochrsi, format_adxr, format_apo, format_ppo, format_mom,
    format_bop, format_cci, format_cmo, format_roc, format_rocr, 
    format_aroon, format_aroonosc, format_mfi, format_trix, format_ultosc, format_dx
)
from ..utils.validation import (
    validate_symbol, validate_enum, validate_number, validate_interval
)
from ..utils.error_handling import format_error_response

async def handle_sma(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Simple Moving Average (SMA) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted SMA data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 20)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "SMA",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_technical_indicator(indicator_data, "SMA")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_ema(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Exponential Moving Average (EMA) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted EMA data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 20)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "EMA",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_technical_indicator(indicator_data, "EMA")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_wma(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Weighted Moving Average (WMA) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted WMA data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 20)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "WMA",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_technical_indicator(indicator_data, "WMA")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_dema(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Double Exponential Moving Average (DEMA) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted DEMA data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 20)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "DEMA",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_technical_indicator(indicator_data, "DEMA")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_tema(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Triple Exponential Moving Average (TEMA) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted TEMA data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 20)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "TEMA",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_technical_indicator(indicator_data, "TEMA")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_macd(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Moving Average Convergence/Divergence (MACD) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, series_type, and period parameters
        
    Returns:
        A list containing a single TextContent with the formatted MACD data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    series_type = arguments.get("series_type", "close")
    fastperiod = arguments.get("fastperiod", 12)
    slowperiod = arguments.get("slowperiod", 26)
    signalperiod = arguments.get("signalperiod", 9)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastperiod, min_value=1, param_name="fastperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(slowperiod, min_value=1, param_name="slowperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(signalperiod, min_value=1, param_name="signalperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "MACD",
            symbol.upper(),
            {
                "interval": interval,
                "series_type": series_type,
                "fastperiod": fastperiod,
                "slowperiod": slowperiod,
                "signalperiod": signalperiod
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_macd(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_rsi(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Relative Strength Index (RSI) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted RSI data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "RSI",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_technical_indicator(indicator_data, "RSI")
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_bbands(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Bollinger Bands (BBANDS) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, series_type, and other parameters
        
    Returns:
        A list containing a single TextContent with the formatted BBANDS data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 20)
    series_type = arguments.get("series_type", "close")
    nbdevup = arguments.get("nbdevup", 2)
    nbdevdn = arguments.get("nbdevdn", 2)
    matype = arguments.get("matype", 0)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(nbdevup, min_value=0, param_name="nbdevup")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(nbdevdn, min_value=0, param_name="nbdevdn")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(matype, min_value=0, max_value=8, param_name="matype")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "BBANDS",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type,
                "nbdevup": nbdevup,
                "nbdevdn": nbdevdn,
                "matype": matype
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_bbands(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_stoch(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Stochastic Oscillator (STOCH) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and various period parameters
        
    Returns:
        A list containing a single TextContent with the formatted STOCH data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    fastkperiod = arguments.get("fastkperiod", 5)
    slowkperiod = arguments.get("slowkperiod", 3)
    slowdperiod = arguments.get("slowdperiod", 3)
    slowkmatype = arguments.get("slowkmatype", 0)
    slowdmatype = arguments.get("slowdmatype", 0)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastkperiod, min_value=1, param_name="fastkperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(slowkperiod, min_value=1, param_name="slowkperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(slowdperiod, min_value=1, param_name="slowdperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(slowkmatype, min_value=0, max_value=8, param_name="slowkmatype")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(slowdmatype, min_value=0, max_value=8, param_name="slowdmatype")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "STOCH",
            symbol.upper(),
            {
                "interval": interval,
                "fastkperiod": fastkperiod,
                "slowkperiod": slowkperiod,
                "slowdperiod": slowdperiod,
                "slowkmatype": slowkmatype,
                "slowdmatype": slowdmatype
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_stoch(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_stochf(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Stochastic Fast (STOCHF) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and period parameters
        
    Returns:
        A list containing a single TextContent with the formatted STOCHF data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    fastkperiod = arguments.get("fastkperiod", 5)
    fastdperiod = arguments.get("fastdperiod", 3)
    fastdmatype = arguments.get("fastdmatype", 0)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastkperiod, min_value=1, param_name="fastkperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastdperiod, min_value=1, param_name="fastdperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastdmatype, min_value=0, max_value=8, param_name="fastdmatype")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "STOCHF",
            symbol.upper(),
            {
                "interval": interval,
                "fastkperiod": fastkperiod,
                "fastdperiod": fastdperiod,
                "fastdmatype": fastdmatype
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_stochf(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_willr(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Williams' %R (WILLR) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time_period
        
    Returns:
        A list containing a single TextContent with the formatted WILLR data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "WILLR",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_willr(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_adx(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Average Directional Movement Index (ADX) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time_period
        
    Returns:
        A list containing a single TextContent with the formatted ADX data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "ADX",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_adx(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_stochrsi(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Stochastic Relative Strength Index (STOCHRSI) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, series_type, and period parameters
        
    Returns:
        A list containing a single TextContent with the formatted STOCHRSI data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    series_type = arguments.get("series_type", "close")
    fastkperiod = arguments.get("fastkperiod", 5)
    fastdperiod = arguments.get("fastdperiod", 3)
    fastdmatype = arguments.get("fastdmatype", 0)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastkperiod, min_value=1, param_name="fastkperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastdperiod, min_value=1, param_name="fastdperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastdmatype, min_value=0, max_value=8, param_name="fastdmatype")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "STOCHRSI",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type,
                "fastkperiod": fastkperiod,
                "fastdperiod": fastdperiod,
                "fastdmatype": fastdmatype
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_stochrsi(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_adxr(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Average Directional Movement Index Rating (ADXR) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time_period
        
    Returns:
        A list containing a single TextContent with the formatted ADXR data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "ADXR",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_adxr(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_apo(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Absolute Price Oscillator (APO) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, series_type, and period parameters
        
    Returns:
        A list containing a single TextContent with the formatted APO data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    series_type = arguments.get("series_type", "close")
    fastperiod = arguments.get("fastperiod", 12)
    slowperiod = arguments.get("slowperiod", 26)
    matype = arguments.get("matype", 0)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastperiod, min_value=1, param_name="fastperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(slowperiod, min_value=1, param_name="slowperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(matype, min_value=0, max_value=8, param_name="matype")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "APO",
            symbol.upper(),
            {
                "interval": interval,
                "series_type": series_type,
                "fastperiod": fastperiod,
                "slowperiod": slowperiod,
                "matype": matype
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_apo(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_ppo(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Percentage Price Oscillator (PPO) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, series_type, and period parameters
        
    Returns:
        A list containing a single TextContent with the formatted PPO data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    series_type = arguments.get("series_type", "close")
    fastperiod = arguments.get("fastperiod", 12)
    slowperiod = arguments.get("slowperiod", 26)
    matype = arguments.get("matype", 0)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(fastperiod, min_value=1, param_name="fastperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(slowperiod, min_value=1, param_name="slowperiod")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(matype, min_value=0, max_value=8, param_name="matype")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "PPO",
            symbol.upper(),
            {
                "interval": interval,
                "series_type": series_type,
                "fastperiod": fastperiod,
                "slowperiod": slowperiod,
                "matype": matype
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_ppo(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_mom(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Momentum (MOM) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted MOM data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 10)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "MOM",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_mom(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_bop(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Balance Of Power (BOP) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol and interval
        
    Returns:
        A list containing a single TextContent with the formatted BOP data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "BOP",
            symbol.upper(),
            {
                "interval": interval
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_bop(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_cci(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Commodity Channel Index (CCI) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time_period
        
    Returns:
        A list containing a single TextContent with the formatted CCI data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 20)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "CCI",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_cci(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_cmo(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Chande Momentum Oscillator (CMO) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted CMO data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "CMO",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_cmo(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_roc(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Rate of Change (ROC) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted ROC data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 10)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "ROC",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_roc(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_rocr(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Rate of Change Ratio (ROCR) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted ROCR data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 10)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "ROCR",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_rocr(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_aroon(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Aroon indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time_period
        
    Returns:
        A list containing a single TextContent with the formatted Aroon data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "AROON",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_aroon(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_aroonosc(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Aroon Oscillator (AROONOSC) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time_period
        
    Returns:
        A list containing a single TextContent with the formatted Aroon Oscillator data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "AROONOSC",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_aroonosc(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_mfi(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Money Flow Index (MFI) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time_period
        
    Returns:
        A list containing a single TextContent with the formatted MFI data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "MFI",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_mfi(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_trix(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Triple Exponential Moving Average (TRIX) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, time_period, and series_type
        
    Returns:
        A list containing a single TextContent with the formatted TRIX data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 30)
    series_type = arguments.get("series_type", "close")
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_enum(series_type, ["close", "open", "high", "low"], "series_type")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "TRIX",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_trix(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_ultosc(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Ultimate Oscillator (ULTOSC) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time period parameters
        
    Returns:
        A list containing a single TextContent with the formatted ULTOSC data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    timeperiod1 = arguments.get("timeperiod1", 7)
    timeperiod2 = arguments.get("timeperiod2", 14)
    timeperiod3 = arguments.get("timeperiod3", 28)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(timeperiod1, min_value=1, param_name="timeperiod1")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(timeperiod2, min_value=1, param_name="timeperiod2")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(timeperiod3, min_value=1, param_name="timeperiod3")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "ULTOSC",
            symbol.upper(),
            {
                "interval": interval,
                "timeperiod1": timeperiod1,
                "timeperiod2": timeperiod2,
                "timeperiod3": timeperiod3
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_ultosc(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

async def handle_dx(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Handle Directional Movement Index (DX) indicator tool requests.
    
    Args:
        arguments: The tool arguments containing the symbol, interval, and time_period
        
    Returns:
        A list containing a single TextContent with the formatted DX data
    """
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "daily")
    time_period = arguments.get("time_period", 14)
    
    # Validate input
    is_valid, error_message = validate_symbol(symbol)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_interval(interval)
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    is_valid, error_message = validate_number(time_period, min_value=1, param_name="time_period")
    if not is_valid:
        return [types.TextContent(type="text", text=format_error_response(error_message))]
    
    # Make API request
    async with httpx.AsyncClient() as client:
        indicator_data = await make_alpha_request(
            client,
            "DX",
            symbol.upper(),
            {
                "interval": interval,
                "time_period": time_period
            }
        )
        
        # Check if indicator_data is an error message (string)
        if isinstance(indicator_data, str):
            return [types.TextContent(type="text", text=format_error_response(indicator_data))]
        
        # Format response
        formatted_response = format_dx(indicator_data)
        
        return [types.TextContent(type="text", text=formatted_response)]

# Export all handlers
__all__ = [
    'handle_sma',
    'handle_ema',
    'handle_wma',
    'handle_dema',
    'handle_tema',
    'handle_macd',
    'handle_rsi',
    'handle_bbands',
    'handle_stoch',
    'handle_stochf',
    'handle_willr',
    'handle_adx',
    'handle_stochrsi',
    'handle_adxr',
    'handle_apo',
    'handle_ppo',
    'handle_mom',
    'handle_bop',
    'handle_cci',
    'handle_cmo',
    'handle_roc',
    'handle_rocr',
    'handle_aroon',
    'handle_aroonosc',
    'handle_mfi',
    'handle_trix',
    'handle_ultosc',
    'handle_dx'
]