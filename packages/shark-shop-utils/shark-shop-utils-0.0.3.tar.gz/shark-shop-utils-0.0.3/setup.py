from setuptools import setup, find_packages
import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setup(
    name='shark-shop-utils',
    version='0.0.3',
    author='Adrian \'Qwizi\' Ciołek',
    author_email='ciolek.adrian@protonmail.com',
    url='',
    install_requires=install_requires
)