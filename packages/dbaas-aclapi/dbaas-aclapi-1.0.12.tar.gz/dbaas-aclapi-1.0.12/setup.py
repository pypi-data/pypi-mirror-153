#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbaas_aclapi import __version__
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open('requirements.txt').read().split('\n')
requirements_txt = open('requirements_test.txt').read().split('\n')

test_requirements = requirements + requirements_txt

setup(
    name='dbaas-aclapi',
    version=__version__,
    description='ACL API integration for DBaaS',
    long_description=readme + '\n\n' + history,
    author='Felippe da Motta Raposo',
    author_email='felippe.gestec@corp.globo.com',
    url='https://github.com/felippemr/dbaas-aclapi',
    packages=[
        'dbaas_aclapi',
    ],
    package_dir={'dbaas_aclapi':
                 'dbaas_aclapi'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='dbaas_aclapi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
