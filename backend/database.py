import sqlite3
from config import DATABASE_PATH

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL CHECK(role IN ('patient','caregiver','doctor','admin')),
        name TEXT NOT NULL,
        age INTEGER,
        blood_group TEXT,
        emergency_contact TEXT,
        allergies TEXT DEFAULT '',
        medicines TEXT DEFAULT '',
        medical_history TEXT DEFAULT '',
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS health_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        heart_rate REAL, spo2 REAL, temperature REAL,
        accel_x REAL, accel_y REAL, accel_z REAL,
        fall_detected INTEGER DEFAULT 0,
        recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        alert_type TEXT NOT NULL,
        message TEXT NOT NULL,
        latitude REAL, longitude REAL,
        status TEXT DEFAULT 'active',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS blood_inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blood_group TEXT NOT NULL,
        units INTEGER NOT NULL DEFAULT 0,
        hospital TEXT NOT NULL,
        location TEXT DEFAULT '',
        status TEXT DEFAULT 'available',
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()
