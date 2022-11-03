#command line
#
# python run_processphotomOneImage.py --reposdir /sdf/home/d/dagoret/repos/repos_w_2022_39 
#                                   --listofimages /sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers/20220630/visitdispersers_20220630_filt_empty-holo4_003.list 
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
parser = argparse.ArgumentParser(prog="run_processphotomOneImage.py",usage="example : python run_processphotomOneImage.py --reposdir /sdf/home/d/dagoret/repos/repos_w_2022_39 --drppipedir /sdf/home/d/dagoret/repos/repos_w_2022_39/drp_pipe --listofimages /sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers/20220630/visitdispersers_20220630_filt_empty-holo4_003.list  --num 1 --outcoll u/dagoret/photo/empty~holo4_003/20220630")# Add an argument
parser.add_argument('--reposdir', type=str,required=True,help="where reposdir is location of personal DM software")
parser.add_argument('--drppipedir', type=str,required=True,help="where DRP_PIPE_DIR is location of DM pipeline software")
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
DRP_PIPE_DIR=args.drppipedir

print("REPOSDIR \t = ",REPOSDIR)
print("DRP_PIPE_DIR \t = ",DRP_PIPE_DIR)
print("listofimages \t = ",listofimages)
print("num \t = " ,num)
print("outcoll \t = ",outcoll)

arr=np.loadtxt(listofimages,delimiter=' ', dtype =float).astype(int)

dates=arr[:,0]
seqnum=arr[:,1]

N=len(seqnum)

dateobs=dates[num-1]
seq=seqnum[num-1]
        

command_line="pipetask run -b /sdf/group/rubin/repo/main -p {}/pipelines/LATISS/DRP.yaml#isr,characterizeImage,calibrate -i LATISS/raw/all,refcats,LATISS/calib -o {} -d \"exposure.day_obs={} and exposure.seq_num={} and instrument='LATISS'\" --register-dataset-types --clobber-outputs -j 8".format(DRP_PIPE_DIR,outcoll,dateobs,seq)

print("#########################################################################################")
print(command_line)
print("#########################################################################################")
os.system(command_line)


