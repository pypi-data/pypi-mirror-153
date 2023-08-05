# pysegmenters_blingfire

[![license](https://img.shields.io/github/license/oterrier/pysegmenters_blingfire)](https://github.com/oterrier/pysegmenters_blingfire/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pysegmenters_blingfire/workflows/tests/badge.svg)](https://github.com/oterrier/pysegmenters_blingfire/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pysegmenters_blingfire)](https://codecov.io/gh/oterrier/pysegmenters_blingfire)
[![docs](https://img.shields.io/readthedocs/pysegmenters_blingfire)](https://pysegmenters_blingfire.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pysegmenters_blingfire)](https://pypi.org/project/pysegmenters_blingfire/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysegmenters_blingfire)](https://pypi.org/project/pysegmenters_blingfire/)

Rule based segmenter based on Spacy

## Installation

You can simply `pip install pysegmenters_blingfire`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pysegmenters_blingfire
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
