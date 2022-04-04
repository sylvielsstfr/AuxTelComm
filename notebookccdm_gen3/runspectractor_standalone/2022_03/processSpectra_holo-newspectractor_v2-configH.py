#!/usr/bin/env python
# coding: utf-8
# %%

# # process spectra for AuxTel with new spectractor (March 2022)

# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab/IN2P3/CNES, DESC-LSST fullmember, behalf AuxTel Teal VERA C. Rubin observatory
# - creation date : Monday 4th April 2022


import sys
print("original python ",sys.path)


nargs = len(sys.argv) - 1

print(f"number of arguments = {nargs}")

if nargs == 2:
    # Output argument-wise
    position = 1
    while (nargs >= position):
        print ("Parameter %i: %s" % (position, sys.argv[position]))
        if position == 1 :
            DAYNUM = sys.argv[position]
        elif position == 2 :
            image_index = int(sys.argv[position])-1
        position = position + 1
        
else:
    print(f"{sys.argv[0]} requires two positional arguments : 1: the datestring 2: the image rank") 
    exit(-1)
    

print("=============================================================================")
print(f"{sys.argv[0]} start with DAYNUM = {DAYNUM}  and  image_index = {image_index}")    


all_paths_to_remove = ['/opt/conda/lib/python3.8/site-packages','/pbs/home/d/dagoret/.local/lib/python3.8/site-packages']

for path_to_remove in all_paths_to_remove:
    if path_to_remove in sys.path:
        print(f"remove {path_to_remove} from sys.path")
        sys.path.remove(path_to_remove)



print("cleaned python path",sys.path)

# suppress calls to X-Server
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt


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



print(sys.executable)
print(sys.version)
#print(sys.version_info)


from iminuit import Minuit
import iminuit

from astropy.io import fits
from spectractor import parameters
from spectractor.extractor.extractor import Spectractor
from spectractor.extractor.images import *
from scipy import ndimage, misc



from scipy.stats import kurtosis,skew
from scipy.stats import kurtosistest,skewtest,normaltest


from distutils.dir_util import copy_tree
import shutil


from datetime import datetime 



############################################################
#   Configuration
###########################################################



version="v5.0"  # version of flipping
# create output directories if not exist and clean existing files
FLAG_MANAGE_OUTPUT_SPECTRACTOR=True
# allow to run reconstruction with Spectractor
FLAG_GO_FOR_RECONSTRUCTION_WTH_SPECTRACTOR=True

FLAG_REMOVE_WCS=False


# path index for each month
#DATE="20220316"
DATE=DAYNUM


# Choose the config filename, here the configF
list_of_spectractorconfigfiles= ["auxtel_configA.ini","auxtel_configB.ini","auxtel_configC.ini","auxtel_configD.ini","auxtel_configE.ini","auxtel_configF.ini","auxtel_configG.ini"]
config_idx = 6
configfilename= os.path.join("./config",list_of_spectractorconfigfiles[config_idx])
configdir = (list_of_spectractorconfigfiles[config_idx].split("_")[-1]).split(".") [0]
configdirshort = configdir
configdir = configdir + "_" + str(image_index)


print(f"selected configuration : {configdir}")

# select if we run at CC or not (locally) 
# /sps/lsst/groups/auxtel/data/2022/holo/20220317
HOSTCC=True



# Set path depending on which computer running (according HOSTCC)
if HOSTCC:
    path_auxtel="/sps/lsst/groups/auxtel"
    path_spectractor=os.path.join(path_auxtel,"softs/github/desc/Spectractor")
    path_spectractor_config=os.path.join(path_spectractor,"config")
    path_images=os.path.join(path_auxtel,"data/2022/holo/"+DATE)
    if configdir == "":
        path_output_spectractor=os.path.join(path_auxtel,"data/2022/OutputSpectractor/holo/"+DATE)
    else:
        path_output_spectractor=os.path.join(path_auxtel,"data/2022/OutputSpectractor/holo/"+configdirshort+"/"+DATE)
        path_topoutput_spectractor=os.path.join(path_auxtel,"data/2022/OutputSpectractor/holo/"+configdirshort)
    
else:
    #path_auxtel="/Users/dagoret/DATA/AuxTelData2021"
    path_auxtel="/Users/sylvie/DATA/AuxTelDATA2022/2022"
    #path_spectractor=os.path.join(path_auxtel,"/users/dagoret/MacOSX/github/LSST/Spectractor")
    path_spectractor=os.path.join(path_auxtel,"/Users/sylvie/MacOSX/GitHub/LSST/Spectractor")
    path_spectractor_config=os.path.join(path_spectractor,"config")
    #path_images=os.path.join(path_auxtel,"holo/quickLookExp_v2/"+DATE)
    path_images=os.path.join(path_auxtel,"holo/"+DATE)
    if configdir == "":
        path_output_spectractor=os.path.join(path_auxtel,"OutputSpectractor/holo/"+DATE)
    else:
        path_output_spectractor=os.path.join(path_auxtel,"OutputSpectractor/holo/"+configdirshort+"/"+DATE)
        path_topoutput_spectractor=os.path.join(path_auxtel,"OutputSpectractor/holo/"+configdirshort)
    #path_output_spectractor=os.path.join(path_auxtel,"holo/OutputSpectractor/"+DATE)

# # Utility Functions


def is_nan(x):
    return (x != x)


# # Logbook for input file selection
# 
# - the logbook contains all input image path and possibily the order 0 position



filename_logbook='logbooks/auxtelholologbook_'+DATE+'_' + version+'.csv'
df=pd.read_csv(filename_logbook,index_col=0)
pd.set_option('display.max_rows', None)


# show the list of input files from the logbook to select the file index in the logbook
print(df)


# # Selection of input file
# - the input file is selected from the logbook list above

idx=image_index

print("input file : ",df.iloc[idx]['file'])


print(df.iloc[idx])


myhome=os.getenv("HOME")

dir_images=path_images
print("directory for images : ",dir_images)


filename_image=df['file'][idx]
print("filename for images ",filename_image)


target = df['object'][idx]
print("target : ",target)


# ## If order 0 position exists in logbook it is selected, otherwise put it by hand

x0=df['Obj-posXpix'][idx]
y0=df['Obj-posYpix'][idx]


FLAG_ORDER0_LOCATION=False


if not is_nan(x0)and not is_nan(y0):
    FLAG_ORDER0_LOCATION=True
    print("Order 0 location from logbook : ({},{})".format(x0,y0))
else:
    print("NO Order 0 location from logbook ! ")      


# ## Spectractor Configuration 
# 
# - Usually the Spectractor configuration file is put in local dir **./config**
# 
# 
# Ma suggestion, pour l'étude du centre optique via les scans des hologrammes, est de **mettre SPECTRACTOR_COMPUTE_ROTATION_ANGLE sur False** . 
# 
# Comme les angles ne sont pas très grands, si les marges du rectangle sont assez larges, réglables avec : 
# 
#     [background subtraction parameters] 
#     # half transverse width of the signal rectangular window in pixels 
#     PIXWIDTH_SIGNAL = 40 
# 
# alors le spectrogramme devrait tenir dans une boite rectangulaire même sans rotation de l'image. **L'important est de garder SPECTRACTOR_DECONVOLUTION_FFM à True car c'est lui qui te donnera l'angle de l'axe de dispersion ajusté sur les données, dont la valeur sera dans le mot clé ROTANGLE du header de sortie**. 



rootfilename = filename_image.split(".")[0]
rootfilename_split =  rootfilename.split("_") 
filenumberdir = rootfilename_split[1] 


print("path output spectractor : ",path_output_spectractor)

# Fullfilename
filename=os.path.join(dir_images,filename_image)


# subdirectory
#subdir=filename_image.split(".")[0]
subdir=filenumberdir

# final output directory (where results will be copied to be backed up at the end)
finalpath_output_spectractor=os.path.join(path_output_spectractor,subdir)



# local directories to put spectra and plots
if configdir =="":
    output_directory="./outputs_process_holo"
    output_figures="figures_process_holo"
else:
    output_directory = "./outputs_process_holo_" + configdir
    output_figures   = "./figures_process_holo_" + configdir
    


# Final output directory


guess = [300,1700]
disperser_label = "holo4_003"
# old version
# config = os.path.join(path_spectractor_config,"auxtel_quicklook.ini")
# new version (September 20th 2021)

# configuration

# standard spectractor init configuration
#config = os.path.join(path_spectractor_config,"auxtel.ini")
# selecte specific config
if configdir=="":
    config="./config/auxtel_scanXY.ini"
else:
    config=configfilename
    
    
    
target=df.iloc[idx]["object"]


# ### manage output dir


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
    
    
    if configdir !="":
    # top directory    
        if not os.path.isdir(path_topoutput_spectractor):
            os.mkdir(path_topoutput_spectractor)   
                
        if not os.path.isdir(path_output_spectractor):
            os.mkdir(path_output_spectractor)

    
    
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    else:
        cleandir(output_directory)
 
    # manage subdirs spectrum/ and plots/
    if not os.path.isdir(output_figures):
        os.mkdir(output_figures)
    else:
        cleandir(output_figures)
    
    if not os.path.isdir(finalpath_output_spectractor):
        os.mkdir(finalpath_output_spectractor)
        os.mkdir(os.path.join(finalpath_output_spectractor,"basespec"))
        os.mkdir(os.path.join(finalpath_output_spectractor,"plots"))
    else:
        #cleandir(finalpath_output_spectractor)
        cleandir(os.path.join(finalpath_output_spectractor,"basespec"))
        cleandir(os.path.join(finalpath_output_spectractor,"plots"))


# # Configuration of the Spectractor running mode


parameters.debug=True
parameters.verbose=True
parameters.display=True
parameters.LIVE_FIT=False



# ## Load the image in the new image file with Spectractor




image=Image(file_name=filename, disperser_label=disperser_label, config=config)
print("image.shape",image.data.shape)


# ## Show relevant parameters



parameters.LSST_SAVEFIGPATH=True
parameters.LSST_SAVEFIGPATH=output_figures






# # Plot image and find the target position
# 
# - this image plotting is used to find the order 0 location to be set in logbook
# 
# - for the moment this is humanly done

# ## Load the new image file with Spectractor



title="{}) {}".format(idx,filename_image)
#image.plot_image(figsize=(12, 10),scale="log",title=title)
# - note now the position are written in the make_logbook.ipynb notebook

# ## Set the 0th order location to be provided to Spectractor



# overwrite if localtion is taken from that in logbook
if FLAG_ORDER0_LOCATION : 
    print("Set Order 0 location from logbook : ({},{})".format(x0,y0))
    guess = [x0,y0]


# ## Let Spectractor find the location of the 0th order



parameters.VERBOSE = True
parameters.DEBUG = True
#x1, y1 = find_target(image, guess,rotated=False, use_wcs=False)
x1, y1 = find_target(image, guess,rotated=False)


print(x1,y1)


# ## Check the location of 0th order and Analysis of the quality of its focus


if x1>100:
    WID=100
else:
    WID=50
    

thumbnail=np.copy(image.data[int(y1)-WID:int(y1)+WID,int(x1)-WID:int(x1)+WID])
thumbnail_y=thumbnail.sum(axis=1)
thumbnail_x=thumbnail.sum(axis=0)
xx=np.linspace(int(x1)-WID,int(x1)+WID,len(thumbnail_x))
yy=np.linspace(int(y1)-WID,int(y1)+WID,len(thumbnail_y))
k0=kurtosis(thumbnail,axis=None,bias=True,fisher=True)
kx=kurtosis(thumbnail_x,bias=True,fisher=True)
ky=kurtosis(thumbnail_y,bias=True,fisher=True)
s0=skew(thumbnail,axis=None,bias=True)
sx=skew(thumbnail_x,bias=True)
sy=skew(thumbnail_y,bias=True)
        


# %%


shape_str='\n'.join((
        r'skew     : Sk0 = {:3.3f}, Skx = {:3.3f}, Sky = {:3.3f} \n'.format(s0,sx,sy),
        r'kurtosis : K0  = {:3.3f}, Kx  = {:3.3f},  Ky = {:3.3f}'.format(k0,kx,ky)))


# %%


skew_str='\n'.join((
        r'skew     : Sk0 = {:3.3f}'.format(s0),
        r'             : Skx = {:3.3f}'.format(sx),
        r'             : Sky = {:3.3f}'.format(sy)))


# %%


kurt_str='\n'.join((
        r'kurtosis : K0 = {:3.3f}'.format(k0),
        r'             : Kx = {:3.3f}'.format(kx),
        r'             : Ky = {:3.3f}'.format(ky)))


# %%


kurtosis_test_prob=kurtosistest(thumbnail,axis=None).pvalue
skew_test_prob=skewtest(thumbnail,axis=None).pvalue
normal_test_prob=normaltest(thumbnail,axis=None).pvalue


# %%


kurtosis_test_val=kurtosistest(thumbnail,axis=None).statistic
skew_test_val=skewtest(thumbnail,axis=None).statistic
normal_test_val=normaltest(thumbnail,axis=None).statistic


# %%


kurtosis_test_prob_x=kurtosistest(thumbnail_x).pvalue
skew_test_prob_x=skewtest(thumbnail_x).pvalue
normal_test_prob_x=normaltest(thumbnail_x).pvalue


# %%


kurtosis_test_prob_y=kurtosistest(thumbnail_y).pvalue
skew_test_prob_y=skewtest(thumbnail_y).pvalue
normal_test_prob_y=normaltest(thumbnail_y).pvalue


# %%


skew_str='\n'.join((
    r'skew     : Sk0 = {:3.3f}'.format(s0),
    r'             : Skx = {:3.3f}'.format(sx),
    r'             : Sky = {:3.3f}'.format(sy),
    r'             : p_test   = {:3.3e}'.format(skew_test_prob),
    r'             : p_test_x = {:3.3e}'.format(skew_test_prob_x),
    r'             : p_test_y = {:3.3e}'.format(skew_test_prob_y)))


# %%


kurt_str='\n'.join((
    r'kurtosis : K0 = {:3.3f}'.format(k0),
    r'             : Kx = {:3.3f}'.format(kx),
    r'             : Ky = {:3.3f}'.format(ky),
    r'             : p_test   = {:3.3e}'.format(kurtosis_test_prob),
    r'             : p_test_x = {:3.3e}'.format(kurtosis_test_prob_x),
    r'             : p_test_y = {:3.3e}'.format(kurtosis_test_prob_y)))


# %%


norm_str='\n'.join((
    r'normal  : p_test   = {:3.3e}'.format(normal_test_prob),
    r'             : p_test_x = {:3.3e}'.format(normal_test_prob_x),
    r'             : p_test_y = {:3.3e}'.format(normal_test_prob_y)))


# %%


props = dict(boxstyle='round',edgecolor="w",facecolor="w", alpha=0.5)


# %%


#matplotlib.pyplot.hist(x, 
#                       bins=10, 
#                       range=None, 
#                       normed=False, 
#                       weights=None, 
#                       cumulative=False, 
#                       bottom=None, 
#                       histtype=u'bar', 
#                       align=u'mid', 
#                       orientation=u'vertical', 
#                       rwidth=None, 
#                       log=False, 
#                       color=None, 
#                       label=None, 
#                       stacked=False, 
#                       hold=None, 
#                       **kwargs)


# %%


if 0:
    fig=plt.figure(figsize=(10,10))
    fig.subplots_adjust(left=0.12, right=0.95, wspace=0.3,
                    bottom=0.15, top=0.9)

    ax=fig.add_subplot(222)
    ax.imshow(thumbnail,origin="lower",extent=(int(x1)-WID,int(x1)+WID,int(y1)-WID,int(y1)+WID))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax=fig.add_subplot(221)
    base = plt.gca().transData
    rot = transforms.Affine2D().rotate_deg(-90)
    #ax.plot(yy,thumbnail_y,"g",rotation=u'vertical')
    ax.plot(-yy,thumbnail_y,"g",transform= rot + base)
    ax.set_ylabel("Y")

    ax=fig.add_subplot(224)
    ax.plot(xx,thumbnail_x,"b")
    ax.set_xlabel("X")
    plt.tight_layout()

    ax=fig.add_subplot(223)
    ax.set_xlim(0,10)
    ax.set_ylim(0,10)
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])

    ax.text(0.05, 0.9, skew_str, transform=ax.transAxes, fontsize=12,verticalalignment='top', bbox=props)
    ax.text(0.05, 0.55, kurt_str, transform=ax.transAxes, fontsize=12,verticalalignment='top', bbox=props)
    ax.text(0.05, 0.2, norm_str, transform=ax.transAxes, fontsize=12,verticalalignment='top', bbox=props)
    plt.suptitle(title)
    plt.show()



# Usually stop here if one just want to get the 0th order location
if not FLAG_GO_FOR_RECONSTRUCTION_WTH_SPECTRACTOR:
    assert False
else:
    assert True



parameters.debug=False
parameters.verbose=False
parameters.display=False
parameters.LIVE_FIT=False



print("*************************************  START RUNNING SPECTRACTOR - STANDALONE VERSION ******************************************")

start_time = datetime.now()
    
try:
    spectrum = Spectractor(filename, output_directory, guess=[x1,y1], target_label=target, disperser_label=disperser_label, config=config)
except:
    errtype = sys.exc_info()[0]  # E.g. <class 'PermissionError'>
    description = sys.exc_info()[1]   # E.g. [Errno 13] Permission denied: ...
        
    print("\t +++++++++++++++++++++ Exception occured +++++++++++++++++++++++++++++++++++++++++")
    print(f"\t >>>>>  errtype = {errtype}")
    print(f"\t >>>>>> description = {description}")
         
           

time_elapsed = datetime.now() - start_time
print('\t >>>>>>>>>>>>>>>>>>>>>>>>>>>>  Time elapsed running Spectractor (hh:mm:ss.ms) {} <<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(time_elapsed))


# # Backup output
copy_tree(output_directory,os.path.join(finalpath_output_spectractor,"basespec"))
copy_tree(output_figures,os.path.join(finalpath_output_spectractor,"plots"))
print("finalpath_output_spectractor :",finalpath_output_spectractor )

print("*************************************  END SPECTRACTOR - STANDALONE VERSION ******************************************")





