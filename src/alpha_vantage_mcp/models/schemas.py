"""
Input schemas for Alpha Vantage MCP tools.

This module defines the JSON schemas for tool inputs using the JSON Schema format.
These schemas are used for validating client requests before making API calls.
"""

# Stock Quote Schema
STOCK_QUOTE_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "Stock symbol (e.g., AAPL, MSFT)"
        }
    },
    "required": ["symbol"]
}

# Company Info Schema
COMPANY_INFO_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "Stock symbol (e.g., AAPL, MSFT)"
        }
    },
    "required": ["symbol"]
}

# Crypto Exchange Rate Schema
CRYPTO_RATE_SCHEMA = {
    "type": "object",
    "properties": {
        "crypto_symbol": {
            "type": "string",
            "description": "Cryptocurrency symbol (e.g., BTC, ETH)"
        },
        "market": {
            "type": "string",
            "description": "Market currency (e.g., USD, EUR)",
            "default": "USD"
        }
    },
    "required": ["crypto_symbol"]
}

# Time Series Schema
TIME_SERIES_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "Stock symbol (e.g., AAPL, MSFT)"
        },
        "outputsize": {
            "type": "string",
            "description": "compact (latest 100 data points) or full (up to 20 years of data)",
            "enum": ["compact", "full"],
            "default": "compact"
        }
    },
    "required": ["symbol"]
}

# Weekly/Monthly Time Series Schema (no outputsize parameter)
WEEKLY_MONTHLY_TIME_SERIES_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "The stock symbol (e.g., AAPL, MSFT) for which to retrieve data."
        }
    },
    "required": ["symbol"]
}

# Intraday Time Series Schema
INTRADAY_TIME_SERIES_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "Stock symbol (e.g., IBM)"
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
    "required": ["symbol"]
}

# News Sentiment Schema
NEWS_SENTIMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "tickers": {
            "type": "string",
            "description": "Comma-separated list of ticker symbols (e.g., 'AAPL,MSFT,GOOG'). Limited to 20 symbols."
        },
        "topics": {
            "type": "string",
            "description": "Comma-separated list of topics (e.g., 'technology,earnings,ipo')"
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
    }
}

# Simple Moving Average (SMA) Schema
SMA_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "Symbol (e.g., IBM, BTC)"
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
    "required": ["symbol"]
}

# Historical Options Schema
HISTORICAL_OPTIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "Stock symbol (e.g., AAPL, MSFT)"
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
            "enum": ["strike", "expiration", "volume", "open_interest", "implied_volatility", 
                    "delta", "gamma", "theta", "vega", "rho", "last", "bid", "ask"],
            "default": "strike"
        },
        "sort_order": {
            "type": "string",
            "description": "Optional: Sort order",
            "enum": ["asc", "desc"],
            "default": "asc"
        }
    },
    "required": ["symbol"]
}

# Crypto Time Series Schema
CRYPTO_TIME_SERIES_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "Cryptocurrency symbol (e.g., BTC, ETH)"
        },
        "market": {
            "type": "string",
            "description": "Market currency (e.g., USD, EUR)",
            "default": "USD"
        }
    },
    "required": ["symbol"]
}

# Technical Indicator Schema (MACD, BBANDS, etc.)
TECHNICAL_INDICATOR_SCHEMA = {
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
        }
    },
    "required": ["symbol"]
}

# STOCHRSI Schema 
STOCHRSI_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each STOCHRSI value. Positive integers are accepted.",
            "default": 14
        },
        "series_type": {
            "type": "string", 
            "description": "Price type.",
            "enum": ["close", "open", "high", "low"],
            "default": "close"
        },
        "fastkperiod": {
            "type": "integer",
            "description": "The time period of the fastk moving average. Positive integers are accepted.",
            "default": 5
        },
        "fastdperiod": {
            "type": "integer",
            "description": "The time period of the fastd moving average. Positive integers are accepted.",
            "default": 3
        },
        "fastdmatype": {
            "type": "integer",
            "description": "Moving average type for the fastd moving average. Integers 0-8 represent different MA types.",
            "enum": [0, 1, 2, 3, 4, 5, 6, 7, 8],
            "default": 0
        }
    },
    "required": ["symbol"]
}

# ADXR Schema
ADXR_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each ADXR value. Positive integers are accepted.",
            "default": 14
        }
    },
    "required": ["symbol"]
}

# APO Schema
APO_SCHEMA = {
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
            "description": "Fast period. Positive integers are accepted.",
            "default": 12
        },
        "slowperiod": {
            "type": "integer",
            "description": "Slow period. Positive integers are accepted.",
            "default": 26
        },
        "matype": {
            "type": "integer",
            "description": "Moving average type. Integers 0-8 represent different MA types.",
            "enum": [0, 1, 2, 3, 4, 5, 6, 7, 8],
            "default": 0
        }
    },
    "required": ["symbol"]
}

# MACD Specific Schema (extends Technical Indicator Schema)
MACD_SCHEMA = {
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
    "required": ["symbol"]
}

# Market Status Schema (no parameters required)
MARKET_STATUS_SCHEMA = {
    "type": "object",
    "properties": {}
}

# Listing Status Schema
LISTING_STATUS_SCHEMA = {
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
    }
}

# ETF Profile Schema
ETF_PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "The ETF symbol (e.g., QQQ, SPY)."
        }
    },
    "required": ["symbol"]
}

# IPO Calendar Schema (no parameters required)
IPO_CALENDAR_SCHEMA = {
    "type": "object",
    "properties": {}
}

# Earnings Call Transcript Schema
EARNINGS_CALL_TRANSCRIPT_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "The stock symbol (e.g., IBM, MSFT)."
        },
        "quarter": {
            "type": "string",
            "description": "Fiscal quarter in YYYYQM format (e.g., 2024Q1). Any quarter since 2010Q1 is supported.",
            "pattern": "^\\d{4}Q[1-4]$"
        }
    },
    "required": ["symbol", "quarter"]
}

# Insider Transactions Schema
INSIDER_TRANSACTIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "The stock symbol (e.g., IBM, MSFT)."
        }
    },
    "required": ["symbol"]
}

# Economic Indicator Schema
ECONOMIC_INDICATOR_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Optional: Data interval (e.g., 'annual', 'quarterly', 'monthly')",
            "enum": ["annual", "quarterly", "monthly"],
            "default": "annual"
        }
    }
}

# Treasury Yield Schema
TREASURY_YIELD_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["daily", "weekly", "monthly"],
            "default": "monthly"
        },
        "maturity": {
            "type": "string",
            "description": "Bond maturity",
            "enum": ["3month", "2year", "5year", "7year", "10year", "30year"],
            "default": "10year"
        }
    }
}

# Fundamental Data Schema
FUNDAMENTAL_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "symbol": {
            "type": "string",
            "description": "The stock symbol (e.g., IBM, MSFT)."
        },
        "period": {
            "type": "string",
            "description": "Reporting period ('annual', 'quarterly')",
            "enum": ["annual", "quarterly"],
            "default": "annual"
        }
    },
    "required": ["symbol"]
}

# Commodity Data Schema
COMMODITY_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["daily", "weekly", "monthly"],
            "default": "monthly"
        }
    }
}

# Metal Commodity Schema (COPPER, ALUMINUM)
METAL_COMMODITY_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "quarterly", "annual"],
            "default": "monthly"
        }
    }
}

# Real GDP Per Capita Schema
REAL_GDP_PER_CAPITA_SCHEMA = {
    "type": "object",
    "properties": {}
}

# Federal Funds Rate Schema
FEDERAL_FUNDS_RATE_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["daily", "weekly", "monthly"],
            "default": "monthly"
        }
    }
}

# PPO Schema (Percentage Price Oscillator)
PPO_SCHEMA = {
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
            "description": "Fast period. Positive integers are accepted.",
            "default": 12
        },
        "slowperiod": {
            "type": "integer",
            "description": "Slow period. Positive integers are accepted.",
            "default": 26
        },
        "matype": {
            "type": "integer",
            "description": "Moving average type. Integers 0-8 represent different MA types.",
            "enum": [0, 1, 2, 3, 4, 5, 6, 7, 8],
            "default": 0
        }
    },
    "required": ["symbol"]
}

# MOM Schema (Momentum)
MOM_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate momentum. Positive integers are accepted.",
            "default": 10
        }
    },
    "required": ["symbol"]
}

# Agricultural Commodity Schema (WHEAT, CORN, etc.)
AGRICULTURAL_COMMODITY_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "quarterly", "annual"],
            "default": "monthly"
        }
    }
}

# Retail Sales Schema
RETAIL_SALES_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "annual"],
            "default": "monthly"
        }
    }
}

# BOP Schema (Balance Of Power)
BOP_SCHEMA = {
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
        }
    },
    "required": ["symbol"]
}

# CCI Schema (Commodity Channel Index)
CCI_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each CCI value. Positive integers are accepted.",
            "default": 20
        }
    },
    "required": ["symbol"]
}

# DURABLES Schema (Durable Goods Orders)
DURABLES_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "annual"],
            "default": "monthly"
        }
    }
}

# COTTON Schema
COTTON_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "quarterly", "annual"],
            "default": "monthly"
        }
    }
}

# SUGAR Schema
SUGAR_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "quarterly", "annual"],
            "default": "monthly"
        }
    }
}

# COFFEE Schema
COFFEE_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "quarterly", "annual"],
            "default": "monthly"
        }
    }
}

# ALL_COMMODITIES Schema
ALL_COMMODITIES_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "quarterly", "annual"],
            "default": "monthly"
        }
    }
}

# CMO Schema (Chande Momentum Oscillator)
CMO_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each CMO value. Positive integers are accepted.",
            "default": 14
        }
    },
    "required": ["symbol"]
}

# ROC Schema (Rate of Change)
ROC_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each ROC value. Positive integers are accepted.",
            "default": 10
        }
    },
    "required": ["symbol"]
}

# ROCR Schema (Rate of Change Ratio)
ROCR_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each ROCR value. Positive integers are accepted.",
            "default": 10
        }
    },
    "required": ["symbol"]
}

# AROON Schema (Aroon)
AROON_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each Aroon value. Positive integers are accepted.",
            "default": 14
        }
    },
    "required": ["symbol"]
}

# AROONOSC Schema (Aroon Oscillator)
AROONOSC_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each Aroon Oscillator value. Positive integers are accepted.",
            "default": 14
        }
    },
    "required": ["symbol"]
}

# UNEMPLOYMENT Schema
UNEMPLOYMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "annual"],
            "default": "monthly"
        }
    }
}

# NONFARM_PAYROLL Schema
NONFARM_PAYROLL_SCHEMA = {
    "type": "object",
    "properties": {
        "interval": {
            "type": "string",
            "description": "Data interval",
            "enum": ["monthly", "annual"],
            "default": "monthly"
        }
    }
}

# MFI Schema (Money Flow Index)
MFI_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each Money Flow Index value. Positive integers are accepted.",
            "default": 14
        }
    },
    "required": ["symbol"]
}

# TRIX Schema (Triple Exponential Moving Average)
TRIX_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate TRIX. Positive integers are accepted.",
            "default": 10
        },
        "series_type": {
            "type": "string", 
            "description": "Price type.",
            "enum": ["close", "open", "high", "low"],
            "default": "close"
        }
    },
    "required": ["symbol"]
}

# ULTOSC Schema (Ultimate Oscillator)
ULTOSC_SCHEMA = {
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
        "time_period_1": {
            "type": "integer",
            "description": "First time period for Ultimate Oscillator calculation. Positive integers are accepted.",
            "default": 7
        },
        "time_period_2": {
            "type": "integer",
            "description": "Second time period for Ultimate Oscillator calculation. Positive integers are accepted.",
            "default": 14
        },
        "time_period_3": {
            "type": "integer",
            "description": "Third time period for Ultimate Oscillator calculation. Positive integers are accepted.",
            "default": 28
        }
    },
    "required": ["symbol"]
}

# DX Schema (Directional Movement Index)
DX_SCHEMA = {
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
        "time_period": {
            "type": "integer",
            "description": "Number of data points used to calculate each DX value. Positive integers are accepted.",
            "default": 14
        }
    },
    "required": ["symbol"]
}

# Export all schemas for use in other modules
__all__ = [
    'STOCK_QUOTE_SCHEMA',
    'COMPANY_INFO_SCHEMA',
    'CRYPTO_RATE_SCHEMA',
    'TIME_SERIES_SCHEMA',
    'WEEKLY_MONTHLY_TIME_SERIES_SCHEMA',
    'INTRADAY_TIME_SERIES_SCHEMA',
    'NEWS_SENTIMENT_SCHEMA',
    'SMA_SCHEMA',
    'HISTORICAL_OPTIONS_SCHEMA',
    'CRYPTO_TIME_SERIES_SCHEMA',
    'TECHNICAL_INDICATOR_SCHEMA',
    'STOCHRSI_SCHEMA',
    'ADXR_SCHEMA',
    'APO_SCHEMA',
    'PPO_SCHEMA',
    'MOM_SCHEMA',
    'MACD_SCHEMA',
    'MARKET_STATUS_SCHEMA',
    'LISTING_STATUS_SCHEMA',
    'ETF_PROFILE_SCHEMA',
    'IPO_CALENDAR_SCHEMA',
    'EARNINGS_CALL_TRANSCRIPT_SCHEMA',
    'INSIDER_TRANSACTIONS_SCHEMA',
    'ECONOMIC_INDICATOR_SCHEMA',
    'TREASURY_YIELD_SCHEMA',
    'FUNDAMENTAL_DATA_SCHEMA',
    'COMMODITY_DATA_SCHEMA',
    'METAL_COMMODITY_SCHEMA',
    'AGRICULTURAL_COMMODITY_SCHEMA',
    'REAL_GDP_PER_CAPITA_SCHEMA',
    'FEDERAL_FUNDS_RATE_SCHEMA',
    'RETAIL_SALES_SCHEMA',
    'BOP_SCHEMA',
    'CCI_SCHEMA',
    'DURABLES_SCHEMA',
    'COTTON_SCHEMA',
    'SUGAR_SCHEMA',
    'COFFEE_SCHEMA',
    'ALL_COMMODITIES_SCHEMA',
    'CMO_SCHEMA',
    'ROC_SCHEMA',
    'ROCR_SCHEMA',
    'AROON_SCHEMA',
    'AROONOSC_SCHEMA',
    'UNEMPLOYMENT_SCHEMA',
    'NONFARM_PAYROLL_SCHEMA',
    'MFI_SCHEMA',
    'TRIX_SCHEMA',
    'ULTOSC_SCHEMA',
    'DX_SCHEMA'
]