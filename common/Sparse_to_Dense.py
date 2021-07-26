import xarray as xr
import numpy as np
import common.Ratio as Ratio

def split_model(model, verbose=False):
    rDu = float(model[2:5])/100
    rBC = float(model[7:10])/100
    rOM = float(model[12:15])/100
    rSS = float(model[17:20])/100
    rSU = float(model[22:25])/100
    rNI = float(model[27:30])/100
    rAM = float(model[32:35])/100
    RH  = float(model[37:40])/100

    if verbose:
        print("rDu=%6.3f | rBC = %6.3f | rOM = %6.3f | rSS = %6.3f | rSU = %6.3f | rNI = %6.3f | rAM = %6.3f | RH = %6.3f" % (rDu, rBC, rOM, rSS, rSU, rNI, rAM, RH))

    return rDu, rBC, rOM, rSS, rSU, rNI, rAM, RH

def to_dense(wavelength_list, ratios, relative_humidity, res_array):

    zeros_arr = np.zeros((len(wavelength_list), ratios.size, ratios.size, ratios.size, ratios.size, ratios.size, ratios.size, ratios.size,
                          len(relative_humidity), res_array['thetas'].size, res_array['tau'].size, res_array['rho_s'].size))
    data = xr.DataArray(zeros_arr,
                        dims=("wavelength", "rDU", "rBC", "rOM", "rSS", "rSU", "rNI", "rAM", "RH", "thetas", "tau", "rho_s"),
                        coords={"wavelength": wavelength_list,
                                "rDU": ratios.coords,
                                "rBC": ratios.coords,
                                "rOM": ratios.coords,
                                "rSS": ratios.coords,
                                "rSU": ratios.coords,
                                "rNI": ratios.coords,
                                "rAM": ratios.coords,
                                "RH": relative_humidity,
                                "thetas": res_array['thetas'].values,
                                "tau": res_array['tau'].values,
                                "rho_s": res_array['rho_s'].values})

    for m in res_array['model'].values:
        rDu, rBC, rOM, rSS, rSU, rNI, rAM, RH = split_model(m)


    thetas_list = res_array['thetas'].values

    print(thetas_list)

    # TODO: go through res_array and allocate documented values to proper data coordinates

res_array = xr.open_dataset("/home/colinj/code/luts_init/multimodes_aer/data_0560.nc")

ratios = Ratio.Ratio(1)
relative_humidity = [30.]

to_dense([0.560], ratios, relative_humidity, res_array)