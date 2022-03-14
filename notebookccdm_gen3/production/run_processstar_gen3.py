
import os
import subprocess
import numpy as np


RERUNDIR="dagoret_withbiasfordispersers2022_03/"
REPOSDIR="repos/w_2022_09"

listofimages="all_visitsdispersers_gen3/visitdispersers_2021-07-07b.list"


arr=np.loadtxt(listofimages,delimiter=' ', dtype =float).astype(int)

dates=arr[:,0]
seqnum=arr[:,1]

N=len(seqnum)

for idx in range(N):
	dateobs=dates[idx]
	seq=seqnum[idx]
	command_line=f"pipetask run -b ./data -p {REPOSDIR}/atmospec/pipelines/processStar.yaml -i LATISS/raw/all,refcats,LATISS/calib -o u/dagoret/first_test -d \"exposure.day_obs={dateobs} and exposure.seq_num={seq} and instrument='LATISS'\" --register-dataset-types --clobber-outputs"


	print(command_line)
	os.system(command_line)


