"""
Formatters for cryptocurrency-related Alpha Vantage API responses.

This module provides functions for formatting cryptocurrency exchange rates,
time series data, and other crypto-related information.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from ..config.settings import MAX_DISPLAY_ITEMS, MAX_TIME_SERIES_POINTS
from .common import (
    format_number, format_percentage, format_date, 
    format_volume, truncate_list, clean_key, extract_metadata,
    format_error_message
)

def format_crypto_rate(crypto_data: Dict[str, Any]) -> str:
    """
    Format cryptocurrency exchange rate into a readable string.
    
    Args:
        crypto_data: The response data from the Alpha Vantage Crypto Currency Exchange Rate endpoint
        
    Returns:
        A formatted string containing the exchange rate information
    """
    try:
        rate_data = crypto_data.get("Realtime Currency Exchange Rate", {})
        if not rate_data:
            return "No cryptocurrency exchange rate data available."
        
        from_currency_code = rate_data.get("1. From_Currency Code", "N/A")
        from_currency_name = rate_data.get("2. From_Currency Name", "N/A")
        to_currency_code = rate_data.get("3. To_Currency Code", "N/A")
        to_currency_name = rate_data.get("4. To_Currency Name", "N/A")
        exchange_rate = rate_data.get("5. Exchange Rate", "N/A")
        last_refreshed = rate_data.get("6. Last Refreshed", "N/A")
        time_zone = rate_data.get("7. Time Zone", "N/A")
        bid_price = rate_data.get("8. Bid Price", "N/A")
        ask_price = rate_data.get("9. Ask Price", "N/A")
        
        output = f"Cryptocurrency exchange rate for {from_currency_code}/{to_currency_code}:\n\n"
        output += f"From: {from_currency_name} ({from_currency_code})\n"
        output += f"To: {to_currency_name} ({to_currency_code})\n"
        output += f"Exchange Rate: {exchange_rate}\n"
        output += f"Last Updated: {last_refreshed} {time_zone}\n"
        
        if bid_price != "N/A" and ask_price != "N/A":
            output += f"Bid Price: {bid_price}\n"
            output += f"Ask Price: {ask_price}\n"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting crypto exchange rate data: {str(e)}")

def format_crypto_time_series(time_series_data: Dict[str, Any], series_type: str) -> str:
    """
    Format cryptocurrency time series data into a readable string.
    
    Args:
        time_series_data: The response data from Alpha Vantage Crypto Time Series endpoints
        series_type: The type of time series ('daily', 'weekly', or 'monthly')
        
    Returns:
        A formatted string containing the crypto time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        
        # Determine the time series key based on the series type
        key_patterns = {
            'daily': ['Digital Currency Daily', 'Time Series (Digital Currency Daily)'],
            'weekly': ['Digital Currency Weekly', 'Time Series (Digital Currency Weekly)'],
            'monthly': ['Digital Currency Monthly', 'Time Series (Digital Currency Monthly)']
        }
        
        time_series_key = None
        for pattern in key_patterns.get(series_type, []):
            for key in time_series_data.keys():
                if pattern in key:
                    time_series_key = key
                    break
            if time_series_key:
                break
                
        if not time_series_key or not time_series_data[time_series_key]:
            return f"No cryptocurrency {series_type} time series data available."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        dates = sorted(series_data.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        market = metadata.get("market", "USD")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        crypto_name = next((v for k, v in metadata.items() if "name" in k.lower()), symbol)
        market_name = next((v for k, v in metadata.items() if "market name" in k.lower()), market)
        
        output = f"{series_type.capitalize()} Time Series for {crypto_name} ({symbol})\n"
        output += f"Market: {market_name} ({market})\n"
        output += f"Last Refreshed: {last_refreshed} UTC\n\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for date in dates[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[date]
            
            # Find the correct keys for the data (keys may have 'USD' or other market code)
            open_key = next((k for k in data_point.keys() if 'open' in k.lower() and market in k), "N/A")
            high_key = next((k for k in data_point.keys() if 'high' in k.lower() and market in k), "N/A")
            low_key = next((k for k in data_point.keys() if 'low' in k.lower() and market in k), "N/A")
            close_key = next((k for k in data_point.keys() if 'close' in k.lower() and market in k), "N/A")
            volume_key = next((k for k in data_point.keys() if 'volume' in k.lower()), "N/A")
            
            # Get the values
            open_value = data_point.get(open_key, "N/A")
            high_value = data_point.get(high_key, "N/A")
            low_value = data_point.get(low_key, "N/A")
            close_value = data_point.get(close_key, "N/A")
            volume_value = data_point.get(volume_key, "N/A")
            
            output += f"Date: {date}\n"
            output += f"Open: {open_value} {market}\n"
            output += f"High: {high_value} {market}\n"
            output += f"Low: {low_value} {market}\n"
            output += f"Close: {close_value} {market}\n"
            output += f"Volume: {volume_value}\n"
            output += "---\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(dates)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting crypto {series_type} time series data: {str(e)}")

def format_fx_rate(fx_data: Dict[str, Any]) -> str:
    """
    Format foreign exchange rate into a readable string.
    
    Args:
        fx_data: The response data from the Alpha Vantage Foreign Exchange Rate endpoint
        
    Returns:
        A formatted string containing the exchange rate information
    """
    try:
        rate_data = fx_data.get("Realtime Currency Exchange Rate", {})
        if not rate_data:
            return "No foreign exchange rate data available."
        
        from_currency_code = rate_data.get("1. From_Currency Code", "N/A")
        from_currency_name = rate_data.get("2. From_Currency Name", "N/A")
        to_currency_code = rate_data.get("3. To_Currency Code", "N/A")
        to_currency_name = rate_data.get("4. To_Currency Name", "N/A")
        exchange_rate = rate_data.get("5. Exchange Rate", "N/A")
        last_refreshed = rate_data.get("6. Last Refreshed", "N/A")
        time_zone = rate_data.get("7. Time Zone", "N/A")
        bid_price = rate_data.get("8. Bid Price", "N/A")
        ask_price = rate_data.get("9. Ask Price", "N/A")
        
        output = f"Foreign Exchange Rate for {from_currency_code}/{to_currency_code}:\n\n"
        output += f"From: {from_currency_name} ({from_currency_code})\n"
        output += f"To: {to_currency_name} ({to_currency_code})\n"
        output += f"Exchange Rate: {exchange_rate}\n"
        output += f"Last Updated: {last_refreshed} {time_zone}\n"
        
        if bid_price != "N/A" and ask_price != "N/A":
            output += f"Bid Price: {bid_price}\n"
            output += f"Ask Price: {ask_price}\n"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting foreign exchange rate data: {str(e)}")

def format_fx_time_series(time_series_data: Dict[str, Any], series_type: str) -> str:
    """
    Format foreign exchange time series data into a readable string.
    
    Args:
        time_series_data: The response data from Alpha Vantage FX Time Series endpoints
        series_type: The type of time series ('daily', 'weekly', or 'monthly')
        
    Returns:
        A formatted string containing the FX time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        
        # Determine the time series key based on the series type
        key_patterns = {
            'daily': ['FX Daily', 'Time Series FX (Daily)'],
            'weekly': ['FX Weekly', 'Time Series FX (Weekly)'],
            'monthly': ['FX Monthly', 'Time Series FX (Monthly)']
        }
        
        time_series_key = None
        for pattern in key_patterns.get(series_type, []):
            for key in time_series_data.keys():
                if pattern in key:
                    time_series_key = key
                    break
            if time_series_key:
                break
                
        if not time_series_key or not time_series_data[time_series_key]:
            return f"No FX {series_type} time series data available."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        dates = sorted(series_data.keys(), reverse=True)
        
        # Create header
        from_symbol = metadata.get("from_symbol", "Unknown")
        to_symbol = metadata.get("to_symbol", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Foreign Exchange {series_type.capitalize()} Time Series for {from_symbol}/{to_symbol}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for date in dates[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[date]
            
            output += f"Date: {date}\n"
            output += f"Open: {data_point.get('1. open', 'N/A')}\n"
            output += f"High: {data_point.get('2. high', 'N/A')}\n"
            output += f"Low: {data_point.get('3. low', 'N/A')}\n"
            output += f"Close: {data_point.get('4. close', 'N/A')}\n"
            output += "---\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(dates)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting FX {series_type} time series data: {str(e)}")

# Export all formatters
__all__ = [
    'format_crypto_rate',
    'format_crypto_time_series',
    'format_fx_rate',
    'format_fx_time_series'
]