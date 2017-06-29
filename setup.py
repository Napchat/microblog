import os
import sys
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'Flask',
    'Flask-Babel',
    'Flask-Login',
    'Flask-Mail',
    'Flask-OpenID',
    'Flask-SQLAlchemy',
    'Flask-WhooshAlchemy>=0.8',
    'Flask-WTF',
    'flipflop',
    'guess-language',
    'coverage',
    'sqlalchemy-migrate'
]

packages = ['app']

about = {}

with open(os.path.join(here, 'app', '__version__.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    include_package_data=True,
    license=about['__license__'],
    zip_safe=False,
    install_requires=requires,
    dependency_links=['https://bitbucket.org/spirit/guess_language/downloads/guess_language-spirit-0.5a4.tar.bz2'],
    classifiers=(
        'Development Status :: 1.0 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: IPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)