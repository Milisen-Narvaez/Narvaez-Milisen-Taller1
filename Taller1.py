import psutil
import platform
import os
import socket

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_network_usage():
    network = psutil.net_io_counters()
    return network.bytes_sent, network.bytes_recv

def get_temperature():
    if platform.system().lower() == 'linux':
        # Check if 'sensors' command is available
        if os.system('command -v sensors >/dev/null 2>&1') == 0:
            temperature_info = os.popen('sensors').read()
            # Extract CPU temperature (assuming it's in Celsius)
            temperature_lines = [line for line in temperature_info.split('\n') if 'Core 0' in line]
            if temperature_lines:
                return float(temperature_lines[0].split('+')[1].split('°C')[0].strip())
    return None

def get_remote_system_info(ip_address):
    try:
        # Create a socket connection to the remote machine
        with socket.create_connection((ip_address, 22), timeout=5) as s:
            # You can add more commands or information retrieval here if needed
            remote_system_info = s.recv(1024)
            return remote_system_info.decode('utf-8')
    except Exception as e:
        print(f"Error connecting to {ip_address}: {e}")
        return None

def main():
    # Local machine information
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    network_usage = get_network_usage()
    temperature = get_temperature()

    print("Local Machine:")
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")
    print(f"Network Usage: Sent {network_usage[0]} bytes, Received {network_usage[1]} bytes")

    if temperature is not None:
        print(f"CPU Temperature: {temperature}°C")
    else:
        print("Unable to retrieve CPU temperature.")

    # Remote machine information
    remote_ips = ['10.3.21.192', '10.3.21.193']
    for remote_ip in remote_ips:
        print(f"\nRemote Machine ({remote_ip}):")
        remote_system_info = get_remote_system_info(remote_ip)
        if remote_system_info is not None:
            print(f"System Information: {remote_system_info}")

if _name_ == "_main_":
    main()
