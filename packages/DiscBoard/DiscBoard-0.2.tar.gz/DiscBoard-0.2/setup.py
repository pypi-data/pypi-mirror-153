from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2'
DESCRIPTION = 'A library written for simple backend development of bot dashboards in python'
LONG_DESCRIPTION = 'Ohhh I have no idea what to write here so Ill just write whatever, for more information please visit the repo xD'

# Setting up
setup(
    name="DiscBoard",
    version=VERSION,
    author="Pimpek01",
    author_email="pimpek.pimposlaw@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'discord.py', 'Dashboard'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)