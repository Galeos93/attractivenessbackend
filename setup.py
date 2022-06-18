import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="attractivenessbackend",
    version="1.0.0",
    author="Alejandro Garcia",
    author_email="alejandro.garcia.ihs@gmail.com",
    description="Repository with various attractiveness related apps",
    license="Proprietary",
    keywords="example documentation tutorial",
    url="http://packages.python.org/an_example_pypi_project",
    packages=['attractivenessbackend', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Tools",
        "License :: Other/Proprietary License",
    ],
)
