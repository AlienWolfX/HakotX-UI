import http.client

def view_server(ip="127.0.0.1", port=80, path="/"):
    try:
        conn = http.client.HTTPConnection(ip, port, timeout=5)
        conn.request("GET", path)
        response = conn.getresponse()
        print(f"HTTP/{response.version/10:.1f} {response.status} {response.reason}")
        for header, value in response.getheaders():
            print(f"{header}: {value}")
        print("\n" + response.read().decode(errors="replace"))
        conn.close()
    except Exception as e:
        print(f"Error connecting to {ip}:{port} - {e}")

if __name__ == "__main__":
    # Example usage: view_server("192.168.1.1", 80)
    import sys
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
        view_server(ip, port)
    else:
        print("Usage: python ip_scanner.py <ip> [port]")