#!/usr/bin/env python
# coding: utf-8

# # Make postISRCCD from raw for Spectractor StandAlone
# 
# 
# - work with Weakly_2023_01
# - use jupyter kernel LSST : **lsst_distrib_2023_01**
# 
# 
# 
# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab
# - creation date : 2023/12/08
# - last update : 2023/07/20
# 
# 


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

DATE = 20230817
FILTER = "empty-holo4_003"


# input filename
#----------------

filename_visits = f"all_visitdispersers/{DATE}/visitdispersers_{DATE}_filt_{FILTER}.list"


# output path
#---------------------
top_path_out="my_postisrccd_img"
path_out=f"{top_path_out}/{DATE}"

# output path of type top/date/filter
#----------------------------------------

if not os.path.exists(path_out):
    os.makedirs(path_out)

path_out=f"{path_out}/{FILTER}"

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


#repo = '/sdf/group/rubin/repo/main'
repo="/sdf/group/rubin/repo/oga/"
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
calibCollections = ['LATISS/calib','LATISS/raw/all',
'LATISS/calib/DM-28636',
'LATISS/calib/DM-28636/curated/19700101T000000Z',
'LATISS/calib/DM-28636/curated/20180101T000000Z',
'LATISS/calib/DM-28636/unbounded',
'LATISS/calib/DM-33875',
'LATISS/calib/DM-36484/bias.20221005a',
'LATISS/calib/DM-36484/biasGen.20221005a',
'LATISS/calib/DM-36484/biasGen.20221005a/20221006T000101Z',
'LATISS/calib/DM-36484/dark.20221006a',
'LATISS/calib/DM-36484/darkGen.20221005a',
'LATISS/calib/DM-36484/darkGen.20221005a/20221006T222501Z',
'LATISS/calib/DM-36484/darkGen.20221006a',
'LATISS/calib/DM-36484/darkGen.20221006a/20221006T222921Z',
'LATISS/calib/DM-36484/flat-SDSSg.20221006a',
'LATISS/calib/DM-36484/flat-SDSSi.20221006a',
'LATISS/calib/DM-36484/flat-SDSSr.20221006a',
'LATISS/calib/DM-36484/flatGen-SDSSg.20221006a',
'LATISS/calib/DM-36484/flatGen-SDSSg.20221006a/20221007T002703Z',
'LATISS/calib/DM-36484/flatGen-SDSSi.20221006a',
'LATISS/calib/DM-36484/flatGen-SDSSi.20221006a/20221007T003732Z',
'LATISS/calib/DM-36484/flatGen-SDSSiD.20221006a',
'LATISS/calib/DM-36484/flatGen-SDSSiD.20221006a/20221007T004708Z',
'LATISS/calib/DM-36484/flatGen-SDSSr.20221006a',
'LATISS/calib/DM-36484/flatGen-SDSSr.20221006a/20221006T233657Z',
'LATISS/calib/DM-36484/verifyBias.20221005a',
'LATISS/calib/DM-36484/verifyBias.20221005a/20221006T000747Z',
'LATISS/calib/DM-36484/verifyBias.20221005a/20221006T213237Z',
'LATISS/calib/DM-36484/verifyBias.20221005b',
'LATISS/calib/DM-36484/verifyBias.20221005b/20221019T205236Z',
'LATISS/calib/DM-36484/verifyDark.20221006a',
'LATISS/calib/DM-36484/verifyDark.20221006a/20221006T224403Z',
'LATISS/calib/DM-36484/verifyFlat-SDSSg.20221006a',
'LATISS/calib/DM-36484/verifyFlat-SDSSg.20221006a/20221007T003418Z',
'LATISS/calib/DM-36484/verifyFlat-SDSSi.20221006a',
'LATISS/calib/DM-36484/verifyFlat-SDSSi.20221006a/20221007T004423Z',
'LATISS/calib/DM-36484/verifyFlat-SDSSr.20221006a',
'LATISS/calib/DM-36484/verifyFlat-SDSSr.20221006a/20221006T234341Z',
'LATISS/calib/DM-36719',
'LATISS/calib/DM-36719/bias.20221107',
'LATISS/calib/DM-36719/biasGen.20221107a',
'LATISS/calib/DM-36719/biasGen.20221107a/20221107T205127Z',
'LATISS/calib/DM-36719/biasGen.20221107b',
'LATISS/calib/DM-36719/biasGen.20221107b/20221107T213306Z',
'LATISS/calib/DM-36719/dark.20221107',
'LATISS/calib/DM-36719/darkGen.20221107a',
'LATISS/calib/DM-36719/darkGen.20221107a/20221107T223409Z',
'LATISS/calib/DM-36719/flat-SDSSg.20221107',
'LATISS/calib/DM-36719/flat-SDSSi.20221107',
'LATISS/calib/DM-36719/flat-SDSSr.20221107',
'LATISS/calib/DM-36719/flatGen-SDSSg.20221107a',
'LATISS/calib/DM-36719/flatGen-SDSSg.20221107a/20221108T002737Z',
'LATISS/calib/DM-36719/flatGen-SDSSi.20221107a',
'LATISS/calib/DM-36719/flatGen-SDSSi.20221107a/20221108T005202Z',
'LATISS/calib/DM-36719/flatGen-SDSSr.20221107a',
'LATISS/calib/DM-36719/flatGen-SDSSr.20221107a/20221107T235401Z',
'LATISS/calib/DM-36719/ptcGen-SDSSr.20221107a',
'LATISS/calib/DM-36719/ptcGen-SDSSr.20221107a/20221108T180421Z',
'LATISS/calib/DM-36719/verifyBias.20221107b',
'LATISS/calib/DM-36719/verifyBias.20221107b/20221107T220410Z',
'LATISS/calib/DM-36719/verifyDark.20221107a',
'LATISS/calib/DM-36719/verifyDark.20221107a/20221107T232823Z',
'LATISS/calib/DM-36719/verifyFlat-SDSSg.20221107a',
'LATISS/calib/DM-36719/verifyFlat-SDSSg.20221107a/20221108T004225Z',
'LATISS/calib/DM-36719/verifyFlat-SDSSi.20221107a',
'LATISS/calib/DM-36719/verifyFlat-SDSSi.20221107a/20221108T012110Z',
'LATISS/calib/DM-36719/verifyFlat-SDSSi.20221107a/20221108T014950Z',
'LATISS/calib/DM-36719/verifyFlat-SDSSr.20221107a',
'LATISS/calib/DM-36719/verifyFlat-SDSSr.20221107a/20221108T000940Z',
'LATISS/calib/DM-39505',                    
'LATISS/calib/DM-39505/crosstalk.20230602',
'LATISS/calib/DM-38946',
'LATISS/calib/DM-38946/noRGseq/bias.20230503',
'LATISS/calib/DM-38946/noRGseq/dark.20230503',
'LATISS/calib/DM-38946/noRGseq/flat-g.20230503',
'LATISS/calib/DM-38946/noRGseq/flat-r.20230503',
'LATISS/calib/DM-38946/noRGseq/flat-i.20230503',
'u/czw/DM-37811/parOStest.20230202a/calib/flat-OG550.20230207a',
'u/czw/DM-37811/parOStest.20230202a/calib/flat-BG40.20230207a', 
'u/czw/DM-37811/parOStest.20230202a/calib/flat-SDSSr.20230203a',
'u/czw/DM-37811/parOStest.20230202a/calib/flat-SDSSg.20230203a',
'u/czw/DM-37811/parOStest.20230202a/calib/flat-SDSSi.20230202a',
'u/czw/DM-37811/parOStest.20230202a/calib/dark.20230202a',
'u/czw/DM-37811/parOStest.20230202a/calib/bias.20230202a',
'LATISS/calib/DM-37587/flat-BG40.20230113a',
'LATISS/calib/DM-37587/flat-OG550.20230113a',
'LATISS/calib/DM-37587/flat-SDSSr.20230113a',
'LATISS/calib/DM-36719',
'LATISS/calib/DM-36719/bias.20221107',
'LATISS/calib/DM-36719/dark.20221107',
'LATISS/calib/DM-36719/flat-SDSSi.20221107',
'LATISS/calib/DM-36719/flat-SDSSr.20221107',
'LATISS/calib/DM-36719/flat-SDSSg.20221107',
'LATISS/calib/DM-36484/bias.20221005a',
'LATISS/calib/DM-36484/dark.20221006a',
'LATISS/calib/DM-36484/flat-SDSSg.20221006a',
'LATISS/calib/DM-36484/flat-SDSSr.20221006a',
'LATISS/calib/DM-36484/flat-SDSSi.20221006a',
'u/czw/defects.20220608',
'LATISS/calib/DM-33875',                                        
'u/czw/DM-28920/calib/bias.20210720',                 
'u/czw/DM-28920/calib/dark.20210720a',     
'u/calib/DM-32209-20211013a-g',
'u/calib/DM-32209-20211013a-felh',
'u/czw/DM-28920/calib/flat.20210720',
'u/czw/DM-28920/calib/defect.20210720a',
'LATISS/calib/DM-39635',
'LATISS/calib/DM-39635/unbounded','LATISS/defaults','LATISS/raw/all']                   
                   
                   


# get Master Bias
#---------------------

butler = dafButler.Butler(repo, collections=calibCollections)
camera = butler.get('camera', instrument=cameraName)
bias = butler.get('bias',instrument=cameraName,detector=0)
defects = butler.get('defects',instrument=cameraName,detector=0)


# Save in files
#-----------------

for index,row in df.iterrows():
    
    exposure_selected =row["date"]*100000+row["seq"]
    
    print(f"=================================== ISR for exposure {exposure_selected} ========================================")

    # must use the calib associated to that exposures
    raw_img= butler.get('raw', dataId={'exposure': exposure_selected, 'instrument': 'LATISS', 'detector': 0}, collections = collection)
    bias = butler.get("bias",instrument=cameraName, exposure= exposure_selected , detector=0, collections=calibCollections)
    defects = butler.get('defects',instrument=cameraName, exposure= exposure_selected ,detector=0,collections=calibCollections)
    
    
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
    





