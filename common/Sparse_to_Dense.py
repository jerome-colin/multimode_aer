import xarray as xr
import numpy as np
import common.Ratio as Ratio
import sys

def split_model(model, verbose=False):
    rDU = float(model[2:5]) / 100
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
            rDU, rBC, rOM, rSS, rSU, rNI, rAM, RH))

    #return '%.1f'%(rDu), '%.1f'%(rBC), '%.1f'%(rOM), '%.1f'%(rSS), '%.1f'%(rSU), '%.1f'%(rNI), '%.1f'%(rAM), '%.1f'%(RH)
    return np.round(rDU, decimals=1), \
           np.round(rBC, decimals=1), \
           np.round(rOM, decimals=1), \
           np.round(rSS, decimals=1), \
           np.round(rSU, decimals=1), \
           np.round(rNI, decimals=1), \
           np.round(rAM, decimals=1), \
           np.round(RH, decimals=3)


def to_dense(wavelength_list, ratios, relative_humidity, res_array):
    zeros_arr = np.zeros((len(wavelength_list), ratios.size, ratios.size, ratios.size, ratios.size, ratios.size,
                          ratios.size, ratios.size,
                          len(relative_humidity), res_array['thetas'].size, res_array['tau'].size,
                          res_array['rho_s'].size), dtype="float32")
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

    #print(data.sel(rDU=0.6, method='nearest').values)

    nmod = 0
    for mod in res_array['model'].values:
        rDU, rBC, rOM, rSS, rSU, rNI, rAM, RH = split_model(mod)

        for the in res_array['thetas'].values:
            for tau in res_array['tau'].values:
                for rho in res_array['rho_s'].values:
                    # print(res_array.sel(model=mod, thetas=the, tau=tau, rho_s=rho).to_array().values[0])
                    try:
                        nmod += 1
                        data.loc[dict(wavelength=wavelength_list[0], rDU=rDU, rBC=rBC, rOM=rOM, rSS=rSS, rSU=rSU, rNI=rNI,
                                      rAM=np.round(rAM, decimals=1), RH=RH, thetas=the, tau=tau, rho_s=rho)] = res_array.sel(model=mod, thetas=the, tau=tau, rho_s=rho).values
                    except KeyError as e:
                        print("ERROR: key error %s for model %i" % (e, nmod))
                        print("   Destination file coordinates: wavelength=%f, rDU=%f, rBC=%f, rOM=%f, rSS=%f, rSU=%f, rNI=%f, rAM=%f, RH=%5.3f, thetas=%5.3f, tau=%5.3f, rho_s=%5.3f" %
                              (wavelength_list[0], rDU, rBC, rOM, rSS, rSU, rNI, rAM, RH, the, tau, rho))
                        print(
                            "   Original file coordinates: model=%s, thetas=%5.3f, tau=%5.3f, rho_s=%5.3f" %
                            (mod, the, tau, rho))


                        print("  Trying to get original file value: %8.6f" % res_array.sel(model=mod, thetas=the, tau=tau, rho_s=rho).values)

                        print("  Destination array structure :")
                        print("    dims: %s " % str(data.dims))
                        print("    coords: %s" % str(data.coords))

                        print("  Trying to get value on destination array: %8.6f" % data.sel(wavelength=wavelength_list[0], rDU=rDU, rBC=rBC, rOM=rOM, rSS=rSS, rSU=rSU, rNI=rNI, rAM=rAM, RH=RH, thetas=the, tau=tau, rho_s=rho).values)


                        sys.exit(1)
    return data





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