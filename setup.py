from setuptools import find_packages, setup

VERSION = "0.0.1"
DESCRIPTION = "Air flags python library"
LONG_DESCRIPTION = "Air flags library to manage Python feature flags"

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("requirements-test.txt") as f:
    test_requires = f.read().splitlines()

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
    install_requires=install_requires,
    tests_require=test_requires,
    python_requires=">=3.6",
    url="https://github.com/devaway/air-flags-python",
    project_urls={
        "Bug Tracker": "https://github.com/devaway/air-flags-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 2",
        "Operating System :: OS Independent",
    ],
)
