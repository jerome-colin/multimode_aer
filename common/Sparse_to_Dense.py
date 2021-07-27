import xarray as xr
import numpy as np
import common.Ratio as Ratio
import sys

def split_model(model, verbose=False):
    rDu = float(model[2:5]) / 100
    rBC = float(model[7:10]) / 100
    rOM = float(model[12:15]) / 100
    rSS = float(model[17:20]) / 100
    rSU = float(model[22:25]) / 100
    rNI = float(model[27:30]) / 100
    rAM = float(model[32:35]) / 100
    RH = float(model[37:40]) / 100

    if verbose:
        print(
            "rDu=%6.3f | rBC = %6.3f | rOM = %6.3f | rSS = %6.3f | rSU = %6.3f | rNI = %6.3f | rAM = %6.3f | RH = %6.3f" % (
            rDu, rBC, rOM, rSS, rSU, rNI, rAM, RH))

    return rDu, rBC, rOM, rSS, rSU, rNI, rAM, RH


def to_dense(wavelength_list, ratios, relative_humidity, res_array):
    zeros_arr = np.zeros((len(wavelength_list), ratios.size, ratios.size, ratios.size, ratios.size, ratios.size,
                          ratios.size, ratios.size,
                          len(relative_humidity), res_array['thetas'].size, res_array['tau'].size,
                          res_array['rho_s'].size))
    data = xr.DataArray(zeros_arr,
                        dims=(
                        "wavelength", "rDU", "rBC", "rOM", "rSS", "rSU", "rNI", "rAM", "RH", "thetas", "tau", "rho_s"),
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

    try:
        for mod in res_array['model'].values:
            rDU, rBC, rOM, rSS, rSU, rNI, rAM, RH = split_model(mod)

            for the in res_array['thetas'].values:
                for tau in res_array['tau'].values:
                    for rho in res_array['rho_s'].values:
                        # print(res_array.sel(model=mod, thetas=the, tau=tau, rho_s=rho).to_array().values[0])
                        data.loc[dict(wavelength=wavelength_list[0], rDU=rDU, rBC=rBC, rOM=rOM, rSS=rSS, rSU=rSU, rNI=rNI,
                                      rAM=rAM, RH=RH, thetas=the, tau=tau, rho_s=rho)] = res_array.sel(model=mod, thetas=the, tau=tau, rho_s=rho).values

        return data

    except KeyError as e:
        print("ERROR: Key error with the following specs")
        print("    res_array dims:")
        print(res_array.dims)
        print(res_array.coords)
        print(res_array['thetas'].values)
        print(res_array['tau'].values)
        print(res_array['rho_s'].values)
        print(    "Vars:")
        print(rDU, rBC, rOM, rSS, rSU, rNI, rAM, RH)
        print("    dense array dims:")
        print(data.dims)
        print(data.coords)
        print(data['wavelength'].values)
        print(data['rDU'].values)
        print(data['rBC'].values)
        print(data['rOM'].values)
        print(data['rSS'].values)
        print(data['rSU'].values)
        print(data['rNI'].values)
        print(data['rAM'].values)
        print(data['RH'].values)
        print(data['thetas'].values)
        print(data['tau'].values)
        print(data['rho_s'].values)
        print(e)
        sys.exit(1)


    # ds = data.to_dataset(name='rho_toa')
    # ds.to_netcdf(outfile)

    # thetas_list = res_array['thetas'].values
    # tau_list = res_array['tau'].values
    # rho_s_list = res_array['rho_s'].values

    # print(tau_list)

    # print(data.sel(wavelength=0.56, rDU=0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=1, RH=0.3, thetas=60, tau=0.8, rho_s=0.7).values)

test = None

if test is not None:
    demo = xr.open_dataset("/home/colinj/code/luts_init/multimodes_aer/data_0560.nc")['rho_toa']
    wavelength_list = [0.56]
    relative_humidity = [0.3]
    ratios = Ratio.Ratio(1)
    data = to_dense(wavelength_list,ratios,relative_humidity,demo)

    print(data.sel(wavelength=0.56, rDU=0, rBC=0, rOM=0, rSS=0, rSU=0, rNI=0, rAM=1, RH=0.3, thetas=60, tau=0.8, rho_s=0.7).values)