# Deploy on server

## Distribution used

[Ubuntu Server 24.04.4 LTS](https://ubuntu.com/download/server/thank-you?version=24.04.4&architecture=amd64&lts=true)

## Packages installation

- `apt update`
- `sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)` to uninstall anything that could make conflict
- follow instructions from the [Official Docker Documentation](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) (visited at 19th of May 2026)
- follow instructions from the [git official guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (Linux Installation Part)

## Clone the project

cd the target repository

clone the project `git clone https://github.com/Alban2701/my_universe_doc.git`

`cd my_universe_doc`

## Access the server (SSH)

All operations on the server are done over SSH (the only port opened for administration. See the firewall section below).

Use key-based authentication and disable password / root login:

```bash
# From your local machine (once): copy your public key
ssh-copyèid user@server-ip

# Then connect
ssh user@server-ip
```

One the eserver, in /etc/ssh/sshd_config:

```conf
PasswordAuthentication no
PermitRootLogin no
```

```bash
sudo systemctl restart ssh
```

## Clean Apache

Apache may be running on your ubuntu.
We will uninstall it.

```bash
sudo systemctl stop apache2
sudo systemctl disable apache2
sudo apt remove --purge apache2 apache2-utils -y
sudo apt autoremove -y
```

Check that anything is no more running on port 80
`sudo ss -tlnp | grep :80`
It must display nothing.

## Launch the project

`sudo docker compose up --build`

### Stop / restart the project

```bash
sudo docker compose down  # stop the stack
sudo docker compose down -v  # stop and wipe the database volume
sudo docker compose up -d --build  # rebuild and start int the background
```

## How to access the app

`ip a` to display your ip adresses.
Look for inet under enp0s3.
You should have an IP like 10.xx.xxx.xx/xx
On your navigator's search bar, search `http://{your-server-ip}`
You should have the app displayed.

## Configure the firewall

The firewall is important to protect your server and your datas by closing ports your are not using.

```bash
sudo ufw enable

# For ssh connection
sudo ufw allow 22/tcp

sudo ufw allow 80/tcp

# Block anything else
sudo ufw default deny incoming
sudo ufw default allow outgoing

# check rules
sudo ufw status verbose
```

## Congratulations

You have now the app running on your server with a configured firewall.
