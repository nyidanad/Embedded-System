import time, serial, psutil, platform
from cpuinfo import get_cpu_info

# Serial port and baud rate
ser = serial.Serial('COM14', 115200)
mem = psutil.virtual_memory()
users = psutil.users()
cpu_info = get_cpu_info()
partititons = psutil.disk_partitions()
disk_usage = psutil.disk_usage('/')
net_info = psutil.net_if_addrs()
k = 1
print('Receiving data from PC...')

while(1):
  try:
    tx_data = ""

    # System info
    tx_data += f"000{k}\n"
    tx_data += f"{'-'*4} System info {'-'*4}\n\n"
    tx_data += f"System: {platform.system()} {platform.architecture()[0]}\n"
    tx_data += f"User:   {str(users[0].name)}\n"
    k += 1


    # CPU info
    tx_data += f"000{k}\n"
    tx_data += f"{'-'*5} CPU info {'-'*6}\n\n"
    tx_data += f"CPU: {cpu_info['brand_raw']}\n"
    tx_data += f"Arch.: {cpu_info['arch']}\n"
    tx_data += f"Cores: {cpu_info['family']}\n"
    tx_data += f"Threads: {cpu_info['count']}\n"
    k += 1


    # CPU threads
    range = 0
    tx_data += f"000{k}\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1), start=1):
      tx_data += f"Core {i}: {percentage}%\n"
      range += 1
      if (range == 6):
        k += 1
        tx_data += f"000{k}\n"
        range = 0
      

    # DISC info
    tx_data += f"{'-'*5} DISC info {'-'*5}\n\n"
    tx_data += f"total:   {round(disk_usage[0]/(1024**3))}Gb\n"
    tx_data += f"used:    {round(disk_usage[1]/(1024**3))}Gb\n"
    tx_data += f"free:    {round(disk_usage[2]/(1024**3))}Gb\n"
    tx_data += f"percent: {disk_usage[3]:.2f}%\n"
    k += 1


    # Partitions info
    tx_data += f"000{k}\n"
    tx_data += f"{'-'*5} PART info {'-'*5}\n\n"
    for i, particion in enumerate(partititons):
      tx_data += f"{particion[0]} | {particion[2]} | {particion[3]}\n"
    k += 1


    # Network info
    ans = {}
    for net in net_info.keys():
      tx_data += f"000{k}\n"
      tx_data += f"{'-'*5} NET info {'-'*5}\n"
      tx_data += f"> {net} <\n"
      for addr in net_info[net]:
        tx_data += f"IP: {addr.address}\n"
      
      k+= 1
    

    # Send the data over UART
    ser.write(tx_data.encode('utf-8'))
    print(tx_data)
    print('Data sent to UART')
    time.sleep(5)

  except Exception as e:
    print(str(e))