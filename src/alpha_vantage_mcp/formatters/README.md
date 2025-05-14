# Formatters Module

This module contains formatting functions that transform raw Alpha Vantage API responses into human-readable text output for the MCP interface.

## Structure

The formatters are organized by data category:

- `common.py`: Common utility functions used across different formatters
- `crypto.py`: Formatters for cryptocurrency data
- `economic.py`: Formatters for economic indicators
- `fundamental.py`: Formatters for fundamental company data
- `stocks.py`: Formatters for stock market data
- `technical.py`: Formatters for technical indicators

## How Formatters Work

Each formatter performs the following steps:

1. Extract metadata from the API response
2. Identify the main data section in the response
3. Format the data into a readable structure with appropriate headers
4. Handle pagination for large datasets (displaying a limited number of data points)
5. Apply consistent number formatting (decimal places, percentages, etc.)
6. Include error handling for malformed or empty responses

## Adding a New Formatter

To add a new formatter:

1. Identify the appropriate category file (or create a new one if needed)
2. Create a function following the pattern:
   ```python
   def format_your_indicator(data: Dict[str, Any]) -> str:
       """
       Format your indicator data into a readable string.
       
       Args:
           data: The response data from the Alpha Vantage endpoint
           
       Returns:
           A formatted string containing the indicator information
       """
   ```
3. Add the new formatter to the module's `__all__` list
4. Import the formatter in the appropriate handler file

## Example

Here's a simplified example of a formatter function:

```python
def format_technical_indicator(data: Dict[str, Any]) -> str:
    try:
        metadata = extract_metadata(data)
        indicator_key = next((k for k in data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not data[indicator_key]:
            return "No data available for this technical indicator."
            
        indicator_values = data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        
        output = f"Technical Indicator for {symbol}\n\n"
        output += f"Interval: {interval}\n\n"
        
        for date in dates[:10]:  # Show 10 most recent data points
            value = indicator_values[date].get("value", "N/A")
            output += f"Date: {date} -> Value: {value}\n"
            
        if len(dates) > 10:
            output += f"\n... and {len(dates) - 10} more data points."
            
        return output
    except Exception as e:
        return f"Error formatting data: {str(e)}"
```