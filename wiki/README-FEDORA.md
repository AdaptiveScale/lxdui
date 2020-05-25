## Prerequisites

The following prerequisites are required to be installed on your system before you can install and use LXDUI.

#### 1) LXD
[LXD](https://linuxcontainers.org/) can be installed in one of three ways; from source, from the Fedora Backports or as a Snap package.  The recommended way is to use Snap package.

#### 2) Python 3
Version 2.0 of LXDUI is a complete rewrite based on [Python 3](https://www.python.org/downloads/), so please be keep in mind that all app related commands, if not specifically called out, will require that you have Python 3 installed on your system. 

#### 3) PIP (included in systems with Python 3.4 or higher)
[PIP](https://pip.pypa.io/en/stable/) is a package manager for Python applications.  In the event that a required package is missing from your system you can use PIP to install it.

#### 3) OpenSSL (openssl-devel)
[OpenSSL](https://www.openssl.org/) is used for certificate management.

#### 4) ZFS
[ZFS](https://zfsonlinux.org/) is a combined file system and logical volume manager.  It's the preferred storage layer for LXD.

### OPTIONAL

#### Virtualenv
[Virtualenv](https://virtualenv.pypa.io/en/stable/) is a tool to create isolated Python environments. Python “[Virtual Environments](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)” allow Python packages to be installed in an isolated location for a particular application, rather than being installed globally.

## Installation:
#### Fedora pre-requisites installation
`sudo dnf install git snapd openssl-devel python3 python3-pip python3-devel -y`
`sudo systemctl enable snapd && sudo systemctl start snapd`

##### Snap Installation
`sudo snap install lxd`

`lxd init`

Accept all the defaults for the prompts from `lxd init`.  For further instructions on installing and configuring LXD please refer to the following [link](https://linuxcontainers.org/lxd/getting-started-cli/).

### Install LXDUI
Follow the instructions located [here](https://github.com/AdaptiveScale/lxdui/wiki/Installing-LXDUI-2.0) to install LXDUI.
