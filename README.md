![logo](https://github.com/AdaptiveScale/lxdui/blob/master/lxdui/static/images/logo.png "LXDUI")

### A web UI for Linux containers based on LXD/LXC.  
Learn more about Linux containers and LXD/LXC here: [linuxcontainers.org](https://linuxcontainers.org/ "linuxcontainers.org")

LXDUI is a Python Flask application that leverages LXD's Python client library, **pylxd** [(https://github.com/lxc/pylxd)](https://github.com/lxc/pylxd "https://github.com/lxc/pylxd"), for interacting with the LXD REST API.  It allows for rapid provisioning and management of large number of containers from a web browser, and you can simultaneously create any number of containers, even from multiple images, in one step.

##
![screencast](https://github.com/vhajdari/testsite/blob/master/lxdui_screencast_2.gif "lxdui screencast")
##

## Installation

### Prerequisites
The following are the prerequisites required to run LDXUI (supported only on Ubuntu 14 & 16):
- **Python 2.7** (lxdui has not been tested with python3).
- **pip** and some additional modules.
	
    To install **pip** run:
    
	`sudo apt-get install libfontconfig libffi-dev libssl-dev build-essential python-dev python-pip python-virtualenv -y`
        
- Your must have **LXD 2.3 or higher** already installed.
    
    The following commands will install the latest stable version of LXC/LXD . 
    
	- `sudo apt-get install software-properties-common -y`
	- `sudo add-apt-repository ppa:ubuntu-lxc/lxd-stable -y`
	- `sudo apt-get update -y`
	- `sudo apt install lxd -y`
	
    **NOTE**:
    
    Make sure you initialize LXD before you can use it with `lxdui`
     - Run `sudo lxd init` 
     - Choose your desired settings
     - For beginners -- you can just start the daemon with its default parameters
     	-  `sudo lxd init --auto`



### 1) Clone the repository
`git clone https://gitlab.com/adaptivescale/lxdui.git`

### 2) Install from source
Go into to the `lxdui` directory and execute `sudo python setup.py install`
   

### 3) Run the app
	
Run the command to start the server: `sudo lxdui`

**NOTE:**
- `lxdui` requires privileged execution (**sudo**)
- To see the available customizable arguments type: `sudo lxdui -h`
- To start the server as a background process type: `sudo lxdui &` 

 **Issues you might run into during installation**
> - **ImportError: No module named build_py**.  
>	- This is a **pip** error, adn is easily fixed by re-running the same install command again.
> - **ImportError: No module named connection**
> 	- **pip** fails to install the correct **urllib3** module according to the required version of the dependencies.
> 	- `pip show urllib3` might deceive you showing you that the right version is already installed.  
> - **urllib3 version mismatch**
>	- `lxdui` will throw the following error: **from urllib3.connection import HTTPConnection**
>   	- `python -c "import urllib3; print urllib3.__version__;"` will show you the installed version.
>   - Fix it by manually installing *urllib3* from the official repo 
>   	- `git clone --branch 1.8 git://github.com/shazow/urllib3.git`
>   	- `cd urllib3 && sudo python setup.py install`

## Install via PIP 
Instructions will be made available soon.

## Default configuration

The configuration file `config.json` found within the **conf** directory gets copied to  the python's packages designated directory as is, upon each installation.

To change the credentials to be used for authenticatication there are 2 alternatives:
- Permanent via `/conf/config.json` located in python's package directory for `lxdui`
- Temporarily via the **-c** application argument where you specify authentication credentials via the `username`:`password` pattern.

## Helpful Info</h1>

- To start the server on a different port with custom authentication credentials use the following command:
    - `sudo lxdui -c admin:secret -p 5555 &`
- To stop `lxdui`, find the **process id** using the `ps` command and issue the kill command on that process:
    -   `ps -ef | grep lxdui`  
	```
	example output:
	
	root 32488  1062  0 10:46 pts/0    00:00:00 sudo lxdui -c admin:secret -p 5555
	root 32489 32488  0 10:46 pts/0    00:00:00 /usr/bin/python /usr/local/bin/lxdui -c admin:secret -p 5555
	```
    - `sudo kill 32489`


# LIMITATIONS
There are a number of things that you can do with the LXC CLI that are notably missing from **lxdui**

Neamely:
- Rename Container
- Snapshots
- Copy/Move Containers
- Management of storage pools

For a list of available commands in **lxc** type:
```sudo lxc -h```
```
  config           Change container or server configuration options
  copy             Copy containers within or in between LXD instances
  delete           Delete containers and snapshots
  exec             Execute commands in containers
  file             Manage files in containers
  image            Manipulate container images
  info             Show container or server information
  launch           Create and start containers from images
  list             List the existing containers
  move             Move containers within or in between LXD instances
  network          Manage and attach containers to networks
  profile          Manage container configuration profiles
  publish          Publish containers as images
  remote           Manage the list of remote LXD servers
  restart          Restart containers
  restore          Restore containers from snapshots
  snapshot         Create container snapshots
  start            Start containers
  stop             Stop containers
  storage          Manage storage pools and volumes
```
# AUTHOR

AdaptiveScale, Inc.
[http://www.adaptivescale.com](http://www.adaptivescale.com)

# LICENSE
Copyright © 2017 AdaptiveScale, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

For details see the file COPYING or visit: http://www.gnu.org/licenses/
