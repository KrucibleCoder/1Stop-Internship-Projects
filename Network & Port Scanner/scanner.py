import argparse
import nmap
import socket
import requests
from concurrent.futures import ThreadPoolExecutor

# Function to detect live hosts
def detect_live_hosts(ip_range):
    nm = nmap.PortScanner()
    print(f"Scanning for live hosts in range: {ip_range}")
    nm.scan(hosts=ip_range, arguments='-sn')  # -sn flag for host discovery
    live_hosts = []
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            live_hosts.append(host)
    return live_hosts

# Function to check open ports on a host
def check_ports(host):
    open_ports = []
    print(f"Scanning ports for {host}")
    for port in range(20, 1025):  # Scanning ports from 20 to 1024
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # 1 second timeout for each port
            result = s.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

# Function to check if a port is open on a host using requests (only for HTTP/HTTPS)
def check_http_ports(host):
    http_ports = []
    for port in [80, 443]:  # Checking common HTTP/HTTPS ports
        url = f"http://{host}:{port}"
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                http_ports.append(port)
        except requests.exceptions.RequestException:
            continue
    return http_ports

# Function to run port scans concurrently
def scan_ports_concurrently(live_hosts):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(check_ports, live_hosts)
    return dict(zip(live_hosts, results))

# Main function to parse arguments and run the scans
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Network and Port Scanner')
    parser.add_argument('ip_range', help='IP range or subnet to scan for live hosts (e.g., 192.168.1.0/24)')
    args = parser.parse_args()

    # Step 1: Detect live hosts
    live_hosts = detect_live_hosts(args.ip_range)
    if not live_hosts:
        print("No live hosts found.")
        return

    print(f"Live hosts detected: {live_hosts}")

    # Step 2: Scan ports concurrently for live hosts
    port_scan_results = scan_ports_concurrently(live_hosts)

    # Step 3: Display the results
    for host, open_ports in port_scan_results.items():
        if open_ports:
            print(f"{host} has open ports: {open_ports}")
        else:
            print(f"{host} has no open ports.")

    # Optionally, check HTTP ports (80/443) using requests
    for host in live_hosts:
        http_ports = check_http_ports(host)
        if http_ports:
            print(f"{host} has open HTTP/HTTPS ports: {http_ports}")

if __name__ == "__main__":
    main()
