sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install docker-ce docker-ce-cli containerd.io -y

curl -s https://aerokube.com/cm/bash | bash
sudo ./cm selenoid start --vnc -g "--limit 8"

sudo ./cm selenoid-ui start

docker run -d --name socks5 -p 1080:1080 -e PROXY_USER=neafiol -e PROXY_PASSWORD=nef441 serjs/go-socks5-proxy

pip3 install -r requirements.txt
timedatectl set-timezone Europe/Moscow

