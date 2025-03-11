#!/usr/bin/env python3
import sys
import subprocess

def run(cmd, ignore_error=False):
    """Exécute une commande shell et gère les erreurs."""
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode and not ignore_error:
        print(f"Error executing: {cmd}")
        sys.exit(result.returncode)

def stop_virtualbox_processes():
    """Arrête les processus VirtualBox avant de décharger les modules."""
    print("Stopping VirtualBox processes...")
    subprocess.run("sudo pkill -f VirtualBox", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run("sudo pkill -f VBoxSVC", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run("sudo pkill -f VBoxHeadless", shell=True, stderr=subprocess.DEVNULL)

def switch_to_virtualbox():
    """Active VirtualBox et désactive KVM."""
    run("sudo systemctl disable --now libvirtd || true")
    run("sudo modprobe -r kvm_intel 2>/dev/null || sudo modprobe -r kvm_amd 2>/dev/null")
    run("sudo modprobe vboxdrv")
    run("sudo modprobe vboxnetflt")
    run("sudo modprobe vboxnetadp")
    print("Switched to VirtualBox mode.")

def switch_to_kvm():
    """Active KVM et désactive VirtualBox."""
    stop_virtualbox_processes()
    run("sudo modprobe -r vboxnetadp 2>/dev/null || true")  
    run("sudo modprobe -r vboxnetflt 2>/dev/null || true")
    run("sudo modprobe -r vboxdrv 2>/dev/null || true")
    run("sudo modprobe kvm_intel 2>/dev/null || sudo modprobe kvm_amd 2>/dev/null")
    run("sudo systemctl enable --now libvirtd || true")
    print("Switched to KVM mode.")

def check_status():
    """Affiche l'état des modules chargés."""
    print("\nModules VirtualBox chargés :")
    subprocess.run("lsmod | grep vbox || echo 'Aucun module VirtualBox actif.'", shell=True)
    
    print("\nModules KVM chargés :")
    subprocess.run("lsmod | grep kvm || echo 'Aucun module KVM actif.'", shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1].lower() not in ("virtualbox", "kvm"):
        print("Usage: {} <virtualbox|kvm>".format(sys.argv[0]))
        sys.exit(1)

    provider = sys.argv[1].lower()
    if provider == "virtualbox":
        switch_to_virtualbox()
    else:
        switch_to_kvm()
    
    check_status()  # Affiche l'état après l'exécution
