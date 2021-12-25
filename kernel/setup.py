import json
from setuptools import setup

with open('../package.json', 'r') as f:
    version = json.load(f)["gammaVersion"]

setup(
    name='gamma',
    version=version,
    packages=['gamma'],
)
