# Alpha Vantage MCP Server Core Module

This is the core module for the Alpha Vantage MCP Server that provides integration with the Alpha Vantage financial API through the Model Context Protocol (MCP).

## Overview

The server.py file in this directory is the main entry point for the MCP server. It:

1. Defines all available tools based on the schemas in the models module
2. Routes tool requests to the appropriate handlers
3. Handles server initialization and configuration
4. Implements the MCP protocol for communication with clients

## Module Structure

The application is organized into several submodules:

- `api/`: HTTP client for communicating with the Alpha Vantage API
- `config/`: Configuration settings and environment variable handling
- `formatters/`: Functions for formatting API responses as human-readable text
- `handlers/`: Request handlers for each supported API endpoint
- `models/`: JSON schema definitions for tool parameters
- `utils/`: Utility functions for error handling, validation, etc.

Each module has its own README.md with detailed documentation.

## Adding New Tools

To add a new Alpha Vantage API endpoint as a tool:

1. Add a JSON schema in `models/schemas.py` to define the input parameters
2. Create a formatter function in the appropriate file in `formatters/`
3. Create a handler function in the appropriate file in `handlers/`
4. Add the handler to the `HANDLER_MAPPING` in `handlers/__init__.py`
5. Import the schema in `server.py` and add a tool definition
6. Update the main README.md with documentation for the new tool

## Server Configuration

The server requires an Alpha Vantage API key to function, which should be provided via the `ALPHA_VANTAGE_API_KEY` environment variable.

Example:
```bash
export ALPHA_VANTAGE_API_KEY="your_api_key"
python -m src.alpha_vantage_mcp.server
```

## Logging and Debugging

The server uses standard Python logging for debugging and error reporting. The log level can be set via the `LOG_LEVEL` environment variable.

Example:
```bash
export LOG_LEVEL="DEBUG"
python -m src.alpha_vantage_mcp.server
```