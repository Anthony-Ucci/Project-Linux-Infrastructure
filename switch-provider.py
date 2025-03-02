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

def is_installed(package):
    """Vérifie si un package est installé."""
    result = subprocess.run(f"dpkg -l | grep -w {package}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def activate_virtualbox():
    # Vérifier si libvirt est installé avant d'essayer de l'arrêter
    if is_installed("libvirt-bin") or is_installed("libvirt-daemon-system"):
        run_command("sudo systemctl stop libvirtd")
    else:
        print("Libvirt n'est pas installé, pas besoin de l'arrêter.")
    
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
    
    # Vérifier si libvirt est installé avant d'essayer de le démarrer
    if is_installed("libvirt-bin") or is_installed("libvirt-daemon-system"):
        run_command("sudo systemctl start libvirtd")
    else:
        print("Libvirt n'est pas installé, pas besoin de le démarrer.")
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
