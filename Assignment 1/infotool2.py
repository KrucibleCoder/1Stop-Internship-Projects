import sys
import requests
import json
import socket

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def get_location_info(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) != 2:
        print("Usage: python infotool.py <websiteurl>")
        sys.exit(1)

    website_url = sys.argv[1]
    ip_address = get_ip_address(website_url)

    if ip_address is None:
        print(json.dumps({"error": "Could not resolve IP address for the given domain"}))
        sys.exit(1)

    location_info = get_location_info(ip_address)
    result = {
        "website_url": website_url,
        "ip_address": ip_address,
        "location_info": location_info
    }

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()