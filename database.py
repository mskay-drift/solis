import sqlite3
from datetime import datetime

# Connect to SQLite
conn = sqlite3.connect("solis.db")
cursor = conn.cursor()

# Create table to store user information (location only)
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    location TEXT UNIQUE
)
""")

# Create table to store when plants were last watered
cursor.execute("""
CREATE TABLE IF NOT EXISTS watering_logs (
    plant_name TEXT,
    last_watered TEXT,
    PRIMARY KEY (plant_name)
)
""")

# Create table to store user plants
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_plants (
    plant_name TEXT,
    PRIMARY KEY (plant_name)
)
""")

conn.commit()
conn.close()

def set_user_location(location):
    """Create or update the user's location."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user (location) 
    VALUES (?) 
    ON CONFLICT(location) DO UPDATE SET location=excluded.location
    """, (location,))

    conn.commit()
    conn.close()

def add_plant(plant_name):
    """Add a plant to the user's list in the database."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_plants (plant_name)
    VALUES (?)
    ON CONFLICT(plant_name) DO NOTHING
    """, (plant_name,))

    conn.commit()
    conn.close()

def get_user_plants():
    """Retrieve all plants the user is tracking."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT plant_name FROM user_plants")
    plants = [row[0] for row in cursor.fetchall()]

    conn.close()
    return plants

def log_watering(plant_name):
    """Log a watering event for a user's plant."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()
    last_watered = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT INTO watering_logs (plant_name, last_watered)
    VALUES (?, ?)
    ON CONFLICT(plant_name) DO UPDATE SET last_watered=excluded.last_watered
    """, (plant_name, last_watered))

    conn.commit()
    conn.close()

def get_user_location():
    """Retrieve the user's location from the database."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT location FROM user")
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else None  # Return the location if found, else None

def get_last_watered(plant_name):
    """Retrieve the last watering date for a specific plant."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT last_watered FROM watering_logs WHERE plant_name = ?", (plant_name,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else None

def user_exists():
    """Check if the user exists in the database."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM user LIMIT 1")
    exists = cursor.fetchone() is not None

    conn.close()
    return exists