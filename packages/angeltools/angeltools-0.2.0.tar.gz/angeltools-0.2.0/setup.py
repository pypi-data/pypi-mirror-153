import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

using_setuptools = True

setup_args = {
    "name": "angeltools",
    "version": "0.2.0",
    "url": "https://github.com/ga1008/angeltools",
    "description": "personal python small tools collection",
    "long_description": long_description,
    "author": "Guardian",
    "author_email": "zhling2012@live.com",
    "maintainer": "Guardian",
    "maintainer_email": "zhling2012@live.com",
    "long_description_content_type": "text/markdown",
    "LICENSE": "MIT",
    "packages": setuptools.find_packages(),
    "include_package_data": True,
    "zip_safe": False,
    "entry_points": {"console_scripts": [
        'txt2char = angeltools.commands:txt2chars',
        'img2char = angeltools.commands:img2chars',
        'cmdsta = angeltools.commands:cmd_status',
        'tmcmd = angeltools.commands:timing_cmd',
    ]},
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    "install_requires": [
        "setuptools~=62.1.0",
        "tqdm~=4.64.0",
        "numpy~=1.22.3",
        "psutil~=5.9.0",
        "redis~=4.2.2",
        "scrapy~=2.6.1",
        "requests~=2.27.1",
        "pygame~=2.1.2",
        "pillow~=9.1.0",
    ],
}

setup(**setup_args)
