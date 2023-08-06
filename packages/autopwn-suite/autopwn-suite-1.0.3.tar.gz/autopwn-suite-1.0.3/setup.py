#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='autopwn-suite',
    version='1.0.3',
    description='AutoPWN Suite is a project for scanning vulnerabilities and exploiting systems automatically.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='GamehunterKaan',
    url='https://auto.pwnspot.com',
    project_urls={
        'Documentation': 'https://auto.pwnspot.com',
        'Source': 'https://github.com/GamehunterKaan/AutoPWN-Suite',
        'Tracker': 'https://github.com/GamehunterKaan/AutoPWN-Suite/issues',
    },
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: Security',
    ],
    entry_points={
        'console_scripts': [
            'autopwn-suite = autopwnsuite.autopwn:main',
        ],
    },
)
