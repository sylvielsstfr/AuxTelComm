#command line
#
# python run_processstarOneImage_oga.py --reposdir /sdf/home/d/dagoret/repos/repos_w_2022_39 
#                                   --listofimages /sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers/20220912/visitdispersers_20220912_filt_empty-holo4_003.list 
#                                   --num=1
#                                   --outcoll u/dagoret/mycoll
#

import os
import subprocess
import numpy as np
import argparse


reposdir="/sdf/home/d/dagoret/repos/repos_w_2022_39"
listofimages="/sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers/20220607/visitdispersers_20220607_filt_empty-holo4_003.list"


# Create the parser
parser = argparse.ArgumentParser(prog="run_processstarOneImage_oga.py",usage="example : python run_processstarOneImage_oga.py --reposdir /sdf/home/d/dagoret/repos/repos_w_2022_39  --listofimages /sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers/20220912/visitdispersers_20220912_filt_empty-holo4_003.list  --num=1 --outcoll u/dagoret/test1_oga")# Add an argument
parser.add_argument('--reposdir', type=str, required=True,help="where reposdir is location of personal DM software")
parser.add_argument('--listofimages', type=str, required=True,help="where listofimages is the path of ascii file list of exposures to process by date and seq number")
parser.add_argument('--num', type=int, required=True,help="where num is the index in the listifimages file")
parser.add_argument('--outcoll', type=str, required=True,help="where outputcoll is the path of user output collection")
args = parser.parse_args()

print("***************************************************************************************")
print("args \t = ",args)

# decode the arguments


REPOSDIR=args.reposdir
listofimages=args.listofimages
num=args.num
outcoll=args.outcoll

print("REPOSDIR \t = ",REPOSDIR)
print("listofimages \t = ",listofimages)
print("num \t = " ,num)
print("outcoll \t = ",outcoll)

arr=np.loadtxt(listofimages,delimiter=' ', dtype =float).astype(int)

dates=arr[:,0]
seqnum=arr[:,1]

N=len(seqnum)

dateobs=dates[num-1]
seq=seqnum[num-1]
        

command_line="pipetask run -b /sdf/group/rubin/repo/oga -p {}/atmospec/pipelines/processStar.yaml -i LATISS/raw/all,refcats,LATISS/calib -o {} -d \"exposure.day_obs={} and exposure.seq_num={} and instrument='LATISS'\" --register-dataset-types --clobber-outputs -j 8".format(REPOSDIR,outcoll,dateobs,seq)

print("#########################################################################################")
print(command_line)
print("#########################################################################################")
os.system(command_line)


