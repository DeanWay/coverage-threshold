from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="coverage_threshold",
    version="0.10.0",
    author="Dean Way",
    description="Tools for coverage threshold limits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeanWay/coverage-treshold",
    packages=["coverage_threshold"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "coverage-threshold = coverage_threshold.__main__",
        ],
    },
    install_requires=[],
    python_requires=">=3.7",
)
