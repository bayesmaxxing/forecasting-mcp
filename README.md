# Forecasting MCP

This is a Model Context Protocol (MCP) implementation for interacting with a forecasting website. It enables LLMs to make, update, and delete forecasts, as well as retrieve forecast data and access external information through Perplexity API.

## Features

- Make forecasts on an existing forecasting website
- Update existing forecasts
- Get information about forecasts
- Access Perplexity AI for additional context and research

## Setup

1. Install the required dependencies:

```bash
pip install .
```

2. Create a `.env` file with the following variables:

```
API_URL=<your_forecasting_api_url>
BOT_USERNAME=<your_bot_username>
BOT_PASSWORD=<your_bot_password>
PERPLEXITY_API_KEY=<your_perplexity_api_key>  # For accessing Perplexity API
```

## Usage

Run the server with:

```bash
uv run forecasting.py
```

## Available MCP Tools

### Forecasts Management

- `get_forecasts`: List forecasts by category and status
- `get_forecast_data`: Get details for a specific forecast
- `update_forecast`: Create a new forecast point for a forecast.

### Forecast Points

- `get_forecast_points`: Get all forecast points for a forecast

### External Information

- `query_perplexity`: Query the Perplexity API for additional information to inform forecasts

## Dependencies

- Python 3.13+
- FastAPI
- httpx
- MCP
- requests

## Development

This server uses FastAPI and the MCP library to provide a standardized interface for LLMs to interact with forecasting data.
