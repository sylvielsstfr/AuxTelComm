#!/usr/bin/env python

import sys,os
#for path in sys.path:
#	print(path)


#source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2021_44/loadLSST.bash
#setup lsst_distrib


INSTALLATIONDIR="/sps/lsst/groups/auxtel/softs/shared/auxteldm/rerun"
RERUNDIR      = "dagoret_fordispersers2022_01"  
RERUNFULLDIR  = os.path.join(INSTALLATIONDIR,RERUNDIR)
RERUNBIASFULLDIR  = os.path.join(RERUNFULLDIR,"bias")
list_of_dates = os.listdir(RERUNBIASFULLDIR) 


for thedate in list_of_dates:
    datedir      = os.path.join(RERUNBIASFULLDIR,thedate)
    biasfile     = os.listdir(datedir)
    for thebiasfile in biasfile :
        fullfilename = os.path.join(datedir,thebiasfile)
        # cmd = "ingestCalibs.py . --validity 360 ./rerun/dagoret_fordisersers2022_01/bias/2021-02-16/bias-det000_2021-02-16.fits --mode copy --rerun 
        #                                                                                                                             dagoret_fordispersers2022_01"
        print("=============================================================================================================================")
        cmd = "ingestCalibs.py . --validity 360 " + fullfilename + " --mode copy --rerun " + RERUNFULLDIR
        print(cmd) 
        print(".............................................................................................................................")
        os.system(cmd)



