#!/usr/bin/env python

#
#  Copyright ©2022. Levo.ai Inc. All Rights Reserved.
#  You may not copy, reproduce, distribute, publish, display, perform, modify, create derivative works, transmit,
#  or in any way exploit any such software/code, nor may you distribute any part of this software/code over any network,
#  including a local area network, sell or offer it for commercial purposes.
#

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


install_requires = [
    "attrs>=20.3",
    "curlify>=2.2.1",
    "grpcio>=1.37.0,<2.0.0",
    "requests>=2.25.1",
]

setuptools.setup(
    name="levo_commons",
    version="0.1.34",
    author="Levo Inc",
    author_email="info@levo.ai",
    description="Common code between Levo CLI and test plans.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/levoai/levo-commons",
    project_urls={
        "Bug Tracker": "https://github.com/levo/levo-commons/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=install_requires,
    extras_require={"test": ["pytest>=6.0", "hypothesis>=6.14.3,<7.0.0"]},
    python_requires=">=3.9",
)
