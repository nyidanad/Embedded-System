import time, serial, psutil, platform
from cpuinfo import get_cpu_info

# Serial port and baud rate
ser = serial.Serial('COM14', 115200)
mem = psutil.virtual_memory()
users = psutil.users()
cpu_info = get_cpu_info()
partititons = psutil.disk_partitions()
disk_usage = psutil.disk_usage('/')
print('Receiving data from PC...')

# rx_data += f"RAM: {str(mem)}\n"

while(1):
  try:
    rx_data = ""

    # System info - '0001'
    rx_data += "0001\n"
    rx_data += f"{'-'*4} System info {'-'*4}\n\n"
    rx_data += f"System: {platform.system()} {platform.architecture()[0]}\n"
    rx_data += f"User:   {str(users[0].name)}\n"

    # CPU info - '0002'
    rx_data += "0002\n"
    rx_data += f"{'-'*5} CPU info {'-'*6}\n\n"
    rx_data += f"CPU: {cpu_info['brand_raw']}\n"
    rx_data += f"Arch.: {cpu_info['arch']}\n"
    rx_data += f"Cores: {cpu_info['family']}\n"
    rx_data += f"Threads: {cpu_info['count']}\n"

    # CPU threads - '0003'
    rx_data += "0003\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1), start=1):
      rx_data += f"Core {i}: {percentage}%\n"

    # Partitions info - '0004'
    rx_data += "0004\n"
    rx_data += f"{'-'*5} DISC info {'-'*5}\n\n"
    rx_data += f"total:   {round(disk_usage[0]/(1024**3))}Gb\n"
    rx_data += f"used:    {round(disk_usage[1]/(1024**3))}Gb\n"
    rx_data += f"free:    {round(disk_usage[2]/(1024**3))}Gb\n"
    rx_data += f"percent: {disk_usage[3]:.2f}%\n"
    rx_data += f"{str(psutil.disk_partitions())}\n"
    # print(f"{str(psutil.disk_partitions())}\n")

    # Network info - '0005'
    rx_data += "0005\n"
    rx_data += f"Network Interfaces:\n{psutil.net_if_addrs()}\n\r"

    # Send the data over UART
    ser.write(rx_data.encode('utf-8'))
    print('Data sent to UART')
    time.sleep(5)

  except Exception as e:
    print(str(e))