
import os
import subprocess
import numpy as np


RERUNDIR="../dagoret_withbiasfordispersers2022_03/"
REPOSDIR="../repos/w_2022_09"

#2022/02

#visitdispersers_20220215_filt_empty-holo4_003.list
#visitdispersers_20220215_filt_empty-ronchi170lpmm.list

#visitdispersers_20220216_filt_empty-holo4_003.list
#visitdispersers_20220216_filt_empty-ronchi170lpmm.list

#2022/03

#visitdispersers_20220316_filt_empty-holo4_003.list
#visitdispersers_20220316_filt_empty-ronchi170lpmm.list

#visitdispersers_20220317_filt_empty-holo4_003.list
#visitdispersers_20220317_filt_empty-ronchi170lpmm.list

#2021/11/04
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_BG40-holo4_003.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_BG40-ronchi170lpmm.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_FELH0600-holo4_003.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_FELH0600-ronchi170lpmm.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_empty-holo4_003.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_empty-ronchi170lpmm.list

listofimages="../all_visitsdispersers_gen3/visitdispersers_20211104_filt_BG40-ronchi170lpmm.list"

arr=np.loadtxt(listofimages,delimiter=' ', dtype =float).astype(int)

dates=arr[:,0]
seqnum=arr[:,1]

N=len(seqnum)

for idx in range(N):
	dateobs=dates[idx]
	seq=seqnum[idx]
	command_line=f"pipetask run -b ../data -p {REPOSDIR}/atmospec/pipelines/processStar.yaml -i LATISS/raw/all,refcats,LATISS/calib -o u/dagoret/first_test2 -d \"exposure.day_obs={dateobs} and exposure.seq_num={seq} and instrument='LATISS'\" --register-dataset-types --clobber-outputs"


	print(command_line)
	os.system(command_line)


