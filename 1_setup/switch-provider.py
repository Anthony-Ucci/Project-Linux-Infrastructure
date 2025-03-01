#!/usr/bin/env python3
import sys
import subprocess

def run_command(cmd):
    """Exécute une commande shell et affiche une erreur en cas de problème."""
    print(f"Exécution : {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de : {cmd}")
        sys.exit(result.returncode)

def activate_virtualbox():
    # Arrêter libvirt (si utilisé par KVM)
    run_command("sudo systemctl stop libvirtd")
    # Décharger les modules KVM
    run_command("sudo modprobe -r kvm_intel 2>/dev/null || sudo modprobe -r kvm_amd 2>/dev/null")
    # Charger les modules VirtualBox
    run_command("sudo modprobe vboxdrv")
    run_command("sudo modprobe vboxnetflt")
    print("Passage en mode VirtualBox terminé.")

def activate_kvm():
    # Décharger les modules VirtualBox
    run_command("sudo modprobe -r vboxnetflt")
    run_command("sudo modprobe -r vboxdrv")
    # Charger les modules KVM (en choisissant celui adapté à votre CPU)
    run_command("sudo modprobe kvm_intel 2>/dev/null || sudo modprobe kvm_amd 2>/dev/null")
    # Démarrer libvirt
    run_command("sudo systemctl start libvirtd")
    print("Passage en mode KVM terminé.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <provider>".format(sys.argv[0]))
        print("   provider: 'virtualbox' ou 'kvm'")
        sys.exit(1)

    provider = sys.argv[1].lower()
    if provider == "virtualbox":
        activate_virtualbox()
    elif provider == "kvm":
        activate_kvm()
    else:
        print(f"Provider inconnu : {provider}. Veuillez choisir 'virtualbox' ou 'kvm'.")
        sys.exit(1)

