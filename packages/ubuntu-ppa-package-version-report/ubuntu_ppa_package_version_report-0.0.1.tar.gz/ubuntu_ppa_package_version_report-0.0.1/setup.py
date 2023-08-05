#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'launchpadlib']

test_requirements = [ ]

setup(
    author="Philip Roche",
    author_email='phil.roche@canonical.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Utility to Generate a report on the versions of packages in specified PPAs",
    entry_points={
        'console_scripts': [
            'ubuntu_ppa_package_version_report=ubuntu_ppa_package_version_report.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ubuntu_ppa_package_version_report',
    name='ubuntu_ppa_package_version_report',
    packages=find_packages(include=['ubuntu_ppa_package_version_report', 'ubuntu_ppa_package_version_report.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/philroche/ubuntu_ppa_package_version_report',
    version='0.0.1',
    zip_safe=False,
)
