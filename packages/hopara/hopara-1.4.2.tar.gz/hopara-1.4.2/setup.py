import os

from setuptools import find_packages, setup

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, 'requirements.txt')) as fp:
    requires = fp.read().splitlines()

with open(os.path.join(current_dir, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='hopara',
    packages=find_packages(include=['hopara']),
    version='1.4.2',
    description='Hopara Python Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Hopara Inc',
    install_requires=requires
)
