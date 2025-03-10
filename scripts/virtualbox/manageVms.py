#!/usr/bin/python3
import os
import sys
import time
import subprocess
from pathlib import Path
import datetime

# Variables
home_dir = Path.home()
config_file = "./vbox-manager.conf"  
vbox_dir = f"{home_dir}/Documents/formation/VirtualBox" 


def clone_vm(vm, distro, ram):
    template = f"0-{distro}"

    cmd_list = [
        ["VBoxManage", "clonevm", template, "--name", vm, "--basefolder", vbox_dir, "--register"],
        ["VBoxManage", "modifyvm", vm, "--memory", ram],
    ]
    for cmd in cmd_list:
        subprocess.run(cmd)
    start_vm(vm)

def start_vm(vm):
    cmd = ["VBoxManage", "startvm", vm, "--type", "headless"]
    subprocess.run(cmd)

def shutdown_vm(vm):
    cmd = ["VBoxManage", "controlvm", vm, "poweroff"]
    subprocess.run(cmd)

def undefine_vm(vm):
    shutdown_vm(vm)
    time.sleep(5)
    cmd = ["VBoxManage", "unregistervm", vm, "--delete"]
    subprocess.run(cmd)

def trigger_request(request, line):
    line = line.strip()
    line = line.split("|")
    
    vm = line[0]
    distro = line[1]
    ram = line[2] 
    
    if request == 'clone':
        clone_vm(vm, distro, ram)
    elif request == 'start':
        start_vm(vm)
    elif request == 'shutdown':
        shutdown_vm(vm)
    elif request == 'undefine':
        undefine_vm(vm)
    else:
        print("**** Usage: clone|start|shutdown|undefine ****")
        sys.exit(22)
        
def process(config_file_path, request):
    with open(config_file_path, "r") as config:
        start_time = int(time.time())
        try:
            for line in config:
                if line == "\n" or line.startswith('#'):
                    continue
                trigger_request(request, line)
        except Exception as e:
            print(f"Error while processing the file {config_file}: {e}\n")

        stop_time = int(time.time())
        run_time = str(datetime.timedelta(seconds=(stop_time - start_time)))
        print(f"#### Run Time {run_time} ####")


if __name__ == "__main__":
    try:
        request = sys.argv[1]
    except IndexError:
        print("**** Usage: clone|start|shutdown|undefine ****")
        sys.exit(22)
    process(config_file, request)
    



