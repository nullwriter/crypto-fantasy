# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Whatsapp Crypto Fantasy Bot',
    version='0.1.0',
    description='Whatsapp bot that plays cryptocurrency fantasy trading.',
    long_description=readme,
    author='Christian Feo',
    author_email='christianfeob@yahoo.com',
    url='https://github.com/nullwriter',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)