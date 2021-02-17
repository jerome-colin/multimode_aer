#!/bin/python
import argparse
import xarray as xr
import numpy as np
import os, sys

import common.Sos as Sos


def exp(wavelength, thetas, aer_file, output_dir, verbose=False,
        tau_min=0, tau_max=1.2, tau_step=0.4,
        rho_s_min=0.1, rho_s_max=1.0, rho_s_step=0.3):
    """
    Create output array and set values from SOS_ABS runs
    :param wavelength: simulation wavelength, in micrometers
    :param thetas: sun zenith angle, 0 is nadir
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

    # Create an xarray container
    data = xr.DataArray(np.zeros((len(tau_list), len(rho_s_list))),
                        dims=("tau", "rho_s"),
                        coords={"tau": tau_list, "rho_s": rho_s_list})

    # Loop over dimensions
    for t in range(len(tau_list)):
        for s in range(len(rho_s_list)):
            r = Sos.Sos_Run_Multimode(wavelength,
                                      thetas,
                                      tau_list[t],
                                      rho_s_list[s],
                                      "%s/t%s_s%s" % (output_dir, str(int(tau_list[t]*100)), str(int(rho_s_list[s]*100))),
                                      aer_defmixture=aer_file)

            rho_toa = r.launch()
            if verbose:
                print("tau: %4.2f, rho_s: %4.2f, rho_toa: %8.6f" % (tau_list[t], rho_s_list[s], rho_toa))

            data[t, s] = rho_toa

    # Saving to netcdf
    data.to_netcdf("%s/data.nc" % output_dir)


def main():
    """
    Intended to launch a sequence of SOS_ABS runs along tau and rho_s to get rho_toa from the combination of args.

    Warning: assumes that the main SOS_ABS exec file is in system path

    Example of usage:
    multimode.py 0.55 0 /home/colinj/code/luts_init/multimodes_aer/resources/dust50_bc50_550nm.aer tmp
    :return: a data.nc in the output_dir
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("wavelength",
                        help="Wavelength ([0.2:4.0] micrometers)",
                        type=float)
    parser.add_argument("thetas",
                        help="Solar zenith angle ([0:90] degrees)",
                        type=float)
    parser.add_argument("aer_file",
                        help="User defined aerosol file",
                        type=str)
    parser.add_argument("output_dir",
                        help="Output directory",
                        type=str)
    parser.add_argument("-v", "--verbose",
                        help="Print values to standard output",
                        action="store_true", default=False)
    args = parser.parse_args()

    # Check args
    if (args.wavelength < 0.2) or (args.wavelength > 4.0):
        print("Error: the wavelength %6.3f is out of SOS_ABS range ([0.2:4.0] micrometers)" % args.wavelength)
        sys.exit(1)
    if (args.thetas < 0.) or (args.thetas > 90.):
        print("Error: the solar zenith angle %6.3f is out of range ([0:90])" % args.thetas)
        sys.exit(1)
    if not os.path.isfile(args.aer_file):
        print("Error: %s is not a file" % args.aer_file)
        sys.exit(1)
    if not os.path.isdir(args.output_dir):
        print("Error: %s is not a directory" % args.output_dir)
        sys.exit(1)

    exp(args.wavelength,
        args.thetas,
        args.aer_file,
        args.output_dir,
        verbose=args.verbose)

    print("Done...")
    sys.exit(0)

if __name__ == "__main__":
    main()
