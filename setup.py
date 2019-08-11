import os
from setuptools import setup, find_packages

NAME = "xml_miner"
VERSION = os.environ.get("XML_MINER_VERSION", '0.0.3')

with open('README.rst', "r") as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', "r") as history_file:
    history = history_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    name=NAME,
    version=VERSION,
    keywords='data mining, xml',
    url='https://github.com/tilaboy/xml-miner',
    description="data mining tool, to mine data from batch of xml files",
    author="Chao Li",
    author_email="chaoli.job@gmail.com",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    long_description=readme + '\n\n' + history,
    test_suite="tests",
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mine-xml=xml_miner.mine_xml:main",
            "mine-trxml=xml_miner.mine_trxml:main",
        ],
    },
    license="MIT license",
    zip_safe=False
)
