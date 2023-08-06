import sys
import os
from setuptools import setup 

VERSION = '0.1.3'

short_desc = 'A module for configuring and initializing Stata within Python'

rootdir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(rootdir, 'README.rst')) as f:
    long_desc = f.read()

CUR_PYTHON = sys.version_info[:2]
REQ_PYTHON2 = (2,7)
REQ_PYTHON3 = (3,4)

def get_python_version(pyver):
    return '.'.join([str(i) for i in pyver])

if CUR_PYTHON < REQ_PYTHON2 and CUR_PYTHON < REQ_PYTHON3:
    sys.stderr.write("""
The minimum Python version required to install stata_setup is Python %s or 
Python %s, but you're trying to install it on Python %s. After the 
minimum requirement is satisfied, try typing 

    $ pip install stata_setup
    
or

    $ pip install --upgrade stata_setup

This will install the latest version of stata_setup that works on your
version of Python.
""" % (get_python_version(REQ_PYTHON2), get_python_version(REQ_PYTHON3), get_python_version(CUR_PYTHON)))

    sys.exit(1)


setup_info = dict(
    name='stata_setup',
    version=VERSION,
    author='StataCorp LLC',
    author_email='tech-support@stata.com',
    url='https://www.stata.com/python/pystata',
    download_url='http://pypi.python.org/pypi/stata_setup',
    description=short_desc,
    long_description=long_desc,
    long_description_content_type ='text/x-rst',
    py_modules=['stata_setup'],
    install_requires=['numpy','pandas','ipython'],
    license='Apache Software License 2.0',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)

setup(**setup_info)
