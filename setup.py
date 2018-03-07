# -*- coding: UTF-8 -*-
import os
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomizedInstallCommand(install):
    def run(self):
        os.system("echo '=============================='")
        os.system("echo \"CURRENT VERSION: <2.0>\"")
        #-----------------#PIP requirements
        os.system("echo '=============================='")
        os.system("echo 'PRE-INSTALL PHASE STARTED !!!'")
        os.system("echo '=============================='")
        #=================
        os.system("sudo apt-get install -y python3-pip")
        os.system("sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev")
       #=================
        os.system("echo '=============================='")
        os.system("echo 'PRE-INSTALL PHASE FINISHED !!!'")
        os.system("echo '=============================='")
        install.run(self)
        
setup(
   cmdclass={ 'install': CustomizedInstallCommand },
   name='lxdui',
   version = '2.0',
   description='lxdui v{}'.format('2.0'),
   long_description='lxdui v{}'.format('2.0'),
   classifiers=[
       'Development Status :: 2.0 - Alpha',
       'Programming Language :: Python :: 3.5',
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
   author='AdaptiveScale, Inc.',
   author_email='info@adaptivescale.com',
   url = 'https://github.com/AdaptiveScale/lxdui',
   license='Apache',
   include_package_data = True,  
   zip_safe=False,
   python_requires='>=3',
   install_requires=[
       'Flask==0.12.2',
       'pylxd==2.2.4'
   ]
)
