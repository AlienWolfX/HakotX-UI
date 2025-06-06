import sqlite3
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def insert_wifi_info(ip, wlan_24, wlan_5, wlan_pwd_24, wlan_pwd_5, source):
    timestamp = datetime.datetime.now().isoformat()
    try:
        c.execute(
            "INSERT INTO wifi_info (ip, wlan_24, wlan_5, wlan_pwd_24, wlan_pwd_5, source, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (ip, wlan_24, wlan_5, wlan_pwd_24, wlan_pwd_5, source, timestamp)
        )
        conn.commit()
        logging.info(f"{ip} has been added to the database")
    except Exception as e:
        logging.error(f"Failed to insert WiFi info for {ip}: {e}")

def display_specific_wifi_info(wlan_24=None, wlan_5=None):
    try:
        if wlan_24:
            c.execute("SELECT * FROM wifi_info WHERE wlan_24 = ?", (wlan_24,))
            row = c.fetchone()
            if row:
                print(row)
                logging.info(f"Displayed WiFi info for wlan_24: {wlan_24}.")
            else:
                logging.warning(f"No records found for wlan_24: {wlan_24}")
        elif wlan_5:
            c.execute("SELECT * FROM wifi_info WHERE wlan_5 = ?", (wlan_5,))
            row = c.fetchone()
            if row:
                print(row)
                logging.info(f"Displayed WiFi info for wlan_5: {wlan_5}.")
            else:
                logging.warning(f"No records found for wlan_5: {wlan_5}")
        else:
            logging.warning("No wlan_24 or wlan_5 provided for lookup.")
    except Exception as e:
        logging.error(f"Failed to display WiFi info: {e}")

def display_wifi_info():
    try:
        c.execute("SELECT * FROM wifi_info")
        rows = c.fetchall()
        for row in rows:
            print(row)
        logging.info("Displayed all WiFi info records.")
    except Exception as e:
        logging.error(f"Failed to display WiFi info: {e}")

def update_wifi_info(record_id, ip=None, wlan_24=None, wlan_5=None, wlan_pwd_24=None, wlan_pwd_5=None, source=None):
    try:
        fields = []
        values = []
        if ip is not None:
            fields.append("ip = ?")
            values.append(ip)
        if wlan_24 is not None:
            fields.append("wlan_24 = ?")
            values.append(wlan_24)
        if wlan_5 is not None:
            fields.append("wlan_5 = ?")
            values.append(wlan_5)
        if wlan_pwd_24 is not None:
            fields.append("wlan_pwd_24 = ?")
            values.append(wlan_pwd_24)
        if wlan_pwd_5 is not None:
            fields.append("wlan_pwd_5 = ?")
            values.append(wlan_pwd_5)
        if source is not None:
            fields.append("source = ?")
            values.append(source)
        if not fields:
            logging.warning("No fields to update.")
            return
        values.append(record_id)
        sql = f"UPDATE wifi_info SET {', '.join(fields)} WHERE id = ?"
        c.execute(sql, values)
        conn.commit()
        logging.info(f"Record {record_id} updated successfully.")
    except Exception as e:
        logging.error(f"Failed to update WiFi info for record {record_id}: {e}")

conn = sqlite3.connect('wifi_stuff.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS wifi_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        wlan_24 TEXT NOT NULL,
        wlan_5 TEXT,
        wlan_pwd_24 TEXT NOT NULL,
        wlan_pwd_5 TEXT,
        source TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
''')

# Example usage:
# insert_wifi_info("192.168.1.1", "MyWiFi_24", "MyWiFi_5", "password24", "password5", "user_input")
# display_wifi_info()
# update_wifi_info(1, ip="192.168.1.2", wlan_pwd_24="newpassword24")