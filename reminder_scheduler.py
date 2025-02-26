import os
from weather import generate_watering_reminder
from dotenv import load_dotenv
import sqlite3
from database import get_last_watered
from tools import check_weather
from datetime import datetime



# Load API keys from .env file
load_dotenv()

# Simulated user database (replace with actual storage later)
users = [
    {"name": "Alice", "location": "San Francisco"},
    {"name": "Bob", "location": "Austin"},
]


def get_all_user_plants():
    """Retrieve all user-plant pairs from the database."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT user_id, plant_name FROM watering_logs")
    plants = cursor.fetchall()

    conn.close()
    return plants


def send_watering_reminders():
    """Check all plants and log a reminder if watering is needed."""
    plants = get_all_user_plants()

    for user_id, plant_name in plants:
        location = "San Francisco"  # Replace with dynamic location later
        if needs_watering(user_id, plant_name, location):
            reminder_message = f"Reminder: Your {plant_name} needs watering today! 🌿"
            print(reminder_message)  # ✅ Later, send SMS/email


def needs_watering(user_id, plant_name, location):
    """Determine if a plant needs watering based on last watered date and weather."""
    last_watered = get_last_watered(user_id, plant_name)
    if not last_watered:
        return True  # If no record, assume it needs watering

    last_watered_date = datetime.fromisoformat(last_watered)
    days_since_watered = (datetime.utcnow() - last_watered_date).days

    # Define watering frequency (customize per plant later)
    WATERING_THRESHOLD = 3  # Days before a plant needs water

    if days_since_watered < WATERING_THRESHOLD:
        return False  # Recently watered, no need

    # Check weather forecast
    weather = check_weather(location)
    if weather.get("rain_mm", 0) > 5:
        return False  # Enough rain, no need

    return True  # Needs watering

def send_notification(user, message):
    """
    Placeholder for sending notifications (email, SMS, etc.).
    Replace this with Twilio, SendGrid, or another service.
    """
    print(f"📢 Sending reminder to {user['name']}: {message}")

def send_daily_reminders():
    """
    Fetches weather data for all users and sends watering reminders.
    """
    for user in users:
        reminder = generate_watering_reminder(user["location"])
        send_notification(user, reminder)

if __name__ == "__main__":
    send_daily_reminders()