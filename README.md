# Forecasting MCP

This is a Model Context Protocol (MCP) implementation for interacting with a forecasting website. It enables LLMs to make, update, and delete forecasts, as well as retrieve forecast data and relevant news articles.

## Features

- Make forecasts on an existing forecasting website
- Create new forecasts
- Update existing forecasts
- Delete forecasts
- Access news articles to inform forecasts

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following variables:

```
API_URL=<your_forecasting_api_url>
BOT_USERNAME=<your_bot_username>
BOT_PASSWORD=<your_bot_password>
NEWS_API_KEY=<your_news_api_key>  # Optional, for accessing news articles
```

## Usage

Run the server with:

```bash
uvicorn forecasting:app --reload
```

## Available MCP Tools

### Forecasts Management

- `get_forecasts`: List forecasts by category and status
- `get_forecast_data`: Get details for a specific forecast
- `create_forecast`: Create a new forecast
- `update_forecast`: Modify an existing forecast
- `delete_forecast`: Remove a forecast

### Forecast Points

- `get_forecast_points`: Get all forecast points for a forecast
- `create_point`: Make a new forecast point with reasoning

### News Integration

- `get_news_articles`: Fetch news articles related to a query to inform forecasts

## Development

This server uses FastAPI and the MCP library to provide a standardized interface for LLMs to interact with forecasting data.