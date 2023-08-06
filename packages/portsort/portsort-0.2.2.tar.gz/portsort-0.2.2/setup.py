from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


VERSION = '0.2.2'
DESCRIPTION = 'A package to sort stocks into portfolios and calculate weighted-average returns.'
LONG_DESCRIPTION = 'A package that allows single, double or triple sorting of stocks into portfolios and calculation of weighted-average returns for these portfolios.'

# Setting up
setup(
    name="portsort",
    version=VERSION,
    author="Ioannis Ropotos",
    author_email="<ioannis.ropotos@ucdconnect.ie>",
    url='https://github.com/ioannisrpt/portsort',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas>=1.0.0', 'numpy>=1.0.0'],
    keywords=['python', 'finance', 'asset-pricing', 'portfolio', 'sort', 'stocks', 'returns'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Microsoft :: Windows",
    ],
)

