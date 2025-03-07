#!/usr/bin/python3
import subprocess

GATEWAY = "gateway2"
LAN = "LAN21"
LOCAL_SSH_PORT = "2222"
RULE_NAME = "ssh"
PROTOCOL = "tcp"
REMOTE_PORT = "22"

def get_guest_ip():
    result = subprocess.run(
        ["VBoxManage", "guestproperty", "get", GATEWAY, "/VirtualBox/GuestInfo/Net/0/V4/IP"],
        stdout=subprocess.PIPE, text=True
    )
    guest_output = result.stdout.strip()
    return guest_output.split("Value:")[1].strip() if guest_output.startswith("Value:") else guest_output

def delete_port_forward():
    subprocess.run(["VBoxManage", "natnetwork", "modify", "--netname", LAN, "--port-forward-4", "delete", RULE_NAME])

def add_port_forward(ip_addr):
    rule = f"{RULE_NAME}:{PROTOCOL}:[]:{LOCAL_SSH_PORT}:[{ip_addr}]:{REMOTE_PORT}"
    subprocess.run(["VBoxManage", "natnetwork", "modify", "--netname", LAN, "--port-forward-4", rule])

def run_ansible():
    command = ["ansible-playbook", "-i", "inventory.ini", "playbook.yml"]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)

def main():
    ip_addr = get_guest_ip()
    print(f"IP address of {GATEWAY} is {ip_addr}")
    print(f"Adding port forwarding rule for {GATEWAY}...")
    delete_port_forward()
    add_port_forward(ip_addr)
    print(f"Port forwarding rule added for {GATEWAY}")
    
    print(f"Configuring the network for {GATEWAY}...")
    run_ansible()
    
    ip_addr = get_guest_ip()
    print(f"IP address of {GATEWAY} is {ip_addr}")
    print(f"Adding port forwarding rule for {GATEWAY}...")
    delete_port_forward()
    add_port_forward(ip_addr)
    print(f"Port forwarding rule added for {GATEWAY}")
    
    subprocess.run(["VBoxManage", "controlvm", GATEWAY, "poweroff"])

if __name__ == '__main__':
    main()
