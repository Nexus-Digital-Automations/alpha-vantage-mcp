# Alpha Vantage MCP Server Architecture

This document describes the architectural design of the Alpha Vantage MCP server.

## Overview

The Alpha Vantage MCP server is built using the Model Context Protocol (MCP) to provide financial data through the Alpha Vantage API. The server exposes a set of tools that can be used by MCP-compatible clients (like Claude) to interact with financial data in a structured manner.

## System Architecture

```
┌────────────────┐      ┌────────────────┐      ┌────────────────┐
│                │      │                │      │                │
│  MCP Client    │◄────►│  MCP Server    │◄────►│  Alpha Vantage │
│  (e.g. Claude) │      │                │      │  API           │
│                │      │                │      │                │
└────────────────┘      └────────────────┘      └────────────────┘
```

### Components

1. **MCP Client** - A client that supports the Model Context Protocol (e.g., Claude, Claude Desktop)
2. **MCP Server** - Our Alpha Vantage MCP server, which implements the MCP protocol and provides tools for accessing financial data
3. **Alpha Vantage API** - The third-party financial data API that our server interacts with

## Code Organization

```
src/
└── alpha_vantage_mcp/
    ├── __init__.py
    ├── server.py       # Main server implementation with MCP protocol handling
    └── tools.py        # Utility functions for API requests and data formatting
```

### Key Files

- **server.py**: Contains the core MCP server implementation, including:
  - Server initialization
  - Tool definitions and schemas
  - Tool execution handlers
  - Main entry point for running the server

- **tools.py**: Contains utility functions for:
  - Making requests to the Alpha Vantage API
  - Formatting API responses into human-readable text
  - Error handling

## Data Flow

1. The MCP client (Claude) receives a request from the user for financial data
2. Claude calls the appropriate tool on our MCP server
3. The MCP server:
   - Validates the input parameters
   - Makes a request to the Alpha Vantage API
   - Formats the response into a human-readable text
   - Returns the formatted response to the client
4. Claude displays the result to the user

## Tool Structure

Each tool follows this general pattern:

1. **Definition** - Defined in the `handle_list_tools()` function with:
   - Name: A descriptive, hyphenated name (e.g., `get-stock-quote`)
   - Description: A short explanation of what the tool does
   - Input Schema: JSON Schema defining the required and optional parameters

2. **Handler** - Implemented in the `handle_call_tool()` function:
   - Validates input parameters
   - Makes requests to the Alpha Vantage API 
   - Formats the response using a corresponding formatter function
   - Returns the formatted data as text content

3. **Formatter** - Defined in tools.py to convert API responses into readable text:
   - Extracts relevant data from the JSON response
   - Formats it into a clean, structured text representation
   - Handles potential errors or missing data

## Current Implementation Status

- Core MCP server functionality: Complete
- Basic Alpha Vantage API integration: Complete
- 13 financial data endpoints implemented:
  - Stock quotes (get-stock-quote)
  - Company information (get-company-info)
  - Cryptocurrency exchange rates (get-crypto-exchange-rate)
  - Daily time series (get-time-series)
  - Weekly time series (get-weekly-time-series)
  - Daily Adjusted time series (get-daily-adjusted-time-series)
  - Intraday time series (get-intraday-time-series)
  - Historical options data (get-historical-options)
  - Cryptocurrency time series (daily, weekly, monthly)
  - News sentiment analysis (get-news-sentiment)
  - Technical indicators (SMA)
- Remaining ~95 endpoints to be implemented (see TODO.md)

## Future Architecture

As more endpoints are added, we may consider:

1. **Modularizing the codebase** - Grouping formatters and handlers by category (e.g., time series, fundamental data, technical indicators)
2. **Adding caching layer** - To reduce API calls and handle rate limits more efficiently
3. **Implementing more sophisticated error handling** - Better recovery from API failures
4. **Adding visualization capabilities** - Returning charts as image content in addition to text

```
Future Architecture:
┌────────────────┐      ┌─────────────────────────────────────┐      ┌────────────────┐
│                │      │           MCP Server                │      │                │
│  MCP Client    │◄────►│  ┌───────────┐       ┌───────────┐  │◄────►│  Alpha Vantage │
│  (e.g. Claude) │      │  │   Tools   │◄─────►│   Cache   │  │      │  API           │
│                │      │  └───────────┘       └───────────┘  │      │                │
└────────────────┘      │          ▲                 ▲        │      └────────────────┘
                        │          │                 │        │
                        │          ▼                 ▼        │
                        │  ┌───────────┐       ┌───────────┐  │
                        │  │ Formatters│       │ Visualizer│  │
                        │  └───────────┘       └───────────┘  │
                        └─────────────────────────────────────┘
``` 