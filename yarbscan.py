import os
os.system("clear")

import pyfiglet
from colorama import Fore, Back, Style, init
import time
import sys
import socket
import threading
import queue
import re

init()

# بانر
banner = pyfiglet.figlet_format("yarbScan")
print(Fore.RED + banner + Style.RESET_ALL)

# رسائل ترحيبية
text1 = "Welcome to my tool!"
text2 = "You can see the open and closed ports on the website."
text3 = "Simple and important tool.."

for text in [text1, text2, text3]:
    for char in text:
        sys.stdout.write(Fore.YELLOW + Back.BLUE + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.05)
    print("\n")

# قائمة الخيارات
menu = [
    "1. Scan Common Web Ports (show open only)",
    "2. Get Detailed Info about a Port",
    "3. Scan Specific Port",
    "4. Exit"
]
for item in menu:
    print(Fore.CYAN + item + Style.RESET_ALL)
    print()

common_ports = [
    20, 21, 22, 23, 25, 53, 80, 110, 143, 443,
    587, 993, 995, 3306, 3389, 8080
]

THREADS = 100
TIMEOUT = 3
RETRIES = 3

q = queue.Queue()

port_info = {
    20: {
        "name": "FTP Data",
        "description": "File Transfer Protocol - Data Transfer",
        "protocol": "TCP",
        "common_usage": "Used for transferring files in FTP sessions",
        "security_notes": "Usually requires authentication; can be vulnerable if misconfigured"
    },
    21: {
        "name": "FTP Control",
        "description": "File Transfer Protocol - Control",
        "protocol": "TCP",
        "common_usage": "Control commands for FTP",
        "security_notes": "Plaintext authentication; consider using FTPS or SFTP"
    },
    22: {
        "name": "SSH",
        "description": "Secure Shell - Encrypted remote login",
        "protocol": "TCP",
        "common_usage": "Secure remote management of systems",
        "security_notes": "Strong security if keys/passwords are well managed"
    },
    23: {
        "name": "Telnet",
        "description": "Unencrypted remote login protocol",
        "protocol": "TCP",
        "common_usage": "Remote management (legacy)",
        "security_notes": "Insecure; avoid usage over untrusted networks"
    },
    25: {
        "name": "SMTP",
        "description": "Simple Mail Transfer Protocol",
        "protocol": "TCP",
        "common_usage": "Sending email",
        "security_notes": "Can be abused for spam; use authentication"
    },
    53: {
        "name": "DNS",
        "description": "Domain Name System",
        "protocol": "UDP/TCP",
        "common_usage": "Domain name resolution",
        "security_notes": "Target for DNS spoofing and amplification attacks"
    },
    80: {
        "name": "HTTP",
        "description": "Hypertext Transfer Protocol",
        "protocol": "TCP",
        "common_usage": "Serving websites",
        "security_notes": "Traffic is unencrypted, vulnerable to sniffing"
    },
    110: {
        "name": "POP3",
        "description": "Post Office Protocol v3",
        "protocol": "TCP",
        "common_usage": "Retrieving email",
        "security_notes": "Usually replaced by IMAP or secured versions"
    },
    143: {
        "name": "IMAP",
        "description": "Internet Message Access Protocol",
        "protocol": "TCP",
        "common_usage": "Retrieving email",
        "security_notes": "Supports encrypted connections"
    },
    443: {
        "name": "HTTPS",
        "description": "HTTP Secure",
        "protocol": "TCP",
        "common_usage": "Encrypted web traffic",
        "security_notes": "Widely used, recommended for secure communication"
    },
    587: {
        "name": "SMTP (Submission)",
        "description": "Mail submission for outgoing email",
        "protocol": "TCP",
        "common_usage": "Sending email securely",
        "security_notes": "Supports encryption and authentication"
    },
    993: {
        "name": "IMAPS",
        "description": "IMAP over SSL",
        "protocol": "TCP",
        "common_usage": "Secure email retrieval",
        "security_notes": "Encrypted protocol"
    },
    995: {
        "name": "POP3S",
        "description": "POP3 over SSL",
        "protocol": "TCP",
        "common_usage": "Secure email retrieval",
        "security_notes": "Encrypted protocol"
    },
    3306: {
        "name": "MySQL",
        "description": "MySQL database system",
        "protocol": "TCP",
        "common_usage": "Database service",
        "security_notes": "Should be protected and not exposed publicly"
    },
    3389: {
        "name": "RDP",
        "description": "Remote Desktop Protocol",
        "protocol": "TCP",
        "common_usage": "Remote desktop access on Windows",
        "security_notes": "Target for brute force attacks; use VPN or MFA"
    },
    8080: {
        "name": "HTTP Alternate",
        "description": "Alternative HTTP port",
        "protocol": "TCP",
        "common_usage": "Web servers and proxies",
        "security_notes": "Same risks as HTTP"
    }
}

def check_port_precise(ip, port, retries=RETRIES, timeout=TIMEOUT):
    for _ in range(retries):
        try:
            s = socket.socket()
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            s.close()
            if result == 0:
                return True
        except:
            pass
    return False

def scan_ports(ip, show_closed=False):
    while not q.empty():
        port = q.get()
        is_open = check_port_precise(ip, port)
        if is_open:
            print(Fore.GREEN + f"[+] Port {port} is OPEN" + Style.RESET_ALL)
        else:
            if show_closed:
                print(Fore.RED + f"[-] Port {port} is CLOSED" + Style.RESET_ALL)
        q.task_done()

def valid_ip(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip)

def show_port_info(port):
    info = port_info.get(port, None)
    if info is None:
        print(Fore.CYAN + f"Port {port} Info:" + Style.RESET_ALL)
        print(" - Service Name: Unknown Service")
        print(" - Description: No description available")
        print(" - Protocol: Unknown")
        print(" - Common Usage: Unknown")
        print(" - Security Notes: None")
        return

    print(Fore.CYAN + f"Port {port} Info:" + Style.RESET_ALL)
    print(f" - Service Name: {info['name']}")
    print(f" - Description: {info['description']}")
    print(f" - Protocol: {info['protocol']}")
    print(f" - Common Usage: {info['common_usage']}")
    print(f" - Security Notes: {info['security_notes']}")

def main():
    choice = input(Fore.YELLOW + "\nChoose an option (1-4): " + Style.RESET_ALL).strip()

    if choice == "4":
        print(Fore.LIGHTBLACK_EX + "Exit." + Style.RESET_ALL)
        sys.exit()

    ip = input(Fore.LIGHTBLACK_EX + "Enter target IP: " + Style.RESET_ALL).strip()
    if not valid_ip(ip):
        print(Fore.RED + "Error: Invalid IP address." + Style.RESET_ALL)
        return

    if choice == "1":
        for port in common_ports:
            q.put(port)
        show_closed = False

        for _ in range(min(THREADS, q.qsize())):
            t = threading.Thread(target=scan_ports, args=(ip, show_closed))
            t.daemon = True
            t.start()

        q.join()
        print(Fore.YELLOW + "\nScan completed." + Style.RESET_ALL)

    elif choice == "2":
        try:
            port = int(input(Fore.LIGHTBLACK_EX + "Enter port number to get info: " + Style.RESET_ALL).strip())
            if port < 1 or port > 65535:
                raise ValueError
            show_port_info(port)
        except:
            print(Fore.RED + "Error: Invalid port number." + Style.RESET_ALL)

    elif choice == "3":
        try:
            port = int(input(Fore.LIGHTBLACK_EX + "Enter port number to scan: " + Style.RESET_ALL).strip())
            if port < 1 or port > 65535:
                raise ValueError
            is_open = check_port_precise(ip, port)
            if is_open:
                print(Fore.GREEN + f"[+] Port {port} is OPEN" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"[-] Port {port} is CLOSED" + Style.RESET_ALL)
        except:
            print(Fore.RED + "Error: Invalid port number." + Style.RESET_ALL)

    else:
        print(Fore.RED + "Error: Invalid option." + Style.RESET_ALL)

if __name__ == "__main__":
    main() 
