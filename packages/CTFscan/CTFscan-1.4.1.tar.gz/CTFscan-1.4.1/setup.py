#!/usr/bin/python3
import setuptools
import re

with open("README.md") as f:
    long_description = f.read()

with open("ctfscan/ctfscan.py") as f:
    __version__ = re.search(r'^__version__ = "(.*)"$', f.read(), re.M)[1]

setuptools.setup(
    name="CTFscan",
    version=__version__,
    author="p7e4",
    author_email="p7e4@qq.com",
    description="a web dir scanner to make sure you won't miss something",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p7e4/CTFscan",
    packages=setuptools.find_packages(),
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ctfscan = ctfscan:run"
        ]
    },
    package_data={
        "ctfscan": ["*.txt"],
    },
    install_requires=[
        "arequest"
    ]
)



