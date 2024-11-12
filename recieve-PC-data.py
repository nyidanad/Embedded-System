import time
import serial
import psutil
from cpuinfo import get_cpu_info
import platform

# serial port and baud rate
ser = serial.Serial('COM10', 115200)
mem = psutil.virtual_memory()

print("--- SYSTEM ---")
print(f"{platform.system()} {platform.architecture()[0]}")
print("\n--- CPU ---")
print(f"brand:\t {get_cpu_info()['brand_raw']} {get_cpu_info()['hz_actual_friendly']}")
print(f"vendor:\t {get_cpu_info()['vendor_id_raw']}")
print(f"arch:\t {get_cpu_info()['arch']}")
print(f"cores:\t {get_cpu_info()['family']}")
print(f"threads: {get_cpu_info()['count']}")
print("\nCPU Usage/Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1), start=1):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

print("\n--- VRAM ---")
print(mem)

print("\n--- PARTICIONS ---")
print(psutil.disk_partitions())

print("\n--- DISK USAGE ---")
print(psutil.disk_usage('/'))

print("\n--- USER(S) ---")
print(psutil.users())

print("\n--- NET ----")
