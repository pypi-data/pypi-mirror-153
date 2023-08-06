#!/usr/bin/env python3
"""Setup file for the ARL package."""
from setuptools import find_packages, setup


with open("VERSION") as freader:
    VERSION = freader.readline().strip()

with open("README.rst") as freader:
    README = freader.read()

install_requirements = [
    # CLI
    "click==8.0.4",
    "click-aliases==1.0.1",
    "appdirs>=1.4.4",
    "tabulate>=0.8.9",
    # YAML, JSON
    "yamale>=3.0.6",
    "ruamel.yaml>=0.17.4",
    "simplejson",
    "jsonpickle>=2.0.0",
    # Process and IPC handling
    "aiomultiprocess>=0.9.0",
    "setproctitle>=1.2.2",
    "pyzmq>=22.0.3",
    "nest_asyncio",
    # Data handling and storage
    "alembic==1.5.8",
    "numpy>=1.18.5",
    "pandas>=1.2.4",
    "psycopg2-binary>=2.8.6",
    "SQLalchemy~=1.4.25",
    "sqlalchemy-utils~=0.37.8",
    # Documentation
    "pandoc",
]

development_requirements = [
    # Tests
    "tox>=3.23.0",
    "robotframework >= 4.0.0",
    "pytest>=6.2.4",
    "pytest-asyncio",
    "pytest-cov",
    "coverage",
    "lxml",
    "mock",
    # Linting
    "black==22.3.0",
    # Type checking
    "mypy",
    "types-click",
    "types-pkg_resources>=0.1.3",
    # Documentation
    "sphinx",
    "nbsphinx",
    "furo",
    "ipython",
    # "eralchemy@git+https://github.com/eveith/eralchemy.git@v1.2.10.1#egg=eralchemy-1.2.10.1",
]

extras = {"dev": development_requirements}

setup(
    name="palaestrai",
    version=VERSION,
    description="A Training Ground for Autonomous Agents",
    long_description=README,
    author="The ARL Developers",
    author_email="eric.veith@offis.de",
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requirements,
    extras_require=extras,
    license="LGPLv2",
    url="http://palaestr.ai/",
    entry_points={
        "console_scripts": [
            "palaestrai = palaestrai.cli.manager:cli",
            "arl-apply-migrations = palaestrai.store.migrations.apply:main",
        ]
    },
    data_files=[
        ("etc/bash_completion.d/", ["palaestrai_completion.sh"]),
        ("etc/zsh_completion.d/", ["palaestrai_completion.zsh"]),
        ("etc/fish_completion.d/", ["palaestrai_completion.fish"]),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
