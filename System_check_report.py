
import platform
from datetime import datetime
import tabula
import socket
import json
import GPUtil
import subprocess ,sys
from xlwt import Workbook
import xlsxwriter
from pathlib import Path
import os
import psutil
#SERVER_IP = ''
#SERVER_PORT = 41000

CMD_MEMORY = 'wmic memorychip list full'

def sendDataToInfoServer(pc_data_dic):
    """
    This function sends the json to the manager.
    param all_packets: all the packets and their data
    type all_packets: list
    return: None
    rtype: None
    """
    # Create a non-specific UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER_IP, SERVER_PORT)
    #  Creating JSON and sending
    data = json.dumps(pc_data_dic)
    try:
        sock.sendto(str.encode(data), server_address)
    except ConnectionError as e:
        print("failed to send pc info:",str(e))
    finally:
        sock.close()
    print("pc info data sent ok")


def getSize(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return "{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def operatingSystemInformation():
    os_data = []
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print("System: {uname.system}")
    os_data.append(uname.system)
    print("Node Name: {uname.node}")
    os_data.append(uname.node)
    print("Release: {uname.release}")
    os_data.append(uname.release)
    print("Version: {uname.version}")
    os_data.append(uname.version)
    print("Machine: {uname.machine}")
    os_data.append(uname.machine)
    print("Processor: {uname.processor}")
    os_data.append(uname.processor)
    return os_data


def computerName():
    comp_name = platform.node()
    return str(platform.node())


def bootTime():
    # Boot Time
    print("="*40, "Boot Time", "="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    boot_time_str=("Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    return boot_time_str


def cpuInformation():
    cpu_data = []
    # let's print CPU information
    #print("="*40, "CPU Info", "="*40)
    #print(f"CPU Type: {platform.processor()}%")
    cpu_data.append(platform.processor())
    # number of cores
    #print("Physical cores:", psutil.cpu_count(logical=False))
    #print("Total cores:", psutil.cpu_count(logical=True))
    cpu_data.append(psutil.cpu_count(True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpu_data.append(cpufreq)
    #print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    #print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    #print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    #print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print("Core {i}: {percentage}%")
    #print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    #print(f"Total CPU Usage: {psutil.cpu_stats()}%")
    return cpu_data


def memoryInformation():
    memo_data = []
    # Memory Information
    #print("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    #print(f"Total: {getSize(svmem.total)}")
    memo_data.append(svmem.total)
    #print(f"Available: {getSize(svmem.available)}")
    #print(f"Used: {getSize(svmem.used)}")
    #print(f"Percentage: {svmem.percent}%")
    #print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    #print(f"Total: {getSize(swap.total)}")
    #print(f"Free: {getSize(swap.free)}")
    #print(f"Used: {getSize(swap.used)}")
    #print(f"Percentage: {swap.percent}%")

    return memo_data


def memorySpeed():
    #memo_process = subprocess.run('wmic memorychip list full')
    memo_process = "wmic memorychip list full"
    result = subprocess.getoutput(memo_process)
    memo_list = result.split('\n')
    memo_list = list(filter(None, memo_list))
    print(memo_list[15] , memo_list[22])
    return memo_list[15],memo_list[22]


def diskInformation():
    global disk_type
    obj_Disk = psutil.disk_usage('/')
    total_size = (obj_Disk.total / (1024.0 ** 3))
    used_size = (obj_Disk.used / (1024.0 ** 3))
    free_space = (obj_Disk.free / (1024.0 ** 3))
    print(obj_Disk.percent)
    print('total_size = %s' % total_size)
    print('free_size = %s' % free_space)
    # Disk Information
    print("="*40, "Disk Information", "="*40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print("=== Device: {partition.device} ===")
        print("  Mountpoint: {partition.mountpoint}")
        print("  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print("  Total Size: {getSize(partition_usage.total)}")
            print("  Used: {getSize(partition_usage.used)}")
            print("  Free: {getSize(partition_usage.free)}")
            print("  Percentage: {partition_usage.percent}%")
        except PermissionError as e:
            # this can be catched due to the disk that
            # isn't ready
            print("DISK ERROR",str(e))
            continue

    # get IO statistics since boot
    process = subprocess.Popen(["powershell.exe",'Get-PhysicalDisk | Select MediaType'],stdout=subprocess.PIPE)
    result = str(process.communicate()[0]).split('\\')
    for d in result:
        if (d.find('nHDD')==0 or d.find('SSD')==0):
            disk_type = d
            print("disk type: ", disk_type[1:-1])
        else:
            disk_type='NA'
    disk_io = psutil.disk_io_counters()
    #print(f"Total read: {getSize(disk_io.read_bytes)}")
    #print(f"Total write: {getSize(disk_io.write_bytes)}")
    return disk_type, total_size, used_size


def networkInformation():
    network_summary = []
    # Network information
    print("="*40, "Network Information", "="*40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print("=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print("  IP Address: {address.address}")
                network_summary.append(address.address)
                print("  Netmask: {address.netmask}")
                network_summary.append(address.netmask)
                print("  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print("  MAC Address: {address.address}")
                network_summary.append(address.address)
                print("  Netmask: {address.netmask}")
                print("  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print("Total Bytes Sent: {getSize(net_io.bytes_sent)}")
    print("Total Bytes Received: {getSize(net_io.bytes_recv)}")
    return network_summary


def collectVideoCard_Info():
    # GPU information
    print("="*40, "GPU Details", "="*40)
    try:
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            # get the GPU id
            gpu_id = gpu.id
            # name of GPU
            gpu_name = gpu.name
            # get % percentage of GPU usage of that GPU
            gpu_load = "{gpu.load * 100}%"
            # get free memory in MB format
            gpu_free_memory = "{gpu.memoryFree}MB"
            # get used memory
            gpu_used_memory = "{gpu.memoryUsed}MB"
            # get total memory
            gpu_total_memory = "{gpu.memoryTotal}MB"
            # get GPU temperature in Celsius
            gpu_temperature = "{gpu.temperature} C"
            gpu_uuid = gpu.uuid
            list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                gpu_total_memory, gpu_temperature, gpu_uuid
            ))
        print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                               "temperature", "uuid")))
    except:
        print("GPU ERROR")


def retriveSerialTagNumber():
    cmd_command = 'wmic bios get serialnumber'
    tag = subprocess.getoutput(cmd_command).split('\n')
    return tag[2]


def collectSystemInfo():
    info_data = []
    sn = retriveSerialTagNumber()
    info_data.append(sn)
    os = operatingSystemInformation()
    info_data.append(os)
    boot_time = bootTime()
    cpu = cpuInformation()
    info_data.append(cpu)
    memory_data = memoryInformation()
    info_data.append(memory_data)
    storage = diskInformation()
    info_data.append(storage)
    network = networkInformation()
    info_data.append(network)
    try:
        display = collectVideoCard_Info()
        info_data.append(display)
        #print(os, boot_time, cpu, memory_data, storage, network, display)
    except:
        display = "VIDEO CARD ERROR"
        #print("no VIDEO CARD found")
        info_data.append(display)
    return info_data


