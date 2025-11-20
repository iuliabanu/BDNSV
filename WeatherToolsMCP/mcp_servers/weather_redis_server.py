#!python mcp_servers/weather_server.py
from fontTools.feaLib import location
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
import calendar

from weather_client import WeatherClient
from redis_connection_manager import RedisManager

mcp = FastMCP("WeatherRedis")
load_dotenv()

if not os.environ.get("OPENWEATHER_API_KEY"):
    print("API key for OpenWeather is not set. Please check your .env file.")
else:
    print("API key loaded successfully.")

weather_client = WeatherClient(api_key=os.environ.get("OPENWEATHER_API_KEY"))
redis_manager = RedisManager()


@mcp.tool()
async def get_weather(location: str, units: str = "metric") -> str:
    """
    Get weather forecast for a location.
    """

    cached = redis_manager.get_cache_value(location)

    if cached:
        print(f"[MCP Cache] Hit for weather:{location}")
        return cached


    # Fetch from API
    weather_data = weather_client.get_current_weather(location, units)
    result = f"""Current weather in {location}:
Temperature: {weather_data['main']['temp']}°C (feels like {weather_data['main']['feels_like']}°C)
Conditions: {weather_data['weather'][0]['description']}
Humidity: {weather_data['main']['humidity']}%
Wind: {weather_data['wind']['speed']} m/s"""

    redis_manager.set_cache_value(location, result)

    return result


@mcp.tool()
async def compare_weather(locations: list[str], month: int) -> str:
    """
    Compare weather across multiple locations for a specific month.
    Demo implementation. Should use an api serving monthly weather data.
    """
    results = []
    for location in locations:
        try:
            weather_data = weather_client.get_forecast(location)
            # Simplified: use first forecast item
            results.append({
                "location": location,
                "temp": weather_data['list'][0]['main']['temp'],
                "conditions": weather_data['list'][0]['weather'][0]['description']
            })
        except Exception as e:
            results.append({
                "location": location,
                "error": str(e)
            })

    # Format comparison
    comparison = f"Weather comparison for {calendar.month_name[month]}:\n\n"
    for r in results:
        if "error" in r:
            comparison += f"{r['location']}: Unable to fetch data\n"
        else:
            comparison += f"{r['location']}: {r['temp']}°C, {r['conditions']}\n"

    return comparison

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
