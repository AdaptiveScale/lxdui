# -*- coding: UTF-8 -*-
import os
from setuptools import setup, find_packages
#customize install
from setuptools.command.install import install
# lxdui/__init__.py
from lxdui.app_metadata import __version__ as LXDUI_VERSION, __giturl__ as LXDUI_GITURL

class CustomizedInstallCommand(install):
    def run(self):
        
        os.system("echo '=============================='")
        os.system("echo \"CURRENT VERSION: <"+LXDUI_VERSION+">\"")
        #-----------------#PIP requirements
        os.system("echo '=============================='")
        os.system("echo 'PRE-INSTALL PHASE STARTED !!!'")
        os.system("echo '=============================='")
        #=================
        os.system("sudo pip install setuptools -U")
        os.system("sudo pip install requests==2.5.2")
        #--- if there is errors try to install urllib3 MANUALLY ---
        os.system("sudo pip install urllib3==1.8")
        #--- if there is errors try to install urllib3 manually ---
        os.system("sudo pip install pylxd==2.2.4")
        #=================
        os.system("sudo pip install netaddr==0.7.19")
        os.system("sudo pip install Flask==0.12")
        os.system("sudo pip install flask-login==0.4.0")
        os.system("sudo pip install bs4==0.0.1")
       #=================
        os.system("echo '=============================='")
        os.system("echo 'PRE-INSTALL PHASE FINISHED !!!'")
        os.system("echo '=============================='")
        #PRE-SCRIPT -> install LXD & ZFS
        #dirname, filename = os.path.split(os.path.abspath(__file__))
        #os.system("sudo chmod 755 {0}/pre-setup/{1}".format(dirname, "install_zfs_lxd_shell.sh"))
        #os.system("sudo {0}/pre-setup/{1}".format(dirname, "install_zfs_lxd_shell.sh"))
        #then the actual INSTALL from pythontools
        install.run(self)
        
setup(
   cmdclass={ 'install': CustomizedInstallCommand },
   name='lxdui',
   version = LXDUI_VERSION,
   description='LXD-UI v{}'.format(LXDUI_VERSION),
   long_description='LXD-UI v{}'.format(LXDUI_VERSION),
   classifiers=[
       'Development Status :: 4 - Beta',
       'Programming Language :: Python :: 2.7',
       'Intended Audience :: Developers',
       'Intended Audience :: System Administrators',
       'Framework :: Flask',
       'Topic :: System :: Containers',
       'Topic :: System :: Clustering',
       'Topic :: System :: Monitoring',
       'License :: OSI Approved :: Apache Software License',
       'Operating System :: POSIX :: Linux'
   ],
   keywords='lxc lxc-containers lxd',
   author='AdaptiveScale',
   author_email='info@adaptivescale.com',
   url = LXDUI_GITURL,
   license='Apache',
   packages=['lxdui'],
   include_package_data = True,  
   zip_safe=False,
   install_requires=[
       'netaddr==0.7.19',
       'Flask==0.12',
       'flask-login==0.4.0',
       'bs4==0.0.1',
       'pylxd==2.2.4'
   ],
   entry_points={
       'console_scripts': [
           'lxdui = lxdui.app:main'
       ]
   }
)
