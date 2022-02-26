import json
from setuptools import setup

with open('../package.json', 'r') as f:
    config = json.load(f)
    name = config['kernelName']
    version = config['kernelVersion']
    homepage = config['homepage']
    author = config['author']
    author_name = author['name']
    author_email = author['email']

setup(
    name=name,
    version=version,
    description='Kernel of SymPy Beta',
    url=f'{homepage}/tree/master/kernel',
    author=f'{author_name}, SymPy Development Team',
    author_email=author_email,
    packages=['gamma'],
    license='BSD-3-Clause',
    platforms=['any'],
)
