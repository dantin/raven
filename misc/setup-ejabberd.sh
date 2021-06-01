#!/usr/bin/env bash
set -e

# Source dependencies
sudo apt update
sudo apt upgrade -y
sudo apt install ejabberd -y
sudo apt install erlang-p1-pgsql -y

echo "ejabberd has been installed!"
echo "Edit /etc/ejabberd/ejabberd.yml to customize it"
