import os
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [line.strip() for line in open("requirements.txt").readlines()]
requirements.extend([line.strip() for line in open("requirements-unix.txt").readlines()])

setup(
    name="timeseer",
    version=os.environ.get('TIMESEER_VERSION', '0.0.0'),
    author="Timeseer.AI",
    author_email="pypi@timeseer.ai",
    description="Timeseer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    python_requires='>=3.9',
    include_package_data=True,
)
