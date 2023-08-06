from setuptools import setup
from setuptools import find_packages

with open("Readme.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='steam_sdk',
    version="0.0.46",
    author="STEAM Team",
    author_email="steam-team@cern.ch",
    description="Source code for APIs for STEAM tools.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.cern.ch/steam/steam_sdk",
    keywords={'STEAM', 'API', 'SDK', 'CERN'},
    install_requires=required,
    python_requires='>=3.8',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8"
        ],
)
