import xarray as xr

ds0560 = xr.open_dataset("/home/colinj/code/luts_init/multimodes_aer/hal/data_0560_dense.nc")['rho_toa']
ds0492 = xr.open_dataset("/home/colinj/code/luts_init/multimodes_aer/hal/data_0492_dense.nc")['rho_toa']
ds0945 = xr.open_dataset("/home/colinj/code/luts_init/multimodes_aer/hal/data_0945_dense.nc")['rho_toa']


print(ds0560.sel(wavelength=0.56, rDU=1, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0, RH=0.3, thetas=15,
                         tau=0.3, rho_s=0.85).values)
print(ds0492.sel(wavelength=0.492, rDU=1, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0, RH=0.3, thetas=15,
                         tau=0.3, rho_s=0.85).values)

#dsall = xr.concat((ds0492, ds0560), dim="wavelength")

#print(dsall.dims)


# print(dsall.sel(wavelength=0.56, rDU=0, rBC=0, rOM=0, rSS=1, rSU=0, rNI=0, rAM=0, RH=0.3, thetas=45,
#                          tau=0.1, rho_s=0.85).values)
# print(dsall.sel(wavelength=0.492, rDU=0, rBC=0, rOM=0, rSS=1, rSU=0, rNI=0, rAM=0, RH=0.3, thetas=45,
#                          tau=0.1, rho_s=0.85).values)