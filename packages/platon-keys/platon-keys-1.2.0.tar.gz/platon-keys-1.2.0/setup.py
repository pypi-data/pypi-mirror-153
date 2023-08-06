#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)


deps = {
    'coincurve': [
        'coincurve>=7.0.0,<13.0.0',
    ],
    'platon-keys': [
        "platon-utils>=1.2.0",
        "platon-typing>=1.2.0",
    ],
    'test': [
        "asn1tools>=0.146.2,<0.147",
        "factory-boy>=3.0.1,<3.1",
        "pyasn1>=0.4.5,<0.5",
        "pytest==5.4.1",
        "hypothesis>=5.10.3, <6.0.0",
        "platon-hash[pysha3];implementation_name=='cpython'",
        "platon-hash[pycryptodome];implementation_name=='pypy'",
    ],
    'lint': [
        'flake8==3.0.4',
        'mypy==0.782',
    ],
    'dev': [
        'tox==3.20.0',
        'bumpversion==0.5.3',
        'twine',
    ],
}

deps['dev'] = (
    deps['dev'] +
    deps['platon-keys'] +
    deps['lint'] +
    deps['test']
)

with open('./README.md') as readme:
    long_description = readme.read()

setup(
    name='platon-keys',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='1.2.0',
    description="""Common API for Platon key operations.""",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shinnng',
    author_email='shinnng@outlook.com',
    url='https://github.com/platonnetwork/platon-keys',
    include_package_data=True,
    install_requires=deps['platon-keys'],
    py_modules=['platon_keys'],
    extras_require=deps,
    license="MIT",
    zip_safe=False,
    package_data={'platon-keys': ['py.typed']},
    keywords='platon',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
