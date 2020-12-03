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
    name="wilma_schedules_reader",
    version="0.1.3",
    url="wilma_schedules_reader",
    license="GNU GENERAL PUBLIC LICENSE Version 3",
    author="Pasi Ollikainen",
    author_email="pasi.ollikainen@outlook.com",
    description="The rest client which reads shedules from the .",
    long_description=read("README.rst"),
    packages=find_packages(exclude=("tests",)),
    install_requires=[],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE Version 3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)
