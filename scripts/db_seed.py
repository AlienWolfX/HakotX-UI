import sqlite3
import datetime

conn = sqlite3.connect('wifi_stuff.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS onu_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        mac TEXT NOT NULL,
        ssid_24 TEXT NOT NULL,
        ssid_5 TEXT,
        wlan_pwd_24 TEXT NOT NULL,
        wlan_pwd_5 TEXT,
        source TEXT NOT NULL,
        last_updated TEXT NOT NULL
    )
''')

now = datetime.datetime.now().isoformat()
sample_data = [
    ("192.168.1.10", "AA:BB:CC:DD:EE:01", "HomeWiFi_24", "HomeWiFi_5", "pass24_1", "pass5_1", "seed_script", now),
    ("192.168.1.11", "AA:BB:CC:DD:EE:02", "OfficeWiFi_24", "OfficeWiFi_5", "pass24_2", "pass5_2", "seed_script", now),
    ("192.168.1.12", "AA:BB:CC:DD:EE:03", "CafeWiFi_24", "CafeWiFi_5", "pass24_3", "pass5_3", "seed_script", now),
]

c.executemany('''
    INSERT INTO onu_info (ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()
print("Database seeded successfully.")