# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

#new line
setup(
    name='baraqda-lib',
    version='0.0.15',
    packages=['tests', 'baraqdalib'],
    url='',
    license='MIT',
    author='Kacper Hanuszewicz, Aleksander Karbowy, Wojciech Marcinkowski, Marcin Rogoń',
    author_email='',
    description='Generator of real fake data for testing purpose using real distribution in society',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent'
    ],
    include_package_data=True,
    install_requires=[]
)
