import sqlite3
import hashlib
import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = c.fetchone()
    if user:
        print("Login successful:", user)
        return user
    else:
        print("Login failed.")
        return None

def register():
    print("=== Register New User ===")
    name = input("Name: ")
    username = input("Username: ")
    password = input("Password: ")
    timestamp = datetime.datetime.now().isoformat()
    try:
        c.execute(
            "INSERT INTO users (name, username, password, timestamp) VALUES (?, ?, ?, ?)",
            (name, username, hash_password(password), timestamp)
        )
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please try another.")

conn = sqlite3.connect('wifi_stuff.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
''')

# Register a new user
# register()

# Example login
# login("b", "12345")