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
    ├── server.py               # Main server implementation with MCP protocol handling
    ├── config/
    │   ├── __init__.py
    │   └── settings.py         # Configuration settings and API key validation
    ├── api/
    │   ├── __init__.py
    │   └── client.py           # Alpha Vantage API client functionality
    ├── formatters/
    │   ├── __init__.py
    │   ├── stocks.py           # Stock-related formatters
    │   ├── crypto.py           # Cryptocurrency-related formatters
    │   ├── technical.py        # Technical indicator formatters
    │   ├── economic.py         # Economic/fundamental data formatters
    │   └── common.py           # Shared formatting utilities
    ├── handlers/
    │   ├── __init__.py
    │   ├── stocks.py           # Stock-related handlers
    │   ├── crypto.py           # Cryptocurrency-related handlers
    │   ├── technical.py        # Technical indicator handlers
    │   └── economic.py         # Economic/fundamental data handlers
    ├── models/
    │   ├── __init__.py
    │   └── schemas.py          # Input schemas for tools
    └── utils/
        ├── __init__.py
        ├── validation.py       # Input validation utilities
        └── error_handling.py   # Error handling utilities
```

### Key Files and Modules

- **server.py**: Contains the core MCP server implementation, including:
  - Server initialization
  - Tool definitions using schemas
  - Handler dispatch mechanism
  - Main entry point for running the server

- **config/settings.py**: Contains configuration settings:
  - API base URL and environment variables
  - Error messages
  - Response formatting settings

- **api/client.py**: Handles API communication:
  - Making requests to the Alpha Vantage API
  - Handling API errors and responses
  - Managing data formats (JSON/CSV)

- **formatters/**: Contains formatters for different data types:
  - **common.py**: Shared utilities for formatting numbers, dates, etc.
  - **stocks.py**: Formatters for stock quotes, time series, company info
  - **crypto.py**: Formatters for cryptocurrency and forex data
  - **technical.py**: Formatters for technical indicators
  - **economic.py**: Formatters for economic indicators and fundamental data

- **handlers/**: Contains tool handlers by category:
  - **stocks.py**: Handlers for stock-related tools
  - **crypto.py**: Handlers for cryptocurrency-related tools
  - **technical.py**: Handlers for technical indicator tools
  - **economic.py**: Handlers for economic/fundamental data tools
  
- **models/schemas.py**: Contains JSON schemas for tool inputs
  
- **utils/**: Contains utility functions:
  - **validation.py**: Input validation utilities
  - **error_handling.py**: Error handling utilities

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

Now that we've modularized the codebase, future enhancements could include:

1. **Adding caching layer** - To reduce API calls and handle rate limits more efficiently
2. **Implementing logging system** - For better debugging and monitoring
3. **Adding visualization capabilities** - Returning charts as image content in addition to text
4. **Adding tests** - For better code quality and reliability
5. **Enhancing error handling and recovery** - For better resilience against API failures

```
Future Architecture:
┌────────────────┐      ┌─────────────────────────────────────────────────────┐      ┌────────────────┐
│                │      │                    MCP Server                       │      │                │
│  MCP Client    │◄────►│  ┌───────────┐      ┌───────────┐      ┌─────────┐  │◄────►│  Alpha Vantage │
│  (e.g. Claude) │      │  │  Handlers │◄────►│   Cache   │◄────►│   API   │  │      │  API           │
│                │      │  └───────────┘      └───────────┘      └─────────┘  │      │                │
└────────────────┘      │        ▲                  ▲                ▲        │      └────────────────┘
                        │        │                  │                │        │
                        │        ▼                  ▼                ▼        │
                        │  ┌───────────┐      ┌───────────┐      ┌─────────┐  │
                        │  │Formatters │      │Visualizer │      │ Logging │  │
                        │  └───────────┘      └───────────┘      └─────────┘  │
                        │        ▲                                            │
                        │        │                                            │
                        │        ▼                                            │
                        │  ┌───────────┐                                      │
                        │  │   Tests   │                                      │
                        │  └───────────┘                                      │
                        └─────────────────────────────────────────────────────┘
``` 