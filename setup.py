from setuptools import find_packages, setup

VERSION = "0.1.4"
DESCRIPTION = "Air flags python library"
LONG_DESCRIPTION = "Air flags library to manage Python feature flags"

setup(
    name="airflags",
    packages=find_packages(include=["air_flags"]),
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="devaway",
    author_email="airflags@devaway.es",
    license="BSD",
    install_requires=["pyyaml==6.0", "jsonschema==4.2.1"],
    python_requires=">=3.4",
    url="https://github.com/devaway/air-flags-python",
    project_urls={
        "Bug Tracker": "https://github.com/devaway/air-flags-python/issues",
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
