#!/bin/python
import argparse
import xarray as xr
import numpy as np
import os, sys

import common.Sos as Sos


def exp(wavelength, thetas, aer_model, output_dir, aer_file,
        tau_min=0, tau_max=1.2, tau_step=0.4,
        rho_s_min=0.1, rho_s_max=1.0, rho_s_step=0.3):
    """
    Create output array and set values from SOS_ABS runs
    :param wavelength: simulation wavelength, in micrometers
    :param thetas: sun zenith angle, 0 is nadir
    :param aer_model: use 5 for multimode
    :param output_dir: root output directory
    :param aer_file: user defined aerosol mixture
    :param tau_min: aerosol AOT at reference wavelength, from
    :param tau_max: aerosol AOT at reference wavelength, to
    :param tau_step: aerosol AOT at reference wavelength, step
    :param rho_s_min: surface reflectance, from
    :param rho_s_max: surface reflectance, to
    :param rho_s_step: surface reflectance, step
    :return: a data.nc in output_dir
    """
    # Set dimensions
    tau_list = np.arange(tau_min, tau_max, tau_step)
    rho_s_list = np.arange(rho_s_min, rho_s_max, rho_s_step)

    data = xr.DataArray(np.zeros((len(tau_list), len(rho_s_list))),
                        dims=("tau", "rho_s"),
                        coords={"tau": tau_list, "rho_s": rho_s_list})

    for t in range(len(tau_list)):
        for s in range(len(rho_s_list)):
            r = Sos.Sos_Run(wavelength,
                            thetas,
                            tau_list[t],
                            aer_model,
                            rho_s_list[s],
                            output_dir,
                            aer_defmixture=aer_file)

            rho_toa = r.launch()
            print("tau: %4.2f, rho_s: %4.2f, rho_toa: %8.6f" % (tau_list[t], rho_s_list[s], rho_toa))

            data[t, s] = rho_toa

    print(data.values)

    data.to_netcdf("%s/data.nc" % output_dir)


def main():
    """
    Intended to launch a sequence of SOS_ABS runs along tau and rho_s to get rho_toa from the combination of args.

    Warning: assumes that the main SOS_ABS exec file is in system path

    Example of usage:
    multimode.py -w 0.55 -s 0 -m 5 -a /home/colinj/code/luts_init/multimodes_aer/resources/dust50_bc50_550nm.aer -o tmp
    :return: a data.nc in the output_dir
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wavelength",
                        help="Wavelength in micrometers",
                        required=False, default=0.55, type=float)
    parser.add_argument("-s", "--thetas",
                        help="Solar zenith angle",
                        required=False, default=0.0, type=float)
    parser.add_argument("-m", "--aer_model",
                        help="Aerosol model, use 5 for SOS_ABS multimode",
                        required=False, default=5, type=int)
    parser.add_argument("-a", "--aer_file",
                        help="User defined aerosol file",
                        required=False, type=str)
    parser.add_argument("-o", "--output_dir",
                        help="Output directory",
                        required=True, type=str)
    args = parser.parse_args()

    # Check args
    assert os.path.isdir(args.output_dir)
    # If multimode (5), a file must by given
    if args.aer_model == 5:
        assert os.path.isfile(args.aer_file)

    exp(args.wavelength,
        args.thetas,
        args.aer_model,
        args.output_dir,
        args.aer_file)

    sys.exit(0)

if __name__ == "__main__":
    main()
