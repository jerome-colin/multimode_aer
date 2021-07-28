import subprocess
import sys, os
import shutil
import platform


def _flatten(in_list):
    flat = ''
    for i in in_list:
        flat += ' ' + i

    return flat


class Sos_Run_Multimode():
    def __init__(self,
                 main_wa,
                 ang_thetas,
                 aer_aotref,
                 surf_alb,
                 aer_defmixture,
                 main_resroot,
                 ang_rad_nbgauss = 40,
                 ang_aer_nbgauss = 40,
                 aer_waref = 0.55,
                 ap_psurf = 1013,
                 view_dphi = 180,
                 surf_type = 0,
                 igmax = 200,
                 aer_dirmie = None ,
                 surf_dir = None,
                 sos_abs_fic = None):
        """
        Create an instance of SOS_ABS run with the following arguments and sys config
        :param main_wa: wavelength in micrometers
        :param ang_thetas: sun zenith angle (0 is nadir)
        :param aer_aotref: aerosol AOT at reference wavelength (0.55)
        :param surf_alb: surface reflectance
        :param main_resroot: output root directory
        :param ang_rad_nbgauss: discrete number of angles used for rad calc, 40 recommended
        :param ang_aer_nbgauss: discrete number of angles used for aer calc, 40 recommended
        :param aer_defmixture: file defining the mixture of aerosols, user defined
        :param aer_waref: reference wavelength for aerosols, use 0.55
        :param ap_psurf: surface pressure, use 1013hPa by default
        :param view_dphi: step of relative azimuth
        :param surf_type: use 0 for lambertian
        :param igmax: RTFM
        :param aer_dirmie: output dir for Mie
        :param surf_dir: output dir for surface
        :param sos_abs_fic: path to be exported as env variable
        """

        # Custom local
        if platform.node() == "":
            self.sos_abs_fic = '/home/colinj/code/SOS_ABS_V4.0_beta6/fic'
        else:
            self.sos_abs_fic = '/work/scratch/colinj/SOS_ABS_V4.0_beta6/fic'

        # Path to root
        self.main_resroot = main_resroot

        if aer_dirmie is None:
            aer_dirmie = main_resroot + '/MIE'

        if surf_dir is None:
            surf_dir = main_resroot + '/BRDF_BPDF'

        # Other settings
        self.args = ['SOS_ABS_MAIN.exe']
        self.args.append("-SOS_Main.Wa %6.3f" % main_wa)
        self.args.append("-SOS_Main.ResRoot %s" % main_resroot)
        self.args.append("-SOS_Main.Log SOS_Main.Log")
        self.args.append("-ANG.Rad.NbGauss %i" % ang_rad_nbgauss)
        self.args.append("-ANG.Aer.NbGauss %i" % ang_aer_nbgauss)
        self.args.append("-ANG.Thetas %6.3f" % ang_thetas)
        self.args.append("-SOS.View 2")
        self.args.append("-SOS.View.Dphi %i" % view_dphi)
        self.args.append("-SOS.IGmax %i" % igmax)
        self.args.append("-SOS.Ipolar 0")
        self.args.append("-SOS.ResFileUp SOS_Up.txt")
        self.args.append("-SOS.ResFileDown SOS_Down.txt")
        self.args.append("-SOS.ResBin SOS_Result.bin")
        self.args.append("-SOS.MDF 0.0279")
        self.args.append("-AP.AerProfile.Type 1")
        self.args.append("-AP.HR 8.0")
        self.args.append("-AP.AerHS.HA 2.0")
        self.args.append("-AP.Psurf %6.1f" % ap_psurf)
        self.args.append("-AP.AbsProfile.Type 7")
        self.args.append("-AP.SpectralResol 10.")
        self.args.append("-AER.DirMie %s" % aer_dirmie)
        self.args.append("-AER.Waref %8.3f" % aer_waref)
        self.args.append("-AER.AOTref %4.2f" % aer_aotref)
        self.args.append("-AER.ResFile Aerosols.txt")
        self.args.append("-AER.Tronca 1")
        self.args.append("-AER.Model 5")
        self.args.append("-AER.DefMixture %s" % aer_defmixture)
        self.args.append("-SURF.Dir %s" % surf_dir)
        self.args.append("-SURF.Type %i" % surf_type)
        self.args.append("-SURF.Alb %6.2f" % surf_alb)
        self.args.append("-SURF.Ind 1.34")
        self.args.append("-SOS.Trans fic_trans.txt")

    def launch(self, main_resroot, cleanup=True):
        """
        creates and launch a SOS_ABS run according to args
        :return: a rho_toa value for dphi = 0
        """
        os.environ['SOS_ABS_FIC'] = self.sos_abs_fic
        cmd = _flatten(self.args)

        if not os.path.isdir("log"):
            os.mkdir("log")
            print("Info: creating log directory")

        with open("log/" + main_resroot.replace('/','_') + '_out.txt', 'w+') as fout:
            with open("log/" + main_resroot.replace('/','_') + '_err.txt', 'w+') as ferr:
                subprocess.call(cmd, shell=True, stdout=fout, stderr=ferr)

        try:
            with open(self.main_resroot + '/SOS/SOS_Up.txt', 'r') as sos_up:
                rho_toa = float(sos_up.readline().split()[2])
                if cleanup:
                    shutil.rmtree(main_resroot)
                return rho_toa

        except FileNotFoundError:
            print("Error: cmd failed (%s)" % cmd)
            print("Error: SOS_ABS failed, check log")
            sys.exit(1)
