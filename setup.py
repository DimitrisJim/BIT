#!/usr/bin/env python
"""The setup script."""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []
setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest>=3', ]

setup(
    author="DFH",
    author_email='jfh@imijmi.eu',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Binary Indexed Tree.",
    install_requires=requirements,
    long_description=readme + '\n\n',
    include_package_data=True,
    keywords='bit',
    name='bit',
    packages=find_packages(include=['bit', 'bit.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DimitrisJim/BIT',
    version='0.1.0',
    zip_safe=False,
)
