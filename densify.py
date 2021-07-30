
import sys
import argparse
import time
import xarray as xr
import common.Sparse_to_Dense as sp
import common.Ratio as ra




def main():
    """

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("infile",
                        help="wavelength",
                        type=str)
    parser.add_argument("wl",
                        help="wavelength",
                        type=float)
    args = parser.parse_args()

    time_init = time.time()

    ds = xr.open_dataset("/home/colinj/code/luts_init/multimodes_aer/hal/data_0560.nc")['rho_toa']
    wavelength_list = [args.wl]
    relative_humidity = [0.3, 0.7, 0.9]
    ratios = ra.Ratio(0.2)
    dense = sp.to_dense(wavelength_list, ratios, relative_humidity, ds)
    dense_ds = dense.to_dataset(name='rho_toa')
    dense_ds.to_netcdf("%s_dense.nc" % (args.infile[:-3]), mode="w")

    time_end = time.time()
    print("Done in %12.2fs..." % (time_end - time_init))
    sys.exit(0)


if __name__ == "__main__":
    main()
