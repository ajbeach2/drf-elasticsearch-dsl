#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from drf_elasticsearch_dsl/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("drf_elasticsearch_dsl", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


install_requires = [
    'Django>=1.10,<=1.12',
    'djangorestframework>=3.7.3',
    'elasticsearch-dsl',
    'elasticsearch-dsl'
]

tests_require = [
    'coverage',
    'mock',
    'flake8',
    'tox',
    'tox-pyenv',
    'nose',
    'fake',
    'codecov'
]

extras_require = {
    'celery': ['celery']
}


setup(
    name='drf-elasticsearch-dsl',
    version=version,
    description="""DRF wrapper around ElasticsearchDSL""",
    long_description=readme + '\n\n' + history,
    author='Alexander Beach',
    author_email='ajbeach2@gmail.com',
    url='https://github.com/ajbeach2/drf-elasticsearch-dsl',
    packages=[
        'drf_elasticsearch_dsl',
    ],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    license="MIT",
    zip_safe=False,
    keywords='drf-elasticsearch-dsl',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
