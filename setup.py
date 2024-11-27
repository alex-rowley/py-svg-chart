#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Alex Rowley",
    author_email='',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Creates svg based charts in python",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='pysvgchart',
    name='pysvgchart',
    packages=find_packages(include=['pysvgchart', 'pysvgchart.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/arowley-ai/py-svg-chart',
    version='0.0.3',
    zip_safe=False,
)
