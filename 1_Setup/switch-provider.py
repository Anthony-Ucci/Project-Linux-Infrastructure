#!/usr/bin/env python3
import sys, subprocess

def run(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode:
        print(f"Error executing: {cmd}")
        sys.exit(result.returncode)

def switch_virtualbox():
    run("sudo systemctl disable --now libvirtd || true")
    run("sudo modprobe -r kvm_intel 2>/dev/null || sudo modprobe -r kvm_amd 2>/dev/null")
    run("sudo modprobe vboxdrv")
    run("sudo modprobe vboxnetflt")
    print("Switched to VirtualBox mode.")

def switch_kvm():
    run("sudo modprobe -r vboxnetflt 2>/dev/null || true")
    run("sudo modprobe -r vboxdrv 2>/dev/null || true")
    run("sudo modprobe kvm_intel 2>/dev/null || sudo modprobe kvm_amd 2>/dev/null")
    run("sudo systemctl enable --now libvirtd || true")
    print("Switched to KVM mode.")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1].lower() not in ("virtualbox", "kvm"):
        print("Usage: {} <virtualbox|kvm>".format(sys.argv[0]))
        sys.exit(1)
    provider = sys.argv[1].lower()
    if provider == "virtualbox":
        switch_virtualbox()
    else:
        switch_kvm()
