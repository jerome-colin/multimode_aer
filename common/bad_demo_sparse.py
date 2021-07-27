import numpy as np
import sparse
import xarray as xr

r = np.arange(100)

x = np.random.random((100, 100, 100))
x[x < 0.9] = 0  # fill most of the array with zeros

s = sparse.COO(x)  # convert to sparse array

data = xr.DataArray(s,
                        dims=("a", "b", "c"),
                        coords={"a": r, "b": r, "c": r})

# Saving to netcdf
data.to_netcdf("sparce.nc")
