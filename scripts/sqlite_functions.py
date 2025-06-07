import sqlite3
import datetime
import logging

logging.basicConfig(filename="./logs/logs.txt", level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def insert_onu_info(ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source):
    last_updated = datetime.datetime.now().isoformat()
    try:
        c.execute(
            "INSERT INTO onu_info (ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated)
        )
        conn.commit()
        logging.info(f"{ip} ({mac}) has been added to the onu_info database")
    except Exception as e:
        logging.error(f"Failed to insert ONU info for {ip}: {e}")

def display_specific_onu_info(ssid_24=None, ssid_5=None):
    try:
        if ssid_24:
            c.execute("SELECT * FROM onu_info WHERE ssid_24 = ?", (ssid_24,))
            rows = c.fetchall()
            if rows:
                for row in rows:
                    print(row)
                logging.info(f"Displayed ONU info for ssid_24: {ssid_24}.")
            else:
                logging.warning(f"No records found for ssid_24: {ssid_24}")
        elif ssid_5:
            c.execute("SELECT * FROM onu_info WHERE ssid_5 = ?", (ssid_5,))
            rows = c.fetchall()
            if rows:
                for row in rows:
                    print(row)
                logging.info(f"Displayed ONU info for ssid_5: {ssid_5}.")
            else:
                logging.warning(f"No records found for ssid_5: {ssid_5}")
        else:
            logging.warning("No ssid_24 or ssid_5 provided for lookup.")
    except Exception as e:
        logging.error(f"Failed to display ONU info: {e}")

def display_onu_info():
    try:
        c.execute("SELECT * FROM onu_info")
        rows = c.fetchall()
        for row in rows:
            print(row)
        logging.info("Displayed all ONU info records.")
    except Exception as e:
        logging.error(f"Failed to display ONU info: {e}")

def update_onu_info(record_id, ip=None, mac=None, ssid_24=None, ssid_5=None, wlan_pwd_24=None, wlan_pwd_5=None, source=None):
    try:
        fields = []
        values = []
        if ip is not None:
            fields.append("ip = ?")
            values.append(ip)
        if mac is not None:
            fields.append("mac = ?")
            values.append(mac)
        if ssid_24 is not None:
            fields.append("ssid_24 = ?")
            values.append(ssid_24)
        if ssid_5 is not None:
            fields.append("ssid_5 = ?")
            values.append(ssid_5)
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
        # Always update last_updated
        fields.append("last_updated = ?")
        values.append(datetime.datetime.now().isoformat())
        values.append(record_id)
        sql = f"UPDATE onu_info SET {', '.join(fields)} WHERE id = ?"
        c.execute(sql, values)
        conn.commit()
        logging.info(f"ONU record {record_id} updated successfully.")
    except Exception as e:
        logging.error(f"Failed to update ONU info for record {record_id}: {e}")

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

# Example usage:
# insert_onu_info("192.168.1.10", "AA:BB:CC:DD:EE:01", "HomeWiFi_24", "HomeWiFi_5", "pass24_1", "pass5_1", "manual")
display_onu_info()
# display_specific_onu_info(ssid_24="HomeWiFi_24")
# update_onu_info(1, ip="192.168.1.100", wlan_pwd_24="newpass24")