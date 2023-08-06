#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['influxdb-client[async]>=1.29.1']

test_requirements = ['pytest>=3', ]

setup(
    author="Robin Song",
    author_email='robin.song@edmonton.ca',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Utility to write logging to influxdb2 in order to gather some application stats. After using this utility, user can create dashboard in Grafana with InfluxDB.",
    entry_points={
        'console_scripts': [
            'log2influx=log2influx.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='log2influx',
    name='log2influx',
    packages=find_packages(include=['log2influx', 'log2influx.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/robsonyeg/log2influx',
    version='0.1.1',
    zip_safe=False,
)
