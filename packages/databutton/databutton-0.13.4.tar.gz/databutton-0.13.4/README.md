# databutton-cli
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
[![PyPI version fury.io](https://badge.fury.io/py/databutton.svg)](https://pypi.python.org/pypi/databutton/)
[![PyPI download week](https://img.shields.io/pypi/dw/databutton.svg)](https://pypi.python.org/pypi/databutton/)
![release](https://github.com/databutton/databutton-cli/actions/workflows/release.yaml/badge.svg)




The CLI for building and deploying databutton projects

## Getting Started

`pip install databutton`

`databutton create my-project`

`databutton login`

`databutton deploy`

## Developing

### Prerequisites
This project uses poetry, so if you haven't already;

`pip install poetry`

### Install dependencies

`poetry install`

### Test

`poetry run pytest`

Alternatively run `poetry run pytest -s` to see `print` statements for debugging purposes.

### Test locally in another package

To test in another package, you can simply

`pip install -e .` assuming you're in this folder. If not, replace the `.` with the path to the `databutton-cli` folder.

## Authors

* **Databutton** - *Initial work* - [github](https://github.com/databutton)

## License: Copyright (c) Databutton

All rights reserved.