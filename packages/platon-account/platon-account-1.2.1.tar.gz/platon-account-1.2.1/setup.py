#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    'test': [
        "hypothesis>=4.18.0,<5",
        "pytest==5.4.1",
        "pytest-xdist",
        "tox==3.14.6",
    ],
    'lint': [
        "flake8==3.7.9",
        "isort>=4.2.15,<5",
        "mypy==0.770",
        "pydocstyle>=5.0.0,<6",
    ],
    'doc': [
        "Sphinx>=1.6.5,<2",
        "sphinx_rtd_theme>=0.1.9,<1",
        "towncrier>=19.2.0, <20",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
    ],
}

extras_require['dev'] = (
    extras_require['dev'] +  # noqa: W504
    extras_require['test'] +  # noqa: W504
    extras_require['lint'] +  # noqa: W504
    extras_require['doc']
)


with open('./README.md') as readme:
    long_description = readme.read()


setup(
    name='platon-account',
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version='1.2.1',
    description="""platon-account: Sign Platon transactions and messages with local private keys""",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shinnng',
    author_email='Shinnng@outlook.com',
    url='https://github.com/platonnetwork/platon-account',
    include_package_data=True,
    package_data={"platon_account": [
        "py.typed",
        "hdaccount/wordlist/*.txt",
    ]},
    install_requires=[
        "bitarray>=1.2.1,<1.3.0",
        "platon-abi>=1.2.0",
        "platon-keyfile>=1.2.0",
        "platon-keys>=1.2.0",
        "platon-rlp>=1.2.0",
        "platon-utils>=1.2.0",
        "hexbytes>=0.1.0,<1",
        "rlp>=1.0.0,<3"
    ],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    py_modules=['platon_account'],
    license="MIT",
    zip_safe=False,
    keywords='platon',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
