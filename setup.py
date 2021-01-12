from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="coverage_threshold",
    version="0.4.2",
    author="Dean Way",
    description="Tools for coverage threshold limits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeanWay/coverage-threshold",
    packages=["coverage_threshold"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "coverage-threshold = coverage_threshold.cli:main",
        ],
    },
    install_requires=["toml >= 0.10.2"],
    python_requires=">=3.7",
)
