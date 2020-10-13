from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gituhubu",
    version="0.2.0",
    author="Jaroslaw Zywert",
    author_email="zywert@gmail.com",
    description="CLI tool for searching github organization repositories using fzf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jzyinq/gituhubu',
    packages=find_packages(),
    scripts=["bin/gituhubu"],
    python_requires=">=3.6.0",
    setup_requires=['wheel'],
    install_requires=[
        "appdirs>=1.4.3,<2",
        "getch>=1.0,<2",
        "iterfzf>=0.4.0.17.3",
        "requests>=2.22.0,<3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
