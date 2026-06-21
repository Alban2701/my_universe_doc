# Deploy on server

## Distribution used

[Ubuntu Server 24.04.4 LTS](https://ubuntu.com/download/server/thank-you?version=24.04.4&architecture=amd64&lts=true)

## Prepare the server to be accessed with ssh

1. Check the server's ssh status

    ```bash
    sudo systemctl status ssh
    ```

    if a message `Unit ssh.service could not be found` is displayed then ssh server is not installed
    else if a message `inactive (dead)` appears, ssh server is installed but not started

    if none of those message appears, please skip to step 3

2. Install and activate ssh server

    ```bash
    sudo apt update
    sudo apt install -y openssh-server
    sudo systemctl enable --now ssh  # start the server now and on each server's boot
    ```

3. Check if the ssh server is listening on the port 22

    ```bash
    sudo ss -tnlp | grep :22
    ```

    You should see line with 0.0.0.0:22 (or *:22).

4. Check the server's IP and username

    ```bash
    hostname -I
    whoami
    ```

## Access the server (SSH)

All operations on the server are done over SSH (only port 22 is opened for administration. See the firewall section below). We use key-based authentication: you log in with an SSH key pair instead of a password.

The flow is the same on every OS: check whether you already have a key, create one if not, copy the public key to the server then connect. Follow the section that matches your local machine.

### From a Linux / macOS client

1. Check whether you already have a key

    ```bash
    ls -al ~/.ssh/id_*.pub
    ```

    if a file such as `id_ed25519.pub` (or `id_rsa.pub`) is listed, you already have a key: Skip to step 3

2. Create a key (only if you don't have one)

    ```bash
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```

    Press Enter to accept the default path. A passphrase is optional but recommended.

3. Copy your public key to the server

    ```bash
    ssh-copy-id <user>@<server-ip>
    ```

    You'll be asked for the server password one last time.
    `user` is the user of the server.
    `server-ip` is the ip of your server.

    It can look like : `server@10.0.2.15`

4. Connect

    ```bash
    ssh user@server-ip
    ```

    No password should be requested anymore and you should be logged in with your key.

### From a Windows Client (Powershell)

1. Check whether you already have a key

    ```powershell
    Get-ChildItem "$env:USERPROFILE\.ssh\*.pub"
    ```

    If a file such as `id_ed25519.pub` is listed, you already have a key. Skip to step 3.

2. Create a key (only if you don't have one)

    ```powershell
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```

    Press Enter to accept the default path (`%USERPROFILE%\.ssh\id_ed25519`).

3. Copy your public key to the server

    ```powershell
    $pubKey = Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"
    ssh <user>@<server-ip> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$pubKey' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
    ```

    You will be asked for the server password one last time. Passing the key through a variable avoids the CRLF/BOM encoding issues a raw pipe can introduce.

    `user` is the user of the server.
    `server-ip` is the ip of your server.

    It can look like : `server@10.0.2.15`

4. Connect

    ```powershell
    ssh user@server-ip
    ```

### Harden the server (after key login works)

Once and only once you can log in with your keys, disable password and root login so the server only accepts key-based authentication.

1. edit the conf file

    ```bash
    sudo nano /etc/ssh/sshd_config
    ```

    ```conf
    PasswordAuthentication no
    PermitRootLogin no
    ```

    (Ctrl+O for saving then `Enter` to validate. Finally Ctrl+X to leave nano)

2. Reload SSH:

    ```bash
    sudo systemctl restart ssh
    ```

3. Check if there is not a contrary order

    ```bash
    sudo sshd -T | grep -iE 'passwordauthentication|permitrootlogin'
    ```

    if yes is return, you must also edit this file and replace `yes` with `no`

Please, do this **only after** confirming key login works, otherwise you can lock yourself out of the server.

## Packages installation

- `apt update`
- `sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)` to uninstall anything that could make conflict
- follow instructions from the [Official Docker Documentation](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) (visited at 19th of May 2026)
- follow instructions from the [git official guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (Linux Installation Part)

## Clone the project

cd the target repository

clone the project `git clone https://github.com/Alban2701/my_universe_doc.git`

`cd my_universe_doc`

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
sudo docker compose up -d --build  # rebuild and start in the background
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
# For ssh connection
sudo ufw allow 22/tcp

sudo ufw allow 80/tcp

# Block anything else
sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw enable

# check rules
sudo ufw status verbose
```

## Congratulations

You have now the app running on your server with a configured firewall.
