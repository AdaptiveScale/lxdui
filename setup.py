# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages
from app import __metadata__ as meta

setup(
   name=meta.APP_NAME,
   version = meta.VERSION,
   description='{} v{}'.format(meta.APP_NAME, meta.VERSION),
   long_description='{} v{}'.format(meta.APP_NAME, meta.VERSION),
   classifiers=[
       'Development Status :: 2.0 - Stable',
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
   keywords=meta.KEYWORDS,
   author=meta.AUTHOR,
   author_email=meta.AUTHOR_EMAIL,
   url = meta.AUTHOR_URL,
   license=meta.LICENSE,
   packages=find_packages(exclude=['conf/lxdui.conf',]) + ['conf', 'logs'],
   include_package_data=True,
   zip_safe=False,
   install_requires=[
       'Click==6.7',
       'Flask==1.0',
       'flask-login==0.4.1',
       'flask_jwt==0.3.2',
       'jsonschema==2.6.0',
       'requests==2.9.1',
       'netaddr==0.7.19',
       'pyopenssl==17.5.0',
       'psutil==5.4.5',
       'pylxd==2.2.7',
       'terminado==0.8.1',
       'tornado==5.0.2',
       'tornado-xstatic',
       'XStatic==1.0.1',
       'XStatic-term.js==0.0.7.0'
   ],
   entry_points={
       'console_scripts': [
           'lxdui = app.run:lxdui'
       ]
   }
)
