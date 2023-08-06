# Python Tlint

*Simple linter that just works and implements various kind of checks.*

[![PyPI version](https://badge.fury.io/py/tlint.svg)](https://badge.fury.io/py/tlint)

## Install

```
pip install tlint
```

## Usage

Generate initial project configuration

```
tlint init
```

Lint project according to generated configuration

```
tlint
```

## Ideas / Roadmap

- determines user defined modules
- foreach user defined module, prevent import based on rules
- theses rules come from a config file that only owner may modify
- a warning is thrown in pipeline if someone else modify this file
