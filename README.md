# l8_angles

This package implements a simple Python interface to the USGS Landsat 8 tool for computing per-pixel solar and sensor azimuth and zenith angles from Angle Coefficient Files. See the [official USGS documentation for details](https://www.usgs.gov/landsat-missions/solar-illumination-and-sensor-viewing-angle-coefficient-files).

## Installation

Clone this repository and install with:

```pip install .```

To do this in a single step, run

```pip install git+ssh://git@github.com/contrailcirrus/l8-angles.git```

## Usage

This package exposes a function `calculate_angles`. See its [docstring](l8angles.pyx) for details.

## Example

The snippet below can be doctested with `python -m doctest -v README.md`.

```python
>>> import l8angles

>>> data = l8angles.calculate_angles(
...     "test_ANG.txt",
...     angle_type="SATELLITE",
...     bands=[3,6,7],
... )

>>> # The output contains azimuth and zenith angles
>>> data.keys()
dict_keys(['sat_az', 'sat_zn'])

>>> # The output is a list of numpy arrays, one for each band
>>> sat_az = data['sat_az']
>>> len(sat_az)
3

>>> sat_az_band3 = sat_az[0]
>>> sat_az_band3.shape
(7931, 7841)

>>> # Print a little slice
>>> sat_az_band3[2000:2003, 2000:2003]
array([[114.15740648, 114.16167023, 114.16593707],
       [114.15843211, 114.16269665, 114.16696429],
       [114.15945794, 114.16372329, 114.16799171]])

```

There is also a `calculate_angles_xarray` function that returns the results as an xarray Dataset.

```python
>>> import l8angles
>>> data = l8angles.calculate_angles_xarray(
...     "test_ANG.txt",
...     angle_type="SATELLITE",
...     bands=9,
... )
>>> ds = data['sat_az']
>>> ds
<xarray.Dataset> Size: 498MB
Dimensions:  (y: 7931, x: 7841)
Coordinates:
  * x        (x) float64 63kB 5.574e+05 5.574e+05 ... 7.926e+05 7.926e+05
  * y        (y) float64 63kB 6.318e+06 6.318e+06 ... 6.08e+06 6.08e+06
Data variables:
    B9       (y, x) float64 497MB nan nan nan nan nan ... nan nan nan nan nan

```
