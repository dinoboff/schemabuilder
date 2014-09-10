#!/usr/bin/env python

try:
    from setuptools import setup

    with open("./requirements.txt") as r:
        extras = {
            "install_requires": [
                l.strip()  for l in  r.readlines() if l.strip()
            ]
        }
except ImportError:
    from distutils.core import setup

    extras = {}


setup(
    name="schemabuilder",
    version="0.1.0",
    description="JSON schema definition helpers",
    author="Damien Lebrun",
    author_email="dinoboff@gmail.com",
    url="https://github.com/dinoboff/schemabuilder",
    packages=["schemabuilder", "schemabuilder.tests"],
    package_dir={"schemabuilder": "src/schemabuilder"},
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    **extras
)
