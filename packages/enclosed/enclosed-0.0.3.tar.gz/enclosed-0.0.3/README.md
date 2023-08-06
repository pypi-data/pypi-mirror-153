# enclosed

Python command line tool and library to extract ecnsloed strings from text


[![Python](https://img.shields.io/pypi/pyversions/enclosed)](#)
[![Coverage](https://img.shields.io/codecov/c/github/joaompinto/enclosed)](https://app.codecov.io/gh/joaompinto/enclosed)
[![PyPi](https://img.shields.io/pypi/v/enclosed.svg?style=flat-square)](https://pypi.python.org/pypi/enclosed)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

## About

This package provides a Python library that will parse an input text and produce tokens enclosed or not enclosed within an _open_symbol_ and _close_symbol_ .


## Install

```bash
pip install enclosed
```

## How to use
```python
from enclosed import Parser

print(Parser().tokenize("Hello {World}"))
```
