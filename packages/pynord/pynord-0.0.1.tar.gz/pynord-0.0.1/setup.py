from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Python library for NordVPN on Linux.'
LONG_DESCRIPTION = 'A Python library for NordVPN. Easily connect to and rotate between NordVPN servers using Python.'

# Setting up
setup(
    name="pynord",
    version=VERSION,
    author="thebrightlizard",
    author_email="<maria.gonzalez5884@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'nordvpn', 'vpn', 'webscraping', 'privacy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)