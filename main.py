#!/usr/bin/env python3
import sys
import os
import subprocess
from scripts import switchHypervisor, checkCommands
from scripts.virtualbox import manageVms, setInterfaces, setupGateway

def check_command(cmd):
    """Check if a command is available in the system."""
    try:
        subprocess.run([cmd, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <hypervisor>")
        sys.exit(1)
    
    hypervisor = sys.argv[1]


    print("--- 1 --- Checking prerequisites...")
    if not check_command("vagrant"):
        sys.stderr.write("Vagrant is not installed. Exiting.\n")
        sys.exit(1)
    if not check_command("ansible-playbook"):
        sys.stderr.write("Ansible is not installed. Exiting.\n")
        sys.exit(1)
    print("Dependencies OK.")


    print("--- 2 --- Switching hypervisor provider...")
    switchHypervisor.switch_provider(hypervisor)


    print("--- 3 --- Creating VMs (Vagrant + Ansible)...")
    vagrant_dir = os.path.join(os.getcwd(), "vagrant")
    subprocess.run(["vagrant", "up", "--provider", hypervisor], cwd=vagrant_dir, check=True)
    subprocess.run(["vagrant", "halt"], cwd=vagrant_dir, check=True)


    # 4) Setting up VMs (Cloning)
    # Assuming you have different functions based on the hypervisor in manage_vms
    vm_scripts_dir = os.path.join(os.getcwd(), "scripts", hypervisor)
    # If you prefer to use the same module, you might pass the directory as a parameter.
    manage_vms.clone_vms(vm_scripts_dir)
    manage_vms.shutdown_vms(vm_scripts_dir)


    # 5) Setting network interfaces on VMs
    set_interfaces.configure_interfaces()

    print("All tasks completed successfully.")

if __name__ == "__main__":
    main()
