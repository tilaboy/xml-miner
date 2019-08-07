import os
from setuptools import setup, find_packages

NAME = "xml_miner"
VERSION = os.environ.get("XML_MINER_VERSION", "0.0.1")

setup(
    name=NAME,
    version=VERSION,
    description="Python tool to select values from xml",
    author="Document Understanding",
    author_email="chaoli.job@gmail.com",
    packages=find_packages(),
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "xml-select=xml_miner.xml_select:main",
            "xml-python-select=xml_miner.xml_select:main",
            "trxml-python-select=xml_miner.trxml_select:main",
        ],
    },
)
