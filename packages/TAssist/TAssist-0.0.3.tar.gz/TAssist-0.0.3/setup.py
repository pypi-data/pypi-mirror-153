from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'An unnoficial python wrapper for the TA Public API (2.0) by Pegasis'

# Setting up
setup(
    name="TAssist",
    version=VERSION,
    author="BearGaming123 (Supreeth Govindaraju)",
    author_email="<supreethG@gmx.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'requests'],
    keywords=['python', 'Teach Assist', 'YRDSB'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)