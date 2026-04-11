import ipaddress
import platform
import subprocess
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from platform import system




def get_IP_range():
    while True:
        start_ip = input("Enter the starting IP address: ").strip()
        end_ip = input("Enter the ending IP address: ").strip()
        
        try:
            start_ip_obj = ipaddress.IPv4Address(start_ip)
            end_ip_obj = ipaddress.IPv4Address(end_ip)
            
            if start_ip_obj > end_ip_obj:
                print("Starting IP address must be less than or equal to ending IP address. Please try again.")
                continue
            
            return start_ip_obj, end_ip_obj
        except ipaddress.AddressValueError:
            print("Invalid IP address format. Please enter valid IPv4 addresses.")
            
def generate_ip_list(start_ip, end_ip):
    return [ipaddress.IPv4Address(ip) for ip in range(int(start_ip), int(end_ip) + 1)] 
    
def ping_ip(ip):
  
    device_OS = platform.system().lower()

    if device_OS == "windows":
        command = ["ping", "-n", "1", "-w", "1000", str(ip)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip)]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        print(f"{ip} is active.")
        return str(ip), True
    else:
        print(f"{ip} is inactive.")
        return str(ip), False


def main():
    
    print("----------------------------------")
    print("Welcome to the IP Scanner!")
    print("This program will scan a range of IP addresses and report which ones are active.")
    print("----------------------------------")
    
    input_choice = input("Do you want to scan a range of IP addresses? (y/n): ")
    if input_choice.lower()==str('y'):
        start_IP, end_IP = get_IP_range()
        start_time = datetime.now()
        print (f"***********{start_time}***********")
        ip_list = generate_ip_list(start_IP, end_IP)
        
        active_hosts = []
        inactive_hosts = []
    
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = list(executor.map(ping_ip, ip_list))
            active_hosts = [ip for ip, is_active in results if is_active]
            inactive_hosts = [ip for ip, is_active in results if not is_active]
            
            print(f"Active hosts: {len(active_hosts)}")
                
    elif input_choice.lower()==str('n'):
        print("Exiting the program.")
    else:
        print("Invalid choice. Please try again.")
        main()
if __name__ == "__main__":
    main()