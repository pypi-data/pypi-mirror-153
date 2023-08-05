from setuptools import setup, find_packages
from codecs import open
from os import path
from sys import platform
here = path.abspath(path.dirname(__file__))

setup(
    name='physicalquantity',
    version='0.0.9',
    description='Simple library for working with physical quantities',
    long_description="""A simple library for working with physical quantities. 
    Implements basic dimensional decomposition of physical quantities and provides
    basic operations (adition, subtraction, multiplication, division, comparison) 
    for working with these quantities.

    Support for non-SI units is available but most operations will result in 
    implicit conversions to SI units. Use the as_absolute() or as_relative()
    methods to convert back to the desired non-SI units.

    Note that while this library supports a wide range of the dimentional analysis
    and related integrity artifacts of working with physical quantities, the prime 
    goal of this library isn't the dimentional integrity of code, but instead the
    unified serialization or rather serializisability of physical quantities. 

    """,
    url='https://github.com/pibara/physicalquantity',
    author='Rob J Meijer',
    author_email='pibara@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Environment :: Other Environment'
    ],
    keywords='units quantities',
    install_requires = ["python-dateutil", "pytz"],
    packages=find_packages(),
)

