import os
import sys
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'Flask==0.10.1',
    'Flask-Babel==0.11.2',
    'Flask-HTTPAuth==3.2.3',
    'Flask-Login==0.4.0',
    'Flask-Mail==0.9.1',
    'Flask-OpenID==1.2.5',
    'Flask-Profiler==1.4',
    'Flask-SQLAlchemy==1.0',
    'Flask-WhooshAlchemy==0.8',
    'Flask-WTF==0.14.2',
    'flipflop==1.0',
    'guess-language-spirit==0.5a4',
    'coverage==4.4.1',
    'sqlalchemy-migrate==0.11.0',
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