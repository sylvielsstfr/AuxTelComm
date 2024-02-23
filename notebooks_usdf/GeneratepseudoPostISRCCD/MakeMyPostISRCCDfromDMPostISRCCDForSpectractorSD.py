#!/usr/bin/env python
# coding: utf-8

# # Make postISRCCD from DM PostISRCCD for Spectractor StandAlone
# 
# 
# - work with Weakly_2023_35
# - use jupyter kernel LSST : **lsst_distrib_2023_01**
# 
# 
# 
# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab
# - creation date : 2023/09/20
# - last update : 2024/02/22
# 
# 
#write output file according hierarchy
#         Filter/DATE


import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.dates as mdates

import numpy as np
import pandas as pd

from matplotlib.colors import LogNorm

from mpl_toolkits.axes_grid1 import make_axes_locatable

import matplotlib.ticker                         # here's where the formatter is
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

from astropy.visualization import (MinMaxInterval, SqrtStretch,ZScaleInterval,PercentileInterval,
                                   ImageNormalize,imshow_norm)
from astropy.visualization.stretch import SinhStretch, LinearStretch,AsinhStretch,LogStretch


from astropy.io import fits


import lsst.daf.butler as dafButler
from lsst.daf.butler import CollectionType

import warnings
warnings.filterwarnings("ignore")


# Configuration
#---------------

#DATE = 20230912
#FILTER="cyl_lens~holo4_001"
#FILTER="cyl_lens~holo4_003"

#my_collection = "u/dagoret/spectro/collimatorholo4003noflat/runs_20230912"
#FILTER="collimator~holo4_003"
#my_collection = "u/dagoret/spectro/emptyholo4003noflat/runs_20230912"
#FILTER="empty~holo4_003"
#my_collection = "u/dagoret/spectro/emptyholo4001noflat/runs_20230912"
#FILTER="empty~holo4_001"


#DATE = 20230913
#my_collection = "u/dagoret/spectro/collimatorholo4003noflat/runs_20230913"
#FILTER="collimator~holo4_003"
#my_collection = "u/dagoret/spectro/emptyholo4003noflat/runs_20230913"
#FILTER="empty~holo4_003"
#my_collection = "u/dagoret/spectro/emptyholo4001noflat/runs_20230913"
#FILTER="empty~holo4_001"



#DATE = 20230914
#my_collection = "u/dagoret/spectro/collimatorholo4003noflat/runs_20230914"
#FILTER="collimator~holo4_003"
#my_collection = "u/dagoret/spectro/emptyholo4003noflat/runs_20230914"
#FILTER="empty~holo4_003"
#my_collection = "u/dagoret/spectro/emptyholo4001noflat/runs_20230914"
#FILTER="empty~holo4_001"


#DATE = 20230117
#my_collection = "u/dagoret/BPS_manyspectro_v100"
#FILTER="empty~holo4_003"


#DATE = 20230118
#my_collection = "u/dagoret/BPS_manyspectro_v102"
#FILTER="empty~holo4_003"



#DATE = 20211006
#my_collection = "u/dagoret/spectro/w_2023_44_spec3.0.3/holo_SDSS_g_oct2021"
#FILTER="SDSS_g~holo4_003"

#DATE = 20211103
#my_collection = "u/dagoret/spectro/w_2023_44_spec3.0.3/holo_SDSS_g_nov2021"
#FILTER="SDSS_g~holo4_003"


DATE = 20230928
my_collection = "u/dagoret/auxtel_atmo_202209_v3.0.3_doGainsPTC_rebin2_231221"
FILTER="empty~holo4_003"


#where_clause = f"instrument=\'LATISS\' AND exposure.day_obs={DATE} AND exposure.science_program=\'spec\'"
where_clause = f"instrument=\'LATISS\' AND exposure.day_obs={DATE}"


# output path
#---------------------
top_path_out="dm_postisrccd_img"
path_out=f"{top_path_out}/{FILTER}"

# output path of type top/date/filter
#----------------------------------------

if not os.path.exists(path_out):
    os.makedirs(path_out)

path_out=f"{path_out}/{DATE}"

if not os.path.exists(path_out):
    os.makedirs(path_out)
    

# read list of exposures
# From the butler and the given user collection
#--------------------------------------------------

#repo = "/sdf/group/rubin/repo/main" # repo/main
repo="/sdf/group/rubin/repo/oga/"  # /repo/embargo
butler = dafButler.Butler(repo)
registry = butler.registry


datasetRefs = registry.queryDatasets(datasetType='postISRCCD', collections=my_collection, where= where_clause)

all_dataId = []
all_postisrccd  = []
all_exposures = []
for i, ref in enumerate(datasetRefs):
   
    print(f"========({i})================datasetType = postISRCCD ============================================")
    print("fullId..................:",ref.dataId.full)
    print("exposure................:",ref.dataId["exposure"])
    print("band....................:",ref.dataId["band"])
    print("physical filter.........:",ref.dataId["physical_filter"])
    print("run.....................:",ref.run)
    the_exposure = ref.dataId["exposure"]
    the_day_obs = ref.dataId["exposure"]//100_000
    the_seq_num = ref.dataId["exposure"]- the_day_obs*100_000    
    the_dataId = {'day_obs': the_day_obs,'seq_num':the_seq_num,'detector':0}
    print(the_dataId)
    #spec       = butler.get('spectraction',the_dataId)
    postisrccd = butler.get('postISRCCD', exposure=the_exposure, detector=0, collections=my_collection, instrument='LATISS')
    all_dataId.append(the_dataId) 
    all_exposures.append(the_exposure)
    all_postisrccd.append(postisrccd)
all_exposures = np.array(all_exposures)



N = len(all_postisrccd)
all_exposures_sortedindexes = np.argsort(all_exposures)


for idx in range(N):
    idx_sorted = all_exposures_sortedindexes[idx]
    dm_postisrccd = all_postisrccd[idx_sorted]
    dm_postisrccd_md = dict(dm_postisrccd.getMetadata())
    print(f"==================={all_exposures[idx_sorted]}=======================")
    print('LSST CALIB DATE BIAS :',dm_postisrccd_md['LSST CALIB DATE BIAS'])
    print('LSST CALIB UUID BIAS :',dm_postisrccd_md['LSST CALIB UUID BIAS']) 
    print('LSST CALIB RUN BIAS  :',dm_postisrccd_md['LSST CALIB RUN BIAS'])
    print("-------")
    print('LSST CALIB DATE DEFECTS :',dm_postisrccd_md['LSST CALIB DATE DEFECTS'])
    print('LSST CALIB UUID DEFECTS :',dm_postisrccd_md['LSST CALIB UUID DEFECTS']) 
    print('LSST CALIB RUN DEFECTS  :',dm_postisrccd_md['LSST CALIB RUN DEFECTS'])
    



# Save in files
#-----------------
# Note only header of raw image is saved because OBJECT name is only in raw image header.
#It is possible to do a clever mixture of both headers later



for idx in range(N):
    idx_sorted = all_exposures_sortedindexes[idx]
    dm_postisrccd = all_postisrccd[idx_sorted]
    dm_postisrccd_md = dict(dm_postisrccd.getMetadata())
    exposure_selected =all_exposures[idx_sorted]
    raw_img= butler.get('raw', dataId={'exposure': exposure_selected, 'instrument': 'LATISS', 'detector': 0}, collections = ['LATISS/calib','LATISS/raw/all',] )

    meta = raw_img.getMetadata()
    md = meta.toDict()
      
    
    print(f"save exposure selected = {exposure_selected}")

    # we will save the postisrccd image
    arr=dm_postisrccd.image.array
    # 180 degree rotation
    rotated_array = arr[::-1,::-1] #rotate the array 180 degrees
    
    
    meta = raw_img.getMetadata()
    md = meta.toDict()

    the_object = md['OBJECT']
    the_am= md['AMSTART']
    the_filter=md['FILTER']
    
    if the_object == "MU-COL":
        md['OBJECT']="HD38666"
        the_object = md['OBJECT']

    filename_out = f"exposure_{exposure_selected}_dmpostisrccd.fits"
    fullfilename_out=os.path.join(path_out,filename_out)
    
    print(f">>>>  output filename {filename_out} object {the_object}")
    
    hdr = fits.Header()
    
    for key,value in md.items():
        if key == 'OBJECT':
            print(key,value)
        hdr[str(key)]=value
        
    # need this    
    hdr["AMEND"] = hdr["AMSTART"]
    
    # be aware weather data may be missing
    if hdr["AIRTEMP"] == None:
        hdr["AIRTEMP"] = 10.0
        print("AIRTEMP key missing")

    if hdr["PRESSURE"] == None:
        hdr["PRESSURE"] = 744.
        print("PRESSURE key missing")

    if hdr["HUMIDITY"] == None:
        hdr["HUMIDITY"] = 50.
        print("HUMIDITY key missing")

    if hdr["WINDSPD"] == None:
        hdr["WINDSPD"] = 5.
        print("WINDSPD key missing")

    if hdr["WINDDIR"] == None:
        hdr["WINDDIR"] = 0.
        print("WINDDIR key missing")

    if hdr["SEEING"] == None:
        hdr["SEEING"] = 1.15
        print("SEEING key missing")
       
    
    # Be carefull for Spectractor Standalone, 2 hdu units are necessary
    
    primary_hdu = fits.PrimaryHDU(header=hdr)
    image_hdu = fits.ImageHDU(rotated_array)
    hdu_list = fits.HDUList([primary_hdu, image_hdu])
    hdu_list.writeto(fullfilename_out,overwrite=True)
    
    
  




