import sqlite3
import datetime
import logging

logging.basicConfig(filename="./logs/logs.txt", level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def insert_onu_info(ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source):
    last_updated = datetime.datetime.now().isoformat()
    try:
        c.execute(
            "SELECT id FROM onu_info WHERE ip=? AND ssid_24=? AND ssid_5=?",
            (ip, ssid_24, ssid_5)
        )
        result = c.fetchone()
        if result:
            update_onu_info(
                result[0],
                ip=ip,
                mac=mac,
                ssid_24=ssid_24,
                ssid_5=ssid_5,
                wlan_pwd_24=wlan_pwd_24,
                wlan_pwd_5=wlan_pwd_5,
                source=source
            )
            logging.info(f"{ip} ({mac}) duplicate found, updated existing record in onu_info database")
        else:
            c.execute(
                "INSERT INTO onu_info (ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated)
            )
            conn.commit()
            logging.info(f"{ip} ({mac}) has been added to the onu_info database")
    except Exception as e:
        logging.error(f"Failed to insert/update ONU info for {ip}: {e}")


def search_onu_info(search_text):
    try:
        query = """
            SELECT ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated
            FROM onu_info
            WHERE ip LIKE ? OR mac LIKE ? OR ssid_24 LIKE ? OR ssid_5 LIKE ?
        """
        like = f"%{search_text}%"
        c.execute(query, (like, like, like, like))
        rows = c.fetchall()
        return rows
    except Exception as e:
        logging.error(f"Failed to search ONU info: {e}")
        return []

def display_onu_info(return_rows=False):
    try:
        c.execute("""
            SELECT ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated
            FROM onu_info
        """)
        rows = c.fetchall()
        if return_rows:
            return rows
        for row in rows:
            print(row)
        logging.info("Displayed all ONU info records.")
    except Exception as e:
        logging.error(f"Failed to display ONU info: {e}")
        return []

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

def get_record_id_by_unique_fields(ip, mac, ssid_24):
    try:
        c.execute(
            "SELECT id FROM onu_info WHERE ip=? AND mac=? AND ssid_24=?",
            (ip, mac, ssid_24)
        )
        result = c.fetchone()
        if result:
            return result[0]
        return None
    except Exception as e:
        logging.error(f"Failed to get record id: {e}")
        return None

def delete_onu_info(record_id):
    """
    Delete a record from onu_info by its id.
    """
    try:
        c.execute("DELETE FROM onu_info WHERE id = ?", (record_id,))
        conn.commit()
        logging.info(f"Deleted ONU record {record_id}.")
        return True
    except Exception as e:
        logging.error(f"Failed to delete ONU info for record {record_id}: {e}")
        return False

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