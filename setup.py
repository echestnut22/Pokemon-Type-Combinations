from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name="pokemon",
    version="1.0",
    packages=find_packages(),
    author="Eric Chestnut",
    author_email="eric.chestnut232@gmail.com",
    description="A package for Pokemon Type Combinations",
    install_requires=required_packages,
    python_requires='>=3.6',
)

