#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="sibyl-ai",
    version="1.0.12",
    author="Francesco Baldisserri",
    author_email="fbaldisserri@gmail.com",
    packages=find_packages(include=["sibyl", "sibyl.models", "sibyl.encoders"]),
    install_requires=["joblib","numpy","pandas","scipy","scikit-learn",
                      "tensorflow","catboost","seaborn", "lightgbm",
                      "matplotlib"],
    description="Wrapper for SKLearn Pipeline with Auto ML features",
    license="MIT",
    keywords="AI ML Pipeline Wrapper AutoML",
    url="https://github.com/sirbradflies/Sibyl"
)
# End of file