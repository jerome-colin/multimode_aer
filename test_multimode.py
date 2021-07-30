import xarray as xr
import multimode as mlt

def test_dense_array_560_oddtau(test_data):
    assert test_data.sel(wavelength=0.56, rDU=0, rBC=0, rOM=0, rSS=1, rSU=0, rNI=0, rAM=0, RH=0.9, thetas='75',
                         tau=0.5, rho_s=0.7).values == 0.152516

    print("TEST COMPLETED...")


# def test_dense_array_560_eventau(test_data):
#
#     pass
#
#     try:
#         assert test_data.sel(wavelength=0.56, rDU=0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=1, RH=0.3, thetas=60, tau=0.8, rho_s=0.7).values == 0.343559
#         assert test_data.sel(wavelength=0.56, rDU=1.0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0., RH=0.7, thetas=30,
#                              tau=0.8, rho_s=0.1).values == 0.140142
#     except KeyError:
#         pass

    # except AssertionError:
    #     print(ini_data.sel(model="DU100BC000OM000SS000SU000NI000AM000RH70", thetas=30, tau=0.8, rho_s=0.1).values)
    #     print(test_data.sel(wavelength=0.56, rDU=1.0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0., RH=0.7, thetas=30, tau=0.8, rho_s=0.1).values)
    #assert test_data.sel(wavelength=0.56, rDU=1.0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0., RH=0.3, thetas=30, tau=0.8, rho_s=0.1).values == 0.140142
    #assert test_data.sel(wavelength=0.56, rDU=1.0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0., RH=0.9, thetas=30, tau=0.8, rho_s=0.1).values == 0.140142
    #assert test_data.sel(wavelength=0.56, rDU=0.5, rBC=0.5, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0., RH=0.7, thetas=0., tau=0.8, rho_s=0.1).values == 0.087949
    #assert test_data.sel(wavelength=0.56, rDU=0.0, rBC=1.0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=0., RH=0.9, thetas=60., tau=0.4, rho_s=0.4).values == 0.072137
    #assert test_data.sel(wavelength=0.56, rDU=0.5, rBC=0.0, rOM=0, rSS=0.5, rSU=0, rNI=0, rAM=0., RH=0.7, thetas=0., tau=0.8, rho_s=0.25).values == 0.286377

if __name__ == "__main__":
    test_data = xr.open_dataset("hal/data_0560_dense.nc")['rho_toa']
    print("INIT TEST...")
    test_dense_array_560_oddtau(test_data)