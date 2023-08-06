# Hestia Data Validation

[![Pipeline Status](https://gitlab.com/hestia-earth/hestia-data-validation/badges/master/pipeline.svg)](https://gitlab.com/hestia-earth/hestia-data-validation/commits/master)
[![Coverage Report](https://gitlab.com/hestia-earth/hestia-data-validation/badges/master/coverage.svg)](https://gitlab.com/hestia-earth/hestia-data-validation/commits/master)
[![Documentation Status](https://readthedocs.org/projects/hestia-data-validation/badge/?version=latest)](https://hestia-data-validation.readthedocs.io/en/latest/?badge=latest)


## Install

```bash
pip install hestia_earth.validation
```

## Usage

```python
from hestia_earth.validation import validate

# for each node, this will return a list containing all the errors/warnings (empty list if no errors/warnings)
errors = validate(nodes)
```
