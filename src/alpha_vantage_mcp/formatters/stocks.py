"""
Formatters for stock-related Alpha Vantage API responses.

This module provides functions for formatting stock quotes, company information,
time series data, and other stock-related information.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from ..config.settings import MAX_DISPLAY_ITEMS, MAX_TIME_SERIES_POINTS
from .common import (
    format_number, format_percentage, format_date, 
    format_volume, truncate_list, clean_key, extract_metadata,
    format_error_message
)

def format_quote(quote_data: Dict[str, Any]) -> str:
    """
    Format stock quote data into a readable string.
    
    Args:
        quote_data: The response data from the Alpha Vantage Global Quote endpoint
        
    Returns:
        A formatted string containing the quote information
    """
    try:
        global_quote = quote_data.get("Global Quote", {})
        if not global_quote:
            return "No quote data available for this symbol."

        symbol = global_quote.get('01. symbol', 'N/A')
        price = format_number(global_quote.get('05. price', 'N/A'), is_currency=True)
        change = format_number(global_quote.get('09. change', 'N/A'), is_currency=True)
        percent = global_quote.get('10. change percent', 'N/A')
        volume = format_volume(global_quote.get('06. volume', 'N/A'))
        high = format_number(global_quote.get('03. high', 'N/A'), is_currency=True)
        low = format_number(global_quote.get('04. low', 'N/A'), is_currency=True)
        
        return f"Stock quote for {symbol}:\n\n" \
               f"Price: {price}\n" \
               f"Change: {change} ({percent})\n" \
               f"Volume: {volume}\n" \
               f"High: {high}\n" \
               f"Low: {low}"
    except Exception as e:
        return format_error_message(f"Error formatting quote data: {str(e)}")

def format_company_info(company_data: Dict[str, Any]) -> str:
    """
    Format company information into a readable string.
    
    Args:
        company_data: The response data from the Alpha Vantage Company Overview endpoint
        
    Returns:
        A formatted string containing the company information
    """
    try:
        if not company_data or "Error Message" in company_data:
            return "No company information available for this symbol."
            
        symbol = company_data.get('Symbol', 'N/A')
        name = company_data.get('Name', 'N/A')
        
        # Format market cap nicely (e.g., $2.5T instead of $2,500,000,000,000)
        market_cap = company_data.get('MarketCapitalization', 'N/A')
        if market_cap and market_cap != 'N/A':
            try:
                market_cap_float = float(market_cap)
                if market_cap_float >= 1e12:
                    market_cap = f"${market_cap_float / 1e12:.2f}T"
                elif market_cap_float >= 1e9:
                    market_cap = f"${market_cap_float / 1e9:.2f}B"
                elif market_cap_float >= 1e6:
                    market_cap = f"${market_cap_float / 1e6:.2f}M"
                else:
                    market_cap = f"${market_cap_float:,.2f}"
            except (ValueError, TypeError):
                market_cap = 'N/A'
        
        # Truncate the description if it's too long
        description = company_data.get('Description', 'N/A')
        if len(description) > 300:
            description = description[:297] + "..."
            
        return f"Company information for {symbol}:\n\n" \
               f"Name: {name}\n" \
               f"Sector: {company_data.get('Sector', 'N/A')}\n" \
               f"Industry: {company_data.get('Industry', 'N/A')}\n" \
               f"Market Cap: {market_cap}\n" \
               f"Description: {description}\n" \
               f"Exchange: {company_data.get('Exchange', 'N/A')}\n" \
               f"Currency: {company_data.get('Currency', 'N/A')}"
    except Exception as e:
        return format_error_message(f"Error formatting company data: {str(e)}")

def format_time_series(time_series_data: Dict[str, Any]) -> str:
    """
    Format daily time series data into a readable string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage Time Series Daily endpoint
        
    Returns:
        A formatted string containing the time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        time_series_key = next((k for k in time_series_data.keys() if "Time Series" in k), None)
        
        if not time_series_key or not time_series_data[time_series_key]:
            return "No time series data available for this symbol."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        dates = sorted(series_data.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        output = f"Time Series Data for {symbol} (Last Refreshed: {last_refreshed}):\n\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for date in dates[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[date]
            
            output += f"Date: {date}\n"
            output += f"Open: ${data_point.get('1. open', 'N/A')}\n"
            output += f"High: ${data_point.get('2. high', 'N/A')}\n"
            output += f"Low: ${data_point.get('3. low', 'N/A')}\n"
            output += f"Close: ${data_point.get('4. close', 'N/A')}\n"
            output += f"Volume: {format_volume(data_point.get('5. volume', 'N/A'))}\n"
            
            if date != dates[min(MAX_TIME_SERIES_POINTS - 1, len(dates) - 1)]:
                output += "---\n"
                
        # Add a note if there are more data points
        if len(dates) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(dates)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting time series data: {str(e)}")

def format_time_series_weekly(time_series_data: Dict[str, Any]) -> str:
    """
    Format weekly time series data into a readable string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage Time Series Weekly endpoint
        
    Returns:
        A formatted string containing the weekly time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        time_series_key = next((k for k in time_series_data.keys() if "Weekly Time Series" in k), None)
        
        if not time_series_key or not time_series_data[time_series_key]:
            return "No weekly time series data available for this symbol."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        dates = sorted(series_data.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        timezone = metadata.get("timezone", "Unknown")
        output = f"Weekly Time Series for {symbol}\nLast Refreshed: {last_refreshed} (Timezone: {timezone})\n---\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for date in dates[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[date]
            
            output += f"Date: {date}\n"
            output += f"  Open: ${data_point.get('1. open', 'N/A')}\n"
            output += f"  High: ${data_point.get('2. high', 'N/A')}\n"
            output += f"  Low: ${data_point.get('3. low', 'N/A')}\n"
            output += f"  Close: ${data_point.get('4. close', 'N/A')}\n"
            output += f"  Volume: {format_volume(data_point.get('5. volume', 'N/A'))}\n"
            
            if date != dates[min(MAX_TIME_SERIES_POINTS - 1, len(dates) - 1)]:
                output += "---\n"
                
        # Add a note if there are more data points
        if len(dates) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(dates)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting weekly time series data: {str(e)}")

def format_time_series_monthly(time_series_data: Dict[str, Any]) -> str:
    """
    Format monthly time series data into a readable string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage Time Series Monthly endpoint
        
    Returns:
        A formatted string containing the monthly time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        time_series_key = next((k for k in time_series_data.keys() if "Monthly Time Series" in k), None)
        
        if not time_series_key or not time_series_data[time_series_key]:
            return "No monthly time series data available for this symbol."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        dates = sorted(series_data.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        timezone = metadata.get("timezone", "Unknown")
        output = f"Monthly Time Series for {symbol}\nLast Refreshed: {last_refreshed} (Timezone: {timezone})\n---\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for date in dates[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[date]
            
            output += f"Date: {date}\n"
            output += f"  Open: ${data_point.get('1. open', 'N/A')}\n"
            output += f"  High: ${data_point.get('2. high', 'N/A')}\n"
            output += f"  Low: ${data_point.get('3. low', 'N/A')}\n"
            output += f"  Close: ${data_point.get('4. close', 'N/A')}\n"
            output += f"  Volume: {format_volume(data_point.get('5. volume', 'N/A'))}\n"
            
            if date != dates[min(MAX_TIME_SERIES_POINTS - 1, len(dates) - 1)]:
                output += "---\n"
                
        # Add a note if there are more data points
        if len(dates) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(dates)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting monthly time series data: {str(e)}")

def format_time_series_daily_adjusted(time_series_data: Dict[str, Any]) -> str:
    """
    Format daily adjusted time series data into a readable string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage Time Series Daily Adjusted endpoint
        
    Returns:
        A formatted string containing the daily adjusted time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        time_series_key = next((k for k in time_series_data.keys() if "Time Series" in k), None)
        
        if not time_series_key or not time_series_data[time_series_key]:
            return "No daily adjusted time series data available for this symbol."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        dates = sorted(series_data.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        timezone = metadata.get("timezone", "Unknown")
        output = f"Daily Adjusted Time Series for {symbol}\nLast Refreshed: {last_refreshed} (Timezone: {timezone})\n---\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for date in dates[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[date]
            
            output += f"Date: {date}\n"
            output += f"  Open: ${data_point.get('1. open', 'N/A')}\n"
            output += f"  High: ${data_point.get('2. high', 'N/A')}\n"
            output += f"  Low: ${data_point.get('3. low', 'N/A')}\n"
            output += f"  Close: ${data_point.get('4. close', 'N/A')}\n"
            output += f"  Adjusted Close: ${data_point.get('5. adjusted close', 'N/A')}\n"
            output += f"  Volume: {format_volume(data_point.get('6. volume', 'N/A'))}\n"
            output += f"  Dividend Amount: ${data_point.get('7. dividend amount', 'N/A')}\n"
            output += f"  Split Coefficient: {data_point.get('8. split coefficient', 'N/A')}\n"
            
            if date != dates[min(MAX_TIME_SERIES_POINTS - 1, len(dates) - 1)]:
                output += "---\n"
                
        # Add a note if there are more data points
        if len(dates) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(dates)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting daily adjusted time series data: {str(e)}")

def format_time_series_weekly_adjusted(time_series_data: Dict[str, Any]) -> str:
    """
    Format weekly adjusted time series data into a readable string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage Time Series Weekly Adjusted endpoint
        
    Returns:
        A formatted string containing the weekly adjusted time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        time_series_key = next((k for k in time_series_data.keys() if "Weekly Adjusted Time Series" in k), None)
        
        if not time_series_key or not time_series_data[time_series_key]:
            return "No weekly adjusted time series data available for this symbol."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        dates = sorted(series_data.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        timezone = metadata.get("timezone", "Unknown")
        output = f"Weekly Adjusted Time Series for {symbol}\nLast Refreshed: {last_refreshed} (Timezone: {timezone})\n---\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for date in dates[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[date]
            
            output += f"Date: {date}\n"
            output += f"  Open: ${data_point.get('1. open', 'N/A')}\n"
            output += f"  High: ${data_point.get('2. high', 'N/A')}\n"
            output += f"  Low: ${data_point.get('3. low', 'N/A')}\n"
            output += f"  Close: ${data_point.get('4. close', 'N/A')}\n"
            output += f"  Adjusted Close: ${data_point.get('5. adjusted close', 'N/A')}\n"
            output += f"  Volume: {format_volume(data_point.get('6. volume', 'N/A'))}\n"
            output += f"  Dividend Amount: ${data_point.get('7. dividend amount', 'N/A')}\n"
            
            if date != dates[min(MAX_TIME_SERIES_POINTS - 1, len(dates) - 1)]:
                output += "---\n"
                
        # Add a note if there are more data points
        if len(dates) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(dates)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting weekly adjusted time series data: {str(e)}")

def format_time_series_monthly_adjusted(time_series_data: Dict[str, Any]) -> str:
    """
    Format monthly adjusted time series data into a readable string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage Time Series Monthly Adjusted endpoint
        
    Returns:
        A formatted string containing the monthly adjusted time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        time_series_key = next((k for k in time_series_data.keys() if "Monthly Adjusted Time Series" in k), None)
        
        if not time_series_key or not time_series_data[time_series_key]:
            return "No monthly adjusted time series data available for this symbol."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        dates = sorted(series_data.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        timezone = metadata.get("timezone", "Unknown")
        output = f"Monthly Adjusted Time Series for {symbol}\nLast Refreshed: {last_refreshed} (Timezone: {timezone})\n---\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for date in dates[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[date]
            
            output += f"Date: {date}\n"
            output += f"  Open: ${data_point.get('1. open', 'N/A')}\n"
            output += f"  High: ${data_point.get('2. high', 'N/A')}\n"
            output += f"  Low: ${data_point.get('3. low', 'N/A')}\n"
            output += f"  Close: ${data_point.get('4. close', 'N/A')}\n"
            output += f"  Adjusted Close: ${data_point.get('5. adjusted close', 'N/A')}\n"
            output += f"  Volume: {format_volume(data_point.get('6. volume', 'N/A'))}\n"
            output += f"  Dividend Amount: ${data_point.get('7. dividend amount', 'N/A')}\n"
            
            if date != dates[min(MAX_TIME_SERIES_POINTS - 1, len(dates) - 1)]:
                output += "---\n"
                
        # Add a note if there are more data points
        if len(dates) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(dates)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting monthly adjusted time series data: {str(e)}")

def format_intraday_time_series(time_series_data: Dict[str, Any]) -> str:
    """
    Format intraday time series data into a readable string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage Time Series Intraday endpoint
        
    Returns:
        A formatted string containing the intraday time series information
    """
    try:
        # Extract metadata and find the time series data
        metadata = extract_metadata(time_series_data)
        time_series_key = next((k for k in time_series_data.keys() if "Time Series" in k), None)
        
        if not time_series_key or not time_series_data[time_series_key]:
            return "No intraday time series data available for this symbol."
            
        # Get time series data and sort by date (most recent first)
        series_data = time_series_data[time_series_key]
        timestamps = sorted(series_data.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = time_series_key.split(" ")[-1].strip("()")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        output_size = metadata.get("output_size", "Unknown")
        output = f"Intraday Time Series for {symbol} (Interval: {interval})\n"
        output += f"Last Refreshed: {last_refreshed} {metadata.get('timezone', '')}\n"
        output += f"Output Size: {output_size}\n\n"
        
        # Add data points (limited to MAX_TIME_SERIES_POINTS)
        for timestamp in timestamps[:MAX_TIME_SERIES_POINTS]:
            data_point = series_data[timestamp]
            
            output += f"Time: {timestamp}\n"
            output += f"Open: ${data_point.get('1. open', 'N/A')}\n"
            output += f"High: ${data_point.get('2. high', 'N/A')}\n"
            output += f"Low: ${data_point.get('3. low', 'N/A')}\n"
            output += f"Close: ${data_point.get('4. close', 'N/A')}\n"
            output += f"Volume: {format_volume(data_point.get('5. volume', 'N/A'))}\n"
            output += "---\n"
                
        # Add a note if there are more data points
        if len(timestamps) > MAX_TIME_SERIES_POINTS:
            output += f"\n(Showing {MAX_TIME_SERIES_POINTS} of {len(timestamps)} data points)"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting intraday time series data: {str(e)}")

def format_market_status(api_data: Dict[str, Any]) -> str:
    """
    Format market status information into a readable string.
    
    Args:
        api_data: The response data from the Alpha Vantage Market Status endpoint
        
    Returns:
        A formatted string containing the market status information
    """
    try:
        if not api_data or "markets" not in api_data:
            return "No market status information available."
            
        markets = api_data.get("markets", [])
        if not markets:
            return "No market status information available."
            
        output = "Global Market Status:\n---\n"
        
        for market in markets:
            market_type = market.get("market_type", "Unknown")
            region = market.get("region", "Unknown")
            primary_exchanges = market.get("primary_exchanges", "N/A")
            local_open = market.get("local_open", "N/A")
            local_close = market.get("local_close", "N/A")
            current_status = market.get("current_status", "UNKNOWN")
            notes = market.get("notes", "")
            
            output += f"Market: {market_type} ({region})\n"
            output += f"  Primary Exchanges: {primary_exchanges}\n"
            output += f"  Hours (Local): {local_open} - {local_close}\n"
            output += f"  Status: {current_status}\n"
            
            if notes:
                output += f"  Notes: {notes}\n"
                
            output += "---\n"
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting market status data: {str(e)}")

def format_listing_status(csv_data: str, state: str) -> str:
    """
    Format listing status information into a readable string.
    
    Args:
        csv_data: The CSV response data from the Alpha Vantage Listing Status endpoint
        state: The requested state ('active' or 'delisted')
        
    Returns:
        A formatted string containing the listing status information
    """
    try:
        if not csv_data or len(csv_data.strip()) == 0:
            return f"No {state} listings found."
            
        # Parse CSV data
        import csv
        import io
        
        reader = csv.reader(io.StringIO(csv_data))
        rows = list(reader)
        
        if len(rows) < 2:
            return f"No {state} listings found."
            
        headers = rows[0]
        listings = rows[1:]
        
        # Format the output
        output = f"Listing Status (State: {state.capitalize()}) - Showing up to {MAX_DISPLAY_ITEMS} listings:\n---\n"
        
        # Add headers
        output += " | ".join(headers) + "\n"
        output += "-" * 62 + "\n"
        
        # Add data (limited to MAX_DISPLAY_ITEMS)
        for i, listing in enumerate(listings[:MAX_DISPLAY_ITEMS]):
            output += " | ".join(listing) + "\n"
            
        # Add a note if there are more listings
        if len(listings) > MAX_DISPLAY_ITEMS:
            output += f"\n... and potentially more listings."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting listing status data: {str(e)}")

def format_historical_options(options_data: Dict[str, Any], limit: int = 10, 
                             sort_by: str = "strike", sort_order: str = "asc") -> str:
    """
    Format historical options data into a readable string.
    
    Args:
        options_data: The response data from the Alpha Vantage Historical Options endpoint
        limit: Maximum number of contracts to display
        sort_by: Field to sort contracts by
        sort_order: Sort order ('asc' or 'desc')
        
    Returns:
        A formatted string containing the historical options information
    """
    try:
        if not options_data or "options" not in options_data:
            return "No options data available for this symbol/date."
            
        # Extract data
        options = options_data.get("options", {})
        underlying = options.get("underlying", "Unknown")
        expiration_date = options.get("expiration_date", "Unknown")
        trading_date = options.get("trading_date", "Unknown")
        
        # Get contracts
        calls = options.get("calls", [])
        puts = options.get("puts", [])
        
        # Sort contracts based on parameters
        def sort_key(contract):
            if sort_by == "strike":
                return float(contract.get("strike", 0))
            elif sort_by in ["expiration", "volume", "open_interest", "implied_volatility", 
                            "delta", "gamma", "theta", "vega", "rho", "last", "bid", "ask"]:
                try:
                    return float(contract.get(sort_by, 0))
                except (ValueError, TypeError):
                    return 0
            return 0
            
        sorted_calls = sorted(calls, key=sort_key, reverse=(sort_order == "desc"))
        sorted_puts = sorted(puts, key=sort_key, reverse=(sort_order == "desc"))
        
        # Format the output
        output = f"Historical Options Data for {underlying} ({trading_date}):\n\n"
        
        # Display calls (limited by limit)
        if calls:
            output += "CALL OPTIONS:\n\n"
            
            for i, contract in enumerate(sorted_calls[:limit]):
                output += f"Contract {i+1}:\n"
                output += f"Strike: ${contract.get('strike', 'N/A')}\n"
                output += f"Expiration: {expiration_date}\n"
                output += f"Last: ${contract.get('last', 'N/A')}\n"
                output += f"Bid: ${contract.get('bid', 'N/A')}\n"
                output += f"Ask: ${contract.get('ask', 'N/A')}\n"
                output += f"Volume: {format_volume(contract.get('volume', 'N/A'))}\n"
                output += f"Open Interest: {format_volume(contract.get('open_interest', 'N/A'))}\n"
                output += f"Implied Volatility: {contract.get('implied_volatility', 'N/A')}\n"
                
                if all(k in contract for k in ['delta', 'gamma', 'theta', 'vega', 'rho']):
                    output += "Greeks:\n"
                    output += f"  Delta: {contract.get('delta', 'N/A')}\n"
                    output += f"  Gamma: {contract.get('gamma', 'N/A')}\n"
                    output += f"  Theta: {contract.get('theta', 'N/A')}\n"
                    output += f"  Vega: {contract.get('vega', 'N/A')}\n"
                    output += f"  Rho: {contract.get('rho', 'N/A')}\n"
                    
                if i < min(limit, len(sorted_calls)) - 1:
                    output += "\n"
                    
            # Add a note if there are more calls
            if len(sorted_calls) > limit:
                output += f"\n... and {len(sorted_calls) - limit} more call contracts."
                
        # Display puts (limited by limit)
        if puts:
            if calls:
                output += "\n\n"
                
            output += "PUT OPTIONS:\n\n"
            
            for i, contract in enumerate(sorted_puts[:limit]):
                output += f"Contract {i+1}:\n"
                output += f"Strike: ${contract.get('strike', 'N/A')}\n"
                output += f"Expiration: {expiration_date}\n"
                output += f"Last: ${contract.get('last', 'N/A')}\n"
                output += f"Bid: ${contract.get('bid', 'N/A')}\n"
                output += f"Ask: ${contract.get('ask', 'N/A')}\n"
                output += f"Volume: {format_volume(contract.get('volume', 'N/A'))}\n"
                output += f"Open Interest: {format_volume(contract.get('open_interest', 'N/A'))}\n"
                output += f"Implied Volatility: {contract.get('implied_volatility', 'N/A')}\n"
                
                if all(k in contract for k in ['delta', 'gamma', 'theta', 'vega', 'rho']):
                    output += "Greeks:\n"
                    output += f"  Delta: {contract.get('delta', 'N/A')}\n"
                    output += f"  Gamma: {contract.get('gamma', 'N/A')}\n"
                    output += f"  Theta: {contract.get('theta', 'N/A')}\n"
                    output += f"  Vega: {contract.get('vega', 'N/A')}\n"
                    output += f"  Rho: {contract.get('rho', 'N/A')}\n"
                    
                if i < min(limit, len(sorted_puts)) - 1:
                    output += "\n"
                    
            # Add a note if there are more puts
            if len(sorted_puts) > limit:
                output += f"\n... and {len(sorted_puts) - limit} more put contracts."
                
        return output
    except Exception as e:
        return format_error_message(f"Error formatting historical options data: {str(e)}")

def format_symbol_search(search_data: Dict[str, Any]) -> str:
    """
    Format symbol search results into a readable string.
    
    Args:
        search_data: The response data from the Alpha Vantage Symbol Search endpoint
        
    Returns:
        A formatted string containing the search results
    """
    try:
        if not search_data or "bestMatches" not in search_data:
            return "No search results found."
            
        matches = search_data.get("bestMatches", [])
        
        if not matches:
            return "No search results found."
            
        output = "Symbol Search Results:\n\n"
        
        for i, match in enumerate(matches):
            symbol = match.get("1. symbol", "N/A")
            name = match.get("2. name", "N/A")
            type_value = match.get("3. type", "N/A")
            region = match.get("4. region", "N/A")
            currency = match.get("8. currency", "N/A")
            score = match.get("9. matchScore", "N/A")
            
            output += f"{i+1}. {symbol} - {name}\n"
            output += f"   Type: {type_value}\n"
            output += f"   Region: {region}\n"
            output += f"   Currency: {currency}\n"
            output += f"   Match Score: {score}\n"
            
            if i < len(matches) - 1:
                output += "\n"
                
        return output
    except Exception as e:
        return format_error_message(f"Error formatting symbol search data: {str(e)}")

def format_etf_profile(etf_data: Dict[str, Any]) -> str:
    """
    Format ETF profile data into a readable string.
    
    Args:
        etf_data: The response data from the Alpha Vantage ETF Profile endpoint
        
    Returns:
        A formatted string containing the ETF profile information
    """
    try:
        if not etf_data or "fund" not in etf_data:
            return "No ETF profile data available."
            
        fund = etf_data.get("fund", {})
        symbol = fund.get("symbol", "Unknown")
        name = fund.get("name", "Unknown")
        
        output = f"ETF Profile for {symbol}:\n\n"
        output += f"ETF Profile: {name} ({symbol})\n---\n"
        
        # Fund details
        output += f"Fund Family: {fund.get('family', 'N/A')}\n"
        output += f"Asset Class: {fund.get('asset_class', 'N/A')}\n"
        output += f"Category: {fund.get('category', 'N/A')}\n"
        
        # Format the net assets nicely
        net_assets = fund.get("net_assets", "N/A")
        if net_assets and net_assets != "N/A":
            try:
                assets_value = float(net_assets)
                if assets_value >= 1e9:
                    net_assets = f"${assets_value / 1e9:.1f} billion"
                elif assets_value >= 1e6:
                    net_assets = f"${assets_value / 1e6:.1f} million"
                else:
                    net_assets = f"${assets_value:,.2f}"
            except (ValueError, TypeError):
                pass
                
        output += f"Net Assets: {net_assets}\n"
        
        # Format expense ratio as percentage
        expense_ratio = fund.get("expense_ratio", "N/A")
        if expense_ratio and expense_ratio != "N/A":
            try:
                expense_ratio = f"{float(expense_ratio):.4%}"
            except (ValueError, TypeError):
                pass
                
        output += f"Expense Ratio: {expense_ratio}\n"
        output += f"Inception Date: {fund.get('inception_date', 'N/A')}\n\n"
        
        # Fund description
        description = fund.get("description", "")
        if description:
            output += f"Description: {description}\n\n"
            
        # Top holdings
        holdings = fund.get("holdings", [])
        if holdings:
            output += "Top Holdings:\n"
            
            for i, holding in enumerate(holdings[:10]):
                symbol = holding.get("symbol", "")
                name = holding.get("name", "Unknown")
                weight = holding.get("weight", "N/A")
                
                if weight and weight != "N/A":
                    try:
                        weight = f"{float(weight):.1%}"
                    except (ValueError, TypeError):
                        pass
                        
                output += f"  {i+1}. {name}"
                if symbol:
                    output += f" ({symbol})"
                output += f": {weight}\n"
                
            if len(holdings) > 10:
                output += f"  ... and {len(holdings) - 10} more holdings\n"
                
            output += "\n"
            
        # Sector allocation
        sectors = fund.get("sector_weights", [])
        if sectors:
            output += "Sector Allocation:\n"
            
            for i, sector in enumerate(sectors[:8]):
                name = sector.get("name", "Unknown")
                weight = sector.get("weight", "N/A")
                
                if weight and weight != "N/A":
                    try:
                        weight = f"{float(weight):.1%}"
                    except (ValueError, TypeError):
                        pass
                        
                output += f"  {name}: {weight}\n"
                
            if len(sectors) > 8:
                output += f"  ... and {len(sectors) - 8} more sectors\n"
                
        return output
    except Exception as e:
        return format_error_message(f"Error formatting ETF profile data: {str(e)}")

def format_ipo_calendar(csv_data: str) -> str:
    """
    Format IPO calendar data into a readable string.
    
    Args:
        csv_data: The CSV response data from the Alpha Vantage IPO Calendar endpoint
        
    Returns:
        A formatted string containing the IPO calendar information
    """
    try:
        if not csv_data or len(csv_data.strip()) == 0:
            return "No upcoming IPOs found."
            
        # Parse CSV data
        import csv
        import io
        
        reader = csv.reader(io.StringIO(csv_data))
        rows = list(reader)
        
        if len(rows) < 2:
            return "No upcoming IPOs found."
            
        headers = rows[0]
        ipos = rows[1:]
        
        # Format the output
        output = f"Upcoming IPO Calendar - Showing up to {MAX_DISPLAY_ITEMS} companies:\n---\n"
        
        # Add headers
        output += " | ".join(headers) + "\n"
        output += "-" * 118 + "\n"
        
        # Add data (limited to MAX_DISPLAY_ITEMS)
        for i, ipo in enumerate(ipos[:MAX_DISPLAY_ITEMS]):
            output += " | ".join(ipo) + "\n"
            
        # Add a note if there are more IPOs
        if len(ipos) > MAX_DISPLAY_ITEMS:
            output += f"... and potentially more upcoming IPOs."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting IPO calendar data: {str(e)}")

def format_earnings_calendar(csv_data: str) -> str:
    """
    Format earnings calendar data into a readable string.
    
    Args:
        csv_data: The CSV response data from the Alpha Vantage Earnings Calendar endpoint
        
    Returns:
        A formatted string containing the earnings calendar information
    """
    try:
        if not csv_data or len(csv_data.strip()) == 0:
            return "No upcoming earnings found."
            
        # Parse CSV data
        import csv
        import io
        
        reader = csv.reader(io.StringIO(csv_data))
        rows = list(reader)
        
        if len(rows) < 2:
            return "No upcoming earnings found."
            
        headers = rows[0]
        earnings = rows[1:]
        
        # Format the output
        output = f"Upcoming Earnings Calendar - Showing up to {MAX_DISPLAY_ITEMS} companies:\n---\n"
        
        # Add headers
        output += " | ".join(headers) + "\n"
        output += "-" * 118 + "\n"
        
        # Add data (limited to MAX_DISPLAY_ITEMS)
        for i, earning in enumerate(earnings[:MAX_DISPLAY_ITEMS]):
            output += " | ".join(earning) + "\n"
            
        # Add a note if there are more earnings
        if len(earnings) > MAX_DISPLAY_ITEMS:
            output += f"... and potentially more upcoming earnings."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting earnings calendar data: {str(e)}")

def format_earnings_call_transcript(transcript_data: Dict[str, Any]) -> str:
    """
    Format earnings call transcript data into a readable string.
    
    Args:
        transcript_data: The response data from the Alpha Vantage Earnings Call Transcript endpoint
        
    Returns:
        A formatted string containing the earnings call transcript information
    """
    try:
        if not transcript_data or "transcript" not in transcript_data:
            return "No earnings call transcript available."
            
        transcript = transcript_data.get("transcript", {})
        
        symbol = transcript.get("symbol", "Unknown")
        company_name = transcript.get("company", "Unknown")
        quarter = transcript.get("quarter", "Unknown")
        call_date = transcript.get("call_date", "Unknown")
        
        # Get participants
        participants = transcript.get("participants", [])
        content_items = transcript.get("content", [])
        
        # Format the output
        output = f"Earnings Call Transcript for {company_name} ({symbol})\n"
        output += f"Fiscal Quarter: {quarter}\n"
        output += f"Call Date: {call_date}\n"
        output += "---\n"
        
        # Add participants
        if participants:
            output += "Participants:\n"
            
            for participant in participants:
                name = participant.get("name", "Unknown")
                title = participant.get("title", "")
                
                output += f"  - {name}"
                if title:
                    output += f" ({title})"
                output += "\n"
                
            output += "---\n"
            
        # Add transcript preview (first 500 words)
        if content_items:
            output += "Transcript Preview:\n"
            
            word_count = 0
            preview_text = ""
            
            for item in content_items:
                name = item.get("name", "")
                text = item.get("text", "")
                
                if name and text:
                    preview_text += f"{name}: {text}\n\n"
                    
                    # Count words in the text
                    words = text.split()
                    word_count += len(words)
                    
                    # Limit to ~500 words
                    if word_count >= 500:
                        preview_text += "...\n\n[Transcript continues for more characters]"
                        break
                        
            output += preview_text
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting earnings call transcript data: {str(e)}")

def format_insider_transactions(transactions_data: Dict[str, Any]) -> str:
    """
    Format insider transactions data into a readable string.
    
    Args:
        transactions_data: The response data from the Alpha Vantage Insider Transactions endpoint
        
    Returns:
        A formatted string containing the insider transactions information
    """
    try:
        if not transactions_data or "transactions" not in transactions_data:
            return "No insider transactions available."
            
        symbol = transactions_data.get("symbol", "Unknown")
        transactions = transactions_data.get("transactions", [])
        
        if not transactions:
            return f"No insider transactions found for {symbol}."
            
        # Format the output
        output = f"Insider Transactions for {symbol}\n"
        output += f"Total Transactions: {len(transactions)}\n"
        output += "---\n"
        
        # Add transactions (limited to MAX_DISPLAY_ITEMS)
        for i, transaction in enumerate(transactions[:MAX_DISPLAY_ITEMS]):
            output += f"Transaction #{i+1}:\n"
            
            # Add transaction details
            output += f"  Date: {transaction.get('date', 'Unknown')}\n"
            output += f"  Executive: {transaction.get('insider_name', 'Unknown')}\n"
            output += f"  Title: {transaction.get('insider_title', 'Unknown')}\n"
            
            security_type = transaction.get("security_type", "Unknown")
            output += f"  Security Type: {security_type}\n"
            
            # Format transaction details
            transaction_type = transaction.get("transaction_type", "")
            shares = transaction.get("shares_traded", "0")
            price = transaction.get("share_price", "0")
            
            try:
                shares_float = float(shares)
                shares_formatted = f"{abs(shares_float):,.1f}"
                
                price_float = float(price)
                price_formatted = f"${price_float:.2f}"
                
                if "sale" in transaction_type.lower() or shares_float < 0:
                    output += f"  Transaction: Disposal of {shares_formatted} shares\n"
                else:
                    output += f"  Transaction: Acquisition of {shares_formatted} shares\n"
                    
                output += f"  Share Price: {price_formatted}\n"
            except (ValueError, TypeError):
                output += f"  Transaction: {transaction_type}\n"
                output += f"  Shares: {shares}\n"
                output += f"  Price: {price}\n"
                
            if i < min(MAX_DISPLAY_ITEMS, len(transactions)) - 1:
                output += "---\n"
                
        # Add a note if there are more transactions
        if len(transactions) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(transactions) - MAX_DISPLAY_ITEMS} more transactions."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting insider transactions data: {str(e)}")

def format_gainers_losers(data: Dict[str, Any]) -> str:
    """
    Format top gainers/losers data into a readable string.
    
    Args:
        data: The response data from the Alpha Vantage Top Gainers/Losers endpoint
        
    Returns:
        A formatted string containing the top gainers/losers information
    """
    try:
        if not data:
            return "No top gainers/losers data available."
            
        # Get the lists of stocks
        gainers = data.get("top_gainers", [])
        losers = data.get("top_losers", [])
        most_active = data.get("most_actively_traded", [])
        
        # Format the output
        output = "Market Movers:\n\n"
        
        # Format gainers
        if gainers:
            output += "TOP GAINERS:\n"
            output += "---\n"
            
            for i, gainer in enumerate(gainers[:10]):
                symbol = gainer.get("ticker", "N/A")
                price = gainer.get("price", "N/A")
                change_amount = gainer.get("change_amount", "N/A")
                change_percent = gainer.get("change_percentage", "N/A")
                volume = gainer.get("volume", "N/A")
                
                output += f"{i+1}. {symbol} at ${price} "
                output += f"(+${change_amount}, +{change_percent})\n"
                output += f"   Volume: {format_volume(volume)}\n"
                
            output += "\n"
            
        # Format losers
        if losers:
            output += "TOP LOSERS:\n"
            output += "---\n"
            
            for i, loser in enumerate(losers[:10]):
                symbol = loser.get("ticker", "N/A")
                price = loser.get("price", "N/A")
                change_amount = loser.get("change_amount", "N/A")
                change_percent = loser.get("change_percentage", "N/A")
                volume = loser.get("volume", "N/A")
                
                output += f"{i+1}. {symbol} at ${price} "
                output += f"(${change_amount}, {change_percent})\n"
                output += f"   Volume: {format_volume(volume)}\n"
                
            output += "\n"
            
        # Format most active
        if most_active:
            output += "MOST ACTIVE:\n"
            output += "---\n"
            
            for i, active in enumerate(most_active[:10]):
                symbol = active.get("ticker", "N/A")
                price = active.get("price", "N/A")
                change_amount = active.get("change_amount", "N/A")
                change_percent = active.get("change_percentage", "N/A")
                volume = active.get("volume", "N/A")
                
                output += f"{i+1}. {symbol} at ${price} "
                
                # Format change with proper sign
                if float(change_amount) >= 0:
                    output += f"(+${change_amount}, +{change_percent})\n"
                else:
                    output += f"(${change_amount}, {change_percent})\n"
                    
                output += f"   Volume: {format_volume(volume)}\n"
                
        return output
    except Exception as e:
        return format_error_message(f"Error formatting top gainers/losers data: {str(e)}")

# Export all formatters
__all__ = [
    'format_quote',
    'format_company_info',
    'format_time_series',
    'format_time_series_weekly',
    'format_time_series_monthly',
    'format_time_series_daily_adjusted',
    'format_time_series_weekly_adjusted',
    'format_time_series_monthly_adjusted',
    'format_market_status',
    'format_listing_status',
    'format_historical_options',
    'format_intraday_time_series',
    'format_symbol_search',
    'format_etf_profile',
    'format_ipo_calendar',
    'format_earnings_calendar',
    'format_earnings_call_transcript',
    'format_insider_transactions',
    'format_gainers_losers'
]