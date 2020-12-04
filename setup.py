import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="WilmaJSONReader",
    packages=["WilmaJSONReader"],
    entry_points={"console_scripts": ["wilmareader=WilmaJSONReader.reader:main"]},
    version="0.2.7",
    url="https://github.com/pasiol/WilmaJSONReader",
    license="GNU Lesser General Public License v3.0 or later (LGPLv3.0+)",
    author="Pasi Ollikainen",
    author_email="pasi.ollikainen@outlook.com",
    description="The Wilma Rest client.",
    install_requires=[
        "mypy>=0.790",
        "validators>=0.18.1",
        "requests>=2.25.0",
        "typing-extensions>=3.7.4.3",
        "click>=7.1.2",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)
