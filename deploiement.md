# Deploy on server

## Kernel used

[Ubuntu Server 24.04.4 LTS](https://ubuntu.com/download/server/thank-you?version=24.04.4&architecture=amd64&lts=true)

## Packages installation

- `apt update`
- `docker --version`
- if not installed : `apt install docker.io`
- `git --version`
- if not installed : `apt install git`

## Git configuration

### Git configuration globally

`git config --global user.name "Name"`
`git config --global user.email "admin@example.com"`

### Generate SSH key of the server if needed

`ssh-keygen -t ed25519 -C "ton.email@example.com"`
let input default, or set it up as you wish.

`cat ~/.ssh/id_ed25519.pub`
copy the key and put it in your ssh keys in github : [github documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

## Clone the project

Before all, make a fork of My Universe Doc's git project
`git clone git@github.com:Alban2701/my_universe_doc.git`

move yourself in the target repository

clone the project `git clone git@github.com:your-username/my_universe_doc.git`

`cd /my_universe_doc`

## Configure Docker

Add the user to the docker group
`sudo usermod -aG docker $USER`
`newgrp docker`

pare feu
écrire la procédure de déploiement
relire les consignes NSA301