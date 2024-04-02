from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
    #long_description = fh.read()
long_description = "The Best of Boots: 'BMP' - an address book application"

setup(
    name='BMPboot',
    version='3.3',
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
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='it@bartoszzygmunt.pl',
    py_modules=['address_book'],
)
