import setuptools
import re

def read(path: str) -> str:
    with open(path) as fp:
        return fp.read()

__version__ = re.search(r'^__version__ = "(.*)"$', read("cover_cli/main.py"), re.M)[1]

setuptools.setup(
    name="cover-cli",
    version=__version__,
    author="p7e4",
    author_email="p7e4@qq.org",
    description="cover-cli.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/p7e4/cover-cli",
    packages=setuptools.find_packages(
        exclude=["docs", "tests*"],
    ),
    license="GPL 3.0",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Topic :: Security",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    python_requires=">=3.8",
    package_data={
        "cover_cli": ["*.txt"]
    },
    entry_points={
        "console_scripts": [
            "cover = cover_cli.main:run"
        ],
    },
    install_requires=[
        "click"
    ]
)
