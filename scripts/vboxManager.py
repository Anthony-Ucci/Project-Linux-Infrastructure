#!/usr/bin/python3
import os
import sys
import time
import subprocess
import datetime

class VBoxManager:
    def __init__(self, config_file_path, vbox_dir="."):
        self.config_file_path = config_file_path
        self.vbox_dir = vbox_dir

    def clone_vm(self, vm, distro, ram):
        template = f"0-{distro}"
        cmd_list = [
            ["VBoxManage", "clonevm", template, "--name", vm, "--basefolder", self.vbox_dir, "--register"],
            ["VBoxManage", "modifyvm", vm, "--memory", ram],
        ]
        for cmd in cmd_list:
            subprocess.run(cmd, check=True)
        self.start_vm(vm)

    def start_vm(self, vm):
        cmd = ["VBoxManage", "startvm", vm, "--type", "headless"]
        subprocess.run(cmd, check=True)

    def shutdown_vm(self, vm):
        cmd = ["VBoxManage", "controlvm", vm, "acpipowerbutton"]
        subprocess.run(cmd, check=True)
        
    def poweroff_vm(self, vm):
        cmd = ["VBoxManage", "controlvm", vm, "poweroff"]
        subprocess.run(cmd, check=True)

    def undefine_vm(self, vm):
        self.poweroff_vm(vm)
        time.sleep(5)
        cmd = ["VBoxManage", "unregistervm", vm, "--delete"]
        subprocess.run(cmd, check=True)

    def trigger_request(self, request, line):
        line = line.strip()
        parts = line.split("|")
        if len(parts) < 3:
            print(f"Invalid configuration line: {line}")
            return
        vm = parts[0]
        distro = parts[1]
        ram = parts[2]
        
        if request == 'clone':
            self.clone_vm(vm, distro, ram)
        elif request == 'start':
            self.start_vm(vm)
        elif request == 'shutdown':
            self.shutdown_vm(vm)
        elif request == 'poweroff':
            self.poweroff_vm(vm)
        elif request == 'undefine':
            self.undefine_vm(vm)
        else:
            print("**** Usage: clone|start|shutdown|poweroff|undefine ****")
            sys.exit(22)
            
    def process(self, request):
        start_time = int(time.time())
        try:
            with open(self.config_file_path, "r") as config:
                for line in config:
                    if line.strip() == "" or line.strip().startswith('#'):
                        continue
                    self.trigger_request(request, line)
        except Exception as e:
            print(f"Error while processing the file {self.config_file_path}: {e}\n")
            sys.exit(1)

        stop_time = int(time.time())
        run_time = str(datetime.timedelta(seconds=(stop_time - start_time)))
        print(f"#### Run Time {run_time} ####")
