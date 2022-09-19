#!/usr/bin/env python
# coding: utf-8

# # Save Exposures of postISRCCD in fits file
# 
# 
# - work with Weakly_2022_09
# - use jupyter kernel LSST
# 
# 
# 
# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab
# - creation date : 2022/09/19
# - last update : 2022/09/19
# 
# source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_09/loadLSST.bash 
# setup lsst_distrib




import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from astropy.io import fits

import lsst.daf.butler as dafButler


# # Configuration
# ## Select flags options


FLAG_ROTATE_IMG = True
FLAG_TRANSFORM = True



# ## Butler

repo = '/sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3/data/butler.yaml'
butler = dafButler.Butler(repo)
registry = butler.registry


# ## Utils



def isflat(row):
    #print(row["filter"])
    if str(row["type"]) == "flat":
        return True
    
    else:
        return False 



collection = "u/dagoret/first_test2"
datasetRefs = registry.queryDatasets(datasetType='postISRCCD', collections=collection, where= "instrument='LATISS'")



pd.set_option('display.max_rows', 2000)
column_names = ["id","run","type_name","band","filter","exposure"]
df = pd.DataFrame(columns = column_names)



all_ref_for_postisrccd = []
    
for count, ref in enumerate(datasetRefs):    
    all_ref_for_postisrccd.append(ref.dataId["exposure"])

    row = [ref.id ,
           ref.run,
           ref.datasetType.name,
           ref.dataId["band"],
           ref.dataId["physical_filter"],
           ref.dataId["exposure"] ]
    #print(row)
    df.loc[count] = row
    
 

all_ref_for_postisrccd=np.array(all_ref_for_postisrccd)
dates_of_exposures = (all_ref_for_postisrccd/100000).astype(int)
df["exposure_date"] = (df["exposure"]//100000).astype(int)
df["expseq"] = df["exposure"] - df["exposure_date"]*100000


print("df.columns \t : ",df.columns)


all_dates = df["exposure_date"].unique()
print("all_dates \t : ",all_dates)


all_filters = df["filter"].unique()
print("all_filters \t : ", all_filters)


# Selection of date only

DATESEL =  20220608

print("Selected date \t : ", DATESEL)


all_filters_thiday = df[df["exposure_date"]== DATESEL]["filter"].unique()
print("all filters this day : ",all_filters_thiday) 

# temporary
#all_filters_thiday = np.delete(all_filters_thiday,0)


NBFILTERSTHIDAY = len(all_filters_thiday) 


#FILTERSEL = "empty~ronchi170lpmm"
#FILTERSEL = 'empty~holo4_003'

# LOOP on filters
for FILTERSEL in all_filters_thiday:

    print("Current filter : \t ", FILTERSEL)

    cut = (df["exposure_date"] == DATESEL) &  (df["filter"] == FILTERSEL)
    df_sel = df[cut]
    print(df_sel)
    all_exposures_selected = df_sel["exposure"].values
    print("\t all exposures selected \t : ",all_exposures_selected)


    # Where all output image goes (year is related to the release, not the observation date
    topoutputdir = "/sps/lsst/groups/auxtel/data/2022"
    outputdir = os.path.join(topoutputdir,FILTERSEL)
    outputsubdir = os.path.join(outputdir,str(DATESEL))

    print("\t output directory \t : ",outputsubdir)

    Path(outputsubdir).mkdir(parents=True, exist_ok=True)


    # LOOP on exposures
    for exposure_selected in all_exposures_selected:
    
        raw= butler.get('raw', dataId={'exposure': exposure_selected, 'instrument': 'LATISS', 'detector': 0}, collections = collection)
        meta = raw.getMetadata()
        md = meta.toDict()
    
        md['HA'] = (md['HASTART']+ md['HAEND'])/2.
    
        targetname = md['OBJECT']
        targetname_split=targetname.split(":")
        print("--- ",targetname)
        if len(targetname_split)==2:
            targetname=targetname_split[-1]
            md['OBJECT']=targetname
            if targetname == "ETADOR" or targetname == "ETA1DOR" or targetname == "ETA2DOR":
                targetname="eta dor"
            if targetname == "MUCOL":
                targetname="mu. col"
        
        print("\t \t target name ",targetname)
        md['OBJECT']=targetname
    
        ccd = butler.get('postISRCCD', dataId={'exposure': exposure_selected, 'instrument': 'LATISS', 'detector': 0}, collections = collection)
        img_data =ccd.image.array
    
        filenameout = "exposure_" + str(exposure_selected)+"_postisrccd.fits"
        fullfilenameout = os.path.join(outputsubdir,filenameout)
    
        #flip_image=np.flip(img_data, 0)  # flip the image for Spectractor
        flip_image = np.flipud(np.fliplr(img_data))
    
    
        hdr = fits.Header()
    
        for key,value in md.items():
            hdr[str(key)]=value
        
        primary_hdu = fits.PrimaryHDU(header=hdr)
        image_hdu = fits.ImageHDU(flip_image)
        hdu_list = fits.HDUList([primary_hdu, image_hdu])
    
        hdu_list.writeto(fullfilenameout ,overwrite=True)
    
    
print("This is the End !")    





