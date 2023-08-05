from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.8.9'
DESCRIPTION = 'A Simple SSH Manager for your terminal written in Python.'
LONG_DESCRIPTION = 'Simple SSH Manager is a terminal utility which keeps track of server ips, passwords, and ssh keys which makes logging into your machines blazingly fast.'

# Setting up
setup(
    name="ssmanager",
    version=VERSION,
    author="Garrett Jones",
    author_email="jonesgc137@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    python_requires='>=3.0',
    install_requires=['appdirs>=1.4.4',  'python-decouple>=3.6', 'requests>=2.25.1','urllib3>=1.26.5'],
    keywords=['ssh', 'manager', 'password', 'networking'],
    entry_points={
        'console_scripts': [
            'ssm=ssm.main:main'
            ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
