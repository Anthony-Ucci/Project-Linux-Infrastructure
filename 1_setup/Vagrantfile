Vagrant.configure("2") do |config|

  # Méthode pour configurer VirtualBox pour une machine donnée
  def configure_virtualbox(machine, name, memory, cpus)
    machine.vm.provider "virtualbox" do |vb|
      vb.name   = name
      vb.memory = memory
      vb.cpus   = cpus
    end
  end

  # Méthode pour configurer libvirt (KVM) pour une machine donnée
  def configure_libvirt(machine, name, memory, cpus)
    machine.vm.provider "libvirt" do |lv|
      lv.name   = name
      lv.memory = memory
      lv.cpus   = cpus
    end
  end



  # DEBIAN 12
  config.vm.define "debian-vm" do |debian|
    debian.vm.box = "generic/debian12"
    debian.vm.box_version = "4.3.12"
    debian.vm.hostname = "debian-vm"
    debian.vm.network "private_network", ip: "192.168.56.12"
    
    debian.vm.provision "ansible" do |ansible|
      ansible.playbook   = "./playbooks/debian-provisionning_playbook.yml"
      ansible.extra_vars = { target_os: "debian" }
      ansible.groups     = { "debian_servers" => ["debian-vm"] }
    end

    # Appliquer la configuration spécifique pour chaque provider
    configure_virtualbox(debian, "Debian_VM_VBox", "2048", 2)
    configure_libvirt(debian, "Debian_VM_KVM", "2048", 2)
  end



  # UBUNTU 24
  config.vm.define "ubuntu-vm" do |ubuntu|
    ubuntu.vm.box = "bento/ubuntu-24.04"
    ubuntu.vm.box_version = "202502.21.0"
    ubuntu.vm.hostname = "ubuntu-vm"
    ubuntu.vm.network "private_network", ip: "192.168.56.10"
    
    ubuntu.vm.provision "ansible" do |ansible|
      ansible.playbook   = "./playbooks/ubuntu-provisionning_playbook.yml"
      ansible.extra_vars = { target_os: "ubuntu" }
      ansible.groups     = { "ubuntu_servers" => ["ubuntu-vm"] }
    end

    # Appliquer la configuration spécifique pour chaque provider
    configure_virtualbox(ubuntu, "Ubuntu_VM_VBox", "2048", 2)
    configure_libvirt(ubuntu, "Ubuntu_VM_KVM", "2048", 2)
  end



  # ROCKY 9
  config.vm.define "rocky-vm" do |rocky|
    rocky.vm.box = "bento/rockylinux-9"
    rocky.vm.box_version = "202502.21.0"
    rocky.vm.hostname = "rocky-vm"
    rocky.vm.network "private_network", ip: "192.168.56.13"
    
    rocky.vm.provision "ansible" do |ansible|
      ansible.playbook   = "./playbooks/rocky-provisionning_playbook.yml"
      ansible.extra_vars = { target_os: "rocky" }
      ansible.groups     = { "rocky_servers" => ["rocky-vm"] }
    end

    # Appliquer la configuration spécifique pour chaque provider
    configure_virtualbox(rocky, "Rocky_VM_VBox", "4096", 4)
    configure_libvirt(rocky, "Rocky_VM_KVM", "4096", 4)
  end

end
