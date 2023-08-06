from setuptools import setup, find_packages
from codecs import open
from os import path


HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="genalpy",
    version="0.1.0",
    description="Genetic algorithms library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://genalpy.readthedocs.io/",
    author="Mariia Kryvets",
    author_email="mkrivets1@email.com",
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
    packages=["genalpy"],
    include_package_data=True,
    install_requires=["numpy", "matplotlib"]
)