# setup_db.py
import sqlite3

connection = sqlite3.connect('database.db')

with connection:
    connection.execute("""
        CREATE TABLE users (
            name TEXT PRIMARY KEY,
            age INTEGER,
            nationality TEXT,
            gender TEXT,
            favorite_subjects TEXT,
            hobbies TEXT,
            bio TEXT,
            water_points INTEGER DEFAULT 0
        )
    """)

print("✅ Database created successfully!")
