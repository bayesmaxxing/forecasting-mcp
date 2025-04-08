from typing import Any 
import httpx 
from mcp.server.fastmcp import FastMCP
import os
import dotenv

dotenv.load_dotenv()

mcp = FastMCP("forecasting")

# Environment variables
API_URL = os.getenv("API_URL")
BOT_USERNAME = os.getenv("BOT_USERNAME")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")

# Helper functions 
async def request(method: str, data: Any, token: str = None, is_protected: bool = False) -> Any:
    """Make a request to the forecaster API"""
    if is_protected:
        url = f"{API_URL}/api/{method}"
    else:
        url = f"{API_URL}/{method}"

    headers = {
        "Content-Type": "application/json",
    }
    
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, json=data, headers=headers)
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None

async def login() -> Any:
    """Login to the forecaster API"""
    data = {
        "username": BOT_USERNAME,
        "password": BOT_PASSWORD
    }
    return await request("POST", data)



async def get_forecasts() -> Any:
    pass 

async def create_point() -> Any:
    pass 

async def login() -> Any:
    pass

async def get_forecast_data(id: int) -> Any:
    pass 

