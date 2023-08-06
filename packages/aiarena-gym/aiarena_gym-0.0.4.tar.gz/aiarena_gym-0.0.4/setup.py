from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Gym environment for training agents in the AI Arena game'

# Setting up
setup(
    name="aiarena_gym",
    version=VERSION,
    author="ArenaX Labs Inc.",
    author_email="<brandon@aiarena.io>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'gym', 'machine learning', 'reinforcement learning', 'fighting', 'game'],
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent"
    ]
)