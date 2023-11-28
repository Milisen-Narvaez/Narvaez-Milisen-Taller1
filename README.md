# Narvaez-Milisen-Taller1
Taller en Clases, sobre el rendimiento del computador
import psutil
import platform
import os


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


def main():
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    network_usage = get_network_usage()
    temperature = get_temperature()

    print(f"Rendimiento del CPU : {cpu_usage}%")
    print(f"Rendimiento de la Memoria: {memory_usage}%")
    print(f"Network Usage: Sent {network_usage[0]} bytes, Received {network_usage[1]} bytes")

    if temperature is not None:
        print(f"CPU Temperature: {temperature}°C")
    else:
        print("Unable to retrieve CPU temperature.")


if __name__ == "__main__":
    main()
