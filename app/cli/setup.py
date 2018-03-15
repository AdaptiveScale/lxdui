from setuptools import setup, find_packages
from app import __metadata__ as meta

setup(
    name='lui',
    version=meta.VERSION,
    packages=find_packages(),
    include_package_data=True,
    url=meta.AUTHOR_URL,
    license=meta.LICENSE,
    author=meta.AUTHOR,
    author_email=meta.AUTHOR_EMAIL,
    description='CLI for {}'.format(meta.APP_NAME),
    install_requires=[
        'Click'
     ],
    entry_points='''
         [console_scripts]
         lui=cli:lui
     '''
)
