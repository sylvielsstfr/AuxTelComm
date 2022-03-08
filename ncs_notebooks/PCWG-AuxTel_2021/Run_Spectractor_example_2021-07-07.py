#!/usr/bin/env python
# coding: utf-8

# # Run Spectractor from notebooks
# 
# - adapted from https://github.com/stubbslab/PCWG-AuxTel/blob/main/Run_Spectractor_example.ipynb
# 
# - author : Sylvie Dagoret-campagne
# - affiliation : IJCLab/IN2P3/CNRS
# - update : September 2021 13th
# - DM-Stack version : **w_2021_36**
# - Big CPU


import sys

import contextlib
import os

import sys,getopt




if __name__ == "__main__":
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"n:h",['n=','help'])
    except getopt.GetoptError:
        print(' Exception bad getopt with :: '+sys.argv[0]+ ' -n <exposure number>')
        sys.exit(2)
        
   
    num=0

    
    # loop on options and their value
    for opt, arg in opts:


        if opt in ('-h', '--help'):
            print('help for usage : '+sys.argv[0]+ ' -n <exposure number>')
            sys.exit(2)
        elif opt in ('-n', '--number'):
            str_num = arg
            num=int(str_num)

        else:
            print(sys.argv[0]+ ' -n <number>')
            sys.exit(2)
                   
      
    
    import lsst.daf.persistence as dafPersist
    # from lsst.log.utils import enable_notebook_logging
    # enable_notebook_logging()


    repoDir='/project/shared/auxTel/rerun/dagoret/outputspectr_scan2021_July'
    butler=  dafPersist.Butler(repoDir)

    dataId = {'dayObs': '2021-07-07', 'seqNum': num}
    
    print(dataId)

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
    
    print("End : Run Spectractor for expo-num = {}".format(str_num))
 




