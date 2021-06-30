#!/bin/python
import argparse
import xarray as xr
import numpy as np
import os, sys, shutil
from collections import OrderedDict
import itertools
import multiprocessing
import uuid

import common.Sos as Sos
import common.aerfile_parser as prs

import time


def launch(params):
    """
    A one-run function, for // purpose
    :param wavelength:
    :param thetas:
    :param tau:
    :param rho_s:
    :param target:
    :param model:
    :return: rho_toa as float
    """

    wavelength = params[0]
    model = params[1]
    thetas = params[2]
    tau = params[3]
    rho_s = params[4]

    target_root = "tmp"

    # Create a random target path for SOS outputs (avoid defining it before calling launch)
    uuid_str = str(uuid.uuid4())
    target = '%s/tmp_%s' % (target_root, uuid_str)

    r = Sos.Sos_Run_Multimode(wavelength,
                              thetas,
                              tau,
                              rho_s,
                              model,
                              target)

    return r.launch(target)


def exp(wavelength, thetas, aer_collection_dir, output_dir, verbose=False,
        thetas_min=0, thetas_max=85, thetas_step=5,
        tau_min=0.0, tau_max=1.2, tau_step=0.2, #0, 1.2, 0.4
        rho_s_min=0.1, rho_s_max=1.15, rho_s_step=0.05, #0.1, 1.15, 0.15
        netcdf_filename="data.nc"):
    """
    Create output array and set values from SOS_ABS runs
    :param wavelength: simulation wavelength, in micrometers
    :param thetas: sun zenith angle, 0 is nadir
    :param output_dir: root output directory
    :param aer_collection_dir: user defined aerosol mixture
    :param tau_min: aerosol AOT at reference wavelength, from
    :param tau_max: aerosol AOT at reference wavelength, to
    :param tau_step: aerosol AOT at reference wavelength, step
    :param rho_s_min: surface reflectance, from
    :param rho_s_max: surface reflectance, to
    :param rho_s_step: surface reflectance, step
    :param netcdf_filename
    :return: a <netcdf_filename> in <output_dir>
    """
    # Set lists for each dimensions

    wavelength_list = [0.55]
    thetas_list = np.round(np.arange(thetas_min, thetas_max, thetas_step), 1)

    aer_list = []  # fullpath to aer model files
    aer_list_coords = []  # clean aer model name for xarray coords
    for f in os.listdir(aer_collection_dir):
        aer_list.append(os.path.join(aer_collection_dir, f))
        aer_list_coords.append(f.split(sep='.')[0])

    tau_list = np.round(np.arange(tau_min, tau_max, tau_step), 2)
    rho_s_list = np.round(np.arange(rho_s_min, rho_s_max, rho_s_step), 2)

    # Generate a list of tuples where each tuple is a combination of parameters.
    # The list will contain all possible combinations of parameters.
    paramlist = list(itertools.product(wavelength_list, aer_list, thetas_list, tau_list, rho_s_list ))

    # Generate processes equal to the number of cores
    pool = multiprocessing.Pool()

    # Distribute the parameter sets evenly across the cores
    res = pool.map(launch, paramlist)

    # Create an xarray container
    res_arr = np.array(res).reshape((len(aer_list), len(thetas_list), len(tau_list), len(rho_s_list)))
    data = xr.DataArray(res_arr,
                        dims=("model", "thetas", "tau", "rho_s"),
                        coords={"model": aer_list_coords, "thetas": thetas_list, "tau": tau_list, "rho_s": rho_s_list})

    # Saving to netcdf
    data.to_netcdf("%s/%s" % (output_dir, netcdf_filename))

    # TEST VALUES
    # dust_only_550nm, wl=550, thetas=0, tau=0, rho_s=0.1, rho_toa=0.126901
    # sulfate_hr30_80_bc_20_550nm, wl=550, thetas=0, tau=0, rho_s=0.1, rho_toa=0.126901
    # sulfate_hr30_only_550nm, wl=550, thetas=0, tau=0.8, rho_s=0.1, rho_tao=0.311694
    # bc_only_550nm, wl=550, thetas=80, tau=0.4, rho_s=0.6, rho_tao=0.028060
    # dust_only_550nm, wl=550, thetas=5, tau=0.6, rho_s=1.05, rho_tao=1.008341
    # sulfate_hr30_80_bc_20_550nm, wl=550, thetas=55, tau=0.4, rho_s=0.15, rho_toa=0.130648


def main():
    """
    Intended to launch a sequence of SOS_ABS runs along tau and rho_s to get rho_toa from the combination of args.

    Warning: assumes that the main SOS_ABS exec file is in system path

    Example of usage:
    multimode.py 0.55 0 /home/colinj/code/luts_init/multimodes_aer/resources/ tmp
    :return: a data.nc in the output_dir
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("wavelength",
                        help="Wavelength ([0.2:4.0] micrometers)",
                        type=float)
    parser.add_argument("thetas",
                        help="Solar zenith angle ([0:90] degrees)",
                        type=float)
    parser.add_argument("aer_collection_dir",
                        help="Directory containing user defined aerosol file with extension .aer",
                        type=str)
    parser.add_argument("output_dir",
                        help="Root of SOS_ABS output directory",
                        type=str)
    parser.add_argument("--rmdir",
                        help="Force deletion of output dir if exist",
                        action="store_true", default=False)
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
    if not os.path.isdir(args.aer_collection_dir):
        print("Error: %s is not a directory" % args.aer_collection_dir)
        sys.exit(1)
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
        print("Warning: %s not found, created it..." % args.output_dir)
    elif args.rmdir:
        shutil.rmtree(args.output_dir)
        os.mkdir(args.output_dir)
        print("Info: %s cleaned-up" % args.output_dir)

    time_init = time.time()

    exp(args.wavelength,
                                     args.thetas,
                                     args.aer_collection_dir,
                                     args.output_dir,
                                     verbose=args.verbose)

    time_end = time.time()
    print("Done in %12.2fs..." % (time_end-time_init))
    sys.exit(0)


if __name__ == "__main__":
    main()
