# Next Task: Implementing TIME_SERIES_MONTHLY_ADJUSTED Endpoint

Based on our progress implementing the TIME_SERIES_DAILY_ADJUSTED endpoint, the next logical endpoint to implement is TIME_SERIES_MONTHLY_ADJUSTED. This document provides detailed instructions for implementing this feature.

## Task Overview

Add support for the Alpha Vantage `TIME_SERIES_MONTHLY_ADJUSTED` endpoint, which provides monthly adjusted time series (date, open, high, low, close, adjusted close, volume, dividend amount, and split coefficient) data for a stock or equity, covering 20+ years of historical data.

## Implementation Steps

### Step 1: Add Formatter Function in tools.py

Create a new Python function to format the JSON response from the `TIME_SERIES_MONTHLY_ADJUSTED` API call:

```python
def format_time_series_monthly_adjusted(time_series_data: Dict[str, Any]) -> str:
    """Format monthly adjusted time series data into a concise string.
    
    Args:
        time_series_data: The response data from the Alpha Vantage TIME_SERIES_MONTHLY_ADJUSTED endpoint
        
    Returns:
        A formatted string containing the monthly adjusted time series information
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
```

Note: This follows the same pattern as the `format_time_series_daily_adjusted` function, with minor adjustments for the monthly data structure. Be aware that the monthly adjusted endpoint doesn't include a split coefficient like the daily adjusted endpoint does.

### Step 2: Update Imports in server.py

Add the new formatting function to the imports at the top of `server.py`:

```python
from .tools import (
    make_alpha_request,
    format_quote,
    format_company_info,
    format_crypto_rate,
    format_time_series,
    format_time_series_weekly,
    format_time_series_daily_adjusted,
    format_time_series_monthly_adjusted,  # Add this line
    format_historical_options,
    format_crypto_time_series,
    format_intraday_time_series,
    format_news_sentiment,
    format_technical_indicator,
    ALPHA_VANTAGE_BASE,
    API_KEY
)
```

### Step 3: Add Tool Definition

Add a new tool definition in the `handle_list_tools()` function, placing it after the `get-daily-adjusted-time-series` tool:

```python
types.Tool(
    name="get-monthly-adjusted-time-series",
    description="Get monthly adjusted time series (open, high, low, close, adjusted close, volume, dividend) for a stock. This is a premium Alpha Vantage endpoint.",
    inputSchema={
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "The stock symbol (e.g., AAPL, MSFT).",
            },
        },
        "required": ["symbol"],
    },
),
```

### Step 4: Add Tool Handler

Add a new handler for the `get-monthly-adjusted-time-series` tool in the `handle_call_tool()` function:

```python
elif name == "get-monthly-adjusted-time-series":
    if not arguments:
        return [types.TextContent(type="text", text="Error: Missing arguments for get-monthly-adjusted-time-series.")]
    
    symbol = arguments.get("symbol")
    if not symbol:
        return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]

    symbol = str(symbol).upper()

    async with httpx.AsyncClient() as client:
        api_response = await make_alpha_request(
            client,
            function="TIME_SERIES_MONTHLY_ADJUSTED", 
            symbol=symbol,
            additional_params=None
        )

        if isinstance(api_response, str):
            return [types.TextContent(type="text", text=f"Error: {api_response}")]
        
        if not isinstance(api_response, dict):
            return [types.TextContent(type="text", text="Error: Unexpected response format from API.")]

        formatted_response = format_time_series_monthly_adjusted(api_response)
        
        return [types.TextContent(type="text", text=formatted_response)]
```

### Step 5: Update README.md

1. Add `get-monthly-adjusted-time-series` to the list of available tools in the README.md:

```markdown
- `get-daily-adjusted-time-series`: Get historical daily adjusted price data with dividends and splits
- `get-monthly-adjusted-time-series`: Get historical monthly adjusted price data with dividends
- `get-intraday-time-series`: Get intraday price data (minutes) for a stock
```

2. Add a new section for the `get-monthly-adjusted-time-series` tool, after the section for `get-daily-adjusted-time-series`:

```markdown
### get-monthly-adjusted-time-series

Retrieves monthly adjusted time series (date, open, high, low, close, adjusted close, volume, and dividend amount) of the global equity specified, covering 20+ years of historical data. 
**Note: This is a premium Alpha Vantage API endpoint and may require a paid API key for full access.**

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "The stock symbol (e.g., AAPL, MSFT)."
    }
}
```

**Example Response (for symbol: IBM, assuming premium access):**
```
Monthly Adjusted Time Series for IBM
Last Refreshed: 2023-12-31 (Timezone: US/Eastern)
---
Date: 2023-12-31
  Open: $170.10
  High: $182.50
  Low: $169.80
  Close: $182.00
  Adjusted Close: $182.00
  Volume: 123456789
  Dividend Amount: $1.6500
---
Date: 2023-11-30
  Open: $158.00
  High: $170.50
  Low: $157.50
  Close: $170.00
  Adjusted Close: $170.00
  Volume: 120101010
  Dividend Amount: $0.0000
---
Date: 2023-10-31
  Open: $155.50
  High: $158.20
  Low: $155.00
  Close: $157.90
  Adjusted Close: $157.90
  Volume: 118765432
  Dividend Amount: $0.0000
---
Date: 2023-09-30
  Open: $154.30
  High: $156.40
  Low: $153.90
  Close: $155.60
  Adjusted Close: $155.60
  Volume: 117654321
  Dividend Amount: $1.6500
---
Date: 2023-08-31
  Open: $156.00
  High: $156.80
  Low: $153.50
  Close: $154.20
  Adjusted Close: $154.20
  Volume: 119876543
  Dividend Amount: $0.0000
---

(Showing 5 of 480 data points)
```
```

### Step 6: Update TODO.md

Update the TODO.md file to mark the `TIME_SERIES_MONTHLY_ADJUSTED` endpoint as completed:

```markdown
### Time Series Data
- [ ] Monthly time series (TIME_SERIES_MONTHLY)
- [x] Monthly Adjusted time series (TIME_SERIES_MONTHLY_ADJUSTED)
- [ ] Weekly Adjusted time series (TIME_SERIES_WEEKLY_ADJUSTED)
- [x] Daily Adjusted time series (TIME_SERIES_DAILY_ADJUSTED)
```

And update the Next Steps section:

```markdown
## Next Steps
1. Implement TIME_SERIES_MONTHLY endpoint
2. ~~Implement TIME_SERIES_MONTHLY_ADJUSTED endpoint~~ (Completed)
3. Implement TIME_SERIES_WEEKLY_ADJUSTED endpoint
4. ~~Implement TIME_SERIES_DAILY_ADJUSTED endpoint~~ (Completed)
```

### Step 7: Testing

1. Restart the MCP server to apply the changes
2. Test the new endpoint:
   - Verify that `get-monthly-adjusted-time-series` appears in the list of available tools
   - Call the tool with a valid symbol (e.g., AAPL, MSFT) and verify the output
   - Test with invalid symbols to check error handling
   - Be aware that as a premium endpoint, you may receive an information message or error with a free API key

## Lessons Learned from TIME_SERIES_DAILY_ADJUSTED Implementation

1. **Premium API Handling**: The `TIME_SERIES_MONTHLY_ADJUSTED` endpoint is a premium Alpha Vantage feature, similar to `TIME_SERIES_DAILY_ADJUSTED`. With a free API key, users will likely receive an informational message rather than actual data. The formatter function includes checks for this.

2. **Error Message Standardization**: We've standardized error messaging across all formatters for consistency, including API errors, rate limits, and premium feature notices.

3. **Data Structure**: The monthly adjusted endpoint has similar structure to daily adjusted but may not include all the same fields (such as split coefficients).

4. **Documentation Importance**: Clear documentation in README.md is crucial to inform users about premium endpoints that may require a paid API key. 