import os
import socket
import random
import requests
import pyqrcode
import phonenumbers
import threading
from barcode import EAN13
from barcode.writer import ImageWriter
from phonenumbers import carrier, geocoder

# Output directory for generated PNG assets.
OUTPUT_DIR = "Generated PNG"

# IP Scanner
def ip_scanner(ip_range):
    print("Scanning IP range:", ip_range)
    for ip in ip_range:
        response = os.system(f"ping -c 1 {ip}")
        print(f"{ip} is {'up' if response == 0 else 'down'}")

# Port Scanner
def port_scanner(target_ip, ports):
    print("Scanning ports on:", target_ip)
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((target_ip, port))
        print(f"Port {port} is {'open' if result == 0 else 'closed'}")
        sock.close()

# Barcode Generator
# Save the barcode image into the generated PNG folder.
def generate_barcode(data, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    barcode = EAN13(data, writer=ImageWriter())
    output_path = os.path.join(OUTPUT_DIR, filename)
    barcode.save(output_path)
    print(f"Barcode saved as {output_path}")

# QR Code Generator
# Save the QR code image into the generated PNG folder.
def generate_qrcode(data, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    qr = pyqrcode.create(data)
    output_path = os.path.join(OUTPUT_DIR, filename)
    qr.png(output_path, scale=8)
    print(f"QR Code saved as {output_path}")

# Password Generator
def generate_password(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = "".join(random.choice(characters) for _ in range(length))
    print("Generated password:", password)

# Wordlist Generator
def generate_wordlist(words, filename):
    with open(filename, 'w') as file:
        file.write("\n".join(words))
    print(f"Wordlist saved as {filename}")

# Phone Number Information Gathering
def phone_number_info(phone_number):
    number = phonenumbers.parse(phone_number)
    carrier_name = carrier.name_for_number(number, "en")
    location = geocoder.description_for_number(number, "en")
    print(f"Carrier: {carrier_name}\nLocation: {location}")

# Subdomain Checker
def subdomain_checker(domain, subdomains):
    print("Checking subdomains for:", domain)
    for subdomain in subdomains:
        url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(url)
            print(f"Subdomain found: {url}" if response.status_code == 200 else f"Subdomain not found: {url}")
        except requests.ConnectionError:
            print(f"Subdomain not found: {url}")

# DDoS Attack Tool (Placeholder)
def ddos_attack_tool():
    print("COMING SOON")

# Example Usage
ip_range = ["192.168.1.1", "192.168.1.2"]
port_scanner("127.0.0.1", range(20, 25))
generate_barcode("123456789012", "barcode.png")
generate_qrcode("https://example.com", "qrcode.png")
generate_password(12)
generate_wordlist(["password1", "password2"], "wordlist.txt")
phone_number_info("+14155552671")
subdomain_checker("example.com", ["www", "mail", "ftp"])
ddos_attack_tool()