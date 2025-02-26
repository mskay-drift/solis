from langchain.tools import tool
from weather import generate_watering_reminder
from database import get_last_watered, log_watering, add_plant, get_user_location, get_user_plants

@tool
def check_weather(location: str) -> str:
    """Fetch the latest weather-based watering recommendation for a given location."""
    return generate_watering_reminder(location)

@tool
def get_user_location_tool() -> str:
    """Retrieve the user's location from the database."""
    location = get_user_location()
    return location if location else "Location not set"

@tool
def get_plant_watering_info(plant_name: str) -> str:
    """Retrieve the last watered date for a plant and determine if it needs watering."""
    last_watered = get_last_watered(plant_name)
    if last_watered:
        return f"📅 Last watered on {last_watered}."
    return f"❌ No record found for {plant_name}. Add it first!"

@tool
def log_watering_event(plant_name: str) -> str:
    """Log a watering event for a plant."""
    log_watering(plant_name)
    return f"💧 Logged! {plant_name} was watered today."

@tool
def add_plant_tool(plant_name: str) -> str:
    """Add a plant to the user's plant list."""
    add_plant(plant_name)
    return f"✅ {plant_name} has been added to your plant list!"

@tool
def get_user_plants_tool() -> str:
    """Retrieve the user's location from the database."""
    plants = get_user_plants()
    return plants if plants else "No plants have been added to your garden yet."