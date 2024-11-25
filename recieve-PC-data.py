import time, serial, psutil, platform
from cpuinfo import get_cpu_info

# Serial port and baud rate
ser = serial.Serial('COM12', 115200)
mem = psutil.virtual_memory()
print('Receiving data from PC...')

while(1):
  try:
    rx_data = ""

    # System info - '0001'
    rx_data += "0001\n"
    rx_data += f"System: {platform.system()} {platform.architecture()[0]}\n"
    rx_data += f"{str(psutil.users())}\n"

    # CPU info - '0002'
    rx_data += "0002\n"
    cpu_info = get_cpu_info()
    rx_data += f"CPU: {cpu_info['brand_raw']} {cpu_info['hz_actual_friendly']}\n"
    rx_data += f"Vendor: {cpu_info['vendor_id_raw']}\n"
    rx_data += f"Architecture: {cpu_info['arch']}\n"
    rx_data += f"Cores: {cpu_info['family']}\n"
    rx_data += f"Threads: {cpu_info['count']}\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1), start=1):
      rx_data += f"Core {i}: {percentage}%\n"
    rx_data += f"Total CPU Usage: {psutil.cpu_percent()}%\n"

    # Partitions info - '0003'
    rx_data += "0003\n"
    rx_data += f"{str(mem)}\n"
    rx_data += f"{str(psutil.disk_partitions())}\n"
    rx_data += f"{str(psutil.disk_usage('/'))}\n"

    # Network info - '0004'
    rx_data += "0004\n"
    rx_data += f"Network Interfaces:\n{psutil.net_if_addrs()}\n\r"

    # Send the data over UART
    ser.write(rx_data.encode('utf-8'))
    print('Data sent to UART')
    time.sleep(5)

  except Exception as e:
    print(str(e))