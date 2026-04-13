import os
import sys
import subprocess
import platform
import re

# Checks host's OS and retrieves a list of available interfaces, then returns them as a list
def get_interface_names():
    os_type = platform.system()
    try:
        if os_type == "Windows":
            command = ["powershell", "-Command", "Get-NetAdapter | Select-Object -ExpandProperty Name"]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
            return [line.strip() for line in output.split('\n') if line.strip()]
        elif os_type == "Linux":
            command = ["ip", "-o", "link", "show"]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
            interfaces = re.findall(r'^\d+: ([^:]+):', output, re.MULTILINE)
            return interfaces
    except Exception as e:
        print(f"Error retrieving interface names: {e}")
        return []


def get_current_mac(interface):
    os_type = platform.system()
    
    try:
        if os_type == "Linux":
            output = subprocess.check_output(["ip", "link", "show", interface]).decode()
            mac_search = re.search(r"link/ether\s+([0-9a-fA-F:]{17})", output)
            
            if mac_search:
                return mac_search.group(1)
            
        elif os_type == "Windows":
            ps_command = f"(Get-NetAdapter -Name '{interface}').MacAddress"
            output = subprocess.check_output(["powershell", "-Command", ps_command], stderr=subprocess.STDOUT).decode().strip()
            mac_search = re.search(r"([0-9a-fA-F-]{17})", output)
            
            if mac_search:
                return mac_search.group(1).replace('-', ':')
            else:
                print(f"Could not find MAC address for interface {interface}. Please check the interface name and try again.")
                return None
            
    except Exception as e:
        print(f"Error retrieving MAC address: {e}")
        return None

def main():
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Welcome to Daniel's MAC ATTK (MAC Address Spoofer)!")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print('Would you like to "Get"/retrieve your current MAC address or "Spoof"/change it?')
    choice = input('choice (type "get" or "spoof"): ').lower()
    
    if choice == 'spoof':
        interface = input("Enter the network interface you want to spoof (e.g., eth0, wlan0, Ethernet): ")
        
        print("MAC address spoofing initiated.")
        current_mac = get_current_mac(interface)
        print(f"Current MAC address for:          {interface}: {current_mac}")
        continue_choice = input("Do you want to continue with spoofing? (y/n): ")
        if continue_choice.lower() == 'y':
            new_mac = input("Enter the new MAC address you want to use (format: XX:XX:XX:XX:XX:XX): ")
            print(f"Changing MAC address for {interface} to {new_mac}...")
            # Spoofing logic would go here (requires admin privileges and is OS-specific)
            operating_system = platform.system()
            
            if operating_system == "Linux":
                try:
                    subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
                    subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac], check=True)
                    subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
                    print("MAC address spoofing completed. Please verify the change using the 'Get' option.")
                except subprocess.CalledProcessError as e:
                    print(f"Error during MAC spoofing: {e}")
            elif operating_system == "Windows":
                print("MAC spoofing on Windows requires additional steps and may not be supported by all network adapters. Please refer to specific guides for your adapter model.")
            else:
                print("MAC spoofing is not supported on this operating system.")
                    
            print("MAC address spoofing completed. Please verify the change using the 'Get' option.")
        
    elif choice == 'get':
        interface = input("Enter the network interface (e.g., eth0, wlan0, Ethernet) Type 'Find interfaces' to get a list of available interfaces: ")
        
        if interface.lower() == "find interfaces" or interface.lower() == "find":
            interface_names = get_interface_names()
            
            if not interface_names:
                print("No interfaces found or error retrieving interfaces.")
                
            else:
                print("--------------------------------------------------")
                print("Available interfaces:")
                print() 
                for index, name in enumerate(interface_names, start=1):
                    print(f"{index}. {name}")
                print("--------------------------------------------------")
                selection = input("Enter the name or number of the interface you want to check the MAC address for: ")
                if selection.isdigit():
                    number_choice = int(selection)
                    if 1 <= number_choice <= len(interface_names):
                        interface = interface_names[number_choice - 1]
                    else:
                        print("Invalid selection. Please try again.")
                        return
                else:
                    interface = selection
                    
                current_mac = get_current_mac(interface)
                print(f"Current MAC address for:          {interface}: {current_mac}")
                quit_choice = input("Do you want to quit the program? (y/n): ")
                if quit_choice.lower() == 'y':
                    print("Exiting the program.")
                    sys.exit()
                else:
                    print("Returning to main menu.")
                    print("-----------------------------------------------------------------------------------------------")

                    main()
                            
                
        else:
            current_mac = get_current_mac(interface)
            print("-----------------------------------------------------------------------------------------------")
            print(f"Current MAC address for:          {interface}: {current_mac}")
            print("-----------------------------------------------------------------------------------------------")

    else:
        print("invalid choice. Please type 'Get' or 'Spoof'.")
        main()

if __name__ == "__main__":
    main()

