# coding=utf8
import os
import sys
from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))

with open("README.md") as f:
    long_description = f.read()


setup(
    name="nitor-devel-backend",
    version="0.1.17",
    description="Tool for running a local proxy in docker to unify a local development backend and live Nitor API sources from dev or prod",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/NitorCreations/nitor-devel-backend",
    download_url="https://github.com/NitorCreations/nitor-devel-backend",
    author="Pasi Niemi",
    author_email="pasi.niemi@nitor.com",
    license="Apache 2.0",
    packages=["nitor_devel_backend"],
    include_package_data=True,
    scripts=[],
    entry_points={
        "console_scripts": ["nitor-devel-backend=nitor_devel_backend.cli:cli_run_backend"],
    },
    setup_requires=["pytest-runner"],
    install_requires=[
        "nameless-deploy-tools>=1.268",
    ]
)
