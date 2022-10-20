#command line
#
# python run_processstarOneImage.py --reposdir /sdf/home/d/dagoret/repos/repos_w_2022_39 
#                                   --listofimages /sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers/20220607/visitdispersers_20220607_filt_empty-holo4_003.list 
#                                   --num=1
#                                   -- outcoll u/dagoret/mycoll
#

import os
import subprocess
import numpy as np
import argparse


reposdir="/sdf/home/d/dagoret/repos/repos_w_2022_39"
listofimages="/sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers/20220607/visitdispersers_20220607_filt_empty-holo4_003.list"


# Create the parser
parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('--reposdir', type=str, required=True)
parser.add_argument('--listofimages', type=str, required=True)
parser.add_argument('--num', type=int, required=True)
parser.add_argument('--outcoll', type=str, required=True)
args = parser.parse_args()

print("args = ",args)

# decode the arguments


REPOSDIR=args.reposdir
listofimages=args.listofimages
num=args.num

print(REPOSDIR)
print(listofimages)
print(num)
print(outcoll)

arr=np.loadtxt(listofimages,delimiter=' ', dtype =float).astype(int)

dates=arr[:,0]
seqnum=arr[:,1]

N=len(seqnum)

dateobs=dates[num-1]
seq=seqnum[num-1]
        

command_line="pipetask run -b /sdf/group/rubin/repo/main -p {}/atmospec/pipelines/processStar.yaml -i LATISS/raw/all,refcats,LATISS/calib -o {} -d \"exposure.day_obs={} and exposure.seq_num={} and instrument='LATISS'\" --register-dataset-types --clobber-outputs".format(REPOSDIR,outcoll,dateobs,seq)

print(command_line)
os.system(command_line)


