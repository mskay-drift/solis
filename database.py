import sqlite3
from datetime import datetime

# Connect to SQLite
conn = sqlite3.connect("solis.db")
cursor = conn.cursor()

# Create table to store user information (name + location)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT PRIMARY KEY,
    location TEXT
)
""")

# Create table to store when plants were last watered
cursor.execute("""
CREATE TABLE IF NOT EXISTS watering_logs (
    user_id TEXT,
    plant_name TEXT,
    last_watered TEXT,
    PRIMARY KEY (user_id, plant_name)
)
""")

# Create table to store user plants
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_plants (
    user_id TEXT,
    plant_name TEXT,
    PRIMARY KEY (user_id, plant_name)
)
""")

conn.commit()
conn.close()

def set_user(name, location):
    """Create or update a user's location."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (name, location) 
    VALUES (?, ?) 
    ON CONFLICT(name) DO UPDATE SET location=excluded.location
    """, (name, location))

    conn.commit()
    conn.close()

def add_plant(user_id, plant_name):
    """Add a plant to the user's list in the database."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_plants (user_id, plant_name)
    VALUES (?, ?)
    ON CONFLICT(user_id, plant_name) DO NOTHING
    """, (user_id, plant_name))

    conn.commit()
    conn.close()


def get_user_plants(user_id):
    """Retrieve all plants a user is tracking."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT plant_name FROM user_plants WHERE user_id = ?", (user_id,))
    plants = [row[0] for row in cursor.fetchall()]

    conn.close()
    return plants

def log_watering(user_id, plant_name):
    """Log a watering event for a user's plant."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()
    last_watered = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT INTO watering_logs (user_id, plant_name, last_watered)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id, plant_name) DO UPDATE SET last_watered=excluded.last_watered
    """, (user_id, plant_name, last_watered))

    conn.commit()
    conn.close()

# Retrieve user location
def get_user_location(name):
    """Retrieve a user's location from the database."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT location FROM users WHERE name = ?", (name,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else None  # Return the location if found, else None

def get_last_watered(user_id, plant_name):
    """Retrieve the last watering date for a specific plant."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT last_watered FROM watering_logs WHERE user_id = ? AND plant_name = ?", (user_id, plant_name))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else None

def user_exists(user_id):
    """Check if a user exists in the database."""
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM users WHERE name = ? LIMIT 1", (user_id,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists
