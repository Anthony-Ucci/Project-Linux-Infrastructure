#!/usr/bin/env python3
from pathlib import Path
import sys
from scripts import checkCommands, setInterfaces, setupGateway
from scripts.vboxManager import VBoxManager
from vagrant.vagrantManager import VagrantManager


VBOX_MGMT_CONF =  "./conf/vbox_manager.conf"
NETI_MGMT_CONF =  "./conf/vbox_net.conf"
VBOX_DIR = f"{Path.home()}/Documents/formation/VirtualBox" 
VAGRANT_DIR = "./vagrant/"

PROGRAM_DEPENDENCIES = ["VBoxManage", "vagrant", "ansible"]


def main(): 
    print("--- 1 --- Checking prerequisites...")
    for dep in PROGRAM_DEPENDENCIES:
        try:
            checkCommands.check(dep)
        except Exception as e:
            sys.exit(1)
    print("Dependencies OK.")

    print("--- 2 --- Creating VMs (Vagrant + Ansible)...")
    vagrant = VagrantManager(vagrant_dir=VAGRANT_DIR)
    vagrant.up()
    vagrant.halt()

    print("--- 3 --- Setting up VMs (Cloning)...")
    manager = VBoxManager(VBOX_MGMT_CONF, VBOX_DIR)
    manager.process("clone")

    # print("--- 5 --- Setting network interfaces on VMs...")
    # setInterfaces.process(NETI_MGMT_CONF)

    # print("--- 6 --- Configuring the gateway...")
    # setupGateway.process()

    print("All tasks completed successfully.")

if __name__ == "__main__":
    main()
