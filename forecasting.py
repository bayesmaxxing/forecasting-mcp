from typing import Any, List, Dict, Optional
import httpx 
from mcp.server.fastmcp import FastMCP
import os
import dotenv
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

dotenv.load_dotenv()

app = FastAPI()
mcp = FastMCP("forecasting")

# Environment variables
API_URL = os.getenv("API_URL")
BOT_USERNAME = os.getenv("BOT_USERNAME")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Helper functions 
async def request(url_postfix: str, data: Any, token: str = None, is_protected: bool = False, method: str = "POST") -> Any:
    """Make a request to the forecaster API"""
    if is_protected:
        url = f"{API_URL}/api/{url_postfix}"
    else:
        url = f"{API_URL}/{url_postfix}"

    headers = {
        "Content-Type": "application/json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, params=data, headers=headers)
            elif method.upper() == "DELETE":
                response = await client.delete(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = await client.put(url, json=data, headers=headers)
            else:  # Default to POST
                response = await client.post(url, json=data, headers=headers)
                
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            print(f"Error occurred: {e}")
            return {"success": False, "error": str(e)}

async def login() -> Any:
    """Login to the forecaster API"""
    data = {
        "username": BOT_USERNAME,
        "password": BOT_PASSWORD
    }
    response = await request("login", data)
    return response["token"]

async def format_timeline(timeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Format the timeline for a given forecast"""
    if not timeline:
        return []
        
    formatted_timeline = []
    # Sort by creation date
    sorted_timeline = sorted(timeline, key=lambda x: x.get('created_at', ''), reverse=True)
    
    for point in sorted_timeline:
        formatted_point = {
            'id': point.get('id'),
            'forecast_id': point.get('forecast_id'),
            'value': point.get('point_forecast'),
            'reason': point.get('reason'),
            'created_at': point.get('created_at'),
            'username': point.get('username', 'AI Assistant')
        }
        formatted_timeline.append(formatted_point)
        
    return formatted_timeline

@mcp.tool()
async def get_forecasts(category: Optional[str] = None, list_type: str = "open") -> List[Dict[str, Any]]:
    """Get a list of forecasts from a given category and list type (open, closed, all)"""
    payload = {"list_type": list_type}
    
    if category:
        payload["category"] = category
    
    response = await request("forecasts", payload, method="POST")
    if not response or "data" not in response:
        return []
        
    return response["data"]

@mcp.tool()
async def create_point(forecast_id: int, point_forecast: float, reason: str) -> Dict[str, Any]:
    """Create a forecast point for a given forecast, along with the reasoning behind the forecast point"""
    token = await login()
    
    payload = {
        "forecast_id": forecast_id, 
        "point_forecast": point_forecast, 
        "reason": reason
    }
    
    response = await request("forecast-points", payload, token=token, is_protected=True, method="PUT")
    if not response or "data" not in response:
        return {"success": False, "error": "Failed to create forecast point"}
        
    return {"success": True, "data": response["data"]}

@mcp.tool()
async def get_forecast_data(id: int) -> Dict[str, Any]:
    """Get the data for a given forecast. This includes the question, the category, and the resolution criteria"""
    response = await request(f"forecasts/{id}", {}, is_protected=False, method="GET")
    if not response or "data" not in response:
        return {"success": False, "error": "Failed to retrieve forecast data"}
        
    return {"success": True, "data": response["data"]}

@mcp.tool()
async def get_forecast_points(forecast_id: int) -> List[Dict[str, Any]]:
    """Get all the forecast points for a given forecast."""
    response = await request(f"forecast-points/{forecast_id}", {}, is_protected=False, method="GET")
    if not response or "data" not in response:
        return []
        
    return await format_timeline(response["data"])

@mcp.tool()
async def update_forecast(forecast_id: int, **update_data) -> Dict[str, Any]:
    """Update an existing forecast with the given details"""
    token = await login()
    
    # Filter out None values
    payload = {k: v for k, v in update_data.items() if v is not None}
    payload["id"] = forecast_id
    
    response = await request(f"forecasts/{forecast_id}", payload, token=token, is_protected=True, method="PUT")
    if not response or "data" not in response:
        return {"success": False, "error": "Failed to update forecast"}
        
    return {"success": True, "data": response["data"]}

@mcp.tool()
async def get_news_articles(query: str, from_date: Optional[str] = None, to_date: Optional[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """Fetch news articles related to a query to help inform forecasts"""
    if not NEWS_API_KEY:
        return [{"error": "NEWS_API_KEY not configured"}]
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": max_results
    }
    
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data.get("status") != "ok":
                return [{"error": data.get("message", "Failed to fetch news articles")}]
            
            articles = data.get("articles", [])
            formatted_articles = []
            
            for article in articles:
                formatted_article = {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "source": article.get("source", {}).get("name"),
                    "published_at": article.get("publishedAt"),
                    "url": article.get("url")
                }
                formatted_articles.append(formatted_article)
                
            return formatted_articles
        except Exception as e:
            return [{"error": f"Error fetching news: {str(e)}"}]

@app.get("/")
async def root():
    return {"message": "Forecasting MCP API"}
