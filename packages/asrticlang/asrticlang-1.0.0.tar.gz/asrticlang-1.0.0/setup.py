# Author: KITA Ryota <kita.h131212@gmail.com>
# Copyright (c) 2022 KITA Ryota
# Licence: MIT

from setuptools import setup

DESCRIPTION = 'Investigate the language ratio of the latest articles of Qiita.'
NAME = 'asrticlang'
AUTHOR = 'KITA Ryota'
AUTHOR_EMAIL = 'kita.h131212@gmail.com'
URL = 'https://github.com/RyotaKITA-12/articlang'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
VERSION = '1.0.0'
PYTHON_REQUIRES = '>=3.6'
INSTALL_REQUIRES = [
    'beautifulsoup4==4.11.1',
    'matplotlib==3.5.2',
    'requests==2.27.1',
    'setuptools==49.2.1',
]
PACKAGES = [
    'articlang'
]
KEYWORDS = 'qiita language graph'
CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6'
]
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)
