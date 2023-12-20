#!/usr/bin/env python
# coding: utf-8

# # Make postISRCCD from raw for Spectractor StandAlone
# 
# 
# - work with Weakly_2023_44
# - use jupyter kernel LSST : **lsst_distrib_2023_01**
# 
# 
# 
# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab
# - creation date : 2023/09/15
# - last update : 2023/12/20
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



# Assembly task
# https://github.com/lsst/ip_isr/blob/main/python/lsst/ip/isr/isrTask.py

from lsst.ip.isr.assembleCcdTask import (AssembleCcdConfig, AssembleCcdTask)
from lsst.ip.isr.isrTask import (IsrTask, IsrTaskConfig)

#https://github.com/lsst/ip_isr/blob/main/python/lsst/ip/isr/overscan.py
from lsst.ip.isr import  OverscanCorrectionTaskConfig, OverscanCorrectionTask



# LSST Display
#import lsst.afw.display as afwDisplay
#afwDisplay.setDefaultBackend('matplotlib')



import lsst.daf.butler as dafButler

import warnings
warnings.filterwarnings("ignore")


# Configuration
#---------------

#DATE = 20230117
#FILTER="empty-holo4_003"
#FILTER="BG40_65mm_1-holo4_003"
#FILTER="OG550_65mm_1-holo4_003"

#DATE = 20230118
#FILTER = "BG40_65mm_1-holo4_003"
#FILTER = "OG550_65mm_1-holo4_003"
#FILTER = "empty-holo4_003"

#DATE = 20230119
#FILTER="empty-holo4_003"
#FILTER="BG40_65mm_1-holo4_003"
#FILTER="OG550_65mm_1-holo4_003"

#DATE = 20230131
#FILTER = "empty-holo4_003"
#FILTER="BG40_65mm_1-holo4_003"
#FILTER="OG550_65mm_1-holo4_003"


#DATE = 20230201
#FILTER = "empty-holo4_003"
#FILTER="BG40_65mm_1-holo4_003"
#FILTER="OG550_65mm_1-holo4_003"


#DATE = 20230202
#FILTER = "empty-holo4_003"
#FILTER="BG40_65mm_1-holo4_003"
#FILTER="OG550_65mm_1-holo4_003"

#DATE = 20230215
#FILTER="empty-holo4_003"


#DATE = 20230315
#FILTER="empty-holo4_003"

#DATE = 20230316
#FILTER="empty-holo4_003"

#DATE = 20230704
#FILTER = "empty-holo4_003"

#DATE = 20230705
#FILTER = "empty-holo4_003"

#DATE = 20230706
#FILTER = "empty-holo4_003"


#DATE = 20230718
#FILTER = "empty-holo4_003"

#DATE = 20230720
#FILTER = "empty-holo4_003"

#DATE = 20230801
#FILTER = "empty-holo4_003"

#DATE = 20230802
#FILTER = "empty-holo4_003"

#DATE = 20230815
#FILTER = "empty-holo4_003"

#DATE = 20230817
#FILTER = "empty-holo4_003"


#DATE = 20230912
#FILTER="cyl_lens~holo4_001"
#FILTER="cyl_lens~holo4_003"
#FILTER="collimator~holo4_003"
#FILTER="empty~holo4_001"
#FILTER="empty~holo4_003"

#DATE = 20230913
#FILTER="collimator~holo4_003"
#FILTER="cyl_lens~holo4_003"
#FILTER="empty~holo4_003"
#FILTER="empty~holo4_001"

#DATE = 20230914
#FILTER="collimator~holo4_003"
#FILTER="cyl_lens~holo4_003"
#FILTER="empty~holo4_003"
#FILTER="empty~holo4_001"




############### 2021 ##############  In repo main
#-rw-r--r-- 1 dagoret rubin_users 338 Dec 20 01:35 visitdispersers_20211006_filt_BG40-holo4_003.list
#-rw-r--r-- 1 dagoret rubin_users 338 Dec 20 01:35 visitdispersers_20211006_filt_empty-holo4_003.list
#-rw-r--r-- 1 dagoret rubin_users 338 Dec 20 01:35 visitdispersers_20211006_filt_FELH0600-holo4_003.list
#-rw-r--r-- 1 dagoret rubin_users 338 Dec 20 01:35 visitdispersers_20211006_filt_SDSSg-holo4_003.list


#DATE = 20211006
#FILTER="SDSSg-holo4_003"
#FILTER="BG40-holo4_003"
#FILTER="collimator-holo4_003"
#FILTER="empty-holo4_003"

#-rw-r--r-- 1 dagoret rubin_users 442 Dec 20 01:36 visitdispersers_20211103_filt_BG40-holo4_003.list
#-rw-r--r-- 1 dagoret rubin_users 442 Dec 20 01:36 visitdispersers_20211103_filt_empty-holo4_003.list
#-rw-r--r-- 1 dagoret rubin_users 559 Dec 20 01:36 visitdispersers_20211103_filt_FELH0600-holo4_003.list
#-rw-r--r-- 1 dagoret rubin_users 442 Dec 20 01:36 visitdispersers_20211103_filt_SDSSg-holo4_003.list


DATE = 20211103
FILTER="SDSSg-holo4_003"
#FILTER="BG40-holo4_003"
#FILTER="collimator-holo4_003"
#FILTER="empty-holo4_003"



# input filename
#----------------

filename_visits = f"all_visitdispersers/{DATE}/visitdispersers_{DATE}_filt_{FILTER}.list"


# output path
#---------------------
top_path_out="my_postisrccd_img"
path_out=f"{top_path_out}/{FILTER}"

# output path of type top/date/filter
#----------------------------------------

if not os.path.exists(path_out):
    os.makedirs(path_out)

path_out=f"{path_out}/{DATE}"

if not os.path.exists(path_out):
    os.makedirs(path_out)
    

# read list of exposures
# - generated by ListOfExposures-hologram.ipynb
#--------------------------------------------------


df = pd.read_csv(filename_visits, header=None,skiprows = 1, sep=' ',names=["date","seq"])




for index,row in df.iterrows():
    exposure_selected =row["date"]*100000+row["seq"]
    print(exposure_selected)



# Butler
#-------


repo = '/sdf/group/rubin/repo/main'
#repo="/sdf/group/rubin/repo/oga/"
butler = dafButler.Butler(repo)
registry = butler.registry


collection='LATISS/raw/all'



# configuration of ISR
#----------------------

isr_config =  IsrTaskConfig()



isr_config.doDark = False
isr_config.doFlat =  False
isr_config.doFringe = False
isr_config.doDefect = True
isr_config.doLinearize = False
isr_config.doCrosstalk =  False
isr_config.doSaturationInterpolation = False
isr_config.overscan.fitType: 'MEDIAN_PER_ROW'
isr_config.doBias: True


isr_task = IsrTask(config=isr_config)

###########################################
# REPO=/repo/embargo
# butler query-collections $REPO LATISS/calib
#############################################

calibType = 'bias'
physical_filter = 'empty~empty'
cameraName = 'LATISS'
# Collection name containing the verification outputs.
calibCollections = ['LATISS/calib','LATISS/raw/all',]                   
                   
                   


# get Master Bias
#---------------------

butler = dafButler.Butler(repo, collections=calibCollections)
camera = butler.get('camera', instrument=cameraName)
#bias = butler.get('bias',instrument=cameraName,detector=0)
#defects = butler.get('defects',instrument=cameraName,detector=0)


# Save in files
#-----------------

for index,row in df.iterrows():
    
    exposure_selected =row["date"]*100000+row["seq"]
    
    print(f"=================================== ISR for exposure {exposure_selected} ========================================")

    # must use the calib associated to that exposures
    raw_img= butler.get('raw', dataId={'exposure': exposure_selected, 'instrument': 'LATISS', 'detector': 0}, collections = collection)
    bias = butler.get("bias",instrument=cameraName, exposure= exposure_selected , detector=0, collections=calibCollections)
    defects = butler.get('defects',instrument=cameraName, exposure= exposure_selected ,detector=0,collections=calibCollections)

    # get metadata
    bias_md = dict(bias.getMetadata())
    try:
        MB_date= bias_md['CALIB_CREATION_DATE']
        MB_time = bias_md['CALIB_CREATION_TIME']
        print(f"Exposure {exposure_selected}, DATE for Master Bias with short calib list",MB_date, MB_time)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        MB_date= bias_md['CALIB_CREATE_DATE']
        MB_time = bias_md['CALIB_CREATE_TIME']
        print(f"Exposure {exposure_selected}, DATE for Master Bias with short calib list",MB_date, MB_time)
            
    
    defects_md = dict(defects.getMetadata()) 
    try:
        DF_date= defects_md['CALIB_CREATION_DATE']
        DF_time = defects_md['CALIB_CREATION_TIME']
        print(f"Exposure {exposure_selected}, DATE for Master Defect with short calib list",DF_date, DF_time)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        DF_date= defects_md['CALIB_CREATE_DATE']
        DF_time = defects_md['CALIB_CREATE_TIME']
        print(f"Exposure {exposure_selected}, DATE for Master Defect with short calib list",DF_date, DF_time)

    
    # perform the ISR
    isr_img = isr_task.run(raw_img,bias=bias,defects=defects)
    
    arr=isr_img.exposure.image.array
    # 180 degree rotation
    rotated_array = arr[::-1,::-1] #rotate the array 180 degrees
    
    
    meta = raw_img.getMetadata()
    md = meta.toDict()

    the_object = md['OBJECT']
    old_name = ""
    
    if the_object == "MU-COL":
        old_name = the_object
        md['OBJECT']="HD38666"
        the_object = md['OBJECT']
        
    if the_object == "ETA1-DOR":
        old_name = the_object
        md['OBJECT']="HD42525"
        the_object = md['OBJECT']
    
    the_am= md['AMSTART']
    the_filter=md['FILTER']

    filename_out = f"exposure_{exposure_selected}_pseudo-postisrccd.fits"
    fullfilename_out=os.path.join(path_out,filename_out)
    
    if old_name == "":
        print(f">>>>  output filename {filename_out} target {the_object}")
    else:
         print(f">>>>  output filename {filename_out} target {the_object} ({old_name})")
        
    
    hdr = fits.Header()
    
    for key,value in md.items():
        hdr[str(key)]=value
        
    # need this    
    hdr["AMEND"] = hdr["AMSTART"]

    # be aware weather data may be missing
    if hdr["AIRTEMP"] == None:
        hdr["AIRTEMP"] = 10.0

    if hdr["PRESSURE"] == None:
        hdr["PRESSURE"] = 744.

    if hdr["HUMIDITY"] == None:
        hdr["HUMIDITY"] = 50.

    if hdr["WINDSPD"] == None:
        hdr["WINDSPD"] = 5.

    if hdr["WINDDIR"] == None:
        hdr["WINDDIR"] = 0.   

    if hdr["SEEING"] == None:
        hdr["SEEING"] = 1.15

    
    # Be carefull for Spectractor, 2 hdu units are necessary
    
    primary_hdu = fits.PrimaryHDU(header=hdr)
    image_hdu = fits.ImageHDU(rotated_array)
    
    hdu_list = fits.HDUList([primary_hdu, image_hdu])
    
    hdu_list.writeto(fullfilename_out,overwrite=True)
    





