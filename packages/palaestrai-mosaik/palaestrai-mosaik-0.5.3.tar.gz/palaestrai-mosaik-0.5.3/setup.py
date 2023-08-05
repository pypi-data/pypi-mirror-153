#!/usr/bin/env python3
"""Setup file for the palaestrAI-mosaik package."""
import setuptools

with open("VERSION") as freader:
    VERSION = freader.readline().strip()


with open("README.md") as freader:
    README = freader.read()

install_requirements = [
    "mosaik",  # ==2.6.0",
    "mosaik_api",  # ==2.4.2",
]
development_requirements = [
    "tox",
    "black",
    "coverage",
    "sphinx",
    "pysimmods",
    "midas-mosaik",
    "palaestrai",
]

extras = {"dev": development_requirements}

setuptools.setup(
    name="palaestrai-mosaik",
    version=VERSION,
    author="The ARL Developers",
    author_email="stephan.balduin@offis.de",
    description="Mosaik Environment for palaestrAI.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="http://palaestr.ai/",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requirements,
    extras_require=extras,
    license="LGPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8.0",
)
