#!/usr/bin/python3
"""setup script"""
from setuptools import setup

LONG_DESCRIPTION = """\
snippetconverter.py can convert the snippet used in Kate or KDevelop IDE to the VSCode IDE
"""

setup(
    name="kate-vscode-snippetconverter",
    version="0.2",
    description="A tool to convert snippet from Kate/KDevelop to VSCode",
    long_description=LONG_DESCRIPTION,
    author="Maxime Haselbauer",
    author_email="maxime.haselbauer@googlemail.com",
    url="https://github.com/renn0xtek9/snippetconverter",
    packages=["snippetconverter"],
    install_requires=[""],
    entry_points={
        "console_scripts": ["snippetconverter=snippetconverter.snippetconverter:main"],
    },
)
