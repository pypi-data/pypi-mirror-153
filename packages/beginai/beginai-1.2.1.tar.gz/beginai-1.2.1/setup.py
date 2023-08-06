# -*- coding: utf-8 -*-
"""
    Setup file for BeginAI lib.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import sys
import os

from pkg_resources import VersionConflict, require
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_requirements(req_file):
    """Read requirements file and return packages and git repos separately"""
    requirements = []
    dependency_links = []
    lines = read(req_file).split("\n")
    for line in lines:
        if line.startswith("git+"):
            dependency_links.append(line)
        else:
            requirements.append(line)
    return requirements, dependency_links


try:
    require("setuptools>=38.3")
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

REQ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pip-dep")
core_reqs, core_dependency_links = get_requirements(os.path.join(REQ_DIR, "requirements.txt"))


if __name__ == "__main__":
    setup(
        name="beginai",
        version="1.2.1",
        author="Begin AI Research & Engineering",
        author_email="engineering@begin.ai",
        description="A library to interact with Begin AI platform in order to build personalisation algorithms.",
        long_description="""
        This is Begin AI python SDK for both batch processing and application integration. 
        It can be used to integrate applications with Begin.ai orchestration platform to deliver applications with
        personalisation algorithms to do:
        1. Predict user engagement.
        2. Provide recommenders for users.
        3. Detect fake content.
        4. Detect fake profiles.
        5. Classify objects, profiles and contents automatically in categories.

        You do not need machine learning experience to use this library, 
        check out our documentation for details. 
        https://docs.begin.ai/b89798c6201243ecbbdc1126ece4e989

        register at begin.ai to get started.
        """,
        long_description_content_type="text/markdown",
        url="https://docs.begin.ai",
        packages=find_packages(exclude=["docs", "examples", "dist", "tests", "pytest.ini"]),
        license="Proprietary",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        use_pyscaffold=True,
        install_requires=core_reqs,
        dependency_links=core_dependency_links
    )
