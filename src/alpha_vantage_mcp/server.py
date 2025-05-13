from typing import Any, List, Dict, Optional
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import os

# Import functions from tools.py
from .tools import (
    make_alpha_request,
    format_quote,
    format_company_info,
    format_crypto_rate,
    format_time_series,
    format_time_series_weekly,
    format_time_series_monthly,
    format_time_series_daily_adjusted,
    format_time_series_weekly_adjusted,
    format_time_series_monthly_adjusted,
    format_market_status,
    format_listing_status,
    format_historical_options,
    format_crypto_time_series,
    format_intraday_time_series,
    format_news_sentiment,
    format_technical_indicator,
    format_symbol_search,
    format_fx_rate,
    format_fx_time_series,
    format_economic_indicator,
    format_treasury_yield,
    format_fundamental_data,
    format_commodity_data,
    format_gainers_losers,
    format_earnings_calendar,
    format_macd,
    format_bbands,
    format_etf_profile,
    format_ipo_calendar,
    format_earnings_call_transcript,
    format_insider_transactions,
    ALPHA_VANTAGE_BASE,
    API_KEY
)

if not API_KEY:
    raise ValueError("Missing ALPHA_VANTAGE_API_KEY environment variable")

server = Server("alpha_vantage_finance")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get-stock-quote",
            description="Get current stock quote information",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-symbol-search",
            description="Search for stocks, ETFs, mutual funds, or options by keywords/tickers",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Keywords to search for (e.g., Microsoft, BA, Tech)",
                    },
                },
                "required": ["keywords"],
            },
        ),
        types.Tool(
            name="get-company-info",
            description="Get detailed company information",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-crypto-exchange-rate",
            description="Get current cryptocurrency exchange rate",
            inputSchema={
                "type": "object",
                "properties": {
                    "crypto_symbol": {
                        "type": "string",
                        "description": "Cryptocurrency symbol (e.g., BTC, ETH)",
                    },
                    "market": {
                        "type": "string",
                        "description": "Market currency (e.g., USD, EUR)",
                        "default": "USD"
                    }
                },
                "required": ["crypto_symbol"],
            },
        ),
        types.Tool(
            name="get-time-series",
            description="Get daily time series data for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)",
                    },
                    "outputsize": {
                        "type": "string",
                        "description": "compact (latest 100 data points) or full (up to 20 years of data)",
                        "enum": ["compact", "full"],
                        "default": "compact"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-weekly-time-series",
            description="Get weekly time series data (date, open, high, low, close, volume) for a stock, covering 20+ years of historical data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., AAPL, MSFT) for which to retrieve weekly data.",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-daily-adjusted-time-series",
            description="Get daily adjusted time series (open, high, low, close, adjusted close, volume, dividend, split coefficient) for a stock. This is a premium Alpha Vantage endpoint.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., AAPL, MSFT).",
                    },
                    "outputsize": {
                        "type": "string",
                        "description": "'compact' (latest 100 data points) or 'full' (full-length time series).",
                        "enum": ["compact", "full"],
                        "default": "compact"
                    }
                    # 'datatype' (json/csv) is optional, defaults to json.
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-weekly-adjusted-time-series",
            description="Get weekly adjusted time series (open, high, low, close, adjusted close, volume, dividend) for a stock, covering 20+ years of historical data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., AAPL, MSFT) for which to retrieve weekly adjusted data.",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-historical-options",
            description="Get historical options chain data for a stock with sorting capabilities",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)",
                    },
                    "date": {
                        "type": "string",
                        "description": "Optional: Trading date in YYYY-MM-DD format (defaults to previous trading day, must be after 2008-01-01)",
                        "pattern": "^20[0-9]{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Optional: Number of contracts to return (default: 10, use -1 for all contracts)",
                        "default": 10,
                        "minimum": -1
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "Optional: Field to sort by",
                        "enum": [
                            "strike",
                            "expiration",
                            "volume",
                            "open_interest",
                            "implied_volatility",
                            "delta",
                            "gamma",
                            "theta",
                            "vega",
                            "rho",
                            "last",
                            "bid",
                            "ask"
                        ],
                        "default": "strike"
                    },
                    "sort_order": {
                        "type": "string",
                        "description": "Optional: Sort order",
                        "enum": ["asc", "desc"],
                        "default": "asc"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-crypto-daily",
            description="Get daily time series data for a cryptocurrency",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Cryptocurrency symbol (e.g., BTC, ETH)",
                    },
                    "market": {
                        "type": "string",
                        "description": "Market currency (e.g., USD, EUR)",
                        "default": "USD"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-crypto-weekly",
            description="Get weekly time series data for a cryptocurrency",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Cryptocurrency symbol (e.g., BTC, ETH)",
                    },
                    "market": {
                        "type": "string",
                        "description": "Market currency (e.g., USD, EUR)",
                        "default": "USD"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-crypto-monthly",
            description="Get monthly time series data for a cryptocurrency",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Cryptocurrency symbol (e.g., BTC, ETH)",
                    },
                    "market": {
                        "type": "string",
                        "description": "Market currency (e.g., USD, EUR)",
                        "default": "USD"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-intraday-time-series",
            description="Get intraday time series data (OHLCV) for a stock, covering 20+ years, including pre/post-market hours.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., IBM)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min"],
                        "default": "15min"
                    },
                    "adjusted": {
                        "type": "boolean",
                        "description": "Set to false for raw (as-traded) data, true for split/dividend-adjusted data.",
                        "default": True
                    },
                    "extended_hours": {
                        "type": "boolean",
                        "description": "Set to false to exclude pre-market and post-market data.",
                        "default": True
                    },
                    "outputsize": {
                        "type": "string",
                        "description": "compact (latest 100 data points) or full (up to 20 years of data)",
                        "enum": ["compact", "full"],
                        "default": "compact"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-news-sentiment",
            description="Get latest news and sentiment analysis for stocks and cryptocurrencies.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tickers": {
                        "type": "string",
                        "description": "Comma-separated list of ticker symbols (e.g., 'AAPL,MSFT,GOOG'). Limited to 20 symbols.",
                    },
                    "topics": {
                        "type": "string",
                        "description": "Comma-separated list of topics (e.g., 'technology,earnings,ipo')",
                    },
                    "time_from": {
                        "type": "string",
                        "description": "Time filter starting time (YYYYMMDDTHHMM format)",
                        "pattern": "^\\d{8}T\\d{4}$"
                    },
                    "time_to": {
                        "type": "string",
                        "description": "Time filter ending time (YYYYMMDDTHHMM format)",
                        "pattern": "^\\d{8}T\\d{4}$"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10, max: 1000)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 1000
                    },
                    "sort": {
                        "type": "string",
                        "description": "Sort order of the results",
                        "enum": ["LATEST", "EARLIEST", "RELEVANCE"],
                        "default": "LATEST"
                    }
                },
            },
        ),
        types.Tool(
            name="get-sma",
            description="Get Simple Moving Average (SMA) technical indicator for a symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Symbol (e.g., IBM, BTC)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
                        "default": "daily"
                    },
                    "time_period": {
                        "type": "integer",
                        "description": "Number of periods to calculate SMA over",
                        "default": 20,
                        "minimum": 1
                    },
                    "series_type": {
                        "type": "string",
                        "description": "The desired price type in the time series",
                        "enum": ["close", "open", "high", "low"],
                        "default": "close"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-ema",
            description="Get Exponential Moving Average (EMA) technical indicator for a symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Symbol (e.g., IBM, BTC)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
                        "default": "daily"
                    },
                    "time_period": {
                        "type": "integer",
                        "description": "Number of periods to calculate EMA over",
                        "default": 20,
                        "minimum": 1
                    },
                    "series_type": {
                        "type": "string",
                        "description": "The desired price type in the time series",
                        "enum": ["close", "open", "high", "low"],
                        "default": "close"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-rsi",
            description="Get Relative Strength Index (RSI) technical indicator for a symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Symbol (e.g., IBM, BTC)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
                        "default": "daily"
                    },
                    "time_period": {
                        "type": "integer",
                        "description": "Number of periods to calculate RSI over",
                        "default": 14,
                        "minimum": 1
                    },
                    "series_type": {
                        "type": "string",
                        "description": "The desired price type in the time series",
                        "enum": ["close", "open", "high", "low"],
                        "default": "close"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-bbands",
            description="Get Bollinger Bands (BBANDS) technical indicator for a symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Symbol (e.g., IBM, BTC)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
                        "default": "daily"
                    },
                    "time_period": {
                        "type": "integer",
                        "description": "Number of periods to calculate the bands over",
                        "default": 20,
                        "minimum": 1
                    },
                    "series_type": {
                        "type": "string",
                        "description": "The desired price type in the time series",
                        "enum": ["close", "open", "high", "low"],
                        "default": "close"
                    },
                    "nbdevup": {
                        "type": "number",
                        "description": "Standard deviation multiplier for upper band",
                        "default": 2
                    },
                    "nbdevdn": {
                        "type": "number",
                        "description": "Standard deviation multiplier for lower band",
                        "default": 2
                    },
                    "matype": {
                        "type": "integer",
                        "description": "Moving average type (0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3)",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 8
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-wma",
            description="Get Weighted Moving Average (WMA) technical indicator for a symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Symbol (e.g., IBM, BTC)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
                        "default": "daily"
                    },
                    "time_period": {
                        "type": "integer",
                        "description": "Number of periods to calculate WMA over",
                        "default": 20,
                        "minimum": 1
                    },
                    "series_type": {
                        "type": "string",
                        "description": "The desired price type in the time series",
                        "enum": ["close", "open", "high", "low"],
                        "default": "close"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-dema",
            description="Get Double Exponential Moving Average (DEMA) technical indicator for a symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Symbol (e.g., IBM, BTC)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
                        "default": "daily"
                    },
                    "time_period": {
                        "type": "integer",
                        "description": "Number of periods to calculate DEMA over",
                        "default": 20,
                        "minimum": 1
                    },
                    "series_type": {
                        "type": "string",
                        "description": "The desired price type in the time series",
                        "enum": ["close", "open", "high", "low"],
                        "default": "close"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-tema",
            description="Get Triple Exponential Moving Average (TEMA) technical indicator for a symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Symbol (e.g., IBM, BTC)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
                        "default": "daily"
                    },
                    "time_period": {
                        "type": "integer",
                        "description": "Number of periods to calculate TEMA over",
                        "default": 20,
                        "minimum": 1
                    },
                    "series_type": {
                        "type": "string",
                        "description": "The desired price type in the time series",
                        "enum": ["close", "open", "high", "low"],
                        "default": "close"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-market-status",
            description="Get the current market status (open/closed) of major trading venues for equities, forex, and cryptocurrencies.",
            inputSchema={
                "type": "object",
                "properties": {}  # No specific input parameters needed for this endpoint
            },
        ),
        types.Tool(
            name="get-listing-status",
            description="Get a list of active or delisted US stocks and ETFs, as of the latest trading day or a specific date.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Optional: Date in YYYY-MM-DD format (e.g., 2013-08-03). Defaults to latest trading day.",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "state": {
                        "type": "string",
                        "description": "Optional: 'active' or 'delisted'. Defaults to 'active'.",
                        "enum": ["active", "delisted"],
                        "default": "active"
                    }
                },
                # No required params, as they have defaults
            },
        ),
        types.Tool(
            name="get-monthly-time-series",
            description="Get monthly time series data (date, open, high, low, close, volume) for a stock, covering 20+ years of historical data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., AAPL, MSFT) for which to retrieve monthly data.",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-monthly-adjusted-time-series",
            description="Get monthly adjusted time series (open, high, low, close, adjusted close, volume, dividend) for a stock, covering 20+ years of historical data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., AAPL, MSFT) for which to retrieve monthly adjusted data.",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-fx-daily",
            description="Get daily foreign exchange rate time series data for a currency pair",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string",
                        "description": "From currency symbol (e.g., USD, EUR)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "To currency symbol (e.g., JPY, GBP)"
                    }
                },
                "required": ["from_currency", "to_currency"],
            },
        ),
        types.Tool(
            name="get-fx-weekly", 
            description="Get weekly foreign exchange rate time series data for a currency pair",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string",
                        "description": "From currency symbol (e.g., USD, EUR)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "To currency symbol (e.g., JPY, GBP)"
                    }
                },
                "required": ["from_currency", "to_currency"],
            },
        ),
        types.Tool(
            name="get-fx-monthly",
            description="Get monthly foreign exchange rate time series data for a currency pair",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string",
                        "description": "From currency symbol (e.g., USD, EUR)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "To currency symbol (e.g., JPY, GBP)"
                    }
                },
                "required": ["from_currency", "to_currency"],
            },
        ),
        types.Tool(
            name="get-real-gdp",
            description="Get annual US Real Gross Domestic Product (GDP) data",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {
                        "type": "string",
                        "description": "Time interval between data points",
                        "enum": ["annual", "quarterly"],
                        "default": "annual"
                    }
                }
            },
        ),
        types.Tool(
            name="get-cpi",
            description="Get monthly US Consumer Price Index (CPI) data",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="get-inflation",
            description="Get monthly US inflation data based on CPI",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="get-income-statement",
            description="Get annual income statements for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-balance-sheet",
            description="Get annual balance sheets for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-cash-flow",
            description="Get annual cash flow statements for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-earnings",
            description="Get annual and quarterly earnings data for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)"
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-wti",
            description="Get WTI (West Texas Intermediate) crude oil prices",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="get-brent",
            description="Get Brent crude oil prices",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="get-natural-gas",
            description="Get natural gas prices",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="get-top-gainers-losers",
            description="Get lists of top gainers, losers, and most active stocks in US markets for the current trading day",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="get-earnings-calendar",
            description="Get a calendar of upcoming earnings releases for a specified date range or symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Optional: Filter earnings by a specific stock symbol. Leave blank to get all upcoming earnings."
                    },
                    "horizon": {
                        "type": "string",
                        "description": "Optional: Time horizon for earnings data - 3month, 6month, 12month",
                        "enum": ["3month", "6month", "12month"],
                        "default": "3month"
                    }
                }
            },
        ),
        types.Tool(
            name="get-treasury-yield",
            description="Get U.S. Treasury yield data for a specified maturity",
            inputSchema={
                "type": "object",
                "properties": {
                    "maturity": {
                        "type": "string",
                        "description": "Treasury maturity",
                        "enum": ["3month", "2year", "5year", "7year", "10year", "30year"],
                        "default": "10year"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Optional: Data interval - daily, weekly, monthly",
                        "enum": ["daily", "weekly", "monthly"],
                        "default": "monthly"
                    }
                },
                "required": ["maturity"]
            },
        ),
        types.Tool(
            name="get-macd",
            description="Get Moving Average Convergence/Divergence (MACD) values. This is a premium Alpha Vantage endpoint.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "Stock symbol (e.g., IBM)"
                    },
                    "interval": {
                        "type": "string", 
                        "description": "Time interval between data points.",
                        "enum": ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
                        "default": "daily"
                    },
                    "series_type": {
                        "type": "string", 
                        "description": "Price type.",
                        "enum": ["close", "open", "high", "low"],
                        "default": "close"
                    },
                    "fastperiod": {
                        "type": "integer", 
                        "description": "Fast period (default 12).",
                        "default": 12
                    },
                    "slowperiod": {
                        "type": "integer", 
                        "description": "Slow period (default 26).",
                        "default": 26
                    },
                    "signalperiod": {
                        "type": "integer", 
                        "description": "Signal period (default 9).",
                        "default": 9
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-etf-profile",
            description="Get key ETF metrics, holdings, and allocation by asset types and sectors.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The ETF symbol (e.g., QQQ, SPY).",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-ipo-calendar",
            description="Get a list of IPOs expected in the next 3 months.",
            inputSchema={
                "type": "object",
                "properties": {}  # No specific input parameters needed for this endpoint
            },
        ),
        types.Tool(
            name="get-earnings-call-transcript",
            description="Get the earnings call transcript for a specific company and fiscal quarter.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., IBM, MSFT)."
                    },
                    "quarter": {
                        "type": "string",
                        "description": "Fiscal quarter in YYYYQM format (e.g., 2024Q1). Any quarter since 2010Q1 is supported.",
                        "pattern": "^\\d{4}Q[1-4]$"  # Format validation for YYYYQM
                    }
                },
                "required": ["symbol", "quarter"]
            },
        ),
        types.Tool(
            name="get-insider-transactions",
            description="Get insider transactions (buys/sells) by company executives, directors, and major shareholders.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., IBM, MSFT)."
                    }
                },
                "required": ["symbol"]
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can fetch financial data and notify clients of changes.
    """
    if not arguments:
        return [types.TextContent(type="text", text="Missing arguments for the request")]

    if name == "get-stock-quote":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]

        symbol = symbol.upper()

        async with httpx.AsyncClient() as client:
            quote_data = await make_alpha_request(
                client,
                "GLOBAL_QUOTE",
                symbol
            )

            if isinstance(quote_data, str):
                return [types.TextContent(type="text", text=f"Error: {quote_data}")]

            formatted_quote = format_quote(quote_data)
            quote_text = f"Stock quote for {symbol}:\n\n{formatted_quote}"

            return [types.TextContent(type="text", text=quote_text)]

    elif name == "get-company-info":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]

        symbol = symbol.upper()

        async with httpx.AsyncClient() as client:
            company_data = await make_alpha_request(
                client,
                "OVERVIEW",
                symbol
            )

            if isinstance(company_data, str):
                return [types.TextContent(type="text", text=f"Error: {company_data}")]

            formatted_info = format_company_info(company_data)
            info_text = f"Company information for {symbol}:\n\n{formatted_info}"

            return [types.TextContent(type="text", text=info_text)]

    elif name == "get-crypto-exchange-rate":
        crypto_symbol = arguments.get("crypto_symbol")
        if not crypto_symbol:
            return [types.TextContent(type="text", text="Missing crypto_symbol parameter")]

        market = arguments.get("market", "USD")
        crypto_symbol = crypto_symbol.upper()
        market = market.upper()

        async with httpx.AsyncClient() as client:
            crypto_data = await make_alpha_request(
                client,
                "CURRENCY_EXCHANGE_RATE",
                None,
                {
                    "from_currency": crypto_symbol,
                    "to_currency": market
                }
            )

            if isinstance(crypto_data, str):
                return [types.TextContent(type="text", text=f"Error: {crypto_data}")]

            formatted_rate = format_crypto_rate(crypto_data)
            rate_text = f"Cryptocurrency exchange rate for {crypto_symbol}/{market}:\n\n{formatted_rate}"

            return [types.TextContent(type="text", text=rate_text)]

    elif name == "get-time-series":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]

        symbol = symbol.upper()
        outputsize = arguments.get("outputsize", "compact")

        async with httpx.AsyncClient() as client:
            time_series_data = await make_alpha_request(
                client,
                "TIME_SERIES_DAILY",
                symbol,
                {"outputsize": outputsize}
            )

            if isinstance(time_series_data, str):
                return [types.TextContent(type="text", text=f"Error: {time_series_data}")]

            formatted_series = format_time_series(time_series_data)
            series_text = f"Time series data for {symbol}:\n\n{formatted_series}"

            return [types.TextContent(type="text", text=series_text)]

    elif name == "get-weekly-time-series":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments for get-weekly-time-series.")]
        
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter for get-weekly-time-series.")]

        symbol = str(symbol).upper()

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="TIME_SERIES_WEEKLY", 
                symbol=symbol,
                additional_params=None
            )

            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=f"Error: {api_response}")]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Unexpected response format from API.")]

            formatted_response = format_time_series_weekly(api_response)
            
            return [types.TextContent(type="text", text=formatted_response)]

    elif name == "get-daily-adjusted-time-series":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments for get-daily-adjusted-time-series.")]
        
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]

        symbol = str(symbol).upper()
        outputsize = arguments.get("outputsize", "compact") # Default to compact if not provided

        additional_params = {"outputsize": outputsize}

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="TIME_SERIES_DAILY_ADJUSTED", 
                symbol=symbol,
                additional_params=additional_params
            )

            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=f"Error: {api_response}")]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Unexpected response format from API.")]

            formatted_response = format_time_series_daily_adjusted(api_response)
            
            return [types.TextContent(type="text", text=formatted_response)]
            
    elif name == "get-weekly-adjusted-time-series":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments for get-weekly-adjusted-time-series.")]
        
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]

        symbol = str(symbol).upper()

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="TIME_SERIES_WEEKLY_ADJUSTED", 
                symbol=symbol,
                additional_params=None
            )

            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=f"Error: {api_response}")]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Unexpected response format from API.")]

            formatted_response = format_time_series_weekly_adjusted(api_response)
            
            return [types.TextContent(type="text", text=formatted_response)]

    elif name == "get-historical-options":
        symbol = arguments.get("symbol")
        date = arguments.get("date")
        limit = arguments.get("limit", 10)
        sort_by = arguments.get("sort_by", "strike")
        sort_order = arguments.get("sort_order", "asc")

        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]

        symbol = symbol.upper()

        async with httpx.AsyncClient() as client:
            params = {}
            if date:
                params["date"] = date

            options_data = await make_alpha_request(
                client,
                "HISTORICAL_OPTIONS",
                symbol,
                params
            )

            if isinstance(options_data, str):
                return [types.TextContent(type="text", text=f"Error: {options_data}")]

            formatted_options = format_historical_options(options_data, limit, sort_by, sort_order)
            options_text = f"Historical options data for {symbol}"
            if date:
                options_text += f" on {date}"
            options_text += f":\n\n{formatted_options}"

            return [types.TextContent(type="text", text=options_text)]
            
    elif name == "get-crypto-daily":
        symbol = arguments.get("symbol")
        market = arguments.get("market", "USD")
        
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]

        symbol = symbol.upper()
        market = market.upper()

        async with httpx.AsyncClient() as client:
            crypto_data = await make_alpha_request(
                client,
                "DIGITAL_CURRENCY_DAILY",
                symbol,
                {"market": market}
            )

            if isinstance(crypto_data, str):
                return [types.TextContent(type="text", text=f"Error: {crypto_data}")]

            formatted_data = format_crypto_time_series(crypto_data, "daily")
            data_text = f"Daily cryptocurrency time series for {symbol} in {market}:\n\n{formatted_data}"

            return [types.TextContent(type="text", text=data_text)]
            
    elif name == "get-crypto-weekly":
        symbol = arguments.get("symbol")
        market = arguments.get("market", "USD")
        
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]

        symbol = symbol.upper()
        market = market.upper()

        async with httpx.AsyncClient() as client:
            crypto_data = await make_alpha_request(
                client,
                "DIGITAL_CURRENCY_WEEKLY",
                symbol,
                {"market": market}
            )

            if isinstance(crypto_data, str):
                return [types.TextContent(type="text", text=f"Error: {crypto_data}")]

            formatted_data = format_crypto_time_series(crypto_data, "weekly")
            data_text = f"Weekly cryptocurrency time series for {symbol} in {market}:\n\n{formatted_data}"

            return [types.TextContent(type="text", text=data_text)]
            
    elif name == "get-crypto-monthly":
        symbol = arguments.get("symbol")
        market = arguments.get("market", "USD")
        
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]

        symbol = symbol.upper()
        market = market.upper()

        async with httpx.AsyncClient() as client:
            crypto_data = await make_alpha_request(
                client,
                "DIGITAL_CURRENCY_MONTHLY",
                symbol,
                {"market": market}
            )

            if isinstance(crypto_data, str):
                return [types.TextContent(type="text", text=f"Error: {crypto_data}")]

            formatted_data = format_crypto_time_series(crypto_data, "monthly")
            data_text = f"Monthly cryptocurrency time series for {symbol} in {market}:\n\n{formatted_data}"

            return [types.TextContent(type="text", text=data_text)]

    elif name == "get-intraday-time-series":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        symbol = symbol.upper()
        interval = arguments.get("interval", "15min")
        adjusted = "true" if arguments.get("adjusted", True) else "false"
        extended_hours = "true" if arguments.get("extended_hours", True) else "false"
        outputsize = arguments.get("outputsize", "compact")
        
        async with httpx.AsyncClient() as client:
            intraday_data = await make_alpha_request(
                client,
                "TIME_SERIES_INTRADAY",
                symbol,
                {
                    "interval": interval,
                    "outputsize": outputsize,
                    "adjusted": adjusted,
                    "extended_hours": extended_hours
                }
            )
            
            if isinstance(intraday_data, str):
                return [types.TextContent(type="text", text=f"Error: {intraday_data}")]
                
            formatted_intraday = format_intraday_time_series(intraday_data)
            intraday_text = f"Intraday time series data for {symbol} ({interval}):\n\n{formatted_intraday}"
            
            return [types.TextContent(type="text", text=intraday_text)]
    
    elif name == "get-news-sentiment":
        params = {}
        
        # Add optional parameters if provided
        if tickers := arguments.get("tickers"):
            params["tickers"] = tickers
            
        if topics := arguments.get("topics"):
            params["topics"] = topics
            
        if time_from := arguments.get("time_from"):
            params["time_from"] = time_from
            
        if time_to := arguments.get("time_to"):
            params["time_to"] = time_to
            
        if limit := arguments.get("limit"):
            params["limit"] = str(limit)
            
        if sort := arguments.get("sort"):
            params["sort"] = sort
            
        if not params:
            return [types.TextContent(type="text", text="At least one of these parameters is required: tickers, topics, time_from, time_to")]
            
        async with httpx.AsyncClient() as client:
            news_data = await make_alpha_request(
                client,
                "NEWS_SENTIMENT",
                None,
                params
            )
            
            if isinstance(news_data, str):
                return [types.TextContent(type="text", text=f"Error: {news_data}")]
                
            formatted_news = format_news_sentiment(news_data)
            news_text = f"News sentiment analysis:\n\n{formatted_news}"
            
            return [types.TextContent(type="text", text=news_text)]
    
    elif name == "get-sma":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        symbol = symbol.upper()
        interval = arguments.get("interval", "daily")
        time_period = arguments.get("time_period", 20)
        series_type = arguments.get("series_type", "close")
        
        async with httpx.AsyncClient() as client:
            sma_data = await make_alpha_request(
                client,
                "SMA",
                symbol,
                {
                    "interval": interval,
                    "time_period": time_period,
                    "series_type": series_type
                }
            )
            
            if isinstance(sma_data, str):
                return [types.TextContent(type="text", text=f"Error: {sma_data}")]
                
            formatted_sma = format_technical_indicator(sma_data, "SMA")
            sma_text = f"Simple Moving Average (SMA) for {symbol}:\n\n{formatted_sma}"
            
            return [types.TextContent(type="text", text=sma_text)]
            
    elif name == "get-ema":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        symbol = symbol.upper()
        interval = arguments.get("interval", "daily")
        time_period = arguments.get("time_period", 20)
        series_type = arguments.get("series_type", "close")
        
        async with httpx.AsyncClient() as client:
            ema_data = await make_alpha_request(
                client,
                "EMA",
                symbol,
                {
                    "interval": interval,
                    "time_period": time_period,
                    "series_type": series_type
                }
            )
            
            if isinstance(ema_data, str):
                return [types.TextContent(type="text", text=f"Error: {ema_data}")]
                
            formatted_ema = format_technical_indicator(ema_data, "EMA")
            ema_text = f"Exponential Moving Average (EMA) for {symbol}:\n\n{formatted_ema}"
            
            return [types.TextContent(type="text", text=ema_text)]
            
    elif name == "get-rsi":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        symbol = symbol.upper()
        interval = arguments.get("interval", "daily")
        time_period = arguments.get("time_period", 14) # Default for RSI is typically 14
        series_type = arguments.get("series_type", "close")
        
        async with httpx.AsyncClient() as client:
            rsi_data = await make_alpha_request(
                client,
                "RSI",
                symbol,
                {
                    "interval": interval,
                    "time_period": time_period,
                    "series_type": series_type
                }
            )
            
            if isinstance(rsi_data, str):
                return [types.TextContent(type="text", text=f"Error: {rsi_data}")]
                
            formatted_rsi = format_technical_indicator(rsi_data, "RSI")
            rsi_text = f"Relative Strength Index (RSI) for {symbol}:\n\n{formatted_rsi}"
            
            return [types.TextContent(type="text", text=rsi_text)]
            
    elif name == "get-bbands":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        symbol = symbol.upper()
        interval = arguments.get("interval", "daily")
        time_period = arguments.get("time_period", 20)
        series_type = arguments.get("series_type", "close")
        nbdevup = arguments.get("nbdevup", 2)
        nbdevdn = arguments.get("nbdevdn", 2)
        matype = arguments.get("matype", 0)
        
        async with httpx.AsyncClient() as client:
            bbands_data = await make_alpha_request(
                client,
                "BBANDS",
                symbol,
                {
                    "interval": interval,
                    "time_period": time_period,
                    "series_type": series_type,
                    "nbdevup": nbdevup,
                    "nbdevdn": nbdevdn,
                    "matype": matype
                }
            )
            
            if isinstance(bbands_data, str):
                return [types.TextContent(type="text", text=f"Error: {bbands_data}")]
                
            formatted_bbands = format_bbands(bbands_data)
            bbands_text = f"Bollinger Bands (BBANDS) for {symbol}:\n\n{formatted_bbands}"
            
            return [types.TextContent(type="text", text=bbands_text)]
    
    elif name == "get-wma":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        symbol = symbol.upper()
        interval = arguments.get("interval", "daily")
        time_period = arguments.get("time_period", 20)
        series_type = arguments.get("series_type", "close")
        
        async with httpx.AsyncClient() as client:
            wma_data = await make_alpha_request(
                client,
                "WMA",
                symbol,
                {
                    "interval": interval,
                    "time_period": time_period,
                    "series_type": series_type
                }
            )
            
            if isinstance(wma_data, str):
                return [types.TextContent(type="text", text=f"Error: {wma_data}")]
                
            formatted_wma = format_technical_indicator(wma_data, "WMA")
            wma_text = f"Weighted Moving Average (WMA) for {symbol}:\n\n{formatted_wma}"
            
            return [types.TextContent(type="text", text=wma_text)]
    
    elif name == "get-dema":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        symbol = symbol.upper()
        interval = arguments.get("interval", "daily")
        time_period = arguments.get("time_period", 20)
        series_type = arguments.get("series_type", "close")
        
        async with httpx.AsyncClient() as client:
            dema_data = await make_alpha_request(
                client,
                "DEMA",
                symbol,
                {
                    "interval": interval,
                    "time_period": time_period,
                    "series_type": series_type
                }
            )
            
            if isinstance(dema_data, str):
                return [types.TextContent(type="text", text=f"Error: {dema_data}")]
                
            formatted_dema = format_technical_indicator(dema_data, "DEMA")
            dema_text = f"Double Exponential Moving Average (DEMA) for {symbol}:\n\n{formatted_dema}"
            
            return [types.TextContent(type="text", text=dema_text)]
    
    elif name == "get-tema":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        symbol = symbol.upper()
        interval = arguments.get("interval", "daily")
        time_period = arguments.get("time_period", 20)
        series_type = arguments.get("series_type", "close")
        
        async with httpx.AsyncClient() as client:
            tema_data = await make_alpha_request(
                client,
                "TEMA",
                symbol,
                {
                    "interval": interval,
                    "time_period": time_period,
                    "series_type": series_type
                }
            )
            
            if isinstance(tema_data, str):
                return [types.TextContent(type="text", text=f"Error: {tema_data}")]
                
            formatted_tema = format_technical_indicator(tema_data, "TEMA")
            tema_text = f"Triple Exponential Moving Average (TEMA) for {symbol}:\n\n{formatted_tema}"
            
            return [types.TextContent(type="text", text=tema_text)]
            
    elif name == "get-market-status":
        # No specific parameters needed for this endpoint
        async with httpx.AsyncClient() as client:
            market_status_data = await make_alpha_request(
                client,
                "MARKET_STATUS",
                None,  # No symbol required
                None   # No additional parameters
            )
            
            if isinstance(market_status_data, str):
                return [types.TextContent(type="text", text=f"Error: {market_status_data}")]
                
            if not isinstance(market_status_data, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
                
            formatted_status = format_market_status(market_status_data)
            
            return [types.TextContent(type="text", text=formatted_status)]
            
    elif name == "get-listing-status":
        # Get parameters or use defaults
        date_param = None if not arguments else arguments.get("date")
        state_param = "active" if not arguments else arguments.get("state", "active")

        additional_params = {}
        if date_param:
            additional_params["date"] = date_param
        if state_param:  # Always pass state, even if default
            additional_params["state"] = state_param

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="LISTING_STATUS",
                symbol=None,  # No symbol for this endpoint
                additional_params=additional_params,
                expected_datatype="csv"  # Tell make_alpha_request to expect CSV text
            )

            if not isinstance(api_response, str):
                # If it's not a string, it's an unexpected response
                return [types.TextContent(type="text", text=f"Error: Unexpected response format - {str(api_response)}")]
            
            # Check if the string response itself indicates an API error
            if api_response.startswith("Alpha Vantage API error:") or \
               api_response.startswith("Alpha Vantage API information:") or \
               api_response.startswith("Alpha Vantage API Note:") or \
               api_response.startswith("Expected CSV response") or \
               api_response.startswith("HTTP error occurred:") or \
               api_response.startswith("Request timed out") or \
               api_response.startswith("Failed to connect") or \
               api_response.startswith("Unexpected error occurred:"):
                return [types.TextContent(type="text", text=api_response)]

            formatted_response = format_listing_status(api_response, state_param)
            return [types.TextContent(type="text", text=formatted_response)]
            
    elif name == "get-symbol-search":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        keywords = arguments.get("keywords")
        if not keywords:
            return [types.TextContent(type="text", text="Error: Missing 'keywords' parameter.")]
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="SYMBOL_SEARCH",
                symbol=None,
                additional_params={"keywords": keywords}
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_symbol_search(api_response)
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-monthly-time-series":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments for get-monthly-time-series.")]
        
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter for get-monthly-time-series.")]

        symbol = str(symbol).upper()

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="TIME_SERIES_MONTHLY", 
                symbol=symbol,
                additional_params=None
            )

            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=f"Error: {api_response}")]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Unexpected response format from API.")]

            formatted_response = format_time_series_monthly(api_response)
            
            return [types.TextContent(type="text", text=formatted_response)]
    
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
    
    elif name == "get-fx-daily":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        from_currency = arguments.get("from_currency")
        to_currency = arguments.get("to_currency")
        
        if not from_currency or not to_currency:
            return [types.TextContent(type="text", text="Error: Both 'from_currency' and 'to_currency' parameters are required.")]
        
        from_currency = str(from_currency).upper()
        to_currency = str(to_currency).upper()
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="FX_DAILY",
                symbol=None,
                additional_params={
                    "from_symbol": from_currency,
                    "to_symbol": to_currency
                }
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_fx_time_series(api_response, "daily")
            return [types.TextContent(type="text", text=f"Daily Foreign Exchange Rate: {from_currency}/{to_currency}\n\n{formatted_response}")]
    
    elif name == "get-fx-weekly":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        from_currency = arguments.get("from_currency")
        to_currency = arguments.get("to_currency")
        
        if not from_currency or not to_currency:
            return [types.TextContent(type="text", text="Error: Both 'from_currency' and 'to_currency' parameters are required.")]
        
        from_currency = str(from_currency).upper()
        to_currency = str(to_currency).upper()
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="FX_WEEKLY",
                symbol=None,
                additional_params={
                    "from_symbol": from_currency,
                    "to_symbol": to_currency
                }
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_fx_time_series(api_response, "weekly")
            return [types.TextContent(type="text", text=f"Weekly Foreign Exchange Rate: {from_currency}/{to_currency}\n\n{formatted_response}")]
    
    elif name == "get-fx-monthly":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        from_currency = arguments.get("from_currency")
        to_currency = arguments.get("to_currency")
        
        if not from_currency or not to_currency:
            return [types.TextContent(type="text", text="Error: Both 'from_currency' and 'to_currency' parameters are required.")]
        
        from_currency = str(from_currency).upper()
        to_currency = str(to_currency).upper()
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="FX_MONTHLY",
                symbol=None,
                additional_params={
                    "from_symbol": from_currency,
                    "to_symbol": to_currency
                }
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_fx_time_series(api_response, "monthly")
            return [types.TextContent(type="text", text=f"Monthly Foreign Exchange Rate: {from_currency}/{to_currency}\n\n{formatted_response}")]
            
    elif name == "get-real-gdp":
        interval = "annual"
        if arguments:
            interval = arguments.get("interval", "annual")
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="REAL_GDP",
                symbol=None,
                additional_params={"interval": interval}
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_economic_indicator(api_response, "REAL_GDP")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-cpi":
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="CPI",
                symbol=None,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_economic_indicator(api_response, "CPI")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-inflation":
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="INFLATION",
                symbol=None,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_economic_indicator(api_response, "INFLATION")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-income-statement":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]
        
        symbol = str(symbol).upper()
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="INCOME_STATEMENT",
                symbol=symbol,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_fundamental_data(api_response, "INCOME_STATEMENT")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-balance-sheet":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]
        
        symbol = str(symbol).upper()
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="BALANCE_SHEET",
                symbol=symbol,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_fundamental_data(api_response, "BALANCE_SHEET")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-cash-flow":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]
        
        symbol = str(symbol).upper()
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="CASH_FLOW",
                symbol=symbol,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_fundamental_data(api_response, "CASH_FLOW")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-earnings":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]
        
        symbol = str(symbol).upper()
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="EARNINGS",
                symbol=symbol,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_fundamental_data(api_response, "EARNINGS")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-wti":
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="WTI",
                symbol=None,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_commodity_data(api_response, "WTI")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-brent":
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="BRENT",
                symbol=None,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_commodity_data(api_response, "BRENT")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-natural-gas":
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="NATURAL_GAS",
                symbol=None,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_commodity_data(api_response, "NATURAL_GAS")
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-top-gainers-losers":
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="TOP_GAINERS_LOSERS",
                symbol=None,
                additional_params=None
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_gainers_losers(api_response)
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-earnings-calendar":
        # Get parameters or use defaults
        symbol = arguments.get("symbol") if arguments else None
        horizon = arguments.get("horizon", "3month") if arguments else "3month"
        
        additional_params = {}
        if symbol:
            additional_params["symbol"] = symbol
        if horizon:
            additional_params["horizon"] = horizon
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="EARNINGS_CALENDAR",
                symbol=None, # No symbol parameter in the URL path
                additional_params=additional_params,
                expected_datatype="csv" # Earnings calendar returns CSV data
            )
            
            if not isinstance(api_response, str): 
                # If it's not a string, it's an unexpected response type
                return [types.TextContent(type="text", text=f"Error: Unexpected response format - {str(api_response)}")]
            
            # Check if the string response indicates an API error
            if api_response.startswith("Alpha Vantage API error:") or \
               api_response.startswith("Alpha Vantage API information:") or \
               api_response.startswith("Alpha Vantage API Note:") or \
               api_response.startswith("Expected CSV response") or \
               api_response.startswith("HTTP error occurred:") or \
               api_response.startswith("Request timed out") or \
               api_response.startswith("Failed to connect") or \
               api_response.startswith("Unexpected error occurred:"):
                return [types.TextContent(type="text", text=api_response)]
            
            formatted_response = format_earnings_calendar(api_response)
            return [types.TextContent(type="text", text=formatted_response)]
            
    elif name == "get-treasury-yield":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
        
        maturity = arguments.get("maturity", "10year")
        interval = arguments.get("interval", "monthly")
        
        if not maturity:
            return [types.TextContent(type="text", text="Error: Missing required 'maturity' parameter.")]
            
        additional_params = {
            "interval": interval,
            "maturity": maturity
        }
        
        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="TREASURY_YIELD",
                symbol=None, # No symbol for this endpoint
                additional_params=additional_params
            )
            
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
            
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
            
            formatted_response = format_treasury_yield(api_response, maturity)
            return [types.TextContent(type="text", text=formatted_response)]
            
    elif name == "get-macd":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments.")]
           
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing required parameter 'symbol'.")]

        symbol = str(symbol).upper()
        interval = arguments.get("interval", "daily")
        series_type = arguments.get("series_type", "close")
        fastperiod = arguments.get("fastperiod", 12)
        slowperiod = arguments.get("slowperiod", 26)
        signalperiod = arguments.get("signalperiod", 9)
           
        # Ensure parameters are strings for the request
        additional_params = {
            "interval": interval,
            "series_type": series_type,
            "fastperiod": str(fastperiod),
            "slowperiod": str(slowperiod),
            "signalperiod": str(signalperiod)
        }

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="MACD",
                symbol=symbol,
                additional_params=additional_params
            )
               
            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=api_response)]
                   
            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Invalid API response format.")]
                   
            formatted_response = format_macd(api_response)
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-etf-profile":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments for get-etf-profile.")]

        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]

        symbol = str(symbol).upper()

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="ETF_PROFILE",
                symbol=symbol,
                additional_params=None
            )

            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=f"Error: {api_response}")]

            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Unexpected response format from API.")]

            formatted_response = format_etf_profile(api_response)
            response_text = f"ETF Profile for {symbol}:\n\n{formatted_response}"
            return [types.TextContent(type="text", text=response_text)]
            
    elif name == "get-ipo-calendar":
        # This endpoint takes no specific arguments other than the API key
        # which is handled by make_alpha_request.

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="IPO_CALENDAR",  # Exact function name from Alpha Vantage API
                symbol=None,             # No symbol for this endpoint
                additional_params=None,  # No additional params for this endpoint
                expected_datatype="csv"  # This endpoint returns CSV data
            )

            if not isinstance(api_response, str):
                # Check if it's an error dict that make_alpha_request might return
                # for non-CSV errors before expecting CSV.
                if isinstance(api_response, dict) and ("Error Message" in api_response or "Information" in api_response or "Note" in api_response):
                     return [types.TextContent(type="text", text=f"API Response: {str(api_response)}")]
                return [types.TextContent(type="text", text=f"Error: Unexpected response format - {str(api_response)}")]

            # The make_alpha_request function might return error strings directly
            if api_response.startswith("Alpha Vantage API error:") or \
               api_response.startswith("HTTP error occurred:") or \
               api_response.startswith("Request timed out:") or \
               api_response.startswith("Failed to connect:") or \
               api_response.startswith("Unexpected error occurred:"):
                return [types.TextContent(type="text", text=api_response)]

            # If it seems like CSV but could still be an informational message not caught as JSON
            if "Error Message" in api_response or "Information" in api_response or "Note" in api_response: # Basic check for error keywords in CSV text
                 if len(api_response.splitlines()) < 3: # Heuristic: error messages are usually short
                    return [types.TextContent(type="text", text=f"API Info: {api_response}")]


            formatted_response = format_ipo_calendar(api_response)
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-earnings-call-transcript":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments for get-earnings-call-transcript.")]

        symbol = arguments.get("symbol")
        quarter = arguments.get("quarter")
        
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]
        if not quarter:
            return [types.TextContent(type="text", text="Error: Missing 'quarter' parameter.")]

        # Validate the quarter format
        import re
        if not re.match(r"^\d{4}Q[1-4]$", quarter):
            return [types.TextContent(type="text", text="Error: Invalid 'quarter' format. It should be in YYYYQM format (e.g., 2024Q1).")]

        symbol = str(symbol).upper()

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="EARNINGS_CALL_TRANSCRIPT",
                symbol=symbol,
                additional_params={"quarter": quarter}
            )

            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=f"Error: {api_response}")]

            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Unexpected response format from API.")]

            formatted_response = format_earnings_call_transcript(api_response)
            return [types.TextContent(type="text", text=formatted_response)]
    
    elif name == "get-insider-transactions":
        if not arguments:
            return [types.TextContent(type="text", text="Error: Missing arguments for get-insider-transactions.")]

        symbol = arguments.get("symbol")
        
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' parameter.")]

        symbol = str(symbol).upper()

        async with httpx.AsyncClient() as client:
            api_response = await make_alpha_request(
                client,
                function="INSIDER_TRANSACTIONS",
                symbol=symbol,
                additional_params=None
            )

            if isinstance(api_response, str):
                return [types.TextContent(type="text", text=f"Error: {api_response}")]

            if not isinstance(api_response, dict):
                return [types.TextContent(type="text", text="Error: Unexpected response format from API.")]

            formatted_response = format_insider_transactions(api_response)
            return [types.TextContent(type="text", text=formatted_response)]
        
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="alpha_vantage_finance",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

# This is needed if you'd like to connect to a custom client
if __name__ == "__main__":
    asyncio.run(main())
