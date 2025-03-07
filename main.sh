#!/usr/bin/env bash
#
# main.sh : Script principal pour lancer l'infrastructure et la configuration

set -e  # Stoppe le script si une commande échoue

# 1) Vérification des prérequis
echo "Vérification des dépendances..."
command -v vagrant >/dev/null 2>&1 || { echo >&2 "Vagrant n'est pas installé. Abandon."; exit 1; }
command -v ansible-playbook >/dev/null 2>&1 || { echo >&2 "Ansible n'est pas installé. Abandon."; exit 1; }

echo "Dépendances OK."

# 2) Lancement des machines virtuelles via Vagrant
echo "Démarrage des VMs..."
cd vagrant
vagrant up

# 3) Exécution des playbooks Ansible
echo "Provisioning Ansible..."
cd ..
ansible-playbook -i ansible/inventory/hosts ansible/playbooks/gateway.yml
ansible-playbook -i ansible/inventory/hosts ansible/playbooks/webserver.yml
ansible-playbook -i ansible/inventory/hosts ansible/playbooks/clients.yml

# 4) (Optionnel) Lancement de scripts Python supplémentaires
# echo "Exécution des scripts Python..."
# python scripts/setup_database.py
# python scripts/create_users.py

echo "Infrastructure et configuration terminées !"
