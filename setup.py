# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages
from app import __metadata__ as meta

setup(
   name=meta.APP_NAME,
   version = meta.VERSION,
   description='{} v{}'.format(meta.APP_NAME, meta.VERSION),
   long_description='{} v{}'.format(meta.APP_NAME, meta.VERSION),
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
   keywords=meta.KEYWORDS,
   author=meta.AUTHOR,
   author_email=meta.AUTHOR_EMAIL,
   url = meta.AUTHOR_URL,
   license=meta.LICENSE,
   packages=find_packages() + ['conf', 'logs'],
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
           'lui = app.run:lui'
       ]
   }
)
