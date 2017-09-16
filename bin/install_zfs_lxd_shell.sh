#!/bin/bash
# LXD installation script for Ubuntu 14 & 16
OS=$(lsb_release -si)
ARCH=$(uname -m | sed 's/x86_//;s/i[3-6]86/32/')
VER=$(lsb_release -sr)
VER=${VER:0:2}


echo "OS: $OS"
echo "ARCHITECUTRE: $ARCH"
echo "VERSION: $VER"
echo "====================="
echo "Installing LXD & ZFS "
echo "====================="

function if_installed
{
	R=$(which "$1" | wc -l)
	if [ "$R" == "1" ];then
		return 1
	else
		return 0
	fi
}

if [ "$OS" = "Ubuntu" ]; then
    #Ubuntu distribution 14.04 - trusty
    if [ "$VER" = "14" ]; then
		#ZFS pre-requisites
		sudo apt-get install software-properties-common -y
		#ZFS repo PPA
		sudo add-apt-repository ppa:zfs-native/stable -y
		#LXC latest STABLE PPA
        sudo add-apt-repository ppa:ubuntu-lxc/lxd-stable -y
		
		#update it - INSTALL TARGETS
        sudo apt-get update -y

		#Install ZFS and load module
		sudo apt-get install ubuntu-zfs -y
		sudo modprobe zfs
		
        sudo apt-get install lxd -y
        #lxd init --auto
		
    #Ubuntu distribution 16.04 - xenial
    elif [ "$VER" = "16" ]; then
		#UPDATE FIRST 
		sudo apt-get install software-properties-common -y
		#LXC PPA for LATEST STABLE
		sudo add-apt-repository ppa:ubuntu-lxc/lxd-stable -y
		
        sudo apt-get update -y
		#install ZFS directly - no need to load module hence it's already loaded from the installation step
		sudo apt install zfs -y
		#install the latest LXD from the stable repo
        sudo apt install lxd -y
        #lxd init --auto
    else
        echo ">> This Ubuntu isn't 14.04, nor 16.04 !"
    fi
else
    echo ">> Sorry but the OS is not Ubuntu distribution !"
fi
