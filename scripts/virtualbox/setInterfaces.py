#!/usr/bin/python3
import sys
import time
import subprocess
import datetime
import re
import ipaddress

#### Variables ####
config_file = "./vbox-net.conf"

#### Functions ####
def ensure_nat_network(vm, netname, network_range, nic_number):
    # Check network_range pattern (ex: 172.16.21.0/24)
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}$"
    if not re.match(pattern, network_range):
        print(f"Error: network_range '{network_range}' does not match the expected pattern IP/mask (e.g., 172.16.21.0/24)")
        sys.exit(1)

    network = ipaddress.ip_network(network_range, strict=False)
    netmask = str(network.netmask)
    all_hosts = list(network.hosts())

    if len(all_hosts) < 2:
        print("Network is too small to assign DHCP range.")
        sys.exit(1)

    server_ip = str(all_hosts[0])    # ex: "172.16.21.1"
    lower_ip  = str(all_hosts[4])    # ex: "172.16.21.5"
    upper_ip  = str(all_hosts[-1])   # ex: "172.16.21.254"

    result = subprocess.run(["VBoxManage", "natnetwork", "list"], stdout=subprocess.PIPE, text=True)
    if netname not in result.stdout:
        print(f"NAT network '{netname}' doesn't exist. Creating...")
    else:
        print(f"NAT network '{netname}' already exists. Recreating...")
        subprocess.run(["VBoxManage", "natnetwork", "stop", "--netname", netname])
        subprocess.run(["VBoxManage", "natnetwork", "remove", "--netname", netname])

    subprocess.run(["VBoxManage", "natnetwork", "add", "--netname", netname, "--network", network_range, "--enable", "--dhcp", "on"])
    subprocess.run(["VBoxManage", "natnetwork", "start", "--netname", netname])
    subprocess.run(["VBoxManage", "dhcpserver", "modify", "--network", netname, "--server-ip", server_ip, "--netmask", netmask, "--lower-ip", lower_ip, "--upper-ip", upper_ip, "--enable"])
    
    subprocess.run(["VBoxManage", "modifyvm", vm, f"--nic{nic_number}", "natnetwork", f"--nat-network{nic_number}", netname])


def set_interface(vm_name, lan_name, inet_type, network_range, nic_number):
    if inet_type == "natnetwork":
        ensure_nat_network(vm_name, lan_name, network_range, nic_number)
    elif inet_type == "intnet":
        subprocess.run(["VBoxManage", "modifyvm", vm_name, f"--nic{nic_number}", "intnet", f"--intnet{nic_number}", lan_name])
        print(f"Interface {nic_number} of VM {vm_name} is set to internal network {lan_name}")


def handle_line(line):
    parts = line.strip().split("|")
    vm_name, lan_name, inet_type, network_range, nic_number = parts
    set_interface(vm_name, lan_name, inet_type, network_range, nic_number)
    
def process(config_file_path):
    with open(config_file_path, "r") as config:
        start_time = int(time.time())
        try:
            for line in config:
                if not line.strip() or line.startswith('#'):
                    continue
                handle_line(line)
        except Exception as e:
            print(f"Error while processing the file {config_file_path}: {e}\n")
        stop_time = int(time.time())
        run_time = str(datetime.timedelta(seconds=(stop_time - start_time)))
        print(f"#### Run Time {run_time} ####")


#### Main ####
if __name__ == "__main__":
    process(config_file)
