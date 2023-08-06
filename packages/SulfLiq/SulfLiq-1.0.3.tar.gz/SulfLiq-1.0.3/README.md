# Sulfide liquid thermodynamic model of Kress
This project contains C++ and Python wrapper code (generated using [PyBind11](https://github.com/pybind/pybind11)) that calculates thermodynamic properties of sulfide liquid according to the models of: 
- Kress, Victor (1997) Thermochemistry of sulfide liquids .1. The system O-S-Fe at 1 bar. Contributions to Mineralogy and Petrology, 127[1-2], 176-186
- Kress, Victor (2000) Thermochemistry of sulfide liquids. II. Associated solution model for sulfide liquids in the system O-S-Fe. Contributions to Mineralogy and Petrology, 139[3], 316-325
- Kress, Victor (2007) Thermochemistry of sulfide liquids III: Ni-bearing liquids at 1 bar. Contributions to Mineralogy and Petrology, 154[2], 191-204
- Kress, Victor; Greene, Lori; Ortiz, Matthew; Mioduszewski, Luke (2008) Thermochemistry of sulfide liquids IV: density measurements and the thermodynamics of O-S-Fe-Ni-Cu liquids at low to moderate pressures. Contributions to Mineralogy and Petrology, 156[6], 785-797

## Local installation
This package is installed locally using the *setup.py* stript with the command
```
pip install .
```
A Jupyter notebook is included (*Tester.ipynb*) to demonstrate usage. Installation scripts require *cmake* and a C++ compiler. 

## Remote installation (PyPI.org)
The package may be added as a dependency and installed via *pip* as
```
pip install SulfLiq
```
Note that installation requires a locally available C++ compiler (either clang or gcc) and has been tested on MacOS and Ubuntu, but not Windows.

## Gitlab CI
On pushing a tagged commit of this repository to Gitlab, the CI configuration script will build an installable Python package and push that update to PyPI.org. For this purpose the following environment variables should be provided in Settings->CI->Variables:
```
GIT_SUBMODULE_STRATEGY recursive
```
```
TWINE_PASSWORD <token retrieved from your user account at PyPI.org>
```
```
TWINE_USERNAME=__token__
```