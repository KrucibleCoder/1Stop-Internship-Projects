import sys
import socket
import requests
import json

def get_ip_address(website):
    try:
        ip_address = socket.gethostbyname(website)
        return ip_address
    except socket.gaierror:
        print("Invalid website URL.")
        sys.exit()

def get_location(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error retrieving location information:", e)
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python infotool.py <websiteurl>")
        sys.exit()

    website = sys.argv[1]
    ip_address = get_ip_address(website)
    print(f"IP Address of {website}: {ip_address}")

    location_info = get_location(ip_address)
    print(json.dumps(location_info, indent=4))