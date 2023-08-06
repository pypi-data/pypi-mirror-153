
from setuptools import find_packages, setup

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name="commandler",
    author="Peter.Harding",
    author_email="plh@performiq.com",
    version="1.0.4",
    description="A small tool for registering command actions and executing using a text string.",
    long_description=long_description,
    license='MIT',
    url="https://github.com/performiq/commandler",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)
