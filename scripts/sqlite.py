import sqlite3
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def insert_wifi_info(ip, wlan_24, wlan_5, wlan_pwd_24, wlan_pwd_5):
    timestamp = datetime.datetime.now().isoformat()
    c.execute(
        "INSERT INTO wifi_info (ip, wlan_24, wlan_5, wlan_pwd_24, wlan_pwd_5, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (ip, wlan_24, wlan_5, wlan_pwd_24, wlan_pwd_5, timestamp)
    )
    conn.commit()
    logging.info(f"{ip} has been added to the database")

conn = sqlite3.connect('wifi_stuff.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS wifi_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        wlan_24 TEXT NOT NULL,
        wlan_5 TEXT NOT NULL,
        wlan_pwd_24 TEXT NOT NULL,
        wlan_pwd_5 TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
''')

# Example usage:
# insert_wifi_info("192.168.1.1", "MyWiFi_24", "MyWiFi_5", "password24", "password5")