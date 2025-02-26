import sqlite3

def drop_database():
    conn = sqlite3.connect("solis.db")
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS user")
    cursor.execute("DROP TABLE IF EXISTS watering_logs")
    cursor.execute("DROP TABLE IF EXISTS user_plants")

if __name__ == "__main__":
    drop_database()
    print("Database has been dropped.")