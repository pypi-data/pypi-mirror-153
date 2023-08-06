# Hestia Aggregation Engine

[![Pipeline Status](https://gitlab.com/hestia-earth/hestia-aggregation-engine/badges/master/pipeline.svg)](https://gitlab.com/hestia-earth/hestia-aggregation-engine/commits/master)
[![Coverage Report](https://gitlab.com/hestia-earth/hestia-aggregation-engine/badges/master/coverage.svg)](https://gitlab.com/hestia-earth/hestia-aggregation-engine/commits/master)
[![Documentation Status](https://readthedocs.org/projects/hestia-aggregation-engine/badge/?version=latest)](https://hestia-aggregation-engine.readthedocs.io/en/latest/?badge=latest)

## Documentation

Official documentation can be found on [Read the Docs](https://hestia-aggregation-engine.readthedocs.io/en/latest/index.html).

Additional models documentation can be found in the [source folder](./hestia_earth/aggregation).

## Install

1. Install the module:
```bash
pip install hestia_earth.aggregation
```

### Usage

```python
import os
from hestia_earth.aggregation import aggregate

os.environ['API_URL'] = 'https://api.hestia.earth'
aggregates = aggregate(country_name='Japan')
```
