# Always prefer setuptools over distutils
from setuptools import setup
from setuptools import find_packages

# This call to setup() does all the work
setup(
    name="currencypairs",
    version="0.0.1",
    description="Classes for storing data for currency pairs",
    long_description=open('README.txt').read(),
    url="",
    author="Surbhi Gupta",
    author_email="sg7319@nyu.edu",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["currencypairs"],
    include_package_data=True,
    install_requires=["math"]
)