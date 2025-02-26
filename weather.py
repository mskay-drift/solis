import os
import requests
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather_data(location):
    """Fetches weather data from WeatherAPI for a given location."""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        forecast = data["forecast"]["forecastday"][0]["day"]

        weather_info = {
            "temperature": forecast["avgtemp_c"],
            "rainfall": forecast["totalprecip_mm"]
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def should_water_plant(weather, plant_type="default"):
    """
    Determines if a plant needs watering based on weather conditions and plant type.
    """
    water_thresholds = {
        "default": 5,  # If less than 5mm of rain, watering is suggested
        "succulent": 1,
        "vegetable": 8,
        "flower": 6
    }

    rainfall = weather["rainfall"]
    threshold = water_thresholds.get(plant_type, water_thresholds["default"])

    return rainfall < threshold


def generate_watering_reminder(location, plant_type="default"):
    """
    Generates a watering reminder based on weather conditions.
    """
    weather = get_weather_data(location)

    if not weather:
        return "⚠️ Unable to retrieve weather data. Please check again later."

    if should_water_plant(weather, plant_type):
        return f"💧 Watering Reminder: It's been dry in {location} with only {weather['rainfall']}mm of rain. Your {plant_type} plants need watering!"
    else:
        return f"✅ No need to water today! {location} has received {weather['rainfall']}mm of rain."