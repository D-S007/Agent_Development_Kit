import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city using Open-Meteo API.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Geocoding to get latitude and longitude
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_resp = requests.get(geo_url)
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return {"status": "error", "error_message": f"Could not find location for '{city}'."}
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        # Get current weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = requests.get(weather_url)
        weather_data = weather_resp.json()
        if "current_weather" not in weather_data:
            return {"status": "error", "error_message": f"Weather data not available for '{city}'."}
        weather = weather_data["current_weather"]
        temp = weather["temperature"]
        wind = weather["windspeed"]
        desc = f"The weather in {city.title()} is {temp}°C with wind speed {wind} km/h."
        return {"status": "success", "report": desc}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city using geocoding and timezone info.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Geocoding to get latitude, longitude, and timezone
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_resp = requests.get(geo_url)
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return {"status": "error", "error_message": f"Could not find location for '{city}'."}
        tz_identifier = geo_data["results"][0].get("timezone")
        if not tz_identifier:
            return {"status": "error", "error_message": f"Timezone information not available for '{city}'."}
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = f'The current time in {city.title()} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)