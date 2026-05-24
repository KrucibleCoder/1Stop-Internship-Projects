import os
import time
import random
import itertools
import sys
import pyqrcode
from barcode import EAN13
from queue import Queue
import socket
import threading
from barcode.writer import ImageWriter
import phonenumbers
from phonenumbers import carrier, geocoder
import requests
from tabulate import tabulate

# Function for IP Scanner
def ip_scanner(ip):
    print(f"Scanning IP: {ip}")
    try:
        hostname = socket.gethostbyaddr(ip)
        print(f"Hostname: {hostname[0]}")
    except socket.herror:
        print("Could not resolve IP.")

# Function for Port Scanner
def port_scanner(ip, ports):
    print(f"Scanning ports on {ip}...")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open.")
        sock.close()

# Function for Barcode Generator
def generate_barcode(data):
    barcode_obj = EAN13(data, writer=ImageWriter())
    barcode_obj.save("barcode")
    print("Barcode saved as barcode.png")

# Function for QR Code Generator
def generate_qrcode(data):
    qr = pyqrcode.create(data)
    qr.png("qrcode.png", scale=6)
    print("QR Code saved as qrcode.png")

# Function for Password Generator
def generate_password(length=12):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()?"
    password = ''.join(random.choice(chars) for _ in range(length))
    print(f"Generated password: {password}")

# Function for Wordlist Generator
def generate_wordlist(word, length=5):
    permutations = itertools.permutations(word, length)
    wordlist = [''.join(p) for p in permutations]
    print("\n".join(wordlist[:10]))  # Display first 10 words

# Function for Phone Number Information Gathering
def phone_info(phone_number):
    parsed_number = phonenumbers.parse(phone_number)
    carrier_info = carrier.name_for_number(parsed_number, "en")
    geo_info = geocoder.description_for_number(parsed_number, "en")
    print(f"Carrier: {carrier_info}, Location: {geo_info}")

# Function for Subdomain Checker
def subdomain_checker(domain, subdomains):
    print(f"Checking subdomains for {domain}")
    for sub in subdomains:
        full_url = f"http://{sub}.{domain}"
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                print(f"Active subdomain found: {full_url}")
        except requests.exceptions.RequestException:
            pass

# Placeholder for DDos Tool
def ddos_attack():
    print("Coming soon")

# Menu
def main():
    while True:
        print("\nRecon & Info Gathering Tool")
        options = [
            "1. IP Scanner", "2. Port Scanner", "3. Barcode Generator",
            "4. QRCode Generator", "5. Password Generator", "6. Wordlist Generator",
            "7. Phone Number Info", "8. Subdomain Checker", "9. DDos Attack", "0. Exit"
        ]
        print(tabulate([[opt] for opt in options], tablefmt="fancy_grid"))

        choice = input("Enter your choice: ")
        if choice == "1":
            ip = input("Enter IP: ")
            ip_scanner(ip)
        elif choice == "2":
            ip = input("Enter IP: ")
            ports = list(map(int, input("Enter ports separated by space: ").split()))
            port_scanner(ip, ports)
        elif choice == "3":
            data = input("Enter numeric data (12 digits): ")
            generate_barcode(data)
        elif choice == "4":
            data = input("Enter data for QR Code: ")
            generate_qrcode(data)
        elif choice == "5":
            length = int(input("Enter password length: "))
            generate_password(length)
        elif choice == "6":
            word = input("Enter base word: ")
            length = int(input("Enter max length of permutations: "))
            generate_wordlist(word, length)
        elif choice == "7":
            phone_number = input("Enter phone number with country code: ")
            phone_info(phone_number)
        elif choice == "8":
            domain = input("Enter domain: ")
            subdomains = input("Enter subdomains separated by space: ").split()
            subdomain_checker(domain, subdomains)
        elif choice == "9":
            ddos_attack()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()