import random
import string
from scripts.sqlite_functions import insert_wifi_info, display_specific_wifi_info, display_wifi_info, update_wifi_info

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

for _ in range(5):
    ip = f"192.168.1.{random.randint(2, 254)}"
    wlan_24 = random_string()
    wlan_5 = random_string()
    wlan_pwd_24 = random_string(12)
    wlan_pwd_5 = random_string(12)
    source = "random_gen"
    insert_wifi_info(ip, wlan_24, wlan_5, wlan_pwd_24, wlan_pwd_5, source)

display_wifi_info()

display_specific_wifi_info(wlan_24=wlan_24)

update_wifi_info(1, wlan_pwd_24="newpassword24")