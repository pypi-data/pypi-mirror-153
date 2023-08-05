import setuptools
from setuptools import setup

NAME = "maintain_PlatoUtils"
VERSION = "0.1.3.94"
PY_MODULES = ["maintain_PlatoUtils"]

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    py_modules=PY_MODULES,
    packages=setuptools.find_packages(),
    url='',
    license='MIT',
    author='Timaos',
    author_email='201436009@uibe.edu.cn',
    description='运营PlatoDB的工具',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy',
                      "nebula-python",
                      "nebula2-python",
                      "pandas",
                      "flashtext",
                      "gensim==3.8.3",
                      "tensorflow==2.5.0",
                      "pyecharts",
                      "stellargraph",
                      "networkx",
                      "chardet"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)