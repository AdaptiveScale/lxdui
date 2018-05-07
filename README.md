![logo](https://github.com/AdaptiveScale/lxdui/blob/master/app/ui/static/images/logo.png)
### A web UI for Linux containers based on LXD/LXC.  
Learn more about Linux containers and LXD/LXC here: [linuxcontainers.org](https://linuxcontainers.org/)

LXDUI leverages LXD's Python client library, 
[**pylxd**](https://github.com/lxc/pylxd), for interacting with the LXD REST API.  It allows for rapid provisioning and management of large number of containers from a web browser, and you can simultaneously create any number of containers, even from multiple images, in one step.

## Version 2.0
[Version 2.0](https://github.com/AdaptiveScale/lxdui/wiki/New-in-2.0) of LXDUI is a complete rewrite of the application that better exposes LXD's feature set with additional functionality. A new CLI is now available for managing LXDUI as well. Learn more about the CLI [here](https://github.com/AdaptiveScale/lxdui/wiki/LXDUI's-CLI). 

[New in 2.0](https://github.com/AdaptiveScale/lxdui/wiki/New-in-2.0)


## Screencast
![Screencast](https://github.com/vhajdari/testsite/blob/master/lxdui_screencast_2.gif)
##

# Getting Started

As the name suggests, LXDUI is a visual interface for the LXD & LXC toolset.  In order to use LXDUI you need to have LXD installed on your system.  The following instructions walk you through the installation process so that you have a working system with LXD and LXDUI.

These instructions are targeted for an Ubuntu distribution, but you should be able to adapt the instructions to use in any distribution where LXD is supported.

For more detailed instructions please refer to the [wiki page](https://github.com/AdaptiveScale/lxdui/wiki).

### Install
**1.** Install the Prerequisites - [instructions here](https://github.com/AdaptiveScale/lxdui/wiki/Installing-the-Prerequisites)

**2.** Clone LXDUI from the GitHub repo:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `git clone https://github.com/AdaptiveScale/lxdui.git`

**3.** **[Optional]** Create a virtual environment for testing. Skip this step if you want to install it globaly on your system.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `python3 -m venv mytestenv`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Activate the virtual environment:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `source mytestenv/bin/activate`

**4.** Run Setup

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `cd lxdui`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `python3 setup.py install`


### Start LXDUI
At this point LXDUI should be installed and ready to start.

To start the app run: `python3 run.py start`  
or use the new CLI:  &nbsp;&nbsp;`lxdui start`

When the app starts open a browser to the following link to access the app:
[http://127.0.0.1:15151](http://127.0.0.1:15151)

**Log In.**  The default account and password are: **admin** | **admin**

## CONTRIBUTION

Your contribution is welcome and greatly appreciated.  Please contribute your fixes and new features via a pull request.
Pull requests and proposed changes will then go through a code review and once approved will be merged into the project.

## AUTHOR

AdaptiveScale, Inc.
[http://www.adaptivescale.com](http://www.adaptivescale.com)

## LICENSE
Copyright © 2018 AdaptiveScale, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. For details see the file COPYING or visit: http://www.gnu.org/licenses/
