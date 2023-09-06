#!/usr/bin/env python
# coding: utf-8

# process spectra for AuxTel Holograms  with new spectractor (version=2.5 July 2023)
# branch  master

# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab/IN2P3/CNES, DESC-LSST fullmember, behalf AuxTel Teal VERA C. Rubin observatory
# - creation date : 2023-09-06
# - Last update : 2023-09-06

# source /sps/lsst/groups/auxtel/softs/MySetup_py39_SDC.sh 

import sys
print("python path       : ",sys.path)
print("python executable : ",sys.executable)
print("python version    : ",sys.version)


def is_nan(x):
    return (x != x)

def GetPaths(computer_name):
    """
    """
    
    if computer_name == "HOSTCC":
        
        path_auxtel="/sps/lsst/groups/auxtel"
        path_spectractor=os.path.join(path_auxtel,"softs/github/desc/Spectractor")
        path_spectractor_config=os.path.join(path_spectractor,"config")
    
        path_images=os.path.join(path_auxtel,"data/hack_usdf/my_postisrccd_img_forspectractor_2023/"+filterdispersername+"/"+DATE)
        if configdir == "":
            path_output_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+DATE)
        else:
            path_output_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir+"/"+DATE)
            path_topoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir)
            path_toptopoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername)
            path_toptoptopoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode)
        
    elif computer_name == "LAPTOP1":
        path_auxtel="/Users/dagoret/DATA/AuxTelData2023"
        path_spectractor=os.path.join(path_auxtel,"/Users/dagoret/MacOSX/GitHub/LSST/Spectractor")
        path_spectractor_config=os.path.join(path_spectractor,"config")
        path_images=os.path.join(path_auxtel,"data/2023/"+filterdispersername+"/"+DATE)
        if configdir == "":
            path_output_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+DATE)
        else:
            path_output_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir+"/"+DATE)
            path_topoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir)
            path_toptopoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername)
            path_toptoptopoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode)
        
        
    elif computer_name == "WORKIMAC":
        path_auxtel="/Users/sylvie/DATA/AuxTelData2023"
        path_spectractor=os.path.join(path_auxtel,"/Users/sylvie/MacOSX/GitHub/LSST/Spectractor")
        path_spectractor_config=os.path.join(path_spectractor,"config")
        path_images=os.path.join(path_auxtel,"data/2023/"+filterdispersername+"/"+DATE)
        if configdir == "":
            path_output_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+DATE)
        else:
            path_output_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir+"/"+DATE)
            path_topoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir)
            path_toptopoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername)
            path_toptoptopoutput_spectractor=os.path.join(path_auxtel,"data/2023/OutputSpectractor/"+imagemode)
            
            
        
    elif computer_name == "HOMEIMAC":
        path_auxtel="/Volumes/Backup2020/DATA"
        path_spectractor=os.path.join(path_auxtel,"MacOSX/GitHub/LSST/Spectractor")
        path_spectractor_config=os.path.join(".","config")
        path_images=os.path.join(path_auxtel,"hack_usdf/my_postisrccd_img_forspectractor_2023/"+filterdispersername+"/"+DATE)
        
        # /Volumes/Backup2020/DATA/AuxTelDATA2023/data/2023/OutputSpectractor
        
        if configdir == "":
            path_output_spectractor=os.path.join(path_auxtel,"AuxTelDATA2023/data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+DATE)
        else:
            path_output_spectractor=os.path.join(path_auxtel,"AuxTelDATA2023/data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir+"/"+DATE)
            path_topoutput_spectractor=os.path.join(path_auxtel,"AuxTelDATA2023/data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir)
            path_toptopoutput_spectractor=os.path.join(path_auxtel,"AuxTelDATA2023/data/2023/OutputSpectractor/"+imagemode+"/"+filterdispersername)
            path_toptoptopoutput_spectractor=os.path.join(path_auxtel,"AuxTelDATA2023/data/2023/OutputSpectractor/"+imagemode)
    
    
    
    
    elif computer_name == "USDF":
        path_auxtel="/sdf/home/d/dagoret/rubin-user/DATA"
        path_spectractor=os.path.join("/sdf/home/d/dagoret","repos/repos_w_2023_35/Spectractor")
        path_spectractor_config=os.path.join(".","config")
        path_images=os.path.join(path_auxtel,"AuxtelData2023/my_postisrccd_img_forspectractor_2023/"+filterdispersername+"/"+DATE)
        
        # /Volumes/Backup2020/DATA/AuxTelDATA2023/data/2023/OutputSpectractor
        
        if configdir == "":
            path_output_spectractor=os.path.join(path_auxtel,"AuxtelData2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+DATE)
        else:
            path_output_spectractor=os.path.join(path_auxtel,"AuxtelData2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir+"/"+DATE)
            path_topoutput_spectractor=os.path.join(path_auxtel,"AuxtelData2023/OutputSpectractor/"+imagemode+"/"+filterdispersername+"/"+configdir)
            path_toptopoutput_spectractor=os.path.join(path_auxtel,"AuxtelData2023/OutputSpectractor/"+imagemode+"/"+filterdispersername)
            path_toptoptopoutput_spectractor=os.path.join(path_auxtel,"AuxtelData2023/OutputSpectractor/"+imagemode)
        
        
    else:
        print(f"Unknown computer {computer_name}")
        
              
    return path_auxtel,path_spectractor,path_spectractor_config,path_images,path_toptoptopoutput_spectractor, path_toptopoutput_spectractor, path_topoutput_spectractor, path_output_spectractor
        


#-----------------------------------------------------------------------------------------------
# Handle input arguments
#-----------------------------------------------------------------------------------------------
#
#  1  : DAYNUM  ex 20230817
#  2  : filterdispersername  ex "empty~holo4_003"
#  3  : image_index in logbook 

nargs = len(sys.argv) - 1

print(f"number of arguments = {nargs}")
print("sys.argv = ",sys.argv)

if nargs == 3:
    # Output argument-wise
    position = 1
    while (nargs >= position):
        print ("Parameter %i: %s" % (position, sys.argv[position]))
        if position == 1 :
            arg_DAYNUM = sys.argv[position]
        elif position == 2:
            arg_filterdispersername = sys.argv[position]
        elif position == 3 :
            arg_image_index = int(sys.argv[position])-1
        position = position + 1
        
else:
    print(f" \t !!!! error {sys.argv[0]} requires 3 positional arguments : 1: the datestring 2: filterdispersername 3: the image rank") 
    print(f" \t - example :  \t python {sys.argv[0]} 20230817 empty~holo4_003 1")
    exit(-1)
    

print("=============================================================================")
print(f"{sys.argv[0]} start with DAYNUM = {arg_DAYNUM}  , filterdispersername = {arg_filterdispersername} and  image_index = {arg_image_index}")    

# remove bad python paths
all_paths_to_remove = ['/opt/conda/lib/python3.8/site-packages','/pbs/home/d/dagoret/.local/lib/python3.8/site-packages']
for path_to_remove in all_paths_to_remove:
    if path_to_remove in sys.path:
        print(f"remove {path_to_remove} from sys.path")
        sys.path.remove(path_to_remove)

# suppress calls to X-Server
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib import  transforms
import pandas as pd

import matplotlib.ticker                         # here's where the formatter is
import os
import re

plt.rcParams["figure.figsize"] = (12,12)
plt.rcParams["axes.labelsize"] = 'xx-large'
plt.rcParams['axes.titlesize'] = 'xx-large'
plt.rcParams['xtick.labelsize']= 'xx-large'
plt.rcParams['ytick.labelsize']= 'xx-large'


from iminuit import Minuit
import iminuit


from astropy.io import fits
from astropy.coordinates import Angle
from astropy import units as u
from spectractor import parameters
from spectractor.extractor.extractor import Spectractor,dumpParameters
# dumpfitparameters
from spectractor.extractor.images import *
from spectractor.config import load_config,set_logger
from scipy import ndimage, misc




from distutils.dir_util import copy_tree
import shutil


# # Configuration
# ## Config for the notebook

version="v7.0"  # version of flipping
# create output directories if not exist and clean existing files
FLAG_MANAGE_OUTPUT_SPECTRACTOR=True
# allow to run reconstruction with Spectractor
FLAG_GO_FOR_RECONSTRUCTION_WTH_SPECTRACTOR=True
FLAG_RUNWITHEXCEPTIONS = False

#----Configuration for Spectractor

print("List of configuration files available : ",os.listdir("./config"))

# Choose the config filename
# Choose the config filename
list_of_spectractorconfigfiles= ['auxtel_config_holo_DECONVOLUTION_FFMv_REBIN2_Janv2023.ini' ,
                                 'auxtel_config_holo_DECONVOLUTION_FFMv_REBIN1_Janv2023.ini']                                
                                
config_idx = len(list_of_spectractorconfigfiles)-2


configfilename= os.path.join("./config",list_of_spectractorconfigfiles[config_idx])
configdir = "config_" + (list_of_spectractorconfigfiles[config_idx].split("auxtel_config_holo_")[-1]).split(".") [0]

print(f"configfilename = {configfilename}")
print(f"configdir      = {configdir}")


load_config(configfilename)
dumpParameters()


#------------

# path index for each month
DATE = arg_DAYNUM
filterdispersername = arg_filterdispersername
dispersername = "holo"
imagemode = "postISRCCD"
#imagemode = "unflattened"

disperser_label = filterdispersername.split("~")[-1]

# select the computer type

mycomputer_name = "USDF"
path_auxtel,path_spectractor,path_spectractor_config,path_images,path_toptoptopoutput_spectractor, path_toptopoutput_spectractor, path_topoutput_spectractor, path_output_spectractor  = GetPaths(mycomputer_name)




print(f"path_images                   = {path_images}")
print(f"path_toptopoutput_spectractor = {path_toptopoutput_spectractor}")
print(f"path_topoutput_spectractor    = {path_topoutput_spectractor}")
print(f"path_output_spectractor       = {path_output_spectractor}")





## logbooks


# # Logbook for input file selection
# - the logbook contains all input image path and possibily the order 0 position

filename_logbook='logbooks/auxtellogbook_'+filterdispersername+"_"+DATE+'_' + version+'.csv'

print(f"filename_logbook              = {filename_logbook}")

# Read logbook file

df=pd.read_csv(filename_logbook,index_col=0)

pd.set_option('display.max_rows', None)

# show the list of input files from the logbook to select the file index in the logbook
print(df)

# # Selection of input file
# - the input file is selected from the logbook list above

idx=arg_image_index
idxmax = len(df)

if idx<0 or idx>=idxmax:
    print(f"Bad filenumber index {idx} max_idx = {idxmax}")
    exit(-2)

print(df.iloc[idx])
dir_images=path_images
filename_image=df['file'][idx]
target = df['object'][idx]

print(f"from logbook : filename_image = {filename_image}")
print(f"from logbook : target         = {target}")

# ## If order 0 position exists in logbook it is selected, otherwise put it by hand
x0=300
y0=1700

if 'Obj-posXpix' in df.columns and 'Obj-posYpix' in df.columns:
    thex0 = df['Obj-posXpix'][idx]
    if not is_nan(thex0):
        x0=thex0
    they0 = df['Obj-posYpix'][idx]
    if not is_nan(they0):
        y0=they0
    
if not is_nan(x0) and not is_nan(y0):

    print("Order 0 location from logbook : ({},{})".format(x0,y0))
else:
    print("NO Order 0 location from logbook ! ")      

print(f"guess (x0,y0) = ({x0},{y0})")

rootfilename = filename_image.split(".")[0]
rootfilename_split =  rootfilename.split("_") 
filenumberdir = rootfilename_split[1] 

# Fullfilename
filename=os.path.join(dir_images,filename_image)
print(f"input exposure filename = {filename}")

# subdirectory
#subdir=filename_image.split(".")[0]
subdir=filenumberdir

# final output directory (where results will be copied to be backed up at the end)
finalpath_output_spectractor=os.path.join(path_output_spectractor,subdir)
print(f"finalpath_output_spectractor = {finalpath_output_spectractor}")


# local directories to put spectra and plots
if configdir =="":
    output_directory="./outputs_process_" + DATE  + '_' + dispersername + "_" + str(idx+1)
    output_figures="figures_process_" + DATE + '_' + dispersername + "_" + str(idx+1)
else:
    output_directory = "./outputs_process_"+ DATE +"_"+ filterdispersername + "_" + configdir + "_" + str(idx+1)
    output_figures   = "./figures_process_"+ DATE +"_"+ filterdispersername + "_" + configdir + "_" + str(idx+1)
    
if not os.path.isdir(output_directory):
    os.mkdir(output_directory)
if not os.path.isdir(output_figures):
    os.mkdir(output_figures)
    
# prepare argument of Spectractor
config=configfilename    
target=df.iloc[idx]["object"]
target_name_stripped = ''.join(target.split())


# # Configuration of the Spectractor running mode

parameters.DEBUG=True
parameters.VERBOSE=True
parameters.DISPLAY=False
parameters.LIVE_FIT=False

parameters.LSST_SAVEFIGPATH=True
parameters.LSST_SAVEFIGPATH=output_figures


image=Image(file_name=filename, disperser_label=disperser_label, config=config)
title="{}) {}".format(idx,filename_image)
image.plot_image(figsize=(12, 10),scale="log",title=title)
parameters.VERBOSE = True
parameters.DEBUG = True
guess = [x0,y0]
x1, y1 = find_target(image, guess,rotated=False)
print(x1,y1)


# Usually stop here if one just want to get the 0th order location
if not FLAG_GO_FOR_RECONSTRUCTION_WTH_SPECTRACTOR:
    assert False
else:
    assert True


if FLAG_RUNWITHEXCEPTIONS:
    try:
        spectrum = Spectractor(filename, output_directory, guess=[x0,y0], target_label=target_name_stripped, disperser_label=disperser_label, config=config)
    except:
        errtype = sys.exc_info()[0]  # E.g. <class 'PermissionError'>
        description = sys.exc_info()[1]   # E.g. [Errno 13] Permission denied: ...
        
        print("\t +++++++++++++++++++++ Exception occured +++++++++++++++++++++++++++++++++++++++++")
        print(f"\t >>>>>  errtype = {errtype}")
        print(f"\t >>>>>> description = {description}")
else:
    spectrum = Spectractor(filename, output_directory, guess=[x0,y0], target_label=target_name_stripped, disperser_label=disperser_label, config=config)


# # Backup output
# - If no crash occurs, arrive here


def cleandir(path):
    if os.path.isdir(path):
        files=os.listdir(path)
        if len(files) > 0:
            for f in files:
                if os.path.isdir(os.path.join(path,f)):
                    if f==".ipynb_checkpoints":
                        shutil.rmtree(os.path.join(path,f))
                    else:
                        print(" Cannot remove this directory {}".format(os.path.join(path,f)))
                else:
                    os.remove(os.path.join(path,f))



# this flag must be set if one want to clean results from previous runs
if FLAG_MANAGE_OUTPUT_SPECTRACTOR:
    
    # manage global output directory of spectractor
    # Basically it has the name of the input file image
    
    if not os.path.isdir(path_toptoptopoutput_spectractor):
        os.mkdir(path_toptoptopoutput_spectractor)
    
    if not os.path.isdir(path_toptopoutput_spectractor):
        os.mkdir(path_toptopoutput_spectractor) 
        
    if configdir !="":
    # top directory    
        if not os.path.isdir(path_topoutput_spectractor):
            os.mkdir(path_topoutput_spectractor)   
            
            
        if not os.path.isdir(path_output_spectractor):
            os.mkdir(path_output_spectractor)

    
    # if not os.path.isdir(output_directory):
    #    os.mkdir(output_directory)
    # else:
    #    cleandir(output_directory)
 
    # manage subdirs spectrum/ and plots/
    # if not os.path.isdir(output_figures):
    #    os.mkdir(output_figures)
    # else:
    #    cleandir(output_figures)
    
    if not os.path.isdir(finalpath_output_spectractor):
        os.mkdir(finalpath_output_spectractor)
        os.mkdir(os.path.join(finalpath_output_spectractor,"basespec"))
        os.mkdir(os.path.join(finalpath_output_spectractor,"plots"))
    else:
        cleandir(os.path.join(finalpath_output_spectractor,"basespec"))
        cleandir(os.path.join(finalpath_output_spectractor,"plots"))


print("******************************** SUCCESS ********************************************")

copy_tree(output_directory,os.path.join(finalpath_output_spectractor,"basespec"))
copy_tree(output_figures,os.path.join(finalpath_output_spectractor,"plots"))

print("finalpath_output_spectractor = ",finalpath_output_spectractor)

os.listdir(os.path.join(finalpath_output_spectractor,"basespec"))
os.listdir(os.path.join(finalpath_output_spectractor,"plots"))

shutil.rmtree(output_directory)
shutil.rmtree(output_figures)



