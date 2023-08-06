from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='DACOpt',
    version='0.0.2',
    packages=['dacopt', 'dacopt.stac'],
    url='',
    license='GPL-3.0 License',
    author='Duc Anh Nguyen',
    author_email='d.a.nguyen@liacs.leidenuniv.nl',
    description='DACOpt: An Efficient Contesting Procedure for AutoML Optimization',
    long_description=long_description,  # Optional
    description_content_type='text/markdown',
    long_description_content_type='text/markdown',
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='AutoML optimization Divide and conquer Bayesian Optimization',  # Optional
)
