
### DEPRECATED ###

import numpy as np
from collections import OrderedDict

def get_aermodel_as_attributes(aer_filename):
    """
    Return an OrderedDict with all the content of user-defined aerosol files
    :param aer_filename: a .aer file
    :return: an OrderedDict
    """
    try:
        with open(aer_filename, 'r') as faer:
            aerosols = {}
            content = faer.readlines()
            nb_aer = int(content[0].split(sep=':')[1])
            aerosols['NB MODES'] = nb_aer
            for i in np.arange(nb_aer):
                aerosol = {}
                #aerosol['NAME'] = content[8*i + 1].split('(')[1].split(sep=')')[0]

                aerosol['MODAL RADIUS (microns)'] = float(content[8*i + 2].split(sep=':')[1])
                aerosol['STANDARD DEVIATION (microns)'] = float(content[8*i + 3].split(sep=':')[1])
                aerosol['REFRACTIVE INDEX at WA_SIMU - Real part'] = float(content[8 * i + 4].split(sep=':')[1])
                aerosol['REFRACTIVE INDEX at WA_SIMU - Imaginary part (<0)'] = float(content[8 * i + 5].split(sep=':')[1])
                aerosol['REFRACTIVE INDEX at WA_REF - Real part'] = float(content[8 * i + 6].split(sep=':')[1])
                aerosol['REFRACTIVE INDEX at WA_REF - Imaginary part (<0)'] = float(content[8 * i + 7].split(sep=':')[1])
                aerosol['PROPORTION TO THE TOTAL AOT at WA_REF'] = float(content[8 * i + 8].split(sep=':')[1])

                aerosols[content[8 * i + 1].split('(')[1].split(sep=')')[0]] = aerosol

                #aerosols.append(aerosol)

        return(aerosols)


    except FileNotFoundError:
        pass

#toto = get_aermodel_as_attributes("/home/colinj/code/luts_init/multimodes_aer/resources/sulfate_hr30_60_dust_20_bc_20_550nm.aer")
#print(toto)