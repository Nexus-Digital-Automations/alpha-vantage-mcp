"""
Formatters for economic and fundamental data Alpha Vantage API responses.

This module provides functions for formatting economic indicators, treasury yields,
fundamental company data, news sentiment, and commodity prices.
"""

from typing import Any, Dict, List, Optional
from ..config.settings import MAX_DISPLAY_ITEMS
from .common import (
    format_number, format_percentage, format_date, 
    format_volume, truncate_list, clean_key, extract_metadata,
    format_error_message
)

def format_economic_indicator(data: Dict[str, Any], indicator_name: str) -> str:
    """
    Format economic indicator data into a readable string.
    
    Args:
        data: The response data from Alpha Vantage Economic Indicator endpoints
        indicator_name: The name of the economic indicator (e.g., GDP, CPI)
        
    Returns:
        A formatted string containing the economic indicator information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return f"No {indicator_name} data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", indicator_name)
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "")
        data_points = data.get("data", [])
        
        if not data_points:
            return f"No {indicator_name} data available."
            
        # Create header
        output = f"{meta_data} ({indicator_name})\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            output += f"Date: {date}, Value: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting {indicator_name} data: {str(e)}")

def format_treasury_yield(data: Dict[str, Any], maturity: str) -> str:
    """
    Format treasury yield data into a readable string.
    
    Args:
        data: The response data from the Alpha Vantage Treasury Yield endpoint
        maturity: The bond maturity (e.g., '3month', '10year')
        
    Returns:
        A formatted string containing the treasury yield information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return f"No Treasury Yield data available for {maturity}."
            
        # Get the metadata and data points
        meta_data = data.get("name", f"Treasury Yield ({maturity})")
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "")
        data_points = data.get("data", [])
        
        if not data_points:
            return f"No Treasury Yield data available for {maturity}."
            
        # Create header
        output = f"{meta_data}\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as percentage if possible
            try:
                value_float = float(value)
                value = f"{value_float:.2f}%"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Yield: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Treasury Yield data: {str(e)}")

def format_fundamental_data(data: Dict[str, Any], report_type: str) -> str:
    """
    Format fundamental company data into a readable string.
    
    Args:
        data: The response data from Alpha Vantage Fundamental Data endpoints
        report_type: The type of fundamental data ('income', 'balance', 'cash')
        
    Returns:
        A formatted string containing the fundamental data information
    """
    try:
        # Determine the appropriate key based on report type
        key_map = {
            'income': 'annualReports',
            'income_quarterly': 'quarterlyReports',
            'balance': 'annualReports',
            'balance_quarterly': 'quarterlyReports',
            'cash': 'annualReports',
            'cash_quarterly': 'quarterlyReports',
            'earnings': 'annualEarnings',
            'earnings_quarterly': 'quarterlyEarnings'
        }
        
        # Get the key for this report type
        data_key = key_map.get(report_type, None)
        if not data_key or data_key not in data:
            return f"No {report_type.replace('_', ' ')} data available."
            
        # Get the report data
        reports = data.get(data_key, [])
        if not reports:
            return f"No {report_type.replace('_', ' ')} data available."
            
        # Get symbol if available
        symbol = data.get("symbol", "Unknown")
        
        # Create header based on report type
        report_titles = {
            'income': f"Income Statement for {symbol}",
            'income_quarterly': f"Quarterly Income Statement for {symbol}",
            'balance': f"Balance Sheet for {symbol}",
            'balance_quarterly': f"Quarterly Balance Sheet for {symbol}",
            'cash': f"Cash Flow Statement for {symbol}",
            'cash_quarterly': f"Quarterly Cash Flow Statement for {symbol}",
            'earnings': f"Annual Earnings for {symbol}",
            'earnings_quarterly': f"Quarterly Earnings for {symbol}"
        }
        
        output = f"{report_titles.get(report_type, f'{report_type.replace('_', ' ')} for {symbol}')}\n\n"
        
        # Format data differently based on report type
        if 'earnings' in report_type:
            # Earnings reports are simple
            for report in reports[:MAX_DISPLAY_ITEMS]:
                fiscal_date = report.get("fiscalDateEnding", "Unknown")
                reported_eps = report.get("reportedEPS", "N/A")
                
                output += f"Period Ending: {fiscal_date}\n"
                output += f"Reported EPS: ${reported_eps}\n"
                
                if 'quarterly' in report_type and 'estimatedEPS' in report:
                    estimated_eps = report.get("estimatedEPS", "N/A")
                    output += f"Estimated EPS: ${estimated_eps}\n"
                    
                    # Calculate surprise if both values are present
                    if reported_eps != "N/A" and estimated_eps != "N/A":
                        try:
                            reported = float(reported_eps)
                            estimated = float(estimated_eps)
                            surprise = reported - estimated
                            surprise_percent = (surprise / abs(estimated)) * 100 if estimated != 0 else 0
                            
                            output += f"Surprise: ${surprise:.2f} ({surprise_percent:.2f}%)\n"
                        except (ValueError, TypeError):
                            pass
                            
                output += "\n"
        else:
            # Financial statements have many line items
            for i, report in enumerate(reports[:MAX_DISPLAY_ITEMS]):
                fiscal_date = report.get("fiscalDateEnding", "Unknown")
                output += f"Period Ending: {fiscal_date}\n\n"
                
                # Filter out metadata fields
                report_items = {k: v for k, v in report.items() if k not in ["fiscalDateEnding", "reportedCurrency"]}
                
                # Display the most important items first
                important_items = []
                if 'income' in report_type:
                    important_items = ["totalRevenue", "grossProfit", "operatingIncome", "netIncome"]
                elif 'balance' in report_type:
                    important_items = ["totalAssets", "totalLiabilities", "totalShareholderEquity", "cashAndCashEquivalents"]
                elif 'cash' in report_type:
                    important_items = ["operatingCashflow", "cashflowFromInvestment", "cashflowFromFinancing", "netIncome"]
                
                # Show important items first
                for item in important_items:
                    if item in report_items:
                        value = report_items.pop(item, "N/A")
                        output += f"{clean_key(item)}: {format_number(value, is_currency=True)}\n"
                
                output += "\nAdditional Items:\n"
                
                # Show remaining items
                for key, value in sorted(report_items.items()):
                    output += f"{clean_key(key)}: {format_number(value, is_currency=True)}\n"
                
                if i < min(MAX_DISPLAY_ITEMS, len(reports)) - 1:
                    output += "\n---\n\n"
        
        # Add a note if there are more reports
        if len(reports) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(reports) - MAX_DISPLAY_ITEMS} more reports."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting {report_type.replace('_', ' ')} data: {str(e)}")

def format_news_sentiment(news_data: Dict[str, Any]) -> str:
    """
    Format news sentiment data into a readable string.
    
    Args:
        news_data: The response data from the Alpha Vantage News Sentiment endpoint
        
    Returns:
        A formatted string containing the news sentiment information
    """
    try:
        # Check if data is available
        if not news_data or "feed" not in news_data:
            return "No news sentiment data available."
            
        # Get the feed and ticker sentiments
        feed = news_data.get("feed", [])
        
        if not feed:
            return "No news articles found in the sentiment feed."
            
        # Create header
        output = "News Sentiment Analysis\n"
        output += "Sentiment Score Definition: The sentiment score ranges from -1.0 (most bearish) to 1.0 (most bullish)\n"
        output += "Relevance Score Definition: The relevance score ranges from 0 to 1, with 1 indicating highest relevance\n\n"
        
        # Add news articles (limited to MAX_DISPLAY_ITEMS)
        for i, article in enumerate(feed[:MAX_DISPLAY_ITEMS]):
            title = article.get("title", "Untitled")
            url = article.get("url", "")
            time_published = article.get("time_published", "Unknown")
            authors = article.get("authors", [])
            summary = article.get("summary", "No summary available")
            overall_sentiment = article.get("overall_sentiment_score", 0)
            
            # Format time published
            if time_published and len(time_published) == 12:
                formatted_time = f"{time_published[:8]}T{time_published[8:]}"
            else:
                formatted_time = time_published
                
            # Format overall sentiment
            sentiment_label = "Neutral"
            if overall_sentiment > 0.35:
                sentiment_label = "Bullish"
            elif overall_sentiment < -0.35:
                sentiment_label = "Bearish"
                
            output += f"News #{i+1}: {title}\n"
            if url:
                output += f"URL: {url}\n"
            output += f"Published: {formatted_time}\n"
            
            if authors:
                authors_str = ", ".join(authors)
                output += f"Authors: {authors_str}\n"
                
            output += f"Summary: {summary[:200]}{'...' if len(summary) > 200 else ''}\n"
            output += f"Overall Sentiment: {sentiment_label} (Score: {overall_sentiment:.2f})\n\n"
            
            # Add ticker sentiments if available
            ticker_sentiment = article.get("ticker_sentiment", [])
            if ticker_sentiment:
                output += "Ticker Sentiments:\n"
                
                for ticker in ticker_sentiment:
                    ticker_symbol = ticker.get("ticker", "")
                    ticker_sentiment_score = ticker.get("ticker_sentiment_score", 0)
                    ticker_relevance_score = ticker.get("relevance_score", 0)
                    
                    # Format ticker sentiment
                    ticker_sentiment_label = "Neutral"
                    if ticker_sentiment_score > 0.35:
                        ticker_sentiment_label = "Bullish"
                    elif ticker_sentiment_score < -0.35:
                        ticker_sentiment_label = "Bearish"
                        
                    output += f"  {ticker_symbol}: {ticker_sentiment_label} (Score: {ticker_sentiment_score:.2f}, Relevance: {ticker_relevance_score:.2f})\n"
                    
            output += "---\n\n"
            
        # Add a note if there are more articles
        if len(feed) > MAX_DISPLAY_ITEMS:
            output += f"... and {len(feed) - MAX_DISPLAY_ITEMS} more news articles."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting news sentiment data: {str(e)}")

def format_commodity_data(data: Dict[str, Any], commodity_name: str) -> str:
    """
    Format commodity price data into a readable string.
    
    Args:
        data: The response data from Alpha Vantage Commodity endpoints
        commodity_name: The name of the commodity (e.g., 'WTI', 'BRENT')
        
    Returns:
        A formatted string containing the commodity price information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return f"No {commodity_name} price data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", commodity_name)
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "")
        data_points = data.get("data", [])
        
        if not data_points:
            return f"No {commodity_name} price data available."
            
        # Create header with more descriptive commodity names
        commodity_descriptions = {
            'WTI': 'West Texas Intermediate (WTI) Crude Oil',
            'BRENT': 'Brent Crude Oil',
            'NATURAL_GAS': 'Natural Gas',
            'COPPER': 'Copper',
            'ALUMINUM': 'Aluminum',
            'WHEAT': 'Wheat',
            'CORN': 'Corn',
            'COTTON': 'Cotton',
            'SUGAR': 'Sugar',
            'COFFEE': 'Coffee'
        }
        
        full_name = commodity_descriptions.get(commodity_name, meta_data)
        output = f"{full_name} Prices\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as currency if possible
            try:
                value_float = float(value)
                value = f"${value_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Price: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting {commodity_name} price data: {str(e)}")

def format_metal_commodity(data: Dict[str, Any], commodity_name: str) -> str:
    """
    Format metal commodity price data into a readable string.
    
    Args:
        data: The response data from Alpha Vantage Metal Commodity endpoints (COPPER, ALUMINUM)
        commodity_name: The name of the commodity (e.g., 'COPPER', 'ALUMINUM')
        
    Returns:
        A formatted string containing the metal commodity price information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return f"No {commodity_name} price data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", commodity_name)
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "")
        data_points = data.get("data", [])
        
        if not data_points:
            return f"No {commodity_name} price data available."
            
        # Create header with more descriptive commodity names
        commodity_descriptions = {
            'COPPER': 'Global Price of Copper',
            'ALUMINUM': 'Global Price of Aluminum',
        }
        
        full_name = commodity_descriptions.get(commodity_name, meta_data)
        output = f"{full_name}\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as currency if possible
            try:
                value_float = float(value)
                value = f"${value_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Price: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting {commodity_name} price data: {str(e)}")

def format_real_gdp_per_capita(data: Dict[str, Any]) -> str:
    """
    Format Real GDP Per Capita data into a readable string.
    
    Args:
        data: The response data from the Alpha Vantage REAL_GDP_PER_CAPITA endpoint
        
    Returns:
        A formatted string containing the Real GDP Per Capita information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return "No Real GDP Per Capita data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", "Real GDP Per Capita")
        unit = data.get("unit", "")
        data_points = data.get("data", [])
        
        if not data_points:
            return "No Real GDP Per Capita data available."
            
        # Create header
        output = f"{meta_data}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as currency if possible
            try:
                value_float = float(value)
                value = f"${value_float:,.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Value: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Real GDP Per Capita data: {str(e)}")

def format_federal_funds_rate(data: Dict[str, Any]) -> str:
    """
    Format Federal Funds Rate data into a readable string.
    
    Args:
        data: The response data from the Alpha Vantage FEDERAL_FUNDS_RATE endpoint
        
    Returns:
        A formatted string containing the Federal Funds Rate information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return "No Federal Funds Rate data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", "Federal Funds Rate")
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "")
        data_points = data.get("data", [])
        
        if not data_points:
            return "No Federal Funds Rate data available."
            
        # Create header
        output = f"{meta_data}\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as percentage if possible
            try:
                value_float = float(value)
                value = f"{value_float:.2f}%"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Rate: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Federal Funds Rate data: {str(e)}")

def format_retail_sales(data: Dict[str, Any]) -> str:
    """
    Format Retail Sales data into a readable string.
    
    Args:
        data: The response data from the Alpha Vantage RETAIL_SALES endpoint
        
    Returns:
        A formatted string containing the Retail Sales information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return "No Retail Sales data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", "Advance Retail Sales")
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "Millions of Dollars")
        data_points = data.get("data", [])
        
        if not data_points:
            return "No Retail Sales data available."
            
        # Create header
        output = f"{meta_data}\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as currency if possible
            try:
                value_float = float(value)
                # Format in millions if value is large
                if value_float >= 1000:
                    value = f"${value_float/1000:.2f} billion"
                else:
                    value = f"${value_float:.2f} million"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Sales: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Retail Sales data: {str(e)}")

def format_durables(data: Dict[str, Any]) -> str:
    """
    Format Durable Goods Orders data into a readable string.
    
    Args:
        data: The response data from the Alpha Vantage DURABLES endpoint
        
    Returns:
        A formatted string containing the Durable Goods Orders information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return "No Durable Goods Orders data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", "Manufacturers' New Orders: Durable Goods")
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "Millions of Dollars")
        data_points = data.get("data", [])
        
        if not data_points:
            return "No Durable Goods Orders data available."
            
        # Create header
        output = f"{meta_data}\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as currency if possible
            try:
                value_float = float(value)
                # Format in millions if value is large
                if value_float >= 1000:
                    value = f"${value_float/1000:.2f} billion"
                else:
                    value = f"${value_float:.2f} million"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Orders: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Durable Goods Orders data: {str(e)}")

def format_agricultural_commodity(data: Dict[str, Any], commodity_name: str) -> str:
    """
    Format agricultural commodity price data into a readable string.
    
    Args:
        data: The response data from Alpha Vantage Agricultural Commodity endpoints (WHEAT, CORN, etc.)
        commodity_name: The name of the commodity (e.g., 'WHEAT', 'CORN')
        
    Returns:
        A formatted string containing the agricultural commodity price information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return f"No {commodity_name} price data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", commodity_name)
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "")
        data_points = data.get("data", [])
        
        if not data_points:
            return f"No {commodity_name} price data available."
            
        # Create header with more descriptive commodity names
        commodity_descriptions = {
            'WHEAT': 'Global Price of Wheat',
            'CORN': 'Global Price of Corn',
            'COTTON': 'Global Price of Cotton',
            'SUGAR': 'Global Price of Sugar',
            'COFFEE': 'Global Price of Coffee'
        }
        
        full_name = commodity_descriptions.get(commodity_name, meta_data)
        output = f"{full_name}\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as currency if possible
            try:
                value_float = float(value)
                value = f"${value_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Price: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting {commodity_name} price data: {str(e)}")

def format_unemployment(data: Dict[str, Any]) -> str:
    """
    Format Unemployment Rate data into a readable string.
    
    Args:
        data: The response data from the Alpha Vantage UNEMPLOYMENT endpoint
        
    Returns:
        A formatted string containing the Unemployment Rate information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return "No Unemployment Rate data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", "U.S. Unemployment Rate")
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "Percent")
        data_points = data.get("data", [])
        
        if not data_points:
            return "No Unemployment Rate data available."
            
        # Create header
        output = f"{meta_data}\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as percentage if possible
            try:
                value_float = float(value)
                value = f"{value_float:.1f}%"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Rate: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Unemployment Rate data: {str(e)}")

def format_nonfarm_payroll(data: Dict[str, Any]) -> str:
    """
    Format Nonfarm Payroll data into a readable string.
    
    Args:
        data: The response data from the Alpha Vantage NONFARM_PAYROLL endpoint
        
    Returns:
        A formatted string containing the Nonfarm Payroll information
    """
    try:
        # Check if data is available
        if not data or "data" not in data:
            return "No Nonfarm Payroll data available."
            
        # Get the metadata and data points
        meta_data = data.get("name", "U.S. Nonfarm Payroll")
        interval = data.get("interval", "Unknown")
        unit = data.get("unit", "Thousands of Persons")
        data_points = data.get("data", [])
        
        if not data_points:
            return "No Nonfarm Payroll data available."
            
        # Create header
        output = f"{meta_data}\n"
        output += f"Interval: {interval}\n"
        if unit:
            output += f"Unit: {unit}\n"
        output += "\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for point in data_points[:MAX_DISPLAY_ITEMS]:
            date = point.get("date", "Unknown")
            value = point.get("value", "N/A")
            
            # Format as number with commas if possible
            try:
                value_float = float(value)
                # Format in millions if value is large (likely in thousands)
                if value_float >= 1000:
                    value = f"{value_float/1000:.2f} million"
                else:
                    value = f"{value_float:,.0f} thousand"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}, Payroll: {value}\n"
            
        # Add a note if there are more data points
        if len(data_points) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(data_points) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Nonfarm Payroll data: {str(e)}")

# Export all formatters
__all__ = [
    'format_economic_indicator',
    'format_treasury_yield',
    'format_fundamental_data',
    'format_news_sentiment',
    'format_commodity_data',
    'format_metal_commodity',
    'format_agricultural_commodity',
    'format_real_gdp_per_capita',
    'format_federal_funds_rate',
    'format_retail_sales',
    'format_durables',
    'format_unemployment',
    'format_nonfarm_payroll'
]