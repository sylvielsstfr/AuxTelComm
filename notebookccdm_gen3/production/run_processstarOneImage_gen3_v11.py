#
# run_processstarOneImage_gen3_v9.py --reposdir repos/w_2022_09 --listofimages all_visitsdispersers_gen3/visitdispersers_20220317_filt_empty-ronchi170lpmm.list --num=3
#

import os
import subprocess
import numpy as np
import argparse


reposdir="repos/w_2022_09"
listofimages="all_visitsdispersers_gen3/visitdispersers_20210909_filt_empty-ronchi170lpmm.list"


# Create the parser
parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('--reposdir', type=str, required=True)
parser.add_argument('--listofimages', type=str, required=True)
parser.add_argument('--num', type=int, required=True)
args = parser.parse_args()

print("args = ",args)

# decode the arguments


REPOSDIR=args.reposdir
listofimages=args.listofimages
num=args.num

print(REPOSDIR)
print(listofimages)
print(num)

arr=np.loadtxt(listofimages,delimiter=' ', dtype =float).astype(int)

dates=arr[:,0]
seqnum=arr[:,1]

N=len(seqnum)

dateobs=dates[num-1]
seq=seqnum[num-1]
        

command_line="pipetask run -b ./data -p {}/atmospec/pipelines/processStar.yaml -i LATISS/raw/all,refcats,LATISS/calib -o u/dagoret/first_test2 -d \"exposure.day_obs={} and exposure.seq_num={} and instrument='LATISS'\" --register-dataset-types --clobber-outputs".format(REPOSDIR,dateobs,seq)

print(command_line)
os.system(command_line)


