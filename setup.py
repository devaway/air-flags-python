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
    author="devaway",
    author_email="core@devaway.es",
    license="BSD",
    install_requires=install_requires,
    tests_require=test_requires,
)
