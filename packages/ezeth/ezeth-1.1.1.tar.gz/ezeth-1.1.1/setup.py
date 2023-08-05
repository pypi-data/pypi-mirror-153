import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version(fname):
    script = open(os.path.join(os.path.dirname(__file__), fname)).read()
    for line in script.splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name="ezeth",
    version=get_version(os.path.join('ezeth','version.py')),
    description="simple python client to access ethereum network",
    long_description=read('README.rst'),
    long_description_content_type="text/x-rst",
    author="Ahmad Fahadh Ilyas",
    author_email="fahadhilyas4@gmail.com",
    url="https://github.com/fahadh4ilyas/Simple-Ethereum-Client.git",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities"
    ],
    keywords=["ethereum", "web3", "solidity"],
    install_requires=[
        "py-solc-x>=1.1.0",
        "web3>=5.20.0"
    ],
    python_requires=">=3.7,<3.11"
)