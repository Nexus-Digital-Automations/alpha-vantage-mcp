# Alpha Vantage MCP Server
[![smithery badge](https://smithery.ai/badge/@berlinbra/alpha-vantage-mcp)](https://smithery.ai/server/@berlinbra/alpha-vantage-mcp)

A Model Context Protocol (MCP) server that provides real-time access to financial market data through the free [Alpha Vantage API](https://www.alphavantage.co/documentation/). This server implements a standardized interface for retrieving stock quotes, company information, technical indicators, and more.

<a href="https://glama.ai/mcp/servers/0wues5td08"><img width="380" height="200" src="https://glama.ai/mcp/servers/0wues5td08/badge" alt="AlphaVantage-MCP MCP server" /></a>

## Features

- Real-time stock quotes with price, volume, and change data
- Detailed company information including sector, industry, and market cap
- Real-time cryptocurrency exchange rates with bid/ask prices
- Intraday, daily, weekly, and monthly time series data
- Technical indicators (SMA, MACD, STOCH, and more) for investment analysis
- News sentiment analysis for stocks and cryptocurrencies
- Historical options chain data with advanced filtering and sorting
- Economic indicators and commodity prices
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

## Development Setup

### Install packages

```
uv install -e .
```

### Running the server

After connecting Claude client with the MCP tool via json file and installing the packages, Claude should see the server's mcp tools:

You can run the server yourself via:
```
uv run src/alpha_vantage_mcp/server.py
```

With inspector:
```
npx @modelcontextprotocol/inspector uv --directory /path/to/alpha-vantage-mcp run src/alpha_vantage_mcp/server.py
```

## Project Structure

The project is organized into several modules, each with its own documentation:

```
src/alpha_vantage_mcp/
├── api/                  # API client for Alpha Vantage
├── config/               # Configuration settings
├── formatters/           # Response formatting
├── handlers/             # Request handlers
├── models/               # Data models and schemas
├── utils/                # Utility functions
└── server.py             # Main MCP server
```

See the README.md files in each directory for detailed documentation about that module.

## Available Tools

The server implements various tools for accessing financial data:

### Stock Market Data
- `get-stock-quote`: Get the latest stock quote
- `get-company-info`: Get company information
- `get-time-series`: Get daily price data
- `get-weekly-time-series`: Get weekly price data
- `get-daily-adjusted-time-series`: Get adjusted price data
- `get-intraday-time-series`: Get intraday price data
- `get-listing-status`: Get active or delisted stocks

### Technical Indicators
- `get-sma`: Simple Moving Average
- `get-macd`: Moving Average Convergence/Divergence
- `get-stoch`: Stochastic Oscillator
- `get-stochrsi`: Stochastic Relative Strength Index
- `get-adxr`: Average Directional Movement Index Rating
- `get-apo`: Absolute Price Oscillator
- `get-ppo`: Percentage Price Oscillator
- `get-mom`: Momentum
- `get-bop`: Balance Of Power
- `get-cci`: Commodity Channel Index
- `get-cmo`: Chande Momentum Oscillator
- `get-roc`: Rate of Change
- `get-rocr`: Rate of Change Ratio
- `get-aroon`: Aroon
- `get-aroonosc`: Aroon Oscillator
- `get-mfi`: Money Flow Index
- `get-trix`: Triple Exponential Moving Average
- `get-ultosc`: Ultimate Oscillator
- `get-dx`: Directional Movement Index

### Cryptocurrency Data
- `get-crypto-exchange-rate`: Get current exchange rates
- `get-crypto-daily`: Get daily time series
- `get-crypto-weekly`: Get weekly time series
- `get-crypto-monthly`: Get monthly time series

### Options Data
- `get-historical-options`: Get historical options data

### News and Fundamentals
- `get-news-sentiment`: Get news and sentiment analysis
- `get-etf-profile`: Get ETF metrics and holdings
- `get-ipo-calendar`: Get upcoming IPOs
- `get-earnings-call-transcript`: Get earnings transcripts
- `get-insider-transactions`: Get insider transactions

### Economic Indicators
- `get-real-gdp-per-capita`: US Real GDP per Capita
- `get-federal-funds-rate`: Federal Funds Rate
- `get-retail-sales`: Retail sales data
- `get-durables`: Durable goods orders
- `get-unemployment`: Unemployment rate
- `get-nonfarm-payroll`: Nonfarm payroll employment

### Commodities
- `get-copper`: Global copper prices
- `get-aluminum`: Global aluminum prices
- `get-wheat`: Global wheat prices
- `get-corn`: Global corn prices
- `get-cotton`: Global cotton prices
- `get-sugar`: Global sugar prices
- `get-coffee`: Global coffee prices
- `get-all-commodities`: Global commodity price index

## API Key

To use this MCP server, you need an Alpha Vantage API key. You can get a free API key at [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

Free API keys are limited to 5 requests per minute and 500 requests per day. If you need higher limits, you can get a [premium API key](https://www.alphavantage.co/premium/).

## Rate Limiting

The Alpha Vantage API has rate limits, and the MCP server handles these limits gracefully. If you exceed the rate limits, the server will return an error message.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## References

- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- [Model Context Protocol (MCP) Documentation](https://modelcontextprotocol.github.io/mcp/)
- [Smithery.ai MCP Server Registry](https://smithery.ai/server/@berlinbra/alpha-vantage-mcp)