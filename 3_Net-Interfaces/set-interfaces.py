#!/usr/bin/python3
import os
import sys
import time
import subprocess
from pathlib import Path
import datetime
import re

#### Variables ####
config_file = "./vbox-net.conf"

#### Functions ####
def ensure_nat_network(vm, netname, network_range, nic_number):
    
    # Check network_range pattern (ex: 172.16.21.0/24)
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}$"
    if not re.match(pattern, network_range):
        print(f"Error: network_range '{network_range}' does not match the expected pattern IP/mask (e.g., 172.16.21.0/24)")
        sys.exit(1)

    result = subprocess.run(["VBoxManage", "natnetwork", "list"], stdout=subprocess.PIPE, text=True)
    if netname not in result.stdout:
        print(f"NAT network '{netname}' doesn't exist. Creating...")
        subprocess.run(["VBoxManage", "natnetwork", "add","--netname", netname, "--network", network_range,"--enable", "--dhcp", "on"])
        subprocess.run(["VBoxManage", "natnetwork", "start", "--netname", netname])
        subprocess.run(["VBoxManage", "modifyvm", vm, f"--nic{nic_number}", "natnetwork", f"--nat-network{nic_number}", netname])

    else:
        print(f"NAT network '{netname}' already exists.")


def set_interface(vm_name, lan_name, inet_type, network_range, nic_number):
    if(inet_type == "natnetwork"):
        ensure_nat_network(vm_name, lan_name, network_range, nic_number)
    elif(inet_type == "intnet"):
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--nic{nic_number}", "intnet", f"--intnet{nic_number}", lan_name])
        print(f"Interface {nic_number} of VM {vm_name} is set to internal network {lan_name}")
         

def handle_line(line):
    line = line.strip()
    line = line.split("|")

    vm_name = line[0]
    lan_name = line[1]
    inet_type = line[2]
    network_range = line[3]
    nic_number = line[4]

    set_interface(vm_name, lan_name, inet_type, network_range, nic_number)


#### Main ####
with open(config_file, "r") as config:
    start_time = int(time.time())
    try:
        for line in config:
            if line == "\n" or line.startswith('#'):
                continue
            handle_line(line)
    except Exception as e:
        print(f"Error while processing the file {config_file}: {e}\n")

    stop_time = int(time.time())
    run_time = str(datetime.timedelta(seconds=(stop_time - start_time)))
    print(f"#### Run Time {run_time} ####")
