
import os
import subprocess
import numpy as np
import sys

# Count the arguments
arguments = len(sys.argv) - 1
print ("The script is called with %i arguments" % (arguments))

if arguments == 1:
	fileindex=int(sys.argv[arguments])
	print(f"fileindex = {fileindex}")
else:
	fileindex=-1


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

#2021/11/04 : 6 files
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_BG40-holo4_003.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_BG40-ronchi170lpmm.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_FELH0600-holo4_003.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_FELH0600-ronchi170lpmm.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_empty-holo4_003.list
#all_visitsdispersers_gen3//visitdispersers_20211104_filt_empty-ronchi170lpmm.list
visit_dispersers_files = ["visitdispersers_20211104_filt_BG40-holo4_003.list",\
                            "visitdispersers_20211104_filt_FELH0600-holo4_003.list",\
                            "visitdispersers_20211104_filt_empty-ronchi170lpmm.list",\
                            "visitdispersers_20211104_filt_BG40-ronchi170lpmm.list",\
                            "visitdispersers_20211104_filt_FELH0600-ronchi170lpmm.list",\
                            "visitdispersers_20211104_filt_empty-ronchi170lpmm.list"] 

#2021/11/02  : 8 files
visit_dispersers_files = ["visitdispersers_20211102_filt_BG40-holo4_003.list",\
                            "visitdispersers_20211102_filt_BG40-ronchi170lpmm.list",\
                            "visitdispersers_20211102_filt_FELH0600-holo4_003.list",\
                            "visitdispersers_20211102_filt_FELH0600-ronchi170lpmm.list",\
                            "visitdispersers_20211102_filt_SDSSg-holo4_003.list",\
                            "visitdispersers_20211102_filt_SDSSg-ronchi170lpmm.list",\
                            "visitdispersers_20211102_filt_empty-holo4_003.list",\
                            "visitdispersers_20211102_filt_empty-ronchi170lpmm.list"]

fileindex_max=len(visit_dispersers_files)

if fileindex < fileindex_max and fileindex >=0  :
    listofimages=os.path.join("../all_visitsdispersers_gen3",visit_dispersers_files[fileindex])
else:
    print(f">>>> Bad file index {fileindex} / fileindex_max = {fileindex_max}")
    exit(-1)


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


