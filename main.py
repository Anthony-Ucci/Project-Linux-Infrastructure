#!/usr/bin/env python3
import sys
import os
import subprocess
from scripts import switchHypervisor, checkCommands, manageVms, setInterfaces, setupGateway

vms_management_config_file =  "./conf/vbox_manager.conf"
neti_management_config_file =  "./conf/vbox_net.conf"

def main():
    # TODO Let the user choose the hypervisor
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <hypervisor>")
        sys.exit(1)
    
    hypervisor = sys.argv[1]

    # TODO Make it be handled by a specific service
    print("--- 1 --- Checking prerequisites...")
    if not checkCommands.check("vagrant"):
        sys.stderr.write("Vagrant is not installed. Exiting.\n")
        sys.exit(1)
    if not checkCommands.check("ansible-playbook"):
        sys.stderr.write("Ansible is not installed. Exiting.\n")
        sys.exit(1)
    print("Dependencies OK.")


    print("--- 2 --- Switching hypervisor provider...")
    # TODO Make it be handled by a specific service
    if hypervisor == "virtualbox":
        switchHypervisor.switch_to_virtualbox()
    #elif hypervisor == "libvirt":
        #switchHypervisor.switch_to_libvirt()
    else:
        print(f"Invalid hypervisor: {hypervisor}")
        sys.exit(1)


    print("--- 3 --- Creating VMs (Vagrant + Ansible)...")
    # TODO Make it be handled by a specific service (Vagrant service object)
    vagrant_dir = os.path.join(os.getcwd(), "vagrant")
    subprocess.run(["vagrant", "up", "--provider", hypervisor], cwd=vagrant_dir, check=True)
    subprocess.run(["vagrant", "halt"], cwd=vagrant_dir, check=True)


    print("--- 4 --- Setting up VMs (Cloning)...")
    # TODO Make it be handled by a specific service (service object)
    manageVms.process(vms_management_config_file, "clone")
    manageVms.process(vms_management_config_file, "shutdown")


    print("--- 5 --- Setting network interfaces on VMs...")
    # TODO Make it be handled by a specific service (service object)
    setInterfaces.process(neti_management_config_file)


    print("--- 6 --- Configuring the gateway...")
    # TODO Work with configuration files
    setupGateway.process()

    print("All tasks completed successfully.")

if __name__ == "__main__":
    main()
