#!/usr/bin/env python
# coding: utf-8

# # process spectra for AuxTel with new spectractor (September 2021): Part 1 guess (x,y) of order 0

# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab/IN2P3/CNES, DESC-LSST fullmember, behalf AuxTel Teal VERA C. Rubin observatory
# - creation date : September 27th 2021
#
# 
# CCIN2P3:
# 
# - works with kernels **anaconda3_auxtel** (with libradtran) and **anaconda3_auxtel_v2** (no libradtran)
# - works with kernel **python 3** locally 

# # Scan
# 
#     # wide scan : HD 160617 
#     # all_myseq_holo=range(234,310)
#     # narrow scan :  HD 160617 
#     # all_myseq_holo=range(317,365)
# 

# # Run Spectractor from python script


# call >> python processSpectra_holo-newspectractor.py -n 93
#


import sys

import contextlib
import os

import sys, getopt

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib import  transforms
import pandas as pd

import matplotlib.ticker                         # here's where the formatter is
import os
import re
from shutil import copyfile


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

from astropy.io import fits



plt.rcParams["figure.figsize"] = (10,10)
plt.rcParams["axes.labelsize"] = 'xx-large'
plt.rcParams['axes.titlesize'] = 'xx-large'
plt.rcParams['xtick.labelsize']= 'xx-large'
plt.rcParams['ytick.labelsize']= 'xx-large'


# Configuration
#--------------

# create output directories if not exist and clean existing files
FLAG_MANAGE_OUTPUT_SPECTRACTOR=True
# allow to run reconstruction with Spectractor
FLAG_GO_FOR_RECONSTRUCTION_WTH_SPECTRACTOR=True


# utility functions
#-------------------
def file_tag_forsorting(filename):
    # m=re.findall('^Cor_holo4_003_.*([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_.*)[.]fits$',filename)
    m = re.findall('^holo4_003_*_(.*)_.*_quickLookExp[.]fits$', filename)
    # print(m)
    words = m[0].split("_")

    outputstring = words[1]

    if outputstring == "slew":
        outputstring += "_icrs"
    return outputstring





def file_target(filename):
    m = file_tag_forsorting(filename)
    if len(m) > 0:
        return m
    elif re.search('NGC4755', filename):
        return ['NGC4755']
    else:
        return []



def cleandir(path):
    if os.path.isdir(path):
        files=os.listdir(path)
        if len(files) > 0:
            for f in files:
                os.remove(os.path.join(path,f))


def is_nan(x):
    return (x != x)


####################################################################################################################
if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:h", ['n=', 'help'])
    except getopt.GetoptError:
        print(' Exception bad getopt with :: ' + sys.argv[0] + ' -n <exposure number>')
        sys.exit(2)




    if len(opts)<=0:
        print(' Exception bad getopt with :: ' + sys.argv[0] + ' -n <exposure number>')
        sys.exit(2)

    num = 0


    # loop on options and their value
    for opt, arg in opts:

        if opt in ('-h', '--help'):
            print('help for usage : ' + sys.argv[0] + ' -n <exposure number>')
            sys.exit(2)
        elif opt in ('-n', '--number'):
            str_num = arg
            num = int(str_num)

        else:
            print(sys.argv[0] + ' -n <number>')
            sys.exit(2)

    print("num=",num)

    #path index for each month
    DATE="2021-07-07"
    DATE2="2021_07_07"


    #paths
    #-------

    # select where to run
    HOSTCC=True
    # select paths


    if HOSTCC:
        path_auxtel="/sps/lsst/groups/auxtel"
        path_spectractor=os.path.join(path_auxtel,"softs/github/desc/Spectractor")
        path_spectractor_config=os.path.join(path_spectractor,"config")
        path_images=os.path.join(path_auxtel,"data/2021/holo/quickLookExp/"+DATE)
        path_output_spectractor = os.path.join(path_auxtel, "data/2021/holo/OutputSpectractor/" + DATE)
    else:
        path_auxtel="/Users/dagoret/DATA/AuxTelData2021"
        path_spectractor=os.path.join(path_auxtel,"/users/dagoret/MacOSX/github/LSST/Spectractor")
        path_spectractor_config=os.path.join(path_spectractor,"config")
        path_images=os.path.join(path_auxtel,"holo/quickLookExp/"+DATE)
        path_output_spectractor=os.path.join(path_auxtel,"holo/OutputSpectractor/"+DATE)




    # Logbook for input file selection
    # -------------------------------
    filename_logbook='logbooks/auxtelholologbook_'+DATE2+'_v3.0.csv'

    df=pd.read_csv(filename_logbook,index_col=0)
    pd.set_option('display.max_rows', None)

    # show the list of input files from the logbook to select the file index in the logbook
    print(df)

    # select the index for input file
    #--------------------------------

    # wide scan : HD 160617
    # all_myseq_holo=range(234,310)

    # narrow scan :  HD 160617
    # all_myseq_holo=range(317,365)

    idx=num

    print(df.iloc[num])

    # check if order 0 location is given in logbook
    #-------------------------------------------------

    FLAG_ORDER0_LOCATION = False
    x0 = df['Obj-posXpix'][idx]
    y0 = df['Obj-posYpix'][idx]

    if not is_nan(x0) and not is_nan(y0):
        FLAG_ORDER0_LOCATION = True
        print("Order 0 location from logbook : ({},{})".format(x0, y0))
    else:
        print("NO Order 0 location from logbook ! ")


    # For Spectractor configuration
    #---------------------------

    myhome=os.getenv("HOME")
    dir_images=path_images

    filename_image=df['file'][idx]
    print(">>> Selected index = {} , input filename = {}".format(idx,filename_image))


    # open image file
    file_target(filename_image)


    # Fullfilename
    filename=os.path.join(dir_images,filename_image)


    # subdirectory
    subdir=filename_image.split(".")[0]

    # final output directory (where results will be copied)
    finalpath_output_spectractor=os.path.join(path_output_spectractor,subdir)

    # local directories
    output_directory="./outputs_process_holo_scan"
    output_figures="figures_process_holo_scan"

    # Final output directory

    disperser_label = "holo4_003"

    # configuration

    # standard configuration
    #config = os.path.join(path_spectractor_config,"auxtel.ini")
    # special for scan in XY
    config="./config/auxtel_scanXY.ini"

    target = file_target(filename_image)[0]





    # manage output directories
    #-------------------------

    # this flag must be set if one want to clean results from previous runs
    if FLAG_MANAGE_OUTPUT_SPECTRACTOR:

        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)
        else:
            cleandir(output_directory)
 
    
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


    # Configuration of the Spectractor running mode
    #---------------------------------------------
    parameters.debug=True
    parameters.verbose=True
    parameters.display=True
    parameters.LIVE_FIT=False


    print("Spectractor configuration")
    print(parameters)



    #parameters.DISPERSER_DIR = os.path.join(spectractor_dir, "extractor/dispersers/")
    #parameters.CONFIG_DIR = os.path.join(spectractor_dir, "../config/")
    #parameters.THROUGHPUT_DIR = os.path.join(spectractor_dir, "simulation/CTIOThroughput/")


    # Transform the input fits file quickExpLook at NCSA under the format expected by Spectractor
    #----------------------------------------------------------------------------------
    copyfile(filename,filename_image)


    # open file
    hdu = fits.open(filename_image)

    hdu.info()


    header=hdu[0].header
    image=hdu[0].data


    hdu.close()


    # Rotate image according what is expected
    rot_image=np.flip(np.flip(image, 1), 0)


    # Remove WCS (not necessary)
    del header['WCSAXES']
    del header['CTYPE1']
    del header['CTYPE2']
    del header['CUNIT1']
    del header['CUNIT2']
    del header['CRVAL1']
    del header['CRVAL2']
    del header['CRPIX1']
    del header['CRPIX2']


    # Reshape the file for load_image_AUXTEL() in Spectractor/spectractor/extractor/images.py
    primary_hdu = fits.PrimaryHDU(header=header)
    image_hdu = fits.ImageHDU(rot_image)

    hdu_list = fits.HDUList([primary_hdu, image_hdu])
    hdu_list.info()
    hdu_list.writeto(filename_image,overwrite=True)

    # Now work on the new image with Spectractor
    image=Image(file_name=filename_image, target_label=target, disperser_label=disperser_label, config=config)


    # Show relevant parameters

    print(parameters.OBS_NAME)
    print(parameters.DISPERSER_DIR)
    print(parameters.DISTANCE2CCD)
    print(parameters.LAMBDA_MIN)
    print(parameters.LAMBDA_MAX)
    print(image.filter_label)


    # set spectractor cnfig
    parameters.LSST_SAVEFIGPATH=True
    parameters.LSST_SAVEFIGPATH=output_figures

    parameters.VERBOSE = True
    parameters.DEBUG = False


    title="{}) {}".format(idx,filename_image)
    image.plot_image(figsize=(10, 8),scale="log",title=title)




    # Order 0 location guess
    #-------------------------

    # with filter
    guess = [600., 2100.] # filename_image=df['file'][0] , holo4_003_RG610_HD160617_20210707_000234_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][1] , holo4_003_RG610_HD160617_20210707_000235_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][2] , holo4_003_RG610_HD160617_20210707_000236_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][3] , holo4_003_RG610_HD160617_20210707_000237_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][4] , holo4_003_RG610_HD160617_20210707_000238_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][5] , holo4_003_RG610_HD160617_20210707_000239_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][6] , holo4_003_RG610_HD160617_20210707_000240_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][7] , holo4_003_RG610_HD160617_20210707_000241_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][8] , holo4_003_RG610_HD160617_20210707_000242_quickLookExp.fits
    guess = [600., 2100.] # filename_image=df['file'][9] , holo4_003_RG610_HD160617_20210707_000243_quickLookExp.fits
    guess = [1300., 700.] # filename_image=df['file'][10] , holo4_003_RG610_HD160617_20210707_000244_quickLookExp.fits
    guess = [250., 1800.] # filename_image=df['file'][11] , holo4_003_RG610_HD160617_20210707_000245_quickLookExp.fits
    guess = [250., 1800.] # filename_image=df['file'][12] , holo4_003_RG610_HD160617_20210707_000246_quickLookExp.fits
    guess = [250., 1800.] # filename_image=df['file'][13] , holo4_003_RG610_HD160617_20210707_000247_quickLookExp.fits


    # wide scan
    guess = [1400., 700.] # filename_image=df['file'][14] , holo4_003_empty_HD160617_20210707_000248_quickLookExp.fits
    guess = [1400., 800.] # filename_image=df['file'][15] , holo4_003_empty_HD160617_20210707_000249_quickLookExp.fits
    guess = [400., 1800.] # filename_image=df['file'][16] , holo4_003_empty_HD160617_20210707_000250_quickLookExp.fits
    guess = [400., 1800.] # filename_image=df['file'][17] , holo4_003_empty_HD160617_20210707_000251_quickLookExp.fits
    guess = [400., 1800.] # filename_image=df['file'][18] , holo4_003_empty_HD160617_20210707_000252_quickLookExp.fits
    #guess = [50., 800.] # filename_image=df['file'][19] , holo4_003_empty_HD160617_20210707_000253_quickLookExp.fits
    #guess = [50., 800.] # filename_image=df['file'][20] , holo4_003_empty_HD160617_20210707_000254_quickLookExp.fits
    #guess = [50., 800.] # filename_image=df['file'][21] , holo4_003_empty_HD160617_20210707_000255_quickLookExp.fits



    # narrrow scan

    guess = [500.,2100.] # filename_image=df['file'][76] , 'holo4_003_empty_HD160617_20210707_000317_quickLookExp.fits'


    # overwrite with the position found in logbook
    if FLAG_ORDER0_LOCATION:
        print("Set Order 0 location from logbook : ({},{})".format(x0, y0))
        guess = [x0, y0]



    # Let spectractor find the target
    #x1, y1 = find_target(image, guess,rotated=False, use_wcs=False)
    x1, y1 = find_target(image, guess,rotated=False)

    print(x1,y1)



    # Check the location of the 0th order and analysis of the quality of its focus
    #----------------------------------------------------------------------------
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
        



    shape_str='\n'.join((
            r'skew     : Sk0 = {:3.3f}, Skx = {:3.3f}, Sky = {:3.3f} \n'.format(s0,sx,sy),
            r'kurtosis : K0  = {:3.3f}, Kx  = {:3.3f},  Ky = {:3.3f}'.format(k0,kx,ky)))



    skew_str='\n'.join((
            r'skew     : Sk0 = {:3.3f}'.format(s0),
            r'             : Skx = {:3.3f}'.format(sx),
            r'             : Sky = {:3.3f}'.format(sy)))



    kurt_str='\n'.join((
            r'kurtosis : K0 = {:3.3f}'.format(k0),
            r'             : Kx = {:3.3f}'.format(kx),
            r'             : Ky = {:3.3f}'.format(ky)))


    kurtosis_test_prob=kurtosistest(thumbnail,axis=None).pvalue
    skew_test_prob=skewtest(thumbnail,axis=None).pvalue
    normal_test_prob=normaltest(thumbnail,axis=None).pvalue



    kurtosis_test_val=kurtosistest(thumbnail,axis=None).statistic
    skew_test_val=skewtest(thumbnail,axis=None).statistic
    normal_test_val=normaltest(thumbnail,axis=None).statistic



    kurtosis_test_prob_x=kurtosistest(thumbnail_x).pvalue
    skew_test_prob_x=skewtest(thumbnail_x).pvalue
    normal_test_prob_x=normaltest(thumbnail_x).pvalue





    kurtosis_test_prob_y=kurtosistest(thumbnail_y).pvalue
    skew_test_prob_y=skewtest(thumbnail_y).pvalue
    normal_test_prob_y=normaltest(thumbnail_y).pvalue





    skew_str='\n'.join((
        r'skew     : Sk0 = {:3.3f}'.format(s0),
        r'             : Skx = {:3.3f}'.format(sx),
        r'             : Sky = {:3.3f}'.format(sy),
        r'             : p_test   = {:3.3e}'.format(skew_test_prob),
        r'             : p_test_x = {:3.3e}'.format(skew_test_prob_x),
        r'             : p_test_y = {:3.3e}'.format(skew_test_prob_y)))



    kurt_str='\n'.join((
        r'kurtosis : K0 = {:3.3f}'.format(k0),
        r'             : Kx = {:3.3f}'.format(kx),
        r'             : Ky = {:3.3f}'.format(ky),
        r'             : p_test   = {:3.3e}'.format(kurtosis_test_prob),
        r'             : p_test_x = {:3.3e}'.format(kurtosis_test_prob_x),
        r'             : p_test_y = {:3.3e}'.format(kurtosis_test_prob_y)))





    norm_str='\n'.join((
        r'normal  : p_test   = {:3.3e}'.format(normal_test_prob),
        r'             : p_test_x = {:3.3e}'.format(normal_test_prob_x),
        r'             : p_test_y = {:3.3e}'.format(normal_test_prob_y)))





    props = dict(boxstyle='round',edgecolor="w",facecolor="w", alpha=0.5)





    #-------------------------------------
    fig=plt.figure(figsize=(10,8))
    fig.subplots_adjust(left=0.12, right=0.95, wspace=0.3,bottom=0.15, top=0.9)

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

    plt.suptitle(title, Y=1.01)
    plt.show()
    # ------------------------------------------------------------------

    # Usually stop here if one just want to get the 0th order location
    if not FLAG_GO_FOR_RECONSTRUCTION_WTH_SPECTRACTOR:
        assert False
    else:
        assert True



    # Go for spectrum reconstruction
    #----------------------------------


    #spectrum = Spectractor(filename, output_directory, guess=[x1,y1], target_label=target, disperser_label=disperser_label, config=config)
    spectrum = Spectractor(filename_image, output_directory, guess=[x1,y1], target_label=target, disperser_label=disperser_label, config=config)




    # End of spectractor, manage files
    #-------------------------------


    # Remove temporary input fits file
    os.remove(filename_image)


    # Backup Spectractor output
    copy_tree(output_directory,os.path.join(finalpath_output_spectractor,"basespec"))
    copy_tree(output_figures,os.path.join(finalpath_output_spectractor,"plots"))


    exit(0)




