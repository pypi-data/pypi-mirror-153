from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='clpm',
    version='1.3.5',
    description="A command-line password manager",
    long_description= (Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="alexjaniak",
    license="MIT 2021",
    url="https://github.com/alexjaniak/clpm",
    packages = find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'prettytable',
        'pycryptodome'
    ],
    entry_points={
        'console_scripts': [
            'clpm = clpm.main:cli',
        ],
    },
)