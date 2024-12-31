Vagrant.configure("2") do |config|
  # Configuração para a primeira máquina
  config.vm.define "machine1" do |machine1|
    machine1.vm.box = "ubuntu/jammy64" # Substitua pela box desejada
    machine1.vm.network "public_network", bridge: "eno1" # Substitua pelo nome correto da interface no host
    machine1.vm.hostname = "machine1.local"
    machine1.vm.provider "virtualbox" do |vb|
      vb.memory = "512" # Ajuste conforme necessário
      vb.cpus = 1
    end
  end

  # Configuração para a segunda máquina
  config.vm.define "machine2" do |machine2|
    machine2.vm.box = "ubuntu/jammy64" # Substitua pela box desejada
    machine2.vm.network "public_network", bridge: "eno1" # Substitua pelo nome correto da interface no host
    machine2.vm.hostname = "machine2.local"
    machine2.vm.provider "virtualbox" do |vb|
      vb.memory = "512" # Ajuste conforme necessário
      vb.cpus = 1
    end
  end
end
