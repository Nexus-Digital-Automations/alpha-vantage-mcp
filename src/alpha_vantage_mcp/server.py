"""
Alpha Vantage MCP Server

This module implements the Model Context Protocol (MCP) server for the Alpha Vantage API.
It provides a set of tools for accessing financial data through the MCP interface.
"""

from typing import Any, List, Dict, Optional
import asyncio
import os
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Import config
from .config.settings import validate_api_key

# Import handler mapping
from .handlers import HANDLER_MAPPING

# Import schemas
from .models.schemas import (
    STOCK_QUOTE_SCHEMA,
    COMPANY_INFO_SCHEMA,
    CRYPTO_RATE_SCHEMA,
    TIME_SERIES_SCHEMA,
    WEEKLY_MONTHLY_TIME_SERIES_SCHEMA,
    INTRADAY_TIME_SERIES_SCHEMA,
    NEWS_SENTIMENT_SCHEMA,
    SMA_SCHEMA,
    HISTORICAL_OPTIONS_SCHEMA,
    CRYPTO_TIME_SERIES_SCHEMA,
    TECHNICAL_INDICATOR_SCHEMA,
    MACD_SCHEMA,
    MARKET_STATUS_SCHEMA,
    LISTING_STATUS_SCHEMA,
    ETF_PROFILE_SCHEMA,
    IPO_CALENDAR_SCHEMA,
    EARNINGS_CALL_TRANSCRIPT_SCHEMA,
    INSIDER_TRANSACTIONS_SCHEMA,
    ECONOMIC_INDICATOR_SCHEMA,
    TREASURY_YIELD_SCHEMA,
    FUNDAMENTAL_DATA_SCHEMA,
    COMMODITY_DATA_SCHEMA,
    COTTON_SCHEMA,
    SUGAR_SCHEMA,
    COFFEE_SCHEMA,
    ALL_COMMODITIES_SCHEMA,
    CMO_SCHEMA,
    ROC_SCHEMA,
    ROCR_SCHEMA,
    AROON_SCHEMA,
    AROONOSC_SCHEMA,
    MFI_SCHEMA,
    TRIX_SCHEMA,
    ULTOSC_SCHEMA,
    DX_SCHEMA
)

async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get-stock-quote",
            description="Get current stock quote information",
            inputSchema=STOCK_QUOTE_SCHEMA
        ),
        types.Tool(
            name="get-company-info",
            description="Get stock-related information for a specific company",
            inputSchema=COMPANY_INFO_SCHEMA
        ),
        types.Tool(
            name="get-crypto-exchange-rate",
            description="Get current cryptocurrency exchange rates",
            inputSchema=CRYPTO_RATE_SCHEMA
        ),
        types.Tool(
            name="get-time-series",
            description="Get historical daily price data for a stock",
            inputSchema=TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-weekly-time-series",
            description="Get historical weekly price data for a stock",
            inputSchema=WEEKLY_MONTHLY_TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-monthly-time-series",
            description="Get historical monthly price data for a stock",
            inputSchema=WEEKLY_MONTHLY_TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-daily-adjusted-time-series",
            description="Get historical daily adjusted price data with dividends and splits",
            inputSchema=TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-weekly-adjusted-time-series",
            description="Get historical weekly adjusted price data with dividends",
            inputSchema=WEEKLY_MONTHLY_TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-monthly-adjusted-time-series",
            description="Get historical monthly adjusted price data with dividends",
            inputSchema=WEEKLY_MONTHLY_TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-intraday-time-series",
            description="Get intraday price data (minutes) for a stock",
            inputSchema=INTRADAY_TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-news-sentiment",
            description="Get news and sentiment analysis for stocks and crypto",
            inputSchema=NEWS_SENTIMENT_SCHEMA
        ),
        types.Tool(
            name="get-sma",
            description="Get Simple Moving Average technical indicator data",
            inputSchema=SMA_SCHEMA
        ),
        types.Tool(
            name="get-ema",
            description="Get Exponential Moving Average technical indicator data",
            inputSchema=SMA_SCHEMA  # Reuse the same schema as SMA
        ),
        types.Tool(
            name="get-wma",
            description="Get Weighted Moving Average technical indicator data",
            inputSchema=SMA_SCHEMA  # Reuse the same schema as SMA
        ),
        types.Tool(
            name="get-dema",
            description="Get Double Exponential Moving Average technical indicator data",
            inputSchema=SMA_SCHEMA  # Reuse the same schema as SMA
        ),
        types.Tool(
            name="get-tema",
            description="Get Triple Exponential Moving Average technical indicator data",
            inputSchema=SMA_SCHEMA  # Reuse the same schema as SMA
        ),
        types.Tool(
            name="get-macd",
            description="Get Moving Average Convergence/Divergence (MACD) indicator data",
            inputSchema=MACD_SCHEMA
        ),
        types.Tool(
            name="get-rsi",
            description="Get Relative Strength Index (RSI) technical indicator data",
            inputSchema=SMA_SCHEMA  # Reuse the same schema as SMA
        ),
        types.Tool(
            name="get-bbands",
            description="Get Bollinger Bands (BBANDS) technical indicator data",
            inputSchema=SMA_SCHEMA  # Reuse the same schema as SMA with additional parameters
        ),
        types.Tool(
            name="get-stoch",
            description="Get Stochastic Oscillator (STOCH) technical indicator data",
            inputSchema=TECHNICAL_INDICATOR_SCHEMA  # Base schema
        ),
        types.Tool(
            name="get-stochf",
            description="Get Stochastic Fast (STOCHF) technical indicator data",
            inputSchema=TECHNICAL_INDICATOR_SCHEMA  # Base schema
        ),
        types.Tool(
            name="get-willr",
            description="Get Williams' %R (WILLR) technical indicator data",
            inputSchema=TECHNICAL_INDICATOR_SCHEMA  # Base schema
        ),
        types.Tool(
            name="get-adx",
            description="Get Average Directional Movement Index (ADX) technical indicator data",
            inputSchema=TECHNICAL_INDICATOR_SCHEMA  # Base schema
        ),
        types.Tool(
            name="get-cmo",
            description="Get Chande Momentum Oscillator (CMO) technical indicator data",
            inputSchema=CMO_SCHEMA
        ),
        types.Tool(
            name="get-roc",
            description="Get Rate of Change (ROC) technical indicator data",
            inputSchema=ROC_SCHEMA
        ),
        types.Tool(
            name="get-rocr",
            description="Get Rate of Change Ratio (ROCR) technical indicator data",
            inputSchema=ROCR_SCHEMA
        ),
        types.Tool(
            name="get-aroon",
            description="Get Aroon technical indicator data",
            inputSchema=AROON_SCHEMA
        ),
        types.Tool(
            name="get-aroonosc",
            description="Get Aroon Oscillator technical indicator data",
            inputSchema=AROONOSC_SCHEMA
        ),
        types.Tool(
            name="get-mfi",
            description="Get Money Flow Index (MFI) technical indicator data",
            inputSchema=MFI_SCHEMA
        ),
        types.Tool(
            name="get-trix",
            description="Get Triple Exponential Average (TRIX) technical indicator data",
            inputSchema=TRIX_SCHEMA
        ),
        types.Tool(
            name="get-ultosc",
            description="Get Ultimate Oscillator (ULTOSC) technical indicator data",
            inputSchema=ULTOSC_SCHEMA
        ),
        types.Tool(
            name="get-dx",
            description="Get Directional Movement Index (DX) technical indicator data",
            inputSchema=DX_SCHEMA
        ),
        types.Tool(
            name="get-historical-options",
            description="Get historical options chain data with advanced filtering and sorting",
            inputSchema=HISTORICAL_OPTIONS_SCHEMA
        ),
        types.Tool(
            name="get-crypto-daily",
            description="Get daily time series data for a cryptocurrency",
            inputSchema=CRYPTO_TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-crypto-weekly",
            description="Get weekly time series data for a cryptocurrency",
            inputSchema=CRYPTO_TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-crypto-monthly",
            description="Get monthly time series data for a cryptocurrency",
            inputSchema=CRYPTO_TIME_SERIES_SCHEMA
        ),
        types.Tool(
            name="get-fx-rate",
            description="Get current foreign exchange rates",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string",
                        "description": "From currency (e.g., USD, EUR)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "To currency (e.g., JPY, GBP)"
                    }
                },
                "required": ["from_currency", "to_currency"]
            }
        ),
        types.Tool(
            name="get-fx-daily",
            description="Get daily foreign exchange rates",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_symbol": {
                        "type": "string",
                        "description": "From currency symbol (e.g., USD, EUR)"
                    },
                    "to_symbol": {
                        "type": "string",
                        "description": "To currency symbol (e.g., JPY, GBP)"
                    }
                },
                "required": ["from_symbol", "to_symbol"]
            }
        ),
        types.Tool(
            name="get-fx-weekly",
            description="Get weekly foreign exchange rates",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_symbol": {
                        "type": "string",
                        "description": "From currency symbol (e.g., USD, EUR)"
                    },
                    "to_symbol": {
                        "type": "string",
                        "description": "To currency symbol (e.g., JPY, GBP)"
                    }
                },
                "required": ["from_symbol", "to_symbol"]
            }
        ),
        types.Tool(
            name="get-fx-monthly",
            description="Get monthly foreign exchange rates",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_symbol": {
                        "type": "string",
                        "description": "From currency symbol (e.g., USD, EUR)"
                    },
                    "to_symbol": {
                        "type": "string",
                        "description": "To currency symbol (e.g., JPY, GBP)"
                    }
                },
                "required": ["from_symbol", "to_symbol"]
            }
        ),
        types.Tool(
            name="get-market-status",
            description="Get current market status (open/closed) for global markets",
            inputSchema=MARKET_STATUS_SCHEMA
        ),
        types.Tool(
            name="get-listing-status",
            description="Get a list of active or delisted US stocks and ETFs",
            inputSchema=LISTING_STATUS_SCHEMA
        ),
        types.Tool(
            name="get-etf-profile",
            description="Get key ETF metrics, holdings, and allocation by asset types and sectors",
            inputSchema=ETF_PROFILE_SCHEMA
        ),
        types.Tool(
            name="get-ipo-calendar",
            description="Get a list of IPOs expected in the next 3 months",
            inputSchema=IPO_CALENDAR_SCHEMA
        ),
        types.Tool(
            name="get-earnings-calendar",
            description="Get a list of company earnings releases expected in the next 3 months",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Optional: Symbol to filter by (e.g., IBM)"
                    },
                    "horizon": {
                        "type": "string",
                        "description": "Optional: Time horizon (3month, 6month, 12month)",
                        "enum": ["3month", "6month", "12month"],
                        "default": "3month"
                    }
                }
            }
        ),
        types.Tool(
            name="get-earnings-call-transcript",
            description="Get the earnings call transcript for a specific company and fiscal quarter",
            inputSchema=EARNINGS_CALL_TRANSCRIPT_SCHEMA
        ),
        types.Tool(
            name="get-insider-transactions",
            description="Get insider transactions (buys/sells) by company executives, directors, and major shareholders",
            inputSchema=INSIDER_TRANSACTIONS_SCHEMA
        ),
        types.Tool(
            name="get-real-gdp",
            description="Get Real Gross Domestic Product (GDP) data",
            inputSchema=ECONOMIC_INDICATOR_SCHEMA
        ),
        types.Tool(
            name="get-cpi",
            description="Get Consumer Price Index (CPI) data",
            inputSchema=ECONOMIC_INDICATOR_SCHEMA
        ),
        types.Tool(
            name="get-inflation",
            description="Get inflation rate data",
            inputSchema=ECONOMIC_INDICATOR_SCHEMA
        ),
        types.Tool(
            name="get-treasury-yield",
            description="Get Treasury yield data for different maturities",
            inputSchema=TREASURY_YIELD_SCHEMA
        ),
        types.Tool(
            name="get-income-statement",
            description="Get income statement data for a company",
            inputSchema=FUNDAMENTAL_DATA_SCHEMA
        ),
        types.Tool(
            name="get-balance-sheet",
            description="Get balance sheet data for a company",
            inputSchema=FUNDAMENTAL_DATA_SCHEMA
        ),
        types.Tool(
            name="get-cash-flow",
            description="Get cash flow data for a company",
            inputSchema=FUNDAMENTAL_DATA_SCHEMA
        ),
        types.Tool(
            name="get-earnings",
            description="Get earnings data for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., IBM, MSFT)."
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get-wti",
            description="Get West Texas Intermediate (WTI) crude oil prices",
            inputSchema=COMMODITY_DATA_SCHEMA
        ),
        types.Tool(
            name="get-brent",
            description="Get Brent crude oil prices",
            inputSchema=COMMODITY_DATA_SCHEMA
        ),
        types.Tool(
            name="get-natural-gas",
            description="Get natural gas prices",
            inputSchema=COMMODITY_DATA_SCHEMA
        ),
        types.Tool(
            name="get-cotton",
            description="Get global cotton prices",
            inputSchema=COTTON_SCHEMA
        ),
        types.Tool(
            name="get-sugar",
            description="Get global sugar prices",
            inputSchema=SUGAR_SCHEMA
        ),
        types.Tool(
            name="get-coffee",
            description="Get global coffee prices",
            inputSchema=COFFEE_SCHEMA
        ),
        types.Tool(
            name="get-all-commodities",
            description="Get global commodity price index",
            inputSchema=ALL_COMMODITIES_SCHEMA
        ),
        types.Tool(
            name="get-top-gainers-losers",
            description="Get the top gainers, losers, and most actively traded US stocks",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get-symbol-search",
            description="Search for ticker symbols across global markets",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Keywords to search for (e.g., company name, ticker symbol)"
                    }
                },
                "required": ["keywords"]
            }
        )
    ]

async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Dispatches to the appropriate handler based on the tool name.
    """
    if not arguments:
        return [types.TextContent(type="text", text="Missing arguments for the request")]
    
    # Check if API key is set
    api_key_error = validate_api_key()
    if api_key_error:
        return [types.TextContent(type="text", text=api_key_error)]
    
    # Use the handler mapping to dispatch to the appropriate handler
    handler = HANDLER_MAPPING.get(name)
    if handler:
        return await handler(arguments)
    else:
        return [types.TextContent(
            type="text", 
            text=f"Unknown tool: {name}. Please check the available tools and try again."
        )]

async def main():
    """
    Main entry point for the Alpha Vantage MCP server.
    Initializes and runs the MCP server.
    """
    # Check if API key is set
    api_key_error = validate_api_key()
    if api_key_error:
        raise ValueError("Missing ALPHA_VANTAGE_API_KEY environment variable")
    
    # Initialize the server
    server = Server("alpha_vantage_finance")
    
    # Register the handlers
    server.register_list_tools_handler(handle_list_tools)
    server.register_call_tool_handler(handle_call_tool)
    
    # Run the server
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())