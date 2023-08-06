"""Package the Timeseer Client for publishing."""

import os
import setuptools

with open("timeseer_client/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timeseer",
    version=os.environ.get("TIMESEER_VERSION", "0.0.0"),
    author="Timeseer.AI",
    author_email="pypi@timeseer.ai",
    description="Timeseer Client allows querying of data and metadata from timeseer.",
    license="Copyright Timeseer.AI 2021",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://timeseer.ai/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=[
        "timeseer_client",
        "timeseer_client.internal",
        "timeseer_client.metadata",
    ],
    install_requires=[
        "kukur >= 0.0.21",
        "pyarrow",
    ],
    python_requires=">=3.9",
)
