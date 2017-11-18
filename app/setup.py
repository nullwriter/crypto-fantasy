# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Crypto-Fantasy',
    version='1.0.1',
    description='Whatsapp bot that plays cryptocurrency fantasy trading.',
    long_description=readme,
    author='Christian Feo',
    author_email='christianfeob@yahoo.com',
    url='https://github.com/nullwriter/crypto-fantasy',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
