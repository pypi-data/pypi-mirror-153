import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hmath",
    version="2.0.0",
    author="caleb7023",
    description="Hmath that can use advanced mathematical functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sites.google.com/view/hmath/home",
    project_urls={
        "Bug Tracker": "https://github.com/caleb7023/hmath",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)

# Author: Kenta Nakamura <c60evaporator@gmail.com>
# Copyright (c) 2020-2021 Kenta Nakamura
# License: BSD 3 clause
