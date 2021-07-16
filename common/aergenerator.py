import numpy as np
import enum
import xarray as xr

class Aerosol:

    def __init__(self):
        self.nb = None
        self.name = None
        self.hr = None
        self.size_distribution_mode = "LND"
        self.modal_radius = None
        self.stddev = None
        self.refractive_index_wa_simu_real = None
        self.refractive_index_wa_simu_img = None
        self.refractive_index_wa_ref_real = None
        self.refractive_index_wa_ref_img = None
        self.proportion = 0

    class Satellite(enum.Enum):
        S2A = 'SENTINEL2-A'
        S2B = 'SENTINEL2-B'

    class Bandes(enum.Enum):
        S2A_WA = [443 , 492, 560, 664, 704, 740, 783, 830, 865, 945, 1373, 1613, 2198]
        S2A_TauRay = [0.23499, 0.15560 , 0.09043, 0.04497, 0.03551, 0.02897, 0.02316, 0.01852, 0.01549, 0.01083, 0.00241, 0.00127, 0.00037]
        S2B_WA = [443 ,491, 559, 665, 704, 739, 780, 830, 864, 943, 1377, 1609, 2181]
        S2B_TauRay = [0.23591, 0.15598, 0.09102, 0.04486, 0.03556, 0.02918, 0.02353, 0.01850, 0.01554, 0.01092, 0.00239, 0.00128, 0.00038]

    def as_str(self):
        aer_str = "SIZE DISTRIBUTION MODE %i (%s): %s\n" % (self.nb, self.name, self.size_distribution_mode)
        aer_str += "    MODAL RADIUS (microns)  : %8.6f\n" % self.modal_radius
        aer_str += "    STANDARD DEVIATION (microns): %8.6f\n" % self.stddev
        aer_str += "    REFRACTIVE INDEX at WA_SIMU - Real part: %8.6f\n" % self.refractive_index_wa_simu_real
        aer_str += "    REFRACTIVE INDEX at WA_SIMU - Imaginary part (<0): %8.6f\n" % self.refractive_index_wa_simu_img
        aer_str += "    REFRACTIVE INDEX at WA_REF - Real part: %8.6f\n" % self.refractive_index_wa_ref_real
        aer_str += "    REFRACTIVE INDEX at WA_REF - Imaginary part (<0): %8.6f\n" % self.refractive_index_wa_ref_img
        aer_str += "    PROPORTION TO THE TOTAL AOT at WA_REF : %8.6f\n" % self.proportion

        return aer_str


