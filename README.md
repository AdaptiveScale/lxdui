<h1>Install from source</h1> 

<h4>0) Prerequisites:</h4>
- Your machine must have **LXC 2.3 or higher** already installed !
    - **NOTE #1**: The following commands will install you the latest stable version of LXC/LXD (supported only for Ubuntu 14 & 16).
        - `sudo apt-get install software-properties-common -y`
        - `sudo add-apt-repository ppa:ubuntu-lxc/lxd-stable -y`
        - `sudo apt-get update -y`
        - `sudo apt install lxd -y`
    - **NOTE #2**: Make sure you initialize LXD before you can use it with `lxdui`
        - run `sudo lxd init` and interactively with your terminal choose the preferred settings
        - for beginners you can just start the daemon with its default parameters by `sudo lxd init --auto`
- Your machine must have **Python 2.7** already installed !
- Your environment must have **pip** installed and some additional important modules !
    - **NOTE:** the following modules could help you get started:<br />`sudo apt-get install libfontconfig libffi-dev libssl-dev build-essential python-dev python-pip python-virtualenv -y`
- Your environment must have access to the internet !

<h4>1) Clone this repository</h4>
- `git clone https://github.com/AdaptiveScale/lxdui.git`
    -  **NOTE:** you must have git installed to do so:
    - `sudo apt-get update -y`
    - `sudo apt-get install git -y`

<h4>2) Installing from source</h4>
- On the same directory you executed the `git clone` command, go inside the directorium */lxd-app-ci/* via `cd` and execute `sudo python setup.py install`
   

<h4>3) Run the app</h4>
- Within your machine terminal, execute `lxdui` command in order to start the
    - **NOTE:**
        - `lxdui` requires privileged credentials (sudo)
        - type `lxdui -h` to check out available customizable arguments
        - use the following command `sudo lxdui &` to start the server as a background process

> <h5>Issues you might run into, during the installation process...</h5>
- **ISSUE #1:** due to the latest **pip** versions the setup script might end with the following line: **ImportError: No module named build_py**
    - this is easily fixed by re-running the same install command again !
- **ISSUE #2:** due to **pip** installation process fails to install the rightful **urllib3** properly according to the required version of the dependencies, trying to run `lxdui` will throw the following errors:<br/>
**from urllib3.connection import HTTPConnection
<br/>ImportError: No module named connection**<br/>
    `pip show urllib3` might deceive you showing the rightful version is already installed...<br/>
    though when runing `python -c "import urllib3; print urllib3.__version__;"` you can see that it actually has not.
    - this can be fixed by manually installing *urllib3* right from their official repo.<br/>
    `git clone --branch 1.8 git://github.com/shazow/urllib3.git`<br/>
    `cd urllib3 && sudo python setup.py install`

<h1>Install via PIP</h1> 
*to be announced soon...*

<h1> Default configuration</h1>

The configuration file `config.json` laying within the **conf** directory actually gets replicated inside the pythons packages designated directory as is, upon each installation.

In case you want to change the credentials to be used for authenticatication, there is 2 alternatives:
- permanent via `/conf/config.json` located in python's package directory of the `lxdui`
- temporal via the **-c** application argument where user must specifying authentication credentials via the `username`:`password` pattern *( which has a priority over the latter each time enforced )*

<h1> Helpful Info</h1>

- To start the server with on a different port, also with different authentication credentials use the following command:
    - `sudo lxdui -c admin:secret -p 5555 &`
- To stop `lxdui`, find the **process id** using the `ps` command and issue the kill command on that process:
    -   `ps -ef | grep lxdui` <br/> example output:<hr/>
        root **32488**  1062  0 10:46 pts/0    00:00:00 sudo lxdui -c admin:secret -p 5555<br/>
        root 32489 **32488**  0 10:46 pts/0    00:00:00 /usr/bin/python /usr/local/bin/lxdui -c admin:secret -p 5555<hr/>
    - `sudo kill 3248`
    


