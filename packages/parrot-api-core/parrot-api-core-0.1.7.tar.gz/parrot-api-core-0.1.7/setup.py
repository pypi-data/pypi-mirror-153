#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'connexion[swagger-ui]>=2.6.0',
    'tenacity',
    'requests[security]',
    'python-jose==3.3.0',
]

test_requirements = [
    'pytest>=3',
    'pytest-aiohttp',
    'pytest-cov>=2.8.1',
    'responses'
]

setup(
    author="Perry Stallings",
    author_email='astal01@gmail.com',
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
    description="Python API Project Framework",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='parrot_api_core',
    name='parrot-api-core',
    packages=['parrot_api.core', 'parrot_api.core.auth', 'parrot_api.core.auth.providers'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/perrystallings/parrot_api_core',
    version='0.1.7',
    zip_safe=False,
    extras_require={
        'async': [
            'aiohttp>=3.6.2',
            'aiohttp_jinja2>=1.2.0',
            'orjson',
            'aioresponses'
        ],
    },
)
