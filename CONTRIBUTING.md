# How to contribute to the Air flags python
`air-flags-python` is an ordinary Python package. You can install it with `pip install -e .` into some virtualenv, edit the sourcecode and test out your changes manually.

## Report Bugs
Report bugs at https://github.com/devaway/air-flags-python/issues.

If you are reporting a bug, please include:
* Your operating system name and version.
* Your Python interpreter type and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Running tests and linters
Make sure you have `virtualenv` installed, and the Python versions you care about. You should have Python 2.7 and the latest Python 3 installed.
Run your virtual env
```shell
python3 -m venv venv
source ./venv/bin/activate
```

We have a `Makefile` that is supposed to help people start contributing. Run `make` or `make help` to list commands.

Of course you can always run the underlying commands yourself.

## Pull Request Guidelines
Before you submit a pull request, check that it meets these guidelines:

## Releases
* Go to Github releases and Draft a new release
* Create a new tag based on [Semantic Versioning](https://semver.org/)
* Add the same tag name as release title
* Include into the release description the proper changes
  * Bug Fixes
  * New Features
  * Code improvements
  * Documentation Updates
* Publish the release
* Release action will be triggered automatically
  * The new version will be updated in the pkg
  * The CHANGELOG will be updated with the body of the release
  * The new version will be released into PyPi
