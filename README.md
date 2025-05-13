# Alpha Vantage MCP Server
[![smithery badge](https://smithery.ai/badge/@berlinbra/alpha-vantage-mcp)](https://smithery.ai/server/@berlinbra/alpha-vantage-mcp)

A Model Context Protocol (MCP) server that provides real-time access to financial market data through the free [Alpha Vantage API](https://www.alphavantage.co/documentation/). This server implements a standardized interface for retrieving stock quotes and company information.

<a href="https://glama.ai/mcp/servers/0wues5td08"><img width="380" height="200" src="https://glama.ai/mcp/servers/0wues5td08/badge" alt="AlphaVantage-MCP MCP server" /></a>

# Features

- Real-time stock quotes with price, volume, and change data
- Detailed company information including sector, industry, and market cap
- Real-time cryptocurrency exchange rates with bid/ask prices
- Intraday, daily, weekly, and monthly time series data
- Technical indicators (SMA) for investment analysis
- News sentiment analysis for stocks and cryptocurrencies
- Historical options chain data with advanced filtering and sorting
- Built-in error handling and rate limit management

## Installation

### Using Claude Desktop

#### Installing via Docker

- Clone the repository and build a local image to be utilized by your Claude desktop client

```sh
cd alpha-vantage-mcp
docker build -t mcp/alpha-vantage .
```

- Change your `claude_desktop_config.json` to match the following, replacing `REPLACE_API_KEY` with your actual key:

 > `claude_desktop_config.json` path
 >
 > - On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
 > - On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "alphavantage": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "-e",
        "ALPHA_VANTAGE_API_KEY",
        "mcp/alpha-vantage"
      ],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "REPLACE_API_KEY"
      }
    }
  }
}
```

#### Installing via Smithery

To install Alpha Vantage MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@berlinbra/alpha-vantage-mcp):

```bash
npx -y @smithery/cli install @berlinbra/alpha-vantage-mcp --client claude
```

<summary> <h3> Development/Unpublished Servers Configuration <h3> </summary>

<details>

```json
{
 "mcpServers": {
  "alpha-vantage-mcp": {
   "args": [
    "--directory",
    "/Users/{INSERT_USER}/YOUR/PATH/TO/alpha-vantage-mcp",
    "run",
    "alpha-vantage-mcp"
   ],
   "command": "uv",
   "env": {
    "ALPHA_VANTAGE_API_KEY": "<insert api key>"
   }
  }
 }
}
```
        
</details>

#### Install packages

```
uv install -e .
```

#### Running

After connecting Claude client with the MCP tool via json file and installing the packages, Claude should see the server's mcp tools:

You can run the sever yourself via:
In alpha-vantage-mcp repo: 
```
uv run src/alpha_vantage_mcp/server.py
```

with inspector
```
* npx @modelcontextprotocol/inspector uv --directory /Users/{INSERT_USER}/YOUR/PATH/TO/alpha-vantage-mcp run src/alpha_vantage_mcp/server.py `
```

## Available Tools

The server implements the following tools:
- `get-stock-quote`: Get the latest stock quote for a specific company
- `get-company-info`: Get stock-related information for a specific company
- `get-crypto-exchange-rate`: Get current cryptocurrency exchange rates
- `get-time-series`: Get historical daily price data for a stock
- `get-weekly-time-series`: Get historical weekly price data for a stock
- `get-weekly-adjusted-time-series`: Get historical weekly adjusted price data with dividends
- `get-daily-adjusted-time-series`: Get historical daily adjusted price data with dividends and splits
- `get-intraday-time-series`: Get intraday price data (minutes) for a stock
- `get-news-sentiment`: Get news and sentiment analysis for stocks and crypto
- `get-sma`: Get Simple Moving Average technical indicator data
- `get-macd`: Get Moving Average Convergence/Divergence (MACD) indicator data
- `get-historical-options`: Get historical options chain data with advanced filtering and sorting
- `get-crypto-daily`: Get daily time series data for a cryptocurrency
- `get-crypto-weekly`: Get weekly time series data for a cryptocurrency
- `get-crypto-monthly`: Get monthly time series data for a cryptocurrency
- `get-market-status`: Get current market status (open/closed) for global markets
- `get-listing-status`: Get a list of active or delisted US stocks and ETFs
- `get-etf-profile`: Get key ETF metrics, holdings, and allocation by asset types and sectors
- `get-ipo-calendar`: Get a list of IPOs expected in the next 3 months
- `get-earnings-call-transcript`: Get the earnings call transcript for a specific company and fiscal quarter

### get-stock-quote

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "Stock symbol (e.g., AAPL, MSFT)"
    }
}
```

**Example Response:**
```
Stock quote for AAPL:

Price: $198.50
Change: $2.50 (+1.25%)
Volume: 58942301
High: $199.62
Low: $197.20
```

### get-company-info

Retrieves detailed company information for a given symbol.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "Stock symbol (e.g., AAPL, MSFT)"
    }
}
```

**Example Response:**
```
Company information for AAPL:

Name: Apple Inc
Sector: Technology
Industry: Consumer Electronics
Market Cap: $3000000000000
Description: Apple Inc. designs, manufactures, and markets smartphones...
Exchange: NASDAQ
Currency: USD
```

### get-crypto-exchange-rate

Retrieves real-time cryptocurrency exchange rates with additional market data.

**Input Schema:**
```json
{
    "crypto_symbol": {
        "type": "string",
        "description": "Cryptocurrency symbol (e.g., BTC, ETH)"
    },
    "market": {
        "type": "string",
        "description": "Market currency (e.g., USD, EUR)",
        "default": "USD"
    }
}
```

**Example Response:**
```
Cryptocurrency exchange rate for BTC/USD:

From: Bitcoin (BTC)
To: United States Dollar (USD)
Exchange Rate: 43521.45000
Last Updated: 2024-12-17 19:45:00 UTC
Bid Price: 43521.00000
Ask Price: 43522.00000
```

### get-time-series

Retrieves daily time series (OHLCV) data.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "Stock symbol (e.g., AAPL, MSFT)"
    },
    "outputsize": {
        "type": "string",
        "description": "compact (latest 100 data points) or full (up to 20 years of data)",
        "default": "compact"
    }
}
```
**Example Response:**
```
Time Series Data for AAPL (Last Refreshed: 2024-12-17 16:00:00):

Date: 2024-12-16
Open: $195.09
High: $197.68
Low: $194.83
Close: $197.57
Volume: 55,751,011
```

### get-weekly-time-series

Retrieves weekly time series (date, open, high, low, close, volume) data for a stock, covering 20+ years of historical data.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "The stock symbol (e.g., AAPL, MSFT) for which to retrieve weekly data."
    }
}
```

**Example Response:**
```
Weekly Time Series for AAPL
Last Refreshed: 2023-12-15 (Timezone: US/Eastern)
---
Date: 2023-12-15
  Open: $195.09
  High: $197.68
  Low: $194.83
  Close: $197.57
  Volume: 55,751,011
---
Date: 2023-12-08
  Open: $190.33
  High: $195.99
  Low: $188.57
  Close: $195.71
  Volume: 53,829,420
---
Date: 2023-12-01
  Open: $189.52
  High: $191.56
  Low: $187.04
  Close: $189.99
  Volume: 60,423,780
---
Date: 2023-11-24
  Open: $191.41
  High: $192.93
  Low: $188.97
  Close: $189.79
  Volume: 48,198,420
---
Date: 2023-11-17
  Open: $187.36
  High: $192.65
  Low: $187.04
  Close: $191.31
  Volume: 62,321,850
---

(Showing 5 of 1304 data points)
```

### get-daily-adjusted-time-series

Retrieves daily time series (date, open, high, low, close, adjusted close, volume, dividend amount, and split coefficient values) of the global equity specified, covering 20+ years of historical data. 
**Note: This is a premium Alpha Vantage API endpoint and may require a paid API key for full access.**

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "The stock symbol (e.g., AAPL, MSFT)."
    },
    "outputsize": {
        "type": "string",
        "description": "'compact' (latest 100 data points) or 'full' (full-length time series).",
        "enum": ["compact", "full"],
        "default": "compact"
    }
}
```

**Example Response (for symbol: IBM, assuming premium access):**
```
Daily Adjusted Time Series for IBM
Last Refreshed: 2023-12-15 (Timezone: US/Eastern)
---
Date: 2023-12-15
  Open: $170.10
  High: $172.50
  Low: $169.80
  Close: $172.00
  Adjusted Close: $172.00
  Volume: 23456789
  Dividend Amount: $0.0000
  Split Coefficient: 1.0
---
Date: 2023-12-14
  Open: $168.00
  High: $170.50
  Low: $167.50
  Close: $170.00
  Adjusted Close: $170.00
  Volume: 20101010
  Dividend Amount: $0.0000
  Split Coefficient: 1.0
---
Date: 2023-12-13
  Open: $165.50
  High: $168.20
  Low: $165.00
  Close: $167.90
  Adjusted Close: $167.90
  Volume: 18765432
  Dividend Amount: $0.0000
  Split Coefficient: 1.0
---
Date: 2023-12-12
  Open: $164.30
  High: $166.40
  Low: $163.90
  Close: $165.60
  Adjusted Close: $165.60
  Volume: 17654321
  Dividend Amount: $0.0000
  Split Coefficient: 1.0
---
Date: 2023-12-11
  Open: $166.00
  High: $166.80
  Low: $163.50
  Close: $164.20
  Adjusted Close: $164.20
  Volume: 19876543
  Dividend Amount: $1.6500
  Split Coefficient: 1.0
---

(Showing 5 of 100 data points)
```

### get-intraday-time-series

Retrieves intraday time series (OHLCV) data in intervals ranging from 1 to 60 minutes.

**Input Schema:**
```json
{
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
        "default": true
    },
    "extended_hours": {
        "type": "boolean",
        "description": "Set to false to exclude pre-market and post-market data.",
        "default": true
    },
    "outputsize": {
        "type": "string",
        "description": "compact (latest 100 data points) or full (up to 20 years of data)",
        "enum": ["compact", "full"],
        "default": "compact"
    }
}
```

**Example Response:**
```
Intraday time series data for MSFT (15min):

Intraday Time Series for MSFT (Interval: 15min)
Last Refreshed: 2024-06-17 16:00:00 US/Eastern
Output Size: compact

Time: 2024-06-17 16:00:00
Open: $425.50
High: $426.75
Low: $425.20
Close: $426.40
Volume: 1432856
---

Time: 2024-06-17 15:45:00
Open: $425.10
High: $425.65
Low: $424.85
Close: $425.50
Volume: 1256741
---

Time: 2024-06-17 15:30:00
Open: $424.75
High: $425.25
Low: $424.60
Close: $425.10
Volume: 985623
---
```

### get-news-sentiment

Retrieves news articles and sentiment analysis for specific tickers or topics.

**Input Schema:**
```json
{
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
```

**Example Response:**
```
News sentiment analysis:

News Sentiment Analysis
Sentiment Score Definition: The sentiment score ranges from -1.0 (most bearish) to 1.0 (most bullish)
Relevance Score Definition: The relevance score ranges from 0 to 1, with 1 indicating highest relevance

News #1: Apple Announces New AI Features at WWDC 2024
URL: https://example.com/news/apple-ai-features
Published: 20240617T1430
Authors: Jane Smith, John Doe
Summary: Apple unveiled a suite of new AI features coming to iOS 18 and macOS 15...
Overall Sentiment: Bullish (Score: 0.75)

Ticker Sentiments:
  AAPL: Bullish (Score: 0.82, Relevance: 0.95)
  MSFT: Neutral (Score: 0.12, Relevance: 0.35)
  GOOG: Bearish (Score: -0.40, Relevance: 0.60)
---

News #2: Tech Stocks Rally on Fed's Decision to Maintain Interest Rates
URL: https://example.com/news/tech-stocks-rally
Published: 20240617T1045
Authors: Robert Johnson
Summary: Technology stocks surged on Wednesday after the Federal Reserve...
Overall Sentiment: Bullish (Score: 0.68)

Ticker Sentiments:
  AAPL: Bullish (Score: 0.65, Relevance: 0.75)
  MSFT: Bullish (Score: 0.70, Relevance: 0.80)
  AMZN: Bullish (Score: 0.72, Relevance: 0.65)
---
```

### get-sma

Retrieves Simple Moving Average (SMA) technical indicator data.

**Input Schema:**
```json
{
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
}
```

**Example Response:**
```
Simple Moving Average (SMA) for AAPL:

Technical Indicator: SMA for AAPL
Interval: daily, Time Period: 20, Series Type: close
Last Refreshed: 2024-06-17 16:00:00 US/Eastern

Date: 2024-06-17, SMA: 195.43
Date: 2024-06-14, SMA: 194.20
Date: 2024-06-13, SMA: 193.15
Date: 2024-06-12, SMA: 192.46
Date: 2024-06-11, SMA: 191.78
Date: 2024-06-10, SMA: 190.65
Date: 2024-06-07, SMA: 189.42
Date: 2024-06-06, SMA: 188.30
Date: 2024-06-05, SMA: 187.15
Date: 2024-06-04, SMA: 185.92
---
```

### get-historical-options

Retrieves historical options chain data with advanced sorting and filtering capabilities.

**Input Schema:**
```json
{
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
        "enum": ["strike", "expiration", "volume", "open_interest", "implied_volatility", "delta", "gamma", "theta", "vega", "rho", "last", "bid", "ask"],
        "default": "strike"
    },
    "sort_order": {
        "type": "string",
        "description": "Optional: Sort order",
        "enum": ["asc", "desc"],
        "default": "asc"
    }
}
```

**Example Response:**
```
Historical Options Data for AAPL (2024-02-20):

Contract 1:
Strike: $190.00
Expiration: 2024-03-15
Last: $8.45
Bid: $8.40
Ask: $8.50
Volume: 1245
Open Interest: 4567
Implied Volatility: 0.25
Greeks:
  Delta: 0.65
  Gamma: 0.04
  Theta: -0.15
  Vega: 0.30
  Rho: 0.25

Contract 2:
...
```

### get-crypto-daily

Retrieves daily time series data for a cryptocurrency.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "Cryptocurrency symbol (e.g., BTC, ETH)"
    },
    "market": {
        "type": "string",
        "description": "Market currency (e.g., USD, EUR)",
        "default": "USD"
    }
}
```

**Example Response:**
```
Daily cryptocurrency time series for SOL in USD:

Daily Time Series for Solana (SOL)
Market: United States Dollar (USD)
Last Refreshed: 2025-04-17 00:00:00 UTC

Date: 2025-04-17
Open: 131.31000000 USD
High: 131.67000000 USD
Low: 130.74000000 USD
Close: 131.15000000 USD
Volume: 39652.22195178
---
Date: 2025-04-16
Open: 126.10000000 USD
High: 133.91000000 USD
Low: 123.46000000 USD
Close: 131.32000000 USD
Volume: 1764240.04195810
---
```

### get-crypto-weekly

Retrieves weekly time series data for a cryptocurrency.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "Cryptocurrency symbol (e.g., BTC, ETH)"
    },
    "market": {
        "type": "string",
        "description": "Market currency (e.g., USD, EUR)",
        "default": "USD"
    }
}
```

**Example Response:**
```
Weekly cryptocurrency time series for SOL in USD:

Weekly Time Series for Solana (SOL)
Market: United States Dollar (USD)
Last Refreshed: 2025-04-17 00:00:00 UTC

Date: 2025-04-17
Open: 128.32000000 USD
High: 136.00000000 USD
Low: 123.46000000 USD
Close: 131.15000000 USD
Volume: 4823091.05667581
---
Date: 2025-04-13
Open: 105.81000000 USD
High: 134.11000000 USD
Low: 95.16000000 USD
Close: 128.32000000 USD
Volume: 18015328.38860037
---
```

### get-crypto-monthly

Retrieves monthly time series data for a cryptocurrency.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "Cryptocurrency symbol (e.g., BTC, ETH)"
    },
    "market": {
        "type": "string",
        "description": "Market currency (e.g., USD, EUR)",
        "default": "USD"
    }
}
```

**Example Response:**
```
Monthly cryptocurrency time series for SOL in USD:

Monthly Time Series for Solana (SOL)
Market: United States Dollar (USD)
Last Refreshed: 2025-04-17 00:00:00 UTC

Date: 2025-04-17
Open: 124.51000000 USD
High: 136.18000000 USD
Low: 95.16000000 USD
Close: 131.15000000 USD
Volume: 34268628.85976021
---
Date: 2025-03-31
Open: 148.09000000 USD
High: 180.00000000 USD
Low: 112.00000000 USD
Close: 124.54000000 USD
Volume: 42360395.75443056
---
```

### get-weekly-adjusted-time-series

Retrieves weekly adjusted time series (open, high, low, close, adjusted close, volume, dividend) data for a stock, covering 20+ years of historical data.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "The stock symbol (e.g., AAPL, MSFT) for which to retrieve weekly adjusted data."
    }
}
```

**Example Response:**
```
Weekly Adjusted Time Series for IBM
Last Refreshed: 2023-12-15 (Timezone: US/Eastern)
---
Date: 2023-12-15
  Open: $160.25
  High: $164.75
  Low: $159.50
  Close: $162.50
  Adjusted Close: $162.50
  Volume: 12456789
  Dividend Amount: $0.0000
---
Date: 2023-12-08
  Open: $157.00
  High: $161.25
  Low: $156.75
  Close: $160.00
  Adjusted Close: $160.00
  Volume: 10987654
  Dividend Amount: $0.0000
---
Date: 2023-12-01
  Open: $155.50
  High: $159.00
  Low: $154.25
  Close: $157.75
  Adjusted Close: $157.75
  Volume: 11234567
  Dividend Amount: $1.6500
---
Date: 2023-11-24
  Open: $152.75
  High: $156.50
  Low: $152.00
  Close: $155.25
  Adjusted Close: $153.67
  Volume: 9876543
  Dividend Amount: $0.0000
---
Date: 2023-11-17
  Open: $150.00
  High: $153.00
  Low: $149.25
  Close: $152.50
  Adjusted Close: $150.94
  Volume: 10123456
  Dividend Amount: $0.0000
---

(Showing 5 of 1242 data points)
```

### get-market-status

Retrieves the current market status (open/closed) of major trading venues for equities, forex, and cryptocurrencies worldwide.

**Input Schema:**
```json
{
    "type": "object",
    "properties": {}
}
```

**Example Response:**
```
Global Market Status:
---
Market: Equity (United States)
  Primary Exchanges: NYSE, NASDAQ, AMEX
  Hours (Local): 09:30 - 16:00
  Status: OPEN
---
Market: Equity (Japan)
  Primary Exchanges: Tokyo Stock Exchange
  Hours (Local): 09:00 - 15:00
  Status: CLOSED
---
Market: FX (Global)
  Primary Exchanges: Electronic Markets
  Hours (Local): 00:00 - 23:59
  Status: OPEN
  Notes: 24/7 trading with reduced liquidity on weekends
---
Market: Crypto (Global)
  Primary Exchanges: Binance, Coinbase, etc.
  Hours (Local): 00:00 - 23:59
  Status: OPEN
  Notes: 24/7 trading
---
```

### get-listing-status

Retrieves a list of active or delisted US stocks and ETFs, as of the latest trading day or a specific date.

**Input Schema:**
```json
{
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
```

**Example Response:**
```
Listing Status (State: Active) - Showing up to 10 listings:
---
symbol | name | exchange | assetType | ipoDate | delistingDate | status
--------------------------------------------------------------
AAPL | Apple Inc | NASDAQ | Stock | 1980-12-12 |  | Active
MSFT | Microsoft Corporation | NASDAQ | Stock | 1986-03-13 |  | Active
AMZN | Amazon.com Inc | NASDAQ | Stock | 1997-05-15 |  | Active
GOOGL | Alphabet Inc | NASDAQ | Stock | 2004-08-19 |  | Active
META | Meta Platforms Inc | NASDAQ | Stock | 2012-05-18 |  | Active
TSLA | Tesla Inc | NASDAQ | Stock | 2010-06-29 |  | Active
NVDA | NVIDIA Corporation | NASDAQ | Stock | 1999-01-22 |  | Active
BRK.A | Berkshire Hathaway Inc | NYSE | Stock | 1964-03-17 |  | Active
JPM | JPMorgan Chase & Co | NYSE | Stock | 1980-03-17 |  | Active
V | Visa Inc | NYSE | Stock | 2008-03-19 |  | Active

... and potentially more listings.
```

### get-etf-profile

Retrieves key ETF metrics (e.g., net assets, expense ratio, and turnover), along with the corresponding ETF holdings/constituents with allocation by asset types and sectors.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "The ETF symbol (e.g., QQQ, SPY)."
    }
}
```

**Example Response:**
```
ETF Profile for SPY:

ETF Profile: SPDR S&P 500 ETF Trust (SPY)
---
Fund Family: State Street Global Advisors
Asset Class: Equity
Category: Large Blend
Net Assets: $456.7 billion
Expense Ratio: 0.0945%
Inception Date: 1993-01-22

Description: The SPDR S&P 500 ETF Trust seeks to provide investment results that, before expenses, correspond generally to the price and yield performance of the S&P 500 Index.

Top Holdings:
  1. Apple Inc.: 7.2%
  2. Microsoft Corporation: 6.8% 
  3. Amazon.com Inc.: 3.5%
  4. NVIDIA Corporation: 3.4%
  5. Alphabet Inc. Class A: 2.1%
  6. Meta Platforms Inc. Class A: 2.0%
  7. Tesla, Inc.: 1.9%
  8. Berkshire Hathaway Inc. Class B: 1.7%
  9. Alphabet Inc. Class C: 1.7%
  10. JPMorgan Chase & Co.: 1.2%
  ... and 490 more holdings

Sector Allocation:
  Information Technology: 29.8%
  Health Care: 12.7%
  Financials: 12.5%
  Consumer Discretionary: 10.7%
  Communication Services: 8.5%
  Industrials: 8.4%
  Consumer Staples: 6.2%
  Energy: 3.9%
  ... and 3 more sectors
```

### get-ipo-calendar

Retrieves a list of IPOs expected in the next 3 months. Data is returned in CSV format.

**Input Schema:**
```json
{
    "type": "object",
    "properties": {} // No specific input parameters apart from API key
}
```

**Example Response:**
```
Upcoming IPO Calendar - Showing up to 15 companies:
---
symbol | name | exchange | ipoDate | priceRangeLow | priceRangeHigh | currency | sharesOffered | expectedReportDate
--------------------------------------------------------------------------------------------------------------------
XYZT | XYZ Tech Inc. | NASDAQ | 2025-06-15 | 15.00 | 17.00 | USD | 10000000 | 2025-06-10
ABCN | ABC Nano Corp. | NYSE | 2025-07-01 | 20.00 | 22.00 | USD | 5000000 | 2025-06-25
... and potentially more upcoming IPOs.
```

### get-macd

Retrieves Moving Average Convergence/Divergence (MACD) values. This is a premium Alpha Vantage endpoint.

**Input Schema:**
```json
{
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
}
```

**Example Response:**
```
Moving Average Convergence/Divergence (MACD) for IBM
Interval: daily, FastP: 12, SlowP: 26, SignalP: 9
Last Refreshed: 2023-12-15
---
Date: 2023-12-15 -> MACD: 1.5236, Signal: 1.2451, Hist: 0.2785
Date: 2023-12-14 -> MACD: 1.3982, Signal: 1.1753, Hist: 0.2229
Date: 2023-12-13 -> MACD: 1.2347, Signal: 1.1092, Hist: 0.1255
Date: 2023-12-12 -> MACD: 1.0923, Signal: 1.0551, Hist: 0.0372
Date: 2023-12-11 -> MACD: 0.9437, Signal: 1.0134, Hist: -0.0697
Date: 2023-12-08 -> MACD: 0.8326, Signal: 0.9834, Hist: -0.1508
Date: 2023-12-07 -> MACD: 0.7451, Signal: 0.9612, Hist: -0.2161
Date: 2023-12-06 -> MACD: 0.6723, Signal: 0.9421, Hist: -0.2698
Date: 2023-12-05 -> MACD: 0.6215, Signal: 0.9253, Hist: -0.3038
Date: 2023-12-04 -> MACD: 0.5947, Signal: 0.9102, Hist: -0.3155

... and 90 more data points.
```

### get-earnings-call-transcript

Retrieves the earnings call transcript for a specific company and fiscal quarter.

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "The stock symbol (e.g., IBM, MSFT)."
    },
    "quarter": {
        "type": "string",
        "description": "Fiscal quarter in YYYYQM format (e.g., 2024Q1). Any quarter since 2010Q1 is supported.",
        "pattern": "^\\d{4}Q[1-4]$"
    }
}
```

**Example Response:**
```
Earnings Call Transcript for International Business Machines Corp (IBM)
Fiscal Quarter: 2023Q4
Call Date: 2024-01-24
---
Participants:
  - Patricia Murphy (VP of IR)
  - Arvind Krishna (Chairman and CEO)
  - James Kavanaugh (CFO)
  - Toni Sacconaghi (Bernstein)
  - Wamsi Mohan (Bank of America)
  - Amit Daryanani (Evercore)
  - Erik Woodring (Morgan Stanley)
  - David Grossman (Stifel)
  - Kyle McNealy (Jefferies)
---
Transcript Preview:
Patricia Murphy: Thank you. This is Patricia Murphy, and I'd like to welcome you to IBM's fourth quarter 2023 earnings presentation. I'm here with Arvind Krishna, IBM's Chairman and Chief Executive Officer, and Jim Kavanaugh, IBM's Senior Vice President and Chief Financial Officer.

We'll post today's prepared remarks on the IBM investor website within a couple of hours, and a replay will be available by this time tomorrow.

Some comments made in this presentation may be considered forward-looking under the Private Securities Litigation Reform Act of 1995. These statements involve factors that could cause our actual results to differ materially...

...

[Transcript continues for 15,478 more characters]
```

## Error Handling

The server includes comprehensive error handling for various scenarios:

- Rate limit exceeded
- Invalid API key
- Network connectivity issues
- Timeout handling
- Malformed responses

Error messages are returned in a clear, human-readable format.

## Prerequisites

- Python 3.12 or higher
- httpx
- mcp

## Contributors

- [berlinbra](https://github.com/berlinbra)
- [zzulanas](https://github.com/zzulanas)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
This MCP server is licensed under the MIT License. 
This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
