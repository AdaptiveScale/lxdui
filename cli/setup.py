from setuptools import setup, find_packages

setup(
    name='lui',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='Apache 2.0',
    author='AdaptiveScale, Inc',
    author_email='info@adaptivescale.com',
    description='CLI for LXDUI',
    install_requires=[
        'Click'
     ],
    entry_points='''
         [console_scripts]
         lui=lui:lui
     '''
)
