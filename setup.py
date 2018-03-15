# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages

setup(
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
   packages=find_packages(),
   include_package_data=True,
   zip_safe=False,
   install_requires=[
       'Flask==0.12.2',
       'pylxd==2.2.5',
       'jsonschema==2.6.0',
       'requests==2.9.1',
       'netaddr==0.7.19',
       'flask-login==0.4.1',
       'Click==6.7',
       'pyopenssl==17.5.0',
       'flask_jwt==0.3.2'
   ],
   entry_points={
       'console_scripts': [
           #'lxdui = app.api.core:startApp',
           'lui = app.run:lui'
       ]
   }
)
