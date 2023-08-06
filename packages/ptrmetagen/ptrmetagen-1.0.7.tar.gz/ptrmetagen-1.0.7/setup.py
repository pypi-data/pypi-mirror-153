import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ptrmetagen",
    version="1.0.7",
    description="Package for generation of metastructures for Panter project",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gisat-panther/ptr-metagen",
    author="Michal Opetal",
    author_email="michal.opletal@gisqt.cw",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"],
    packages=["metagen", "metagen.components"],
    include_package_data=True,
    )
