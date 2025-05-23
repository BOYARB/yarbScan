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

banner = pyfiglet.figlet_format("yarbScan")
print(Fore.RED + banner + Style.RESET_ALL)

text1 = "Welcome to my tool!"
for char in text1:
    sys.stdout.write(Fore.BLUE + Back.LIGHTMAGENTA_EX + char + Style.RESET_ALL)
    sys.stdout.flush()
    time.sleep(0.1)
print()

text2 = "You can see the open ports on the website."
for char in text2:
    sys.stdout.write(Fore.YELLOW + Back.CYAN + char + Style.RESET_ALL)
    sys.stdout.flush()
    time.sleep(0.1)
print()

text3 = "Simple and important tool.."
for char in text3:
    sys.stdout.write(Fore.RED + Back.LIGHTWHITE_EX + char + Style.RESET_ALL)
    sys.stdout.flush()
    time.sleep(0.1)
print("\n")

important_ports = [
    80,
    443,
    8080,
    8000,
    8443,
    3000,
    5000,
    8888,
    9080,
    81,
    82,
    8008,
]

q = queue.Queue()

def scan(ip):
    while not q.empty():
        port = q.get()
        if check_port(ip, port):
            print(Fore.GREEN + f"[+] Port {port} is OPEN" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"[-] Port {port} is CLOSED" + Style.RESET_ALL)
        q.task_done()

def check_port(ip, port, retries=3):
    for _ in range(retries):
        try:
            s = socket.socket()
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            s.close()
            if result == 0:
                return True
        except:
            pass
    return False

def valid_ip(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip)

def main():
    sys.stdout.write(Fore.LIGHTBLACK_EX + "Enter target IP: " + Style.RESET_ALL)
    target_ip = input().strip()

    if not target_ip or not valid_ip(target_ip):
        print(Fore.RED + "Error: Please enter a valid IP address." + Style.RESET_ALL)
        return

    for port in important_ports:
        q.put(port)

    thread_count = min(50, len(important_ports))
    for _ in range(thread_count):
        t = threading.Thread(target=scan, args=(target_ip,))
        t.daemon = True
        t.start()

    q.join()
    print(Fore.YELLOW + "Scan completed." + Style.RESET_ALL)

if __name__ == "__main__":
    main() 
