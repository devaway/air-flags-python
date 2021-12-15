from setuptools import find_packages, setup
from pkg_resources import parse_requirements

VERSION = "0.1.0"
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
    install_requires=[
        str(requirement)
        for requirement
        in parse_requirements("requirements.txt")
    ],
    tests_require=[
        str(test_requirement)
        for test_requirement
        in parse_requirements("requirements-test.txt")
    ],
    python_requires=">=3.6",
    url="https://github.com/devaway/air-flags-python",
    project_urls={
        "Bug Tracker": "https://github.com/devaway/air-flags-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
