import requests

class WeatherClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, location: str, units: str = "metric") -> dict:
        """Get current weather for location"""
        endpoint = f"{self.base_url}/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units
        }
        response = requests.get(endpoint, params=params)
        return response.json()

    def get_forecast(self, location: str) -> dict:
        """Get weather forecast for location"""
        endpoint = f"{self.base_url}/forecast"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(endpoint, params=params)
        return response.json()