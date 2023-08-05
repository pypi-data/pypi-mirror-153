from setuptools import setup, find_packages


with open("README.md", "r") as readme:
    description = readme.read()

setup(
    name="python-console",
    version="1.3.0",
    author="DaHunterTime",
    description="A (basic) cross-platform python console manager",
    long_description=description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/DaHunterTime/PyConsole",
    project_urls={
        "Bug Tracker": "https://github.com/DaHunterTime/PyConsole/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        "pyinputhandler >= 1.2.2"
    ],
    python_requires=">=3.8",
)
