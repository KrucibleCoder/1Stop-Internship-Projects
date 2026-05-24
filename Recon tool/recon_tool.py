import os
import time
import random
import sys
import socket
import threading
import itertools
import requests
import pyqrcode
from queue import Queue
from barcode import EAN13
from barcode.writer import ImageWriter
from tqdm import tqdm
from pyfiglet import Figlet
import phonenumbers
from phonenumbers import carrier, geocoder
from tabulate import tabulate

def loading():
    for _ in tqdm(range(100), desc="LOADING...", ascii=False, ncols=75):
        time.sleep(0.01)

def font(text):
    cool_text = Figlet(font="slant")
    return str(cool_text.renderText(text))

def window_size(columns=120, height=30):
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.name == 'nt':
        os.system(f'mode con: cols={columns} lines={height}')

def find_my_ip():
    window_size()
    print(font("FIND MY IP"))
    loading()
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print(f"\nYour Device Name: {hostname}")
    print(f"Your IP Address : {IPAddr}")
    input("\nPress ENTER to return to menu...")

def password_generator():
    window_size()
    print(font("PASSWORD GENERATOR"))
    loading()
    length = int(input("\nEnter desired password length: "))
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#$%^&*()[]{}/?<>\|"
    password = ''.join(random.sample(chars, length))
    print(f"\nGenerated Password: {password}")
    input("\nPress ENTER to return to menu...")

def wordlist_generator():
    window_size()
    print(font("WORDLIST GENERATOR"))
    loading()
    chars = input("\nEnter letters/characters for wordlist: ")
    min_len = int(input("Enter minimum password length: "))
    max_len = int(input("Enter maximum password length: "))
    filename = input("Enter filename to save wordlist: ")
    
    with open(filename, 'w') as f:
        for length in range(min_len, max_len + 1):
            for combo in itertools.product(chars, repeat=length):
                f.write(''.join(combo) + '\n')
    print(f"\nWordlist saved as '{filename}'!")
    input("\nPress ENTER to return to menu...")

def barcode_generator():
    window_size()
    print(font("BARCODE GENERATOR"))
    loading()
    number = input("\nEnter 12 digit number (EAN13 requires 12 digits): ")
    if len(number) != 12 or not number.isdigit():
        print("Invalid input. Must be 12 digits.")
        return
    barcode = EAN13(number, writer=ImageWriter())
    filename = input("Enter filename to save barcode (without extension): ")
    barcode.save(filename)
    print(f"\nBarcode saved as {filename}.png!")
    input("\nPress ENTER to return to menu...")

def qr_generator():
    window_size()
    print(font("QR CODE GENERATOR"))
    loading()
    data = input("\nEnter data for QR Code: ")
    qr = pyqrcode.create(data)
    filename = input("Enter filename to save QR code (without extension): ")
    qr.png(f"{filename}.png", scale=8)
    print(f"\nQR Code saved as {filename}.png!")
    input("\nPress ENTER to return to menu...")

def phone_number_info():
    window_size()
    print(font("PHONE INFO"))
    loading()
    number = input("\nEnter phone number with country code (e.g., +14155552671): ")
    parsed = phonenumbers.parse(number)
    carrier_name = carrier.name_for_number(parsed, "en")
    region_name = geocoder.description_for_number(parsed, "en")
    print("\nPhone Number Information:")
    print(tabulate([["Carrier", carrier_name], ["Region", region_name]], headers=["Field", "Info"], tablefmt="grid"))
    input("\nPress ENTER to return to menu...")

def subdomain_scanner():
    window_size()
    print(font("SUBDOMAIN SCANNER"))
    loading()
    domain = input("\nEnter domain (e.g., example.com): ")
    subdomains = ["www", "mail", "ftp", "test", "blog", "dev"]
    found = []
    for sub in subdomains:
        url = f"http://{sub}.{domain}"
        try:
            requests.get(url)
            found.append(url)
        except requests.ConnectionError:
            pass
    if found:
        print("\nFound Subdomains:")
        for url in found:
            print(url)
    else:
        print("\nNo subdomains found!")
    input("\nPress ENTER to return to menu...")

def port_scanner():
    window_size()
    print(font("PORT SCANNER"))
    loading()
    target = input("\nEnter target IP or domain: ")
    ports = [21, 22, 80, 443, 3306, 8080]
    open_ports = []

    def scan_port(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        try:
            s.connect((target, port))
            open_ports.append(port)
            s.close()
        except:
            pass

    threads = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if open_ports:
        print("\nOpen Ports:")
        for port in open_ports:
            print(f"Port {port} is OPEN")
    else:
        print("\nNo open ports detected!")
    input("\nPress ENTER to return to menu...")

def ddos_attack_tool():
    window_size()
    print(font("DDOS ATTACK"))
    loading()
    print("\nCOMING SOON!")
    input("\nPress ENTER to return to menu...")

def main():
    while True:
        window_size()
        print(font("RECON TOOL"))
        print("1. My IP Address")
        print("2. Password Generator")
        print("3. Wordlist Generator")
        print("4. Barcode Generator")
        print("5. QR Code Generator")
        print("6. Phone Number Info")
        print("7. Subdomain Scanner")
        print("8. Port Scanner")
        print("9. DDOS Attack Tool")
        print("10. Exit\n")
        
        try:
            choice = int(input("Enter your choice >>> "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if choice == 1:
            find_my_ip()
        elif choice == 2:
            password_generator()
        elif choice == 3:
            wordlist_generator()
        elif choice == 4:
            barcode_generator()
        elif choice == 5:
            qr_generator()
        elif choice == 6:
            phone_number_info()
        elif choice == 7:
            subdomain_scanner()
        elif choice == 8:
            port_scanner()
        elif choice == 9:
            ddos_attack_tool()
        elif choice == 10:
            print("\nEXITTING PROGRAM...")
            sys.exit()
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
