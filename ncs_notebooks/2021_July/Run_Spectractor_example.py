#!/usr/bin/env python
# coding: utf-8

# # Run Spectractor from notebooks
# 
# - adapted from https://github.com/stubbslab/PCWG-AuxTel/blob/main/Run_Spectractor_example.ipynb
# 
# - author : Sylvie Dagoret-campagne
# - affiliation : IJCLab/IN2P3/CNRS
# - creationdate : September 2021 13th
# - update : September 2021 14th
# - DM-Stack version : **w_2021_36**
# - Big CPU


import sys

import contextlib
import os

import sys,getopt




if __name__ == "__main__":
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"n:d:h",['n=','d=','help'])
    except getopt.GetoptError:
        print(' Exception bad getopt with :: '+sys.argv[0]+ ' -n <exposure number> -d <date>')
        print(' Example :: '+sys.argv[0]+ ' -n 100 -d 2021-07-07')
        sys.exit(2)
        
   
    num=0
    str_date='2021-07-07'

    
    # loop on options and their value
    for opt, arg in opts:


        if opt in ('-h', '--help'):
            print('help for usage : '+sys.argv[0]+ ' -n <exposure number> -d <date>')
            print(' Example :: '+sys.argv[0]+ ' -n 100 -d 2021-07-07')
            sys.exit(2)
        elif opt in ('-n', '--number'):
            str_num = arg
            num=int(str_num)
        elif opt in ('-d', '--date'):
            str_date = arg
        else:
            print(sys.argv[0]+ ' -n <number> -d <date>')
            sys.exit(2)
                   
 
    # from lsst.log.utils import enable_notebook_logging
    # enable_notebook_logging()

    # Buttler
    import lsst.daf.persistence as dafPersist

    repoDir='/project/shared/auxTel/rerun/dagoret/outputspectr_scan2021_July'
    butler=  dafPersist.Butler(repoDir)

    dataId = {'dayObs': str_date, 'seqNum': num} 
    print('===============================',dataId,'==========================')

    dataRef = butler.dataRef('raw', **dataId)


    # Instantiate the task, set our config options

    from lsst.atmospec import ProcessStarTask

    config = ProcessStarTask.ConfigClass()
    config.doDisplayPlots = False  # show the plots in the notebook
    config.spectractorDebugMode = True  # make all the debug plots along the way
    config.binning = 4

    # pretty minimal ISR because some things we don't have the calib products available for
    # most of this would be picked up automatically if running from the command line from config files
    config.isr.doLinearize = False
    config.isr.doDark = False
    config.isr.doFlat = False
    config.isr.doFringe = False
    config.isr.doDefect = True
    config.isr.doCrosstalk = False
    config.isr.doSaturationInterpolation = False

    #print("call ProcessStarTask with config = ",config)
    task = ProcessStarTask(config=config)
    
    result = task.runDataRef(dataRef)
    
    print("=================== End : Run Spectractor for expo-num = {} ================".format(str_num))
 




