from setuptools import setup, Extension
import setuptools
import os
import sys

# get __version__, __author__, and __email__
exec(open("./komoog/metadata.py").read())

setup(
    name='komoog',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url='https://github.com/benmaier/komoog',
    license=__license__,
    description="Convert komoot hiking trips to sounds.",
    long_description='',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
                       'numpy>=1.17',
                       'scipy>=1.5',
                       'gpxpy>=1.4.2',
                       'simplejson>=3.17.2',
                       'simpleaudio>=1.0.4',
    ],
    tests_require=['pytest', 'pytest-cov'],
    setup_requires=['pytest-runner'],
    classifiers=['License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 ],
    project_urls={
        'Documentation': 'http://komoog.benmaier.org',
        'Contributing Statement': 'https://github.com/benmaier/komoog/blob/master/CONTRIBUTING.md',
        'Bug Reports': 'https://github.com/benmaier/komoog/issues',
        'Source': 'https://github.com/benmaier/komoog/',
        'PyPI': 'https://pypi.org/project/komoog/',
    },
    include_package_data=True,
    zip_safe=False,
)
