"""
Install with
pip install wale-net
"""

import setuptools
import subprocess


def git(*args):
    return subprocess.check_output(["git"] + list(args))


# get latest tag
latest = git("describe", "--tags").decode().strip()
latest = latest.split("-")[0]
# for pypi package the tag must be set manually
# latest = "2.0.1"

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


long_description = """
This package provides a Recurrent Neural Network (RNN) for vehicle trajectory prediction with uncertainties.
It builds up on the work of [Convolutional Social Pooling](https://github.com/nachiket92/conv-social-pooling).
It has been adapted to CommonRoad and extended by the ability of scene understanding and online learning.

For further information see the Readme here:
https://github.com/TUMFTM/Wale-Net
"""


setuptools.setup(
    name="wale-net",
    version=latest,
    author="Maximilian Geisslinger, Phillip Karle",
    author_email="maximilian.geisslinger@tum.de, karle@ftm.mw.tum.de",
    description="Prediction module for CommonRoad",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TUMFTM/Wale-Net",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)
