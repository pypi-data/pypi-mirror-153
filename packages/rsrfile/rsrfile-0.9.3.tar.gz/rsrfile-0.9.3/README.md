# rsrfile
Python module for read RSR files (RiskSpectrum PSA result files)

[![image](https://img.shields.io/pypi/v/rsrfile.svg)](https://pypi.python.org/pypi/rsrfile/)

## Features
* Read minimal cut sets;
* Read of importance measurements table of basic events, CCF groups, attributes, systems, components and events groups;
* Read CDF and PDF value table;
* Read common calculation info. Such as calculation time, number of MCS, cutoff threshold, etc.

## Installation
```sh
# PyPI
pip install rsrfile
```

## Usage
The code below displays common information on the calculation and a table of importance measurementscfor attributes:
```python
import rsrfile
import pandas as pd

with rsrfile.open('<path to RSR file>', '<open mode> "r" or "w"') as f:
    print(f.MCSSummary)
    attr = pd.DataFrame(
        f.AttrImpTable[1:],
        columns=f.AttrImpTable[0])
    print(attr)
```