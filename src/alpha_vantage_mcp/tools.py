"""
Alpha Vantage MCP Tools Module

This module contains utility functions for making requests to the Alpha Vantage API
and formatting the responses.
"""

from typing import Any, Dict, Optional
import httpx
import os
import csv
import io
import re

ALPHA_VANTAGE_BASE = "https://www.alphavantage.co/query"
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

async def make_alpha_request(client: httpx.AsyncClient, function: str, symbol: Optional[str], 
                            additional_params: Optional[Dict[str, Any]] = None, 
                            expected_datatype: str = "json") -> Dict[str, Any] | str:
    """Make a request to the Alpha Vantage API with proper error handling.
    
    Args:
        client: An httpx AsyncClient instance
        function: The Alpha Vantage API function to call
        symbol: The stock/crypto symbol (can be None for some endpoints)
        additional_params: Additional parameters to include in the request
        expected_datatype: 'json' or 'csv' to determine parsing
        
    Returns:
        Either a dictionary (for JSON) or string (for CSV, or error message)
    """
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
            ALPHA_VANTAGE_BASE,
            params=params,
            timeout=30.0
        )

        # Check for specific error responses
        if response.status_code == 429:
            return f"Rate limit exceeded. Error details: {response.text}"
        elif response.status_code == 403:
            return f"API key invalid or expired. Error details: {response.text}"

        response.raise_for_status()

        if expected_datatype == "csv":
            # Check if response is indeed CSV, otherwise it might be an error JSON
            if 'text/csv' in response.headers.get('Content-Type', '').lower():
                return response.text  # Return raw CSV text
            else:  # It might be an error message in JSON format
                try:
                    data = response.json()
                    if "Error Message" in data: 
                        return f"Alpha Vantage API error: {data['Error Message']}"
                    if "Information" in data: 
                        return f"Alpha Vantage API information: {data['Information']}"
                    if "Note" in data: 
                        return f"Alpha Vantage API Note: {data['Note']}"
                except ValueError:  # Not JSON
                    pass  # Fall through to generic error
                
                return f"Expected CSV response, but received: {response.headers.get('Content-Type', 'Unknown')}. Content: {response.text[:200]}..."

        # Default JSON processing
        data = response.json()

        # Check for Alpha Vantage specific error messages
        if "Error Message" in data:
            return f"Alpha Vantage API error: {data['Error Message']}"
        if "Information" in data:
            return f"Alpha Vantage API information: {data['Information']}"
        if "Note" in data and "API call frequency" in data["Note"]:
            return f"Rate limit warning: {data['Note']}"

        return data
    except httpx.TimeoutException:
        return "Request timed out after 30 seconds. The Alpha Vantage API may be experiencing delays."
    except httpx.ConnectError:
        return "Failed to connect to Alpha Vantage API. Please check your internet connection."
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {str(e)} - Response: {e.response.text}"
    except Exception as e:
        return f"Unexpected error occurred: {str(e)}"


def format_quote(quote_data: Dict[str, Any]) -> str:
    """Format quote data into a concise string.
    
    Args:
        quote_data: The response data from the Alpha Vantage Global Quote endpoint
        
    Returns:
        A formatted string containing the quote information
    """
    try:
        global_quote = quote_data.get("Global Quote", {})
        if not global_quote:
            return "No quote data available in the response"

        return (
            f"Price: ${global_quote.get('05. price', 'N/A')}\n"
            f"Change: ${global_quote.get('09. change', 'N/A')} "
            f"({global_quote.get('10. change percent', 'N/A')})\n"
            f"Volume: {global_quote.get('06. volume', 'N/A')}\n"
            f"High: ${global_quote.get('03. high', 'N/A')}\n"
            f"Low: ${global_quote.get('04. low', 'N/A')}\n"
            "---"
        )
    except Exception as e:
        return f"Error formatting quote data: {str(e)}"


def format_company_info(overview_data: Dict[str, Any]) -> str:
    """Format company information into a concise string.
    
    Args:
        overview_data: The response data from the Alpha Vantage OVERVIEW endpoint
        
    Returns:
        A formatted string containing the company information
    """
    try:
        if not overview_data:
            return "No company information available in the response"

        return (
            f"Name: {overview_data.get('Name', 'N/A')}\n"
            f"Sector: {overview_data.get('Sector', 'N/A')}\n"
            f"Industry: {overview_data.get('Industry', 'N/A')}\n"
            f"Market Cap: ${overview_data.get('MarketCapitalization', 'N/A')}\n"
            f"Description: {overview_data.get('Description', 'N/A')}\n"
            f"Exchange: {overview_data.get('Exchange', 'N/A')}\n"
            f"Currency: {overview_data.get('Currency', 'N/A')}\n"
            "---"
        )
    except Exception as e:
        return f"Error formatting company data: {str(e)}"


def format_crypto_rate(crypto_data: Dict[str, Any]) -> str:
    """Format cryptocurrency exchange rate data into a concise string.
    
    Args:
        crypto_data: The response data from the Alpha Vantage CURRENCY_EXCHANGE_RATE endpoint
        
    Returns:
        A formatted string containing the cryptocurrency exchange rate information
    """
    try:
        realtime_data = crypto_data.get("Realtime Currency Exchange Rate", {})
        if not realtime_data:
            return "No exchange rate data available in the response"

        return (
            f"From: {realtime_data.get('2. From_Currency Name', 'N/A')} ({realtime_data.get('1. From_Currency Code', 'N/A')})\n"
            f"To: {realtime_data.get('4. To_Currency Name', 'N/A')} ({realtime_data.get('3. To_Currency Code', 'N/A')})\n"
            f"Exchange Rate: {realtime_data.get('5. Exchange Rate', 'N/A')}\n"
            f"Last Updated: {realtime_data.get('6. Last Refreshed', 'N/A')} {realtime_data.get('7. Time Zone', 'N/A')}\n"
            f"Bid Price: {realtime_data.get('8. Bid Price', 'N/A')}\n"
            f"Ask Price: {realtime_data.get('9. Ask Price', 'N/A')}\n"
            "---"
        )
    except Exception as e:
        return f"Error formatting cryptocurrency data: {str(e)}"


def format_time_series(time_series_data: Dict[str, Any]) -> str:
    """Format time series data into a concise string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage TIME_SERIES_DAILY endpoint
        
    Returns:
        A formatted string containing the time series information
    """
    try:
        # Get the daily time series data
        time_series = time_series_data.get("Time Series (Daily)", {})
        if not time_series:
            return "No time series data available in the response"

        # Get metadata
        metadata = time_series_data.get("Meta Data", {})
        symbol = metadata.get("2. Symbol", "Unknown")
        last_refreshed = metadata.get("3. Last Refreshed", "Unknown")

        # Format the most recent 5 days of data
        formatted_data = [
            f"Time Series Data for {symbol} (Last Refreshed: {last_refreshed})\n\n"
        ]

        for date, values in list(time_series.items())[:5]:
            formatted_data.append(
                f"Date: {date}\n"
                f"Open: ${values.get('1. open', 'N/A')}\n"
                f"High: ${values.get('2. high', 'N/A')}\n"
                f"Low: ${values.get('3. low', 'N/A')}\n"
                f"Close: ${values.get('4. close', 'N/A')}\n"
                f"Volume: {values.get('5. volume', 'N/A')}\n"
                "---\n"
            )

        return "\n".join(formatted_data)
    except Exception as e:
        return f"Error formatting time series data: {str(e)}"


def format_time_series_weekly(time_series_data: Dict[str, Any]) -> str:
    """Format weekly time series data into a concise string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage TIME_SERIES_WEEKLY endpoint
        
    Returns:
        A formatted string containing the weekly time series information
    """
    try:
        # The main data key in the JSON response for weekly data is "Weekly Time Series"
        time_series = time_series_data.get("Weekly Time Series", {})
        if not time_series:
            if "Error Message" in time_series_data:
                return f"Alpha Vantage API error: {time_series_data['Error Message']}"
            if "Information" in time_series_data: # API may return info for invalid symbols on free tier or rate limits
                return f"Alpha Vantage API information: {time_series_data['Information']}"
            return "No weekly time series data available in the response."

        metadata = time_series_data.get("Meta Data", {})
        symbol = metadata.get("2. Symbol", "Unknown Symbol")
        last_refreshed = metadata.get("3. Last Refreshed", "Unknown Date")
        time_zone = metadata.get("4. Time Zone", "N/A")

        formatted_output = [
            f"Weekly Time Series for {symbol}",
            f"Last Refreshed: {last_refreshed} (Timezone: {time_zone})",
            "---"
        ]

        # Display the latest 5 data points (weeks)
        count = 0
        for date, values in time_series.items():
            if count >= 5:
                break
            formatted_output.append(
                f"Date: {date}\n"
                f"  Open: ${values.get('1. open', 'N/A')}\n"
                f"  High: ${values.get('2. high', 'N/A')}\n"
                f"  Low: ${values.get('3. low', 'N/A')}\n"
                f"  Close: ${values.get('4. close', 'N/A')}\n"
                f"  Volume: {values.get('5. volume', 'N/A')}\n"
                "---"
            )
            count += 1
        
        if len(time_series) > 5:
            formatted_output.append(f"\n(Showing 5 of {len(time_series)} data points)")

        return "\n".join(formatted_output)
    except Exception as e:
        return f"Error formatting weekly time series data: {str(e)}"


def format_time_series_daily_adjusted(time_series_data: Dict[str, Any]) -> str:
    """Format daily adjusted time series data into a concise string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage 
                          TIME_SERIES_DAILY_ADJUSTED endpoint.
        
    Returns:
        A formatted string containing the daily adjusted time series information.
    """
    try:
        # The main data key in the JSON response is "Time Series (Daily)"
        # This is similar to TIME_SERIES_DAILY but includes adjusted fields.
        time_series = time_series_data.get("Time Series (Daily)", {})
        if not time_series:
            if "Error Message" in time_series_data:
                return f"Alpha Vantage API error: {time_series_data['Error Message']}"
            if "Information" in time_series_data: # Premium endpoints might return this on free tier
                return f"Alpha Vantage API information: {time_series_data['Information']}"
            if "Note" in time_series_data: # Rate limit notes
                 return f"Alpha Vantage API Note: {time_series_data['Note']}"
            return "No daily adjusted time series data available in the response."

        metadata = time_series_data.get("Meta Data", {})
        symbol = metadata.get("2. Symbol", "Unknown Symbol")
        last_refreshed = metadata.get("3. Last Refreshed", "Unknown Date")
        time_zone = metadata.get("4. Time Zone", "N/A")

        formatted_output = [
            f"Daily Adjusted Time Series for {symbol}",
            f"Last Refreshed: {last_refreshed} (Timezone: {time_zone})",
            "---"
        ]

        # Display the latest 5 data points (days)
        count = 0
        for date, values in time_series.items():
            if count >= 5:
                break
            formatted_output.append(
                f"Date: {date}\n"
                f"  Open: ${values.get('1. open', 'N/A')}\n"
                f"  High: ${values.get('2. high', 'N/A')}\n"
                f"  Low: ${values.get('3. low', 'N/A')}\n"
                f"  Close: ${values.get('4. close', 'N/A')}\n"
                f"  Adjusted Close: ${values.get('5. adjusted close', 'N/A')}\n"
                f"  Volume: {values.get('6. volume', 'N/A')}\n"
                f"  Dividend Amount: ${values.get('7. dividend amount', 'N/A')}\n"
                f"  Split Coefficient: {values.get('8. split coefficient', 'N/A')}\n"
                "---"
            )
            count += 1
        
        if len(time_series) > 5:
            formatted_output.append(f"\n(Showing 5 of {len(time_series)} data points)")

        return "\n".join(formatted_output)
    except Exception as e:
        return f"Error formatting daily adjusted time series data: {str(e)}"


def format_time_series_weekly_adjusted(time_series_data: Dict[str, Any]) -> str:
    """Format weekly adjusted time series data into a concise string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage 
                          TIME_SERIES_WEEKLY_ADJUSTED endpoint.
        
    Returns:
        A formatted string containing the weekly adjusted time series information.
    """
    try:
        # The main data key in the JSON response is "Weekly Adjusted Time Series"
        time_series = time_series_data.get("Weekly Adjusted Time Series", {})
        if not time_series:
            if "Error Message" in time_series_data:
                return f"Alpha Vantage API error: {time_series_data['Error Message']}"
            if "Information" in time_series_data: # Premium endpoints might return this on free tier
                return f"Alpha Vantage API information: {time_series_data['Information']}"
            if "Note" in time_series_data: # Rate limit notes
                 return f"Alpha Vantage API Note: {time_series_data['Note']}"
            return "No weekly adjusted time series data available in the response."

        metadata = time_series_data.get("Meta Data", {})
        symbol = metadata.get("2. Symbol", "Unknown Symbol")
        last_refreshed = metadata.get("3. Last Refreshed", "Unknown Date")
        time_zone = metadata.get("4. Time Zone", "N/A")

        formatted_output = [
            f"Weekly Adjusted Time Series for {symbol}",
            f"Last Refreshed: {last_refreshed} (Timezone: {time_zone})",
            "---"
        ]

        # Display the latest 5 data points (weeks)
        count = 0
        for date, values in time_series.items():
            if count >= 5:
                break
            formatted_output.append(
                f"Date: {date}\n"
                f"  Open: ${values.get('1. open', 'N/A')}\n"
                f"  High: ${values.get('2. high', 'N/A')}\n"
                f"  Low: ${values.get('3. low', 'N/A')}\n"
                f"  Close: ${values.get('4. close', 'N/A')}\n"
                f"  Adjusted Close: ${values.get('5. adjusted close', 'N/A')}\n"
                f"  Volume: {values.get('6. volume', 'N/A')}\n"
                f"  Dividend Amount: ${values.get('7. dividend amount', 'N/A')}\n"
                "---"
            )
            count += 1
        
        if len(time_series) > 5:
            formatted_output.append(f"\n(Showing 5 of {len(time_series)} data points)")

        return "\n".join(formatted_output)
    except Exception as e:
        return f"Error formatting weekly adjusted time series data: {str(e)}"


def format_time_series_monthly(time_series_data: Dict[str, Any]) -> str:
    """Format monthly time series data into a concise string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage TIME_SERIES_MONTHLY endpoint
        
    Returns:
        A formatted string containing the monthly time series information
    """
    try:
        # The main data key in the JSON response for monthly data is "Monthly Time Series"
        time_series = time_series_data.get("Monthly Time Series", {})
        if not time_series:
            if "Error Message" in time_series_data:
                return f"Alpha Vantage API error: {time_series_data['Error Message']}"
            if "Information" in time_series_data: # API may return info for invalid symbols on free tier or rate limits
                return f"Alpha Vantage API information: {time_series_data['Information']}"
            if "Note" in time_series_data: # Rate limit notes
                return f"Alpha Vantage API Note: {time_series_data['Note']}"
            return "No monthly time series data available in the response."

        metadata = time_series_data.get("Meta Data", {})
        symbol = metadata.get("2. Symbol", "Unknown Symbol")
        last_refreshed = metadata.get("3. Last Refreshed", "Unknown Date")
        time_zone = metadata.get("4. Time Zone", "N/A")

        formatted_output = [
            f"Monthly Time Series for {symbol}",
            f"Last Refreshed: {last_refreshed} (Timezone: {time_zone})",
            "---"
        ]

        # Display the latest 5 data points (months)
        count = 0
        for date, values in time_series.items():
            if count >= 5:
                break
            formatted_output.append(
                f"Date: {date}\n"
                f"  Open: ${values.get('1. open', 'N/A')}\n"
                f"  High: ${values.get('2. high', 'N/A')}\n"
                f"  Low: ${values.get('3. low', 'N/A')}\n"
                f"  Close: ${values.get('4. close', 'N/A')}\n"
                f"  Volume: {values.get('5. volume', 'N/A')}\n"
                "---"
            )
            count += 1
        
        if len(time_series) > 5:
            formatted_output.append(f"\n(Showing 5 of {len(time_series)} data points)")

        return "\n".join(formatted_output)
    except Exception as e:
        return f"Error formatting monthly time series data: {str(e)}"


def format_market_status(api_data: Dict[str, Any]) -> str:
    """Format market status data into a concise string.
    
    Args:
        api_data: The response data from the Alpha Vantage MARKET_STATUS endpoint
        
    Returns:
        A formatted string containing the market status information
    """
    try:
        if "Error Message" in api_data:
            return f"Alpha Vantage API error: {api_data['Error Message']}"
        if "Information" in api_data:
            return f"Alpha Vantage API information: {api_data['Information']}"
        if "Note" in api_data: # Rate limit notes
            return f"Alpha Vantage API Note: {api_data['Note']}"
            
        markets = api_data.get("markets", [])
        if not markets:
            return "No market status data available or unexpected format."

        output_lines = ["Global Market Status:", "---"]
        
        for market_data in markets:
            market_type = market_data.get("market_type", "N/A")
            region = market_data.get("region", "N/A")
            primary_exchanges = market_data.get("primary_exchanges", "N/A")
            local_open = market_data.get("local_open", "N/A")
            local_close = market_data.get("local_close", "N/A")
            current_status = market_data.get("current_status", "N/A")
            notes = market_data.get("notes", "")
            
            output_lines.append(
                f"Market: {market_type} ({region})\n"
                f"  Primary Exchanges: {primary_exchanges}\n"
                f"  Hours (Local): {local_open} - {local_close}\n"
                f"  Status: {current_status}"
            )
            if notes:
                output_lines.append(f"  Notes: {notes}")
            output_lines.append("---")
        
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting market status: {str(e)}"


import csv
import io

def format_listing_status(csv_data: str, state: str) -> str:
    """Format listing status CSV data into a concise string.
    
    Args:
        csv_data: CSV response from the Alpha Vantage LISTING_STATUS endpoint
        state: The state filter used ('active' or 'delisted')
        
    Returns:
        A formatted string containing the listing status information
    """
    try:
        # Use io.StringIO to treat the string as a file for the csv.reader
        csvfile = io.StringIO(csv_data)
        reader = csv.reader(csvfile)
        
        header = next(reader, None)  # Expected: symbol,name,exchange,assetType,ipoDate,delistingDate,status
        if not header:
            return "Empty CSV data or missing header."

        output_lines = [f"Listing Status (State: {state.capitalize()}) - Showing up to 10 listings:", "---"]
        # Create a formatted header row
        header_fmt = " | ".join(header)
        output_lines.append(header_fmt)
        output_lines.append("-" * len(header_fmt))  # Separator line

        count = 0
        for row in reader:
            if count >= 10:  # Limit output to 10 entries
                output_lines.append("\n... and potentially more listings.")
                break
            if row:  # Ensure row is not empty
                output_lines.append(" | ".join(row))
            count += 1
        
        if count == 0:
            return f"No listings found for state: {state.capitalize()}."

        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting listing status CSV data: {str(e)}"


def format_crypto_time_series(time_series_data: Dict[str, Any], series_type: str) -> str:
    """Format cryptocurrency time series data into a concise string.
    
    Args:
        time_series_data: The response data from Alpha Vantage Digital Currency endpoints
        series_type: Type of time series (daily, weekly, monthly)
        
    Returns:
        A formatted string containing the cryptocurrency time series information
    """
    try:
        # Determine the time series key based on series_type
        time_series_key = ""
        if series_type == "daily":
            time_series_key = "Time Series (Digital Currency Daily)"
        elif series_type == "weekly":
            time_series_key = "Time Series (Digital Currency Weekly)"
        elif series_type == "monthly":
            time_series_key = "Time Series (Digital Currency Monthly)"
        else:
            return f"Unknown series type: {series_type}"
            
        # Get the time series data
        time_series = time_series_data.get(time_series_key, {})
        if not time_series:
            all_keys = ", ".join(time_series_data.keys())
            return f"No cryptocurrency time series data found with key: '{time_series_key}'.\nAvailable keys: {all_keys}"

        # Get metadata
        metadata = time_series_data.get("Meta Data", {})
        crypto_symbol = metadata.get("2. Digital Currency Code", "Unknown")
        crypto_name = metadata.get("3. Digital Currency Name", "Unknown")
        market = metadata.get("4. Market Code", "Unknown")
        market_name = metadata.get("5. Market Name", "Unknown")
        last_refreshed = metadata.get("6. Last Refreshed", "Unknown")
        time_zone = metadata.get("7. Time Zone", "Unknown")

        # Format the header
        formatted_data = [
            f"{series_type.capitalize()} Time Series for {crypto_name} ({crypto_symbol})",
            f"Market: {market_name} ({market})",
            f"Last Refreshed: {last_refreshed} {time_zone}",
            ""
        ]

        # Format the most recent 5 data points
        for date, values in list(time_series.items())[:5]:
            # Get price information - based on the API response, we now know the correct field names
            open_price = values.get("1. open", "N/A")
            high_price = values.get("2. high", "N/A")
            low_price = values.get("3. low", "N/A")
            close_price = values.get("4. close", "N/A")
            volume = values.get("5. volume", "N/A")
            
            formatted_data.append(f"Date: {date}")
            formatted_data.append(f"Open: {open_price} {market}")
            formatted_data.append(f"High: {high_price} {market}")
            formatted_data.append(f"Low: {low_price} {market}")
            formatted_data.append(f"Close: {close_price} {market}")
            formatted_data.append(f"Volume: {volume}")
            formatted_data.append("---")
        
        return "\n".join(formatted_data)
    except Exception as e:
        return f"Error formatting cryptocurrency time series data: {str(e)}"


def format_historical_options(options_data: Dict[str, Any], limit: int = 10, sort_by: str = "strike", sort_order: str = "asc") -> str:
    """Format historical options chain data into a concise string with sorting.
    
    Args:
        options_data: The response data from the Alpha Vantage HISTORICAL_OPTIONS endpoint
        limit: Number of contracts to return (-1 for all)
        sort_by: Field to sort by
        sort_order: Sort order (asc or desc)
        
    Returns:
        A formatted string containing the historical options information
    """
    try:
        if "Error Message" in options_data:
            return f"Error: {options_data['Error Message']}"

        options_chain = options_data.get("data", [])

        if not options_chain:
            return "No options data available in the response"

        formatted = [
            f"Historical Options Data:\n",
            f"Status: {options_data.get('message', 'N/A')}\n",
            f"Sorted by: {sort_by} ({sort_order})\n\n"
        ]

        # Convert string values to float for numeric sorting
        def get_sort_key(contract):
            value = contract.get(sort_by, 0)
            try:
                # Remove $ and % signs if present
                if isinstance(value, str):
                    value = value.replace('$', '').replace('%', '')
                return float(value)
            except (ValueError, TypeError):
                return value

        # Sort the options chain
        sorted_chain = sorted(
            options_chain,
            key=get_sort_key,
            reverse=(sort_order == "desc")
        )

        # If limit is -1, show all contracts
        display_contracts = sorted_chain if limit == -1 else sorted_chain[:limit]

        for contract in display_contracts:
            formatted.append(f"Contract Details:\n")
            formatted.append(f"Contract ID: {contract.get('contractID', 'N/A')}\n")
            formatted.append(f"Expiration: {contract.get('expiration', 'N/A')}\n")
            formatted.append(f"Strike: ${contract.get('strike', 'N/A')}\n")
            formatted.append(f"Type: {contract.get('type', 'N/A')}\n")
            formatted.append(f"Last: ${contract.get('last', 'N/A')}\n")
            formatted.append(f"Mark: ${contract.get('mark', 'N/A')}\n")
            formatted.append(f"Bid: ${contract.get('bid', 'N/A')} (Size: {contract.get('bid_size', 'N/A')})\n")
            formatted.append(f"Ask: ${contract.get('ask', 'N/A')} (Size: {contract.get('ask_size', 'N/A')})\n")
            formatted.append(f"Volume: {contract.get('volume', 'N/A')}\n")
            formatted.append(f"Open Interest: {contract.get('open_interest', 'N/A')}\n")
            formatted.append(f"IV: {contract.get('implied_volatility', 'N/A')}\n")
            formatted.append(f"Delta: {contract.get('delta', 'N/A')}\n")
            formatted.append(f"Gamma: {contract.get('gamma', 'N/A')}\n")
            formatted.append(f"Theta: {contract.get('theta', 'N/A')}\n")
            formatted.append(f"Vega: {contract.get('vega', 'N/A')}\n")
            formatted.append(f"Rho: {contract.get('rho', 'N/A')}\n")
            formatted.append("---\n")

        if limit != -1 and len(sorted_chain) > limit:
            formatted.append(f"\n... and {len(sorted_chain) - limit} more contracts")

        return "".join(formatted)
    except Exception as e:
        return f"Error formatting options data: {str(e)}"


def format_intraday_time_series(time_series_data: Dict[str, Any]) -> str:
    """Format intraday time series data into a concise string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage TIME_SERIES_INTRADAY endpoint
        
    Returns:
        A formatted string containing the intraday time series information
    """
    try:
        # Get metadata
        metadata = time_series_data.get("Meta Data", {})
        if not metadata:
            return "No metadata available in the response"
            
        symbol = metadata.get("2. Symbol", "Unknown")
        last_refreshed = metadata.get("3. Last Refreshed", "Unknown")
        interval = metadata.get("4. Interval", "Unknown")
        output_size = metadata.get("5. Output Size", "Unknown")
        time_zone = metadata.get("6. Time Zone", "Unknown")
        
        # Determine the time series key based on interval
        time_series_key = f"Time Series ({interval})"
        time_series = time_series_data.get(time_series_key, {})
        
        if not time_series:
            all_keys = ", ".join(time_series_data.keys())
            return f"No intraday time series data available. Available keys: {all_keys}"

        # Format the header
        formatted_data = [
            f"Intraday Time Series for {symbol} (Interval: {interval})",
            f"Last Refreshed: {last_refreshed} {time_zone}",
            f"Output Size: {output_size}",
            ""
        ]

        # Format the most recent 10 data points
        for timestamp, values in list(time_series.items())[:10]:
            formatted_data.append(
                f"Time: {timestamp}\n"
                f"Open: ${values.get('1. open', 'N/A')}\n"
                f"High: ${values.get('2. high', 'N/A')}\n"
                f"Low: ${values.get('3. low', 'N/A')}\n"
                f"Close: ${values.get('4. close', 'N/A')}\n"
                f"Volume: {values.get('5. volume', 'N/A')}\n"
                "---\n"
            )

        return "\n".join(formatted_data)
    except Exception as e:
        return f"Error formatting intraday time series data: {str(e)}"


def format_news_sentiment(news_data: Dict[str, Any]) -> str:
    """Format news sentiment data into a concise string.
    
    Args:
        news_data: The response data from the Alpha Vantage NEWS_SENTIMENT endpoint
        
    Returns:
        A formatted string containing the news sentiment information
    """
    try:
        # Get feed entries
        feed = news_data.get("feed", [])
        if not feed:
            return "No news data available in the response"
        
        # Get metadata
        sentiment_score_definition = news_data.get("sentiment_score_definition", "Not provided")
        relevance_score_definition = news_data.get("relevance_score_definition", "Not provided")
        
        # Format the header
        formatted_data = [
            "News Sentiment Analysis",
            f"Sentiment Score Definition: {sentiment_score_definition}",
            f"Relevance Score Definition: {relevance_score_definition}",
            ""
        ]
        
        # Format the news items (up to 5)
        for i, item in enumerate(feed[:5]):
            title = item.get("title", "No title")
            url = item.get("url", "No URL")
            time_published = item.get("time_published", "Unknown")
            authors = item.get("authors", [])
            summary = item.get("summary", "No summary")
            overall_sentiment_score = item.get("overall_sentiment_score", "N/A")
            overall_sentiment_label = item.get("overall_sentiment_label", "N/A")
            
            # Get ticker sentiments if available
            ticker_sentiments = item.get("ticker_sentiment", [])
            
            formatted_data.append(f"News #{i+1}: {title}")
            formatted_data.append(f"URL: {url}")
            formatted_data.append(f"Published: {time_published}")
            formatted_data.append(f"Authors: {', '.join(authors) if authors else 'Not specified'}")
            formatted_data.append(f"Summary: {summary}")
            formatted_data.append(f"Overall Sentiment: {overall_sentiment_label} (Score: {overall_sentiment_score})")
            
            if ticker_sentiments:
                formatted_data.append("\nTicker Sentiments:")
                for ticker in ticker_sentiments[:3]:  # Limit to 3 tickers per news item
                    ticker_symbol = ticker.get("ticker", "Unknown")
                    ticker_relevance = ticker.get("relevance_score", "N/A")
                    ticker_sentiment = ticker.get("ticker_sentiment_score", "N/A")
                    ticker_label = ticker.get("ticker_sentiment_label", "N/A")
                    formatted_data.append(f"  {ticker_symbol}: {ticker_label} (Score: {ticker_sentiment}, Relevance: {ticker_relevance})")
            
            formatted_data.append("---")
        
        # Add a note if there are more news items
        if len(feed) > 5:
            formatted_data.append(f"\n... and {len(feed) - 5} more news items")
            
        return "\n".join(formatted_data)
    except Exception as e:
        return f"Error formatting news sentiment data: {str(e)}"


def format_technical_indicator(indicator_data: Dict[str, Any], indicator_name: str) -> str:
    """Format technical indicator data into a concise string.
    
    Args:
        indicator_data: The response data from an Alpha Vantage Technical Indicator endpoint
        indicator_name: The name of the technical indicator (e.g., SMA, EMA)
        
    Returns:
        A formatted string containing the technical indicator information
    """
    try:
        # Get metadata
        metadata = indicator_data.get("Meta Data", {})
        if not metadata:
            if "Error Message" in indicator_data:
                return f"Alpha Vantage API error: {indicator_data['Error Message']}"
            if "Information" in indicator_data:
                return f"Alpha Vantage API information: {indicator_data['Information']}"
            if "Note" in indicator_data:
                return f"Alpha Vantage API Note: {indicator_data['Note']}"
            return "No metadata available in the response"
            
        symbol = metadata.get("1: Symbol", "Unknown")
        indicator = metadata.get("2: Indicator", "Unknown")
        last_refreshed = metadata.get("3: Last Refreshed", "Unknown")
        interval = metadata.get("4: Interval", "Unknown")
        
        # Time period might be at different positions depending on indicator
        time_period = "N/A"
        for key in metadata.keys():
            if "Time Period" in key:
                time_period = metadata.get(key, "Unknown")
                break
        
        # Series type might be at different positions depending on indicator
        series_type = "N/A"
        for key in metadata.keys():
            if "Series Type" in key:
                series_type = metadata.get(key, "Unknown")
                break
                
        time_zone = metadata.get("7: Time Zone", "N/A")
        
        # Determine the indicator data key
        indicator_key = f"Technical Analysis: {indicator_name}"
        indicator_values = indicator_data.get(indicator_key, {})
        
        if not indicator_values:
            all_keys = ", ".join(indicator_data.keys())
            return f"No technical indicator data available. Available keys: {all_keys}"

        # Format the header
        formatted_data = [
            f"Technical Indicator: {indicator_name} for {symbol}",
            f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}",
            f"Last Refreshed: {last_refreshed}",
            ""
        ]

        # Format the most recent 10 data points
        for date, values in list(indicator_values.items())[:10]:
            indicator_value = values.get(indicator_name, "N/A")
            formatted_data.append(f"Date: {date}, {indicator_name}: {indicator_value}")
        
        formatted_data.append("---")
        
        return "\n".join(formatted_data)
    except Exception as e:
        return f"Error formatting technical indicator data: {str(e)}"


def format_bbands(indicator_data: Dict[str, Any]) -> str:
    """Format Bollinger Bands (BBANDS) indicator data.
    
    Args:
        indicator_data: The response data from the Alpha Vantage BBANDS endpoint
        
    Returns:
        A formatted string containing the BBANDS information
    """
    try:
        # Get metadata
        metadata = indicator_data.get("Meta Data", {})
        if not metadata:
            if "Error Message" in indicator_data:
                return f"Alpha Vantage API error: {indicator_data['Error Message']}"
            if "Information" in indicator_data:
                return f"Alpha Vantage API information: {indicator_data['Information']}"
            if "Note" in indicator_data:
                return f"Alpha Vantage API Note: {indicator_data['Note']}"
            return "No metadata available in BBANDS response."
            
        symbol = metadata.get("1: Symbol", "Unknown")
        indicator_name = metadata.get("2: Indicator", "BBANDS")
        last_refreshed = metadata.get("3: Last Refreshed", "N/A")
        interval = metadata.get("4: Interval", "N/A")
        time_period = metadata.get("5: Time Period", "N/A")
        deviation_multiplier = metadata.get("6: Deviation multiplier for upper band", "N/A")
        deviation_multiplier_lower = metadata.get("7: Deviation multiplier for lower band", "N/A")
        series_type = metadata.get("8: Series Type", "N/A")

        # The data key is "Technical Analysis: BBANDS"
        bbands_values = indicator_data.get("Technical Analysis: BBANDS", {})
        if not bbands_values:
            return "No BBANDS data available."

        output_lines = [
            f"Bollinger Bands (BBANDS) for {symbol}",
            f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}",
            f"Deviation Multiplier: Upper: {deviation_multiplier}, Lower: {deviation_multiplier_lower}",
            f"Last Refreshed: {last_refreshed}",
            "---"
        ]

        # Format the most recent 10 data points
        for date, values in list(bbands_values.items())[:10]:
            upper_band = values.get("Real Upper Band", "N/A")
            middle_band = values.get("Real Middle Band", "N/A")
            lower_band = values.get("Real Lower Band", "N/A")
            output_lines.append(f"Date: {date} -> Upper: {upper_band}, Middle: {middle_band}, Lower: {lower_band}")
        
        if len(bbands_values) > 10:
            output_lines.append(f"\n... and {len(bbands_values) - 10} more data points.")
        
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting BBANDS data: {str(e)}"


def format_time_series_monthly_adjusted(time_series_data: Dict[str, Any]) -> str:
    """Format monthly adjusted time series data into a concise string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage 
                          TIME_SERIES_MONTHLY_ADJUSTED endpoint.
        
    Returns:
        A formatted string containing the monthly adjusted time series information.
    """
    try:
        # The main data key in the JSON response is "Monthly Adjusted Time Series"
        time_series = time_series_data.get("Monthly Adjusted Time Series", {})
        if not time_series:
            if "Error Message" in time_series_data:
                return f"Alpha Vantage API error: {time_series_data['Error Message']}"
            if "Information" in time_series_data: # Premium endpoints might return this on free tier
                return f"Alpha Vantage API information: {time_series_data['Information']}"
            if "Note" in time_series_data: # Rate limit notes
                 return f"Alpha Vantage API Note: {time_series_data['Note']}"
            return "No monthly adjusted time series data available in the response."

        metadata = time_series_data.get("Meta Data", {})
        symbol = metadata.get("2. Symbol", "Unknown Symbol")
        last_refreshed = metadata.get("3. Last Refreshed", "Unknown Date")
        time_zone = metadata.get("4. Time Zone", "N/A")

        formatted_output = [
            f"Monthly Adjusted Time Series for {symbol}",
            f"Last Refreshed: {last_refreshed} (Timezone: {time_zone})",
            "---"
        ]

        # Display the latest 5 data points (months)
        count = 0
        for date, values in time_series.items():
            if count >= 5:
                break
            formatted_output.append(
                f"Date: {date}\n"
                f"  Open: ${values.get('1. open', 'N/A')}\n"
                f"  High: ${values.get('2. high', 'N/A')}\n"
                f"  Low: ${values.get('3. low', 'N/A')}\n"
                f"  Close: ${values.get('4. close', 'N/A')}\n"
                f"  Adjusted Close: ${values.get('5. adjusted close', 'N/A')}\n"
                f"  Volume: {values.get('6. volume', 'N/A')}\n"
                f"  Dividend Amount: ${values.get('7. dividend amount', 'N/A')}\n"
                "---"
            )
            count += 1
        
        if len(time_series) > 5:
            formatted_output.append(f"\n(Showing 5 of {len(time_series)} data points)")

        return "\n".join(formatted_output)
    except Exception as e:
        return f"Error formatting monthly adjusted time series data: {str(e)}"


def format_symbol_search(search_data: Dict[str, Any]) -> str:
    """Format symbol search results into a concise string.
    
    Args:
        search_data: The response data from the Alpha Vantage SYMBOL_SEARCH endpoint
        
    Returns:
        A formatted string containing the search results
    """
    try:
        # The main key for search results is "bestMatches"
        matches = search_data.get("bestMatches", [])
        if not matches:
            if "Error Message" in search_data:
                return f"Alpha Vantage API error: {search_data['Error Message']}"
            if "Information" in search_data:
                return f"Alpha Vantage API information: {search_data['Information']}"
            if "Note" in search_data:
                return f"Alpha Vantage API Note: {search_data['Note']}"
            return "No search results found."

        formatted_output = [f"Symbol Search Results: {len(matches)} matches found", "---"]
        
        for i, match in enumerate(matches):
            symbol = match.get("1. symbol", "N/A")
            name = match.get("2. name", "N/A")
            type_val = match.get("3. type", "N/A")
            region = match.get("4. region", "N/A")
            market_open = match.get("5. marketOpen", "N/A")
            market_close = match.get("6. marketClose", "N/A")
            timezone = match.get("7. timezone", "N/A")
            currency = match.get("8. currency", "N/A")
            match_score = match.get("9. matchScore", "N/A")
            
            formatted_output.append(
                f"Symbol: {symbol}\n"
                f"Name: {name}\n"
                f"Type: {type_val}\n"
                f"Region: {region}\n"
                f"Currency: {currency}\n"
                f"Match Score: {match_score}\n"
                f"Trading Hours: {market_open} - {market_close} ({timezone})\n"
                "---"
            )
            
            # Limit to showing first 10 matches if there are more
            if i >= 9 and len(matches) > 10:
                formatted_output.append(f"... and {len(matches) - 10} more matches.")
                break
                
        return "\n".join(formatted_output)
    except Exception as e:
        return f"Error formatting symbol search results: {str(e)}"


def format_fx_rate(fx_data: Dict[str, Any]) -> str:
    """Format forex exchange rate data into a concise string.
    
    Args:
        fx_data: The response data from Alpha Vantage forex endpoints
        
    Returns:
        A formatted string containing the forex exchange rate information
    """
    try:
        realtime_data = fx_data.get("Realtime Currency Exchange Rate", {})
        if not realtime_data:
            if "Error Message" in fx_data:
                return f"Alpha Vantage API error: {fx_data['Error Message']}"
            if "Information" in fx_data:
                return f"Alpha Vantage API information: {fx_data['Information']}"
            if "Note" in fx_data:
                return f"Alpha Vantage API Note: {fx_data['Note']}"
            return "No forex exchange rate data available in the response."

        return (
            f"From: {realtime_data.get('2. From_Currency Name', 'N/A')} ({realtime_data.get('1. From_Currency Code', 'N/A')})\n"
            f"To: {realtime_data.get('4. To_Currency Name', 'N/A')} ({realtime_data.get('3. To_Currency Code', 'N/A')})\n"
            f"Exchange Rate: {realtime_data.get('5. Exchange Rate', 'N/A')}\n"
            f"Last Updated: {realtime_data.get('6. Last Refreshed', 'N/A')} {realtime_data.get('7. Time Zone', 'N/A')}\n"
            f"Bid Price: {realtime_data.get('8. Bid Price', 'N/A')}\n"
            f"Ask Price: {realtime_data.get('9. Ask Price', 'N/A')}\n"
            "---"
        )
    except Exception as e:
        return f"Error formatting forex data: {str(e)}"


def format_fx_time_series(time_series_data: Dict[str, Any], series_type: str) -> str:
    """Format forex time series data into a concise string.
    
    Args:
        time_series_data: The response data from Alpha Vantage FX endpoints (daily, weekly, monthly)
        series_type: Type of time series (daily, weekly, monthly)
        
    Returns:
        A formatted string containing the forex time series information
    """
    try:
        # Determine the time series key based on series_type
        time_series_key = ""
        if series_type == "daily":
            time_series_key = "Time Series FX (Daily)"
        elif series_type == "weekly":
            time_series_key = "Time Series FX (Weekly)"
        elif series_type == "monthly":
            time_series_key = "Time Series FX (Monthly)"
        else:
            return f"Unknown series type: {series_type}"
            
        # Get the time series data
        time_series = time_series_data.get(time_series_key, {})
        if not time_series:
            if "Error Message" in time_series_data:
                return f"Alpha Vantage API error: {time_series_data['Error Message']}"
            if "Information" in time_series_data:
                return f"Alpha Vantage API information: {time_series_data['Information']}"
            if "Note" in time_series_data:
                return f"Alpha Vantage API Note: {time_series_data['Note']}"
            all_keys = ", ".join(time_series_data.keys())
            return f"No forex time series data found with key: '{time_series_key}'.\nAvailable keys: {all_keys}"

        # Get metadata
        metadata = time_series_data.get("Meta Data", {})
        from_symbol = metadata.get("2. From Symbol", "Unknown")
        to_symbol = metadata.get("3. To Symbol", "Unknown")
        last_refreshed = metadata.get("5. Last Refreshed", "Unknown")
        time_zone = metadata.get("6. Time Zone", "Unknown")

        # Format the header
        formatted_data = [
            f"Forex {series_type.capitalize()} Time Series for {from_symbol}/{to_symbol}",
            f"Last Refreshed: {last_refreshed} ({time_zone})",
            "---"
        ]

        # Format the most recent 5 data points
        count = 0
        for date, values in time_series.items():
            if count >= 5:
                break
            formatted_data.append(
                f"Date: {date}\n"
                f"  Open: {values.get('1. open', 'N/A')}\n"
                f"  High: {values.get('2. high', 'N/A')}\n"
                f"  Low: {values.get('3. low', 'N/A')}\n"
                f"  Close: {values.get('4. close', 'N/A')}\n"
                "---"
            )
            count += 1
        
        if len(time_series) > 5:
            formatted_data.append(f"\n(Showing 5 of {len(time_series)} data points)")
            
        return "\n".join(formatted_data)
    except Exception as e:
        return f"Error formatting forex time series data: {str(e)}"


def format_fundamental_data(data: Dict[str, Any], report_type: str) -> str:
    """Format company fundamental data into a concise string.
    
    Args:
        data: The response data from Alpha Vantage fundamental data endpoints
        report_type: The type of report (e.g., INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW)
        
    Returns:
        A formatted string containing the fundamental data information
    """
    try:
        if "Error Message" in data:
            return f"Alpha Vantage API error: {data['Error Message']}"
        if "Information" in data:
            return f"Alpha Vantage API information: {data['Information']}"
        if "Note" in data:
            return f"Alpha Vantage API Note: {data['Note']}"
            
        # Check if symbol and reports exist
        symbol = data.get("symbol", "Unknown")
        
        # Check for the appropriate report key based on report_type
        if report_type == "INCOME_STATEMENT":
            reports = data.get("annualReports", [])
            report_key = "Annual Income Statements"
        elif report_type == "BALANCE_SHEET":
            reports = data.get("annualReports", [])
            report_key = "Annual Balance Sheets"
        elif report_type == "CASH_FLOW":
            reports = data.get("annualReports", [])
            report_key = "Annual Cash Flows"
        elif report_type == "EARNINGS":
            annual_reports = data.get("annualEarnings", [])
            quarterly_reports = data.get("quarterlyEarnings", [])
            reports = annual_reports or quarterly_reports  # Use whichever one exists
            report_key = "Earnings Data"
        else:
            reports = data.get("annualReports", []) or data.get("quarterlyReports", [])
            report_key = f"{report_type} Reports"
        
        if not reports:
            all_keys = ", ".join(data.keys())
            return f"No {report_type.lower()} data found for {symbol}. Available keys: {all_keys}"
        
        # Format the header
        output_lines = [
            f"{report_key} for {symbol}",
            "---"
        ]
        
        # Format each report (up to 3 most recent)
        for i, report in enumerate(reports[:3]):
            fiscal_date = report.get("fiscalDateEnding", "N/A")
            output_lines.append(f"Report for fiscal period ending: {fiscal_date}")
            
            # Get all the financial items, excluding fiscalDateEnding
            items = [(k, v) for k, v in report.items() if k != "fiscalDateEnding"]
            
            # Sort items alphabetically for consistency
            items.sort(key=lambda x: x[0])
            
            # Display up to 10 key financial metrics per report
            for j, (key, value) in enumerate(items[:10]):
                # Format the key for readability
                formatted_key = " ".join(word.capitalize() for word in key.split("_") if word)
                formatted_key = formatted_key.replace("And", "and")
                
                output_lines.append(f"  {formatted_key}: {value}")
                
            if len(items) > 10:
                output_lines.append(f"  ... and {len(items) - 10} more items")
                
            output_lines.append("---")
            
        if len(reports) > 3:
            output_lines.append(f"\n... and {len(reports) - 3} more reports available.")
            
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting fundamental data: {str(e)}"


def format_gainers_losers(data: Dict[str, Any]) -> str:
    """Format top gainers and losers data into a concise string.
    
    Args:
        data: The response data from Alpha Vantage TOP_GAINERS_LOSERS endpoint
        
    Returns:
        A formatted string containing top gainers and losers information
    """
    try:
        if "Error Message" in data:
            return f"Alpha Vantage API error: {data['Error Message']}"
        if "Information" in data:
            return f"Alpha Vantage API information: {data['Information']}"
        if "Note" in data:
            return f"Alpha Vantage API Note: {data['Note']}"
        
        # The endpoint returns three main sections: metadata, top gainers, and top losers
        metadata = data.get("metadata", {})
        gainers = data.get("top_gainers", [])
        losers = data.get("top_losers", [])
        most_actively_traded = data.get("most_actively_traded", [])
        
        # Get metadata information if available
        last_updated = metadata.get("last_updated", "Unknown")
        
        # Format the output
        output_lines = [
            "Top Gainers, Losers, and Most Active Stocks",
            f"Last Updated: {last_updated}",
            "---"
        ]
        
        # Format top gainers
        if gainers:
            output_lines.append("\n✅ TOP GAINERS")
            for i, stock in enumerate(gainers[:5]):
                ticker = stock.get("ticker", "N/A")
                price = stock.get("price", "N/A")
                change_amount = stock.get("change_amount", "N/A")
                change_percentage = stock.get("change_percentage", "N/A")
                volume = stock.get("volume", "N/A")
                
                output_lines.append(
                    f"{i+1}. {ticker}: ${price} "  # Base info
                    f"(+${change_amount}, +{change_percentage}), "  # Change
                    f"Vol: {volume}"  # Volume
                )
            
            if len(gainers) > 5:
                output_lines.append(f"... and {len(gainers) - 5} more gainers")
        
        # Format top losers
        if losers:
            output_lines.append("\n❌ TOP LOSERS")
            for i, stock in enumerate(losers[:5]):
                ticker = stock.get("ticker", "N/A")
                price = stock.get("price", "N/A")
                change_amount = stock.get("change_amount", "N/A")
                change_percentage = stock.get("change_percentage", "N/A")
                volume = stock.get("volume", "N/A")
                
                output_lines.append(
                    f"{i+1}. {ticker}: ${price} "  # Base info
                    f"(${change_amount}, {change_percentage}), "  # Change
                    f"Vol: {volume}"  # Volume
                )
            
            if len(losers) > 5:
                output_lines.append(f"... and {len(losers) - 5} more losers")
        
        # Format most actively traded
        if most_actively_traded:
            output_lines.append("\n📊 MOST ACTIVELY TRADED")
            for i, stock in enumerate(most_actively_traded[:5]):
                ticker = stock.get("ticker", "N/A")
                price = stock.get("price", "N/A")
                change_amount = stock.get("change_amount", "N/A")
                change_percentage = stock.get("change_percentage", "N/A")
                volume = stock.get("volume", "N/A")
                
                output_lines.append(
                    f"{i+1}. {ticker}: ${price} "  # Base info
                    f"({change_amount}, {change_percentage}), "  # Change
                    f"Vol: {volume}"  # Volume
                )
            
            if len(most_actively_traded) > 5:
                output_lines.append(f"... and {len(most_actively_traded) - 5} more active stocks")
        
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting gainers/losers data: {str(e)}"


def format_earnings_calendar(csv_data: str) -> str:
    """Format earnings calendar CSV data into a concise string.
    
    Args:
        csv_data: CSV response from the Alpha Vantage EARNINGS_CALENDAR endpoint
        
    Returns:
        A formatted string containing the earnings calendar information
    """
    try:
        # Use io.StringIO to treat the string as a file for the csv.reader
        csvfile = io.StringIO(csv_data)
        reader = csv.reader(csvfile)
        
        header = next(reader, None)  # Expected header: symbol,name,reportDate,fiscalDateEnding,estimate,currency,etc.
        if not header:
            return "Empty CSV data or missing header."

        # Sort data by report date
        rows = list(reader)
        # Try to find the reportDate column index
        report_date_idx = None
        for i, column in enumerate(header):
            if column.lower() == "reportdate":
                report_date_idx = i
                break
        
        if report_date_idx is not None:
            # Sort by report date (if found)
            rows.sort(key=lambda x: x[report_date_idx] if len(x) > report_date_idx else "")
            
        # Format output
        output_lines = ["Upcoming Earnings Calendar - Showing up to 15 companies:", "---"]
        
        # Create a nicely formatted header row
        header_fmt = " | ".join(header)
        output_lines.append(header_fmt)
        output_lines.append("-" * len(header_fmt))

        count = 0
        for row in rows:
            if count >= 15:  # Limit output to 15 entries
                output_lines.append("\n... and potentially more upcoming earnings.")
                break
            if row:  # Ensure row is not empty
                output_lines.append(" | ".join(row))
            count += 1
        
        if count == 0:
            return "No upcoming earnings found in the calendar."

        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting earnings calendar CSV data: {str(e)}"


def format_commodity_data(data: Dict[str, Any], commodity_name: str) -> str:
    """Format commodity data into a concise string.
    
    Args:
        data: The response data from Alpha Vantage commodity endpoints
        commodity_name: The name of the commodity (e.g., WTI, BRENT, NATURAL_GAS)
        
    Returns:
        A formatted string containing the commodity price information
    """
    try:
        if "Error Message" in data:
            return f"Alpha Vantage API error: {data['Error Message']}"
        if "Information" in data:
            return f"Alpha Vantage API information: {data['Information']}"
        if "Note" in data:
            return f"Alpha Vantage API Note: {data['Note']}"
            
        # Find the data key
        data_key = None
        for key in data.keys():
            if key not in ["Meta Data", "Information", "Note", "Error Message"]:
                data_key = key
                break
                
        if not data_key or not data.get(data_key):
            all_keys = ", ".join(data.keys())
            return f"No commodity data found in response. Available keys: {all_keys}"
            
        # Get the commodity data values
        commodity_values = data.get(data_key, {})
        
        # Determine commodity name and unit from response if possible
        commodity_full_name = "Unknown Commodity"
        unit = "USD"
        
        if commodity_name == "WTI":
            commodity_full_name = "WTI (West Texas Intermediate) Crude Oil"
            unit = "USD per barrel"
        elif commodity_name == "BRENT":
            commodity_full_name = "Brent Crude Oil"
            unit = "USD per barrel"
        elif commodity_name == "NATURAL_GAS":
            commodity_full_name = "Natural Gas"
            unit = "USD per MMBtu"
        elif commodity_name == "COPPER":
            commodity_full_name = "Copper"
            unit = "USD per pound"
        elif commodity_name == "ALUMINUM":
            commodity_full_name = "Aluminum"
            unit = "USD per tonne"
        # Add other commodities as needed
        
        # Format the header
        output_lines = [
            f"{commodity_full_name} Prices",
            f"Unit: {unit}",
            "---"
        ]
        
        # Format data points (up to 10 most recent)
        if isinstance(commodity_values, dict):
            count = 0
            for date, values in list(sorted(commodity_values.items(), reverse=True))[:10]:
                if isinstance(values, dict):
                    value = values.get("value", "N/A")
                else:
                    value = values
                output_lines.append(f"Date: {date}, Price: {value} {unit}")
                count += 1
                
            if len(commodity_values) > 10:
                output_lines.append(f"\n... and {len(commodity_values) - 10} more data points.")
                
        elif isinstance(commodity_values, list):
            # Handle list format (some endpoints might return this)
            sorted_values = sorted(commodity_values, key=lambda x: x.get("date", ""), reverse=True)[:10]
            for value in sorted_values:
                date = value.get("date", "N/A")
                price = value.get("value", "N/A")
                output_lines.append(f"Date: {date}, Price: {price} {unit}")
                
            if len(commodity_values) > 10:
                output_lines.append(f"\n... and {len(commodity_values) - 10} more data points.")
                
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting commodity data: {str(e)}"


def format_treasury_yield(data: Dict[str, Any], maturity: str) -> str:
    """Format treasury yield data into a concise string.
    
    Args:
        data: The response data from Alpha Vantage TREASURY_YIELD endpoint
        maturity: The treasury maturity (e.g., '3month', '2year', '10year', etc.)
        
    Returns:
        A formatted string containing the treasury yield information
    """
    try:
        if "Error Message" in data:
            return f"Alpha Vantage API error: {data['Error Message']}"
        if "Information" in data:
            return f"Alpha Vantage API information: {data['Information']}"
        if "Note" in data:
            return f"Alpha Vantage API Note: {data['Note']}"
            
        # The data key is "data" containing an array of rates
        data_points = data.get("data", [])
        if not data_points:
            return f"No treasury yield data available for {maturity} maturity."
            
        # Get a human-readable maturity description
        maturity_desc = {
            "3month": "3-Month",
            "2year": "2-Year",
            "5year": "5-Year",
            "7year": "7-Year",
            "10year": "10-Year",
            "30year": "30-Year"
        }.get(maturity, maturity)
        
        # Format the header
        output_lines = [
            f"U.S. Treasury Yield Data - {maturity_desc} Maturity",
            "---"
        ]
        
        # Sort data by date, most recent first
        data_points.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        # Format the most recent 15 data points
        for i, point in enumerate(data_points[:15]):
            date = point.get("date", "N/A")
            value = point.get("value", "N/A")
            output_lines.append(f"Date: {date}, Yield: {value}%")
            
        if len(data_points) > 15:
            output_lines.append(f"\n... and {len(data_points) - 15} more historical yield data points.")
            
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting treasury yield data: {str(e)}"


def format_economic_indicator(data: Dict[str, Any], indicator_name: str) -> str:
    """Format economic indicator data into a concise string.
    
    Args:
        data: The response data from Alpha Vantage economic indicator endpoints
        indicator_name: The name of the economic indicator (e.g., REAL_GDP, CPI, INFLATION)
        
    Returns:
        A formatted string containing the economic indicator information
    """
    try:
        if "Error Message" in data:
            return f"Alpha Vantage API error: {data['Error Message']}"
        if "Information" in data:
            return f"Alpha Vantage API information: {data['Information']}"
        if "Note" in data:
            return f"Alpha Vantage API Note: {data['Note']}"
            
        # The key for economic indicator data varies by endpoint
        # Try a few common patterns
        data_key = None
        for key in data.keys():
            if key.startswith("data"):
                data_key = key
                break
            if key.startswith(indicator_name):
                data_key = key
                break
            if key not in ["Meta Data", "Information", "Note", "Error Message"]:
                data_key = key
                # Don't break here; continue to check for more specific keys
                
        if not data_key or not data.get(data_key):
            all_keys = ", ".join(data.keys())
            return f"No economic indicator data found in response. Available keys: {all_keys}"
            
        # For most economic indicators, the data is a list of dictionaries
        indicator_values = data.get(data_key, [])
        
        # Get metadata if available
        name = data.get("name", indicator_name)
        interval = data.get("interval", "annual") # Most economic indicators are annual
        unit = data.get("unit", "")  # Units like % or $ may be provided
        
        # Format the header
        output_lines = [
            f"{name} - {interval.capitalize()} Data",
            f"Unit: {unit}" if unit else "", # Include unit if available
            "---"
        ]
        
        # Filter out empty lines
        output_lines = [line for line in output_lines if line]
        
        # Format data points (up to 10 most recent)
        if isinstance(indicator_values, list):
            for i, value in enumerate(indicator_values[:10]):
                date = value.get("date", "N/A")
                data_value = value.get("value", "N/A")
                output_lines.append(f"Date: {date}, Value: {data_value}{' ' + unit if unit else ''}")
                
            if len(indicator_values) > 10:
                output_lines.append(f"\n... and {len(indicator_values) - 10} more data points.")
        elif isinstance(indicator_values, dict):
            # Some endpoints might return data as a dictionary with dates as keys
            count = 0
            for date, value in list(indicator_values.items())[:10]:
                if isinstance(value, dict):
                    # If value is a dictionary, try to get 'value' key
                    data_value = value.get("value", "N/A")
                else:
                    # If value is a scalar, use it directly
                    data_value = value
                output_lines.append(f"Date: {date}, Value: {data_value}{' ' + unit if unit else ''}")
                count += 1
                
            if len(indicator_values) > 10:
                output_lines.append(f"\n... and {len(indicator_values) - 10} more data points.")
                
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting economic indicator data: {str(e)}"


def format_macd(indicator_data: Dict[str, Any]) -> str:
    """Format MACD (Moving Average Convergence/Divergence) indicator data.
    
    Args:
        indicator_data: The response data from the Alpha Vantage MACD endpoint
        
    Returns:
        A formatted string containing the MACD information
    """
    try:
        # Get metadata
        metadata = indicator_data.get("Meta Data", {})
        if not metadata:
            if "Error Message" in indicator_data: 
                return f"Alpha Vantage API error: {indicator_data['Error Message']}"
            if "Information" in indicator_data:
                return f"Alpha Vantage API information: {indicator_data['Information']}"
            if "Note" in indicator_data:
                return f"Alpha Vantage API Note: {indicator_data['Note']}"
            return "No metadata available in MACD response."
            
        symbol = metadata.get("1: Symbol", "Unknown")
        indicator_name_full = metadata.get("2: Indicator", "MACD")  # e.g., "Moving Average Convergence/Divergence (MACD)"
        last_refreshed = metadata.get("3: Last Refreshed", "N/A")
        interval = metadata.get("4: Interval", "N/A")
        
        # MACD specific parameters from metadata
        fast_period = metadata.get("5.1: Fast Period", "N/A") 
        slow_period = metadata.get("5.2: Slow Period", "N/A")
        signal_period = metadata.get("5.3: Signal Period", "N/A")
        series_type = metadata.get("6: Series Type", "N/A")
        time_zone = metadata.get("7: Time Zone", "N/A")

        # The data key is "Technical Analysis: MACD"
        macd_values = indicator_data.get("Technical Analysis: MACD", {})
        if not macd_values:
            return "No MACD data available. This might be a premium endpoint."

        output_lines = [
            f"{indicator_name_full} for {symbol}",
            f"Interval: {interval}, FastP: {fast_period}, SlowP: {slow_period}, SignalP: {signal_period}",
            f"Last Refreshed: {last_refreshed}",
            "---"
        ]

        # Format the most recent 10 data points
        for date, values in list(macd_values.items())[:10]:
            macd_val = values.get("MACD", "N/A")
            signal_val = values.get("MACD_Signal", "N/A")
            hist_val = values.get("MACD_Hist", "N/A")
            output_lines.append(f"Date: {date} -> MACD: {macd_val}, Signal: {signal_val}, Hist: {hist_val}")
        
        if len(macd_values) > 10:
            output_lines.append(f"\n... and {len(macd_values) - 10} more data points.")
        
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting MACD data: {str(e)}"


def format_etf_profile(etf_data: Dict[str, Any]) -> str:
    """Format ETF profile data into a concise string.
    
    Args:
        etf_data: The response data from the Alpha Vantage ETF_PROFILE endpoint
        
    Returns:
        A formatted string containing the ETF profile information
    """
    try:
        # Check for Alpha Vantage specific error messages or notes
        if "Error Message" in etf_data:
            return f"Alpha Vantage API error: {etf_data['Error Message']}"
        if "Information" in etf_data:
            return f"Alpha Vantage API information: {etf_data['Information']}"
        if "Note" in etf_data:
            return f"Alpha Vantage API Note: {etf_data['Note']}"
        
        # Look for the ETF profile data
        # Based on API documentation, there might be a specific key for ETF data
        # If unsure about the exact structure, we check for common patterns
        
        profile_data = None
        for key in etf_data.keys():
            if "etf" in key.lower() or "profile" in key.lower() or "fund" in key.lower():
                profile_data = etf_data.get(key, {})
                break
                
        # If no specific ETF key found, try using the data directly
        # We might get a more accurate understanding of the response structure after testing
        if not profile_data:
            profile_data = etf_data
            
        # If we still have no data, provide a helpful message
        if not profile_data or len(profile_data) == 0:
            return "No ETF profile data available in the response."
            
        # Initialize output
        output_lines = []
        
        # Get ETF symbol and name if available
        # The exact fields may vary, so we check multiple possible keys
        etf_symbol = profile_data.get("Symbol", profile_data.get("symbol", "N/A"))
        etf_name = profile_data.get("Name", profile_data.get("name", profile_data.get("fund_name", "N/A")))
        
        # Add header
        output_lines.append(f"ETF Profile: {etf_name} ({etf_symbol})")
        output_lines.append("---")
        
        # Now we format the various ETF profile fields
        # We check for common ETF profile data fields
        fund_family = profile_data.get("FundFamily", profile_data.get("fund_family", "N/A"))
        asset_class = profile_data.get("AssetClass", profile_data.get("asset_class", "N/A"))
        category = profile_data.get("Category", profile_data.get("category", "N/A"))
        net_assets = profile_data.get("NetAssets", profile_data.get("net_assets", profile_data.get("aum", "N/A")))
        expense_ratio = profile_data.get("ExpenseRatio", profile_data.get("expense_ratio", "N/A"))
        inception_date = profile_data.get("InceptionDate", profile_data.get("inception_date", "N/A"))
        description = profile_data.get("Description", profile_data.get("description", "N/A"))
        
        # Add basic profile information
        if fund_family != "N/A":
            output_lines.append(f"Fund Family: {fund_family}")
        if asset_class != "N/A":
            output_lines.append(f"Asset Class: {asset_class}")
        if category != "N/A":
            output_lines.append(f"Category: {category}")
        if net_assets != "N/A":
            output_lines.append(f"Net Assets: {net_assets}")
        if expense_ratio != "N/A":
            output_lines.append(f"Expense Ratio: {expense_ratio}")
        if inception_date != "N/A":
            output_lines.append(f"Inception Date: {inception_date}")
        
        # Add description (if available)
        if description != "N/A" and len(description) > 0:
            # Format long descriptions to fit nicely
            if len(description) > 300:
                description = description[:297] + "..."
            output_lines.append(f"\nDescription: {description}")
        
        # Check for holdings data
        holdings = profile_data.get("Holdings", profile_data.get("holdings", profile_data.get("top_holdings", [])))
        if holdings and isinstance(holdings, list) and len(holdings) > 0:
            output_lines.append("\nTop Holdings:")
            for i, holding in enumerate(holdings[:10]):  # Show top 10 holdings max
                if isinstance(holding, dict):
                    holding_name = holding.get("Name", holding.get("name", "N/A"))
                    holding_weight = holding.get("Weight", holding.get("weight", "N/A"))
                    output_lines.append(f"  {i+1}. {holding_name}: {holding_weight}")
                else:
                    output_lines.append(f"  {i+1}. {holding}")
            
            if len(holdings) > 10:
                output_lines.append(f"  ... and {len(holdings) - 10} more holdings")
        
        # Check for sector allocations
        sectors = profile_data.get("SectorWeights", profile_data.get("sector_weights", profile_data.get("sectors", [])))
        if sectors and isinstance(sectors, list) and len(sectors) > 0:
            output_lines.append("\nSector Allocation:")
            for i, sector in enumerate(sectors[:8]):  # Show top 8 sectors max
                if isinstance(sector, dict):
                    sector_name = sector.get("Name", sector.get("name", "N/A"))
                    sector_weight = sector.get("Weight", sector.get("weight", "N/A"))
                    output_lines.append(f"  {sector_name}: {sector_weight}")
                else:
                    output_lines.append(f"  {sector}")
            
            if len(sectors) > 8:
                output_lines.append(f"  ... and {len(sectors) - 8} more sectors")
        
        # Add any additional fields that are common to ETF profiles
        for key, value in profile_data.items():
            if key not in ["Symbol", "symbol", "Name", "name", "fund_name", "FundFamily", "fund_family", 
                          "AssetClass", "asset_class", "Category", "category", "NetAssets", "net_assets", 
                          "aum", "ExpenseRatio", "expense_ratio", "InceptionDate", "inception_date",
                          "Description", "description", "Holdings", "holdings", "top_holdings",
                          "SectorWeights", "sector_weights", "sectors"]:
                # This ensures we don't miss important fields in case the API response has a different structure
                if isinstance(value, (str, int, float)) and value:
                    # Format key from camelCase or snake_case to Title Words
                    formatted_key = " ".join(word.capitalize() for word in re.split(r'(?=[A-Z])|_', key))
                    output_lines.append(f"{formatted_key}: {value}")
        
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting ETF profile data: {str(e)}"


def format_ipo_calendar(csv_data: str) -> str:
    """Format IPO calendar CSV data into a concise string.
    
    Args:
        csv_data: CSV response from the Alpha Vantage IPO_CALENDAR endpoint
        
    Returns:
        A formatted string containing the IPO calendar information
    """
    try:
        if not csv_data or not isinstance(csv_data, str):
            return "No IPO calendar data received or data is not in expected CSV format."
            
        # Use io.StringIO to treat the string as a file for the csv.reader
        csvfile = io.StringIO(csv_data)
        reader = csv.reader(csvfile)
        
        header = next(reader, None)  # Expected header like: symbol,name,ipoDate,exchange,priceRangeLow,...
        if not header:
            return "Empty CSV data or missing header for IPO calendar."
            
        # Read all rows so we can sort them by IPO date
        rows = list(reader)
        
        # Try to find the ipoDate column index
        ipo_date_idx = None
        for i, column in enumerate(header):
            if "ipodate" in column.lower():
                ipo_date_idx = i
                break
                
        # If we found the IPO date column, sort by that
        if ipo_date_idx is not None and len(rows) > 0:
            try:
                # Sort by IPO date (ascending)
                rows.sort(key=lambda x: x[ipo_date_idx] if len(x) > ipo_date_idx else "")
            except Exception:
                # If sorting fails, just leave the original order
                pass
                
        output_lines = ["Upcoming IPO Calendar - Showing up to 15 companies:", "---"]
        
        # Create a nicely formatted header row
        header_fmt = " | ".join(header)
        output_lines.append(header_fmt)
        output_lines.append("-" * len(header_fmt))  # Separator line
        
        count = 0
        for row in rows:
            if count >= 15:  # Limit output to 15 entries
                output_lines.append("\n... and potentially more upcoming IPOs.")
                break
            if row:  # Ensure row is not empty
                output_lines.append(" | ".join(row))
            count += 1
            
        if count == 0:  # After header
            return "No upcoming IPOs found in the calendar."
            
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting IPO calendar CSV data: {str(e)}"


def format_earnings_call_transcript(transcript_data: Dict[str, Any]) -> str:
    """Format earnings call transcript data into a concise string.
    
    Args:
        transcript_data: The response data from the Alpha Vantage EARNINGS_CALL_TRANSCRIPT endpoint
        
    Returns:
        A formatted string containing the earnings call transcript information
    """
    try:
        # Check for Alpha Vantage specific error messages or notes
        if "Error Message" in transcript_data:
            return f"Alpha Vantage API error: {transcript_data['Error Message']}"
        if "Information" in transcript_data:
            return f"Alpha Vantage API information: {transcript_data['Information']}"
        if "Note" in transcript_data:
            return f"Alpha Vantage API Note: {transcript_data['Note']}"
            
        # Look for the key components of the transcript data
        # The key structure may vary in actual API response
        # We'll check for common variations and handle them appropriately
        
        # First, get the metadata about the earnings call
        symbol = transcript_data.get("symbol", "N/A")
        quarter = transcript_data.get("fiscal_quarter", transcript_data.get("quarter", "N/A"))
        call_date = transcript_data.get("call_date", transcript_data.get("date", "N/A"))
        company_name = transcript_data.get("company_name", transcript_data.get("name", symbol))
        
        # Look for the transcript content
        transcript = ""
        # Try different possible keys where the transcript might be stored
        if "transcript" in transcript_data:
            transcript = transcript_data["transcript"]
        elif "content" in transcript_data:
            transcript = transcript_data["content"]
        
        # If we couldn't find the transcript text in expected keys, search more deeply
        if not transcript:
            # Look through any nested structures that might contain the transcript
            for key, value in transcript_data.items():
                if isinstance(value, dict) and "transcript" in value:
                    transcript = value["transcript"]
                    break
                if isinstance(value, dict) and "content" in value:
                    transcript = value["content"]
                    break
                    
        # If still no transcript, check for the expected structure more thoroughly
        if not transcript:
            all_keys = ", ".join(transcript_data.keys())
            return f"No transcript content found in the API response. Available keys: {all_keys}"
        
        # Extract participants if available
        participants = []
        if "participants" in transcript_data:
            participants_data = transcript_data["participants"]
            if isinstance(participants_data, list):
                for participant in participants_data:
                    if isinstance(participant, dict):
                        name = participant.get("name", "")
                        title = participant.get("title", "")
                        if name:
                            if title:
                                participants.append(f"{name} ({title})")
                            else:
                                participants.append(name)
        
        # Format the output
        output_lines = [
            f"Earnings Call Transcript for {company_name} ({symbol})",
            f"Fiscal Quarter: {quarter}",
            f"Call Date: {call_date}",
            "---"
        ]
        
        # Add participants if available
        if participants:
            output_lines.append("Participants:")
            for participant in participants[:10]:  # Limit to first 10 participants
                output_lines.append(f"  - {participant}")
            if len(participants) > 10:
                output_lines.append(f"  ...and {len(participants) - 10} more participants")
            output_lines.append("---")
        
        # Add transcript preview (first 1000 characters)
        if isinstance(transcript, str) and len(transcript) > 0:
            # Clean up the transcript text if needed
            transcript = transcript.strip()
            
            # For previewing, show first 1000 characters
            preview_length = 1000
            transcript_preview = transcript[:preview_length]
            
            output_lines.append("Transcript Preview:")
            output_lines.append(transcript_preview)
            
            if len(transcript) > preview_length:
                output_lines.append("...")
                output_lines.append(f"[Transcript continues for {len(transcript) - preview_length} more characters]")
        else:
            # If the transcript is not a string or is empty
            output_lines.append("No transcript text available.")
        
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting earnings call transcript data: {str(e)}"


def format_insider_transactions(transactions_data: Dict[str, Any]) -> str:
    """Format insider transactions data into a concise string.
    
    Args:
        transactions_data: The response data from the Alpha Vantage INSIDER_TRANSACTIONS endpoint
        
    Returns:
        A formatted string containing the insider transactions information
    """
    try:
        # Check for Alpha Vantage specific error messages or notes
        if "Error Message" in transactions_data:
            return f"Alpha Vantage API error: {transactions_data['Error Message']}"
        if "Information" in transactions_data:
            return f"Alpha Vantage API information: {transactions_data['Information']}"
        if "Note" in transactions_data:
            return f"Alpha Vantage API Note: {transactions_data['Note']}"
        
        # Get the symbol if available
        symbol = transactions_data.get("symbol", "Unknown")
        
        # Look for the transactions data
        # Based on the sample response, transactions may be in a list under a specific key
        transactions = []
        
        # Try to find transactions under different possible keys
        if "transactions" in transactions_data:
            transactions = transactions_data["transactions"]
        elif "data" in transactions_data:
            transactions = transactions_data["data"]
        else:
            # Check if the data is directly in the root of the response as a list of transaction objects
            for key, value in transactions_data.items():
                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    # This looks like a list of transaction records
                    transactions = value
                    break
        
        # If we still didn't find transactions, the structure might be unexpected
        if not transactions:
            all_keys = ", ".join(transactions_data.keys())
            return f"No insider transactions data found for {symbol}. Available keys: {all_keys}"
        
        # Format the output
        output_lines = [
            f"Insider Transactions for {symbol}",
            f"Total Transactions: {len(transactions)}",
            "---"
        ]
        
        # Sort transactions by date (most recent first) if transaction_date is available
        try:
            transactions = sorted(
                transactions,
                key=lambda x: x.get("transaction_date", ""),
                reverse=True
            )
        except:
            # If sorting fails, use the original order
            pass
        
        # Format the most recent 15 transactions
        for i, transaction in enumerate(transactions[:15]):
            # Extract transaction information
            date = transaction.get("transaction_date", "N/A")
            ticker = transaction.get("ticker", symbol)
            executive = transaction.get("executive", "N/A")
            executive_title = transaction.get("executive_title", "N/A")
            security_type = transaction.get("security_type", "N/A")
            acquisition_or_disposal = transaction.get("acquisition_or_disposal", "N/A")
            shares = transaction.get("shares", "N/A")
            share_price = transaction.get("share_price", "N/A")
            
            # Convert acquisition/disposal code to more readable format
            transaction_type = "Acquisition" if acquisition_or_disposal == "A" else "Disposal" if acquisition_or_disposal == "D" else acquisition_or_disposal
            
            # Format the transaction entry
            output_lines.append(
                f"Transaction #{i+1}:\n"
                f"  Date: {date}\n"
                f"  Executive: {executive}\n"
                f"  Title: {executive_title}\n"
                f"  Security Type: {security_type}\n"
                f"  Transaction: {transaction_type} of {shares} shares\n"
                f"  Share Price: ${share_price}\n"
                "---"
            )
        
        # Add note if there are more transactions
        if len(transactions) > 15:
            output_lines.append(f"\n... and {len(transactions) - 15} more transactions.")
        
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error formatting insider transactions data: {str(e)}"
