# libAtmosphericFit
#
# Author          : Sylvie Dagoret-Campagne
# Affiliaton      : IJCLab/IN2P3/CNRS
# Creation Date   : 2023/02/16
#
# A python tool to fit quickly atmospheric transmission of Auxtel Spectra with scipy.optimize and
# using the atmospheric emulator atmosphtransmemullsst
# 
#
#
import os
import atmosphtransmemullsst
from atmosphtransmemullsst.simpleatmospherictransparencyemulator import SimpleAtmEmulator

from scipy.optimize import curve_fit,least_squares
from scipy.interpolate import RegularGridInterpolator

# global variable
 emul = SimpleAtmEmulator(os.path.join(atmosphtransmemullsst.__path__[0],'../data/simplegrid'))


# function definition
class FitAtmosphericParams:
    def __init__(self, wlt,thr,wls,sed,wld,fld):
        self.wlt = wlt
        self.thr = thr
        self.wls = wls
        self.sed = sed
        self.wld = wld
        self.fld = fld


    def fit():
        pass

if __name__ == '__main__':
     emul = SimpleAtmEmulator(os.path.join(atmosphtransmemullsst.__path__[0],'../data/simplegrid'))
