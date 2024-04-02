from setuptools import setup, find_packages

setup(
    name='BMPboot',
    version='3.1',
    install_requires=[
        'thefuzz',
    ],
    entry_points={
        'console_scripts': [
            'start = BMPboot.main:main',
        ],
    },
    author='Bartosz, Michał, Piotr',
    packages=find_packages(),
    description='The Best of Boots: "BMP" - an address book application',
    py_modules=['address_book'],
)
