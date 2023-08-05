# h5parm
Provides H5Parm data interface

# Example

```python
from h5parm.utils import make_example_datapack
from h5parm import DataPack
datapack = make_example_datapack(4,5,6)
#select your slices
datapack.select(ant="RS*", time=slice(0,None,2), freq=2)
```
This will select all antennas with names starting with 'RS', every other time, and the 3rd frequency.
```python
#get your soltab
phase, axes = datapack.phase
#get the coordinates of axes
patch_names, directions = datapack.get_directions(axes['dir'])
antenna_labels, antennas = datapack.get_antennas(axes['ant'])
timestamp, times = datapack.get_antennas(axes['time'])
freq_labels, freqs = datapack.get_freqs(axes['freq'])
pol_labels, pols = datapack.get_pols(axes['pol'])
```
In general the first element returned by all `get_*` methods are string labels, and the second is a dimensionful `astropy` object, e.g. `ICRS` object, `Time` object etc.
