import http.client

def get_server_software(ip="127.0.0.1", port=80, path="/"):
    try:
        conn = http.client.HTTPConnection(ip, port, timeout=5)
        conn.request("GET", path)
        response = conn.getresponse()
        server_header = dict(response.getheaders()).get("Server", None)
        if server_header:
            print(f"Server software at {ip}:{port} is: {server_header}")
        else:
            print(f"No Server header found at {ip}:{port}.")
        conn.close()
    except Exception as e:
        print(f"Error connecting to {ip}:{port} - {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
        get_server_software(ip, port)
    else:
        print("Usage: python ip_scanner.py <ip> [port]")