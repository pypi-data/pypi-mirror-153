import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chameleon_fetcher",
    version="0.0.1",
    author="Joerg Baach",
    author_email="mail@baach.de",
    description="Utility to quickly fetch and render a chameleon template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhb/chameleon_fetcher",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["Chameleon"],
    extras_require = {
        'tests':  ["pytest"]
    },
    py_modules=['chameleon_fetcher'],
    python_requires=">=3.6",
)