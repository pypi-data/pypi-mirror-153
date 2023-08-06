import runpy
from pathlib import Path

from setuptools import find_packages, setup

name = "pyece"
description = "Tools for working with markup elements"
authors = "Elizaveta Dakhova; Vladislav A. Proskurov"
author_email = "rilshok@pm.me"
classifiers = [
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Development Status :: 1 - Planning",
    "Topic :: Scientific/Engineering :: Image Recognition",
    "Topic :: Scientific/Engineering :: Visualization",
]


version_path = Path(__file__).resolve().parent / name / "__version__.py"
version = runpy.run_path(str(version_path))["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as file:
    requirements = file.read().splitlines()

setup(
    name=name,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author=authors,
    author_email=author_email,
    version=version,
    url="https://github.com/rilshok/pyece",
    packages=find_packages(include=(name,)),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    classifiers=classifiers,
    python_requires=">=3.6",
)
