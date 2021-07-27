import xarray as xr
import numpy as np



def test_dense_array_560():
    test_data = xr.open_dataset("tmp/data_0560.nc")['rho_toa']

    assert test_data.sel(wavelength=0.56, rDU=0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=1, RH=0.3, thetas=60, tau=0.8, rho_s=0.7).values == 0.343559
    assert test_data.sel(wavelength=0.56, rDU=1.0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0., RH=0.7, thetas=30, tau=0.8, rho_s=0.1).values == 0.140142