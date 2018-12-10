# this is to solve the challenge of imports by installing as a package
# using $ pip install -e .
# the -e flag stands for editable, . means current directory
from setuptools import setup, find_packages

setup(name='chingu', version='0.1', packages=find_packages())