# Handlers Module

This module contains handler functions that process MCP tool requests, communicate with the Alpha Vantage API, and return formatted responses.

## Structure

The handlers are organized by data category:

- `crypto.py`: Handlers for cryptocurrency data
- `economic.py`: Handlers for economic indicators
- `fundamental.py`: Handlers for fundamental company data
- `stocks.py`: Handlers for stock market data
- `technical.py`: Handlers for technical indicators
- `__init__.py`: Handler registry and mapping

## How Handlers Work

Each handler performs the following steps:

1. Validate input parameters
2. Construct an API request for Alpha Vantage
3. Send the request and receive the raw response
4. Process the response using the appropriate formatter
5. Return the formatted response as an MCP TextContent
6. Handle errors and exceptions during the process

## Handler Registry

The `HANDLER_MAPPING` dictionary in `__init__.py` maps tool names to their corresponding handler functions. This allows the MCP server to route tool requests to the appropriate handler.

Example:
```python
HANDLER_MAPPING = {
    'get-stock-quote': handle_stock_quote,
    'get-company-info': handle_company_info,
    'get-time-series': handle_time_series,
    # ...more mappings
}
```

## Adding a New Handler

To add a new handler function:

1. Identify the appropriate category file (or create a new one if needed)
2. Create an async function following this pattern:
   ```python
   async def handle_your_endpoint(
       symbol: str,
       param1: Optional[str] = None,
       param2: Optional[int] = None
   ) -> TextContent:
       """
       Handle requests for your Alpha Vantage endpoint.
       
       Args:
           symbol: The stock symbol to query
           param1: Optional parameter 1
           param2: Optional parameter 2
           
       Returns:
           Formatted text response
       """
       try:
           # Validate input parameters
           # ...validation code...
           
           # Set up the API request parameters
           params = {
               "function": "YOUR_FUNCTION",
               "symbol": symbol,
           }
           
           if param1 is not None:
               params["param1"] = param1
               
           if param2 is not None:
               params["param2"] = str(param2)
           
           # Make the API request
           response_data = await make_alpha_vantage_request(params)
           
           # Format the response
           formatted_response = format_your_endpoint(response_data)
           
           return TextContent(formatted_response)
       except Exception as e:
           # Handle any errors
           error_message = handle_api_error(e)
           return TextContent(error_message)
   ```
3. Add the handler function to the module's `__all__` list
4. Import the handler in `__init__.py` and add it to the `HANDLER_MAPPING` dictionary

## Example

Here's a simplified example of a handler:

```python
async def handle_technical_indicator(
    symbol: str, 
    interval: str = "daily",
    time_period: int = 14
) -> TextContent:
    try:
        # Validate input parameters
        validate_symbol(symbol)
        validate_interval(interval)
        validate_time_period(time_period)
        
        # Construct API request params
        params = {
            "function": "INDICATOR",
            "symbol": symbol,
            "interval": interval,
            "time_period": str(time_period),
        }
        
        # Make API request
        response_data = await make_alpha_vantage_request(params)
        
        # Format response
        formatted_response = format_technical_indicator(response_data)
        
        return TextContent(formatted_response)
    except Exception as e:
        error_message = handle_api_error(e)
        return TextContent(error_message)
```