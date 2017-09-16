![logo](https://github.com/AdaptiveScale/lxdui/blob/master/lxdui/static/images/logo.png "LXDUI")

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
    	- example output:
        	```root **32488**  1062  0 10:46 pts/0    00:00:00 sudo lxdui -c admin:secret -p 5555
		   root 32489 **32488**  0 10:46 pts/0    00:00:00 /usr/bin/python /usr/local/bin/lxdui -c admin:secret -p 555```
    - `sudo kill 32489`
