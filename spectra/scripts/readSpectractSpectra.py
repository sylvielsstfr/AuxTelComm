#!/usr/bin/env python
# coding: utf-8

# # Study spectra

# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab/IN2P3/CNES, DESC-LSST fullmember, behalf AuxTel Teal VERA C. Rubin observatory
# - creation date : March 29th 2021
# - version 

# # Imports




import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd

import matplotlib.ticker                         # here's where the formatter is
import os
import re

plt.rcParams["figure.figsize"] = (16,5)
plt.rcParams["axes.labelsize"] = 'xx-large'
plt.rcParams['axes.titlesize'] = 'xx-large'
plt.rcParams['xtick.labelsize']= 'xx-large'
plt.rcParams['ytick.labelsize']= 'xx-large'



from spectractor.extractor.spectrum import Spectrum



dir_spectra="/Users/dagoret/DATA/AuxTelData2021/holo/SpectractorQuickLook/FlipCleans"
dir_spectra_model="/Users/dagoret/DATA/AuxTelData2021/holo/SpectractorForwardModel/FlipCleans"


all_files=os.listdir(dir_spectra)
all_files_model=os.listdir(dir_spectra_model)




all_spectra_files = []
for filename in all_files:
    if re.search("_spectrum.fits$",filename):
        all_spectra_files.append(filename)
N=len(all_spectra_files)



all_spectra_files_model = []
for filename in all_files_model:
    if re.search("_spectrum.fits$",filename):
        all_spectra_files_model.append(filename)
N1=len(all_spectra_files_model)





for filename in all_spectra_files:
    fig, axes  = plt.subplots(1, 2)
    fullfilename = os.path.join(dir_spectra,filename)
    
    s=Spectrum(fullfilename, config="config/auxtel_quicklook.ini")
    s.plot_spectrum(ax=axes[0],force_lines=True)
    axes[0].set_title(filename)
    
    if filename in all_spectra_files_model:
        print("found {}".format(filename))
        fullfilename2 = os.path.join(dir_spectra_model,filename)
        print(fullfilename2)
        s2=Spectrum(fullfilename2, config="config/auxtel_quicklook.ini")
        
        print(s2.target.label)
        s2.plot_spectrum(ax=axes[1],force_lines=False)
        axes[1].set_title(filename)
    else:
        print("NOT found {}".format(filename))
    
    plt.show()






