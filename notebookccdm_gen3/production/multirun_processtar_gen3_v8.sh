
import os
import subprocess
import numpy as np

import sys
print("original python ",sys.path)


nargs = len(sys.argv) - 1

print(f"number of arguments = {nargs}")

if nargs == 2:
	    # Output argument-wise
	        position = 1
		    while (nargs >= position):
			            print ("Parameter %i: %s" % (position, sys.argv[position]))
				            if position == 1 :
						                DAYNUM = sys.argv[position]
								        elif position == 2 :
										            image_index = int(sys.argv[position])-1
											            position = position + 1
												            
											    else:
												        print(f"{sys.argv[0]} requires two positional arguments : 1: the datestring 2: the image rank") 
													    exit(-1)
													        

													    print("=============================================================================")
													    print(f"{sys.argv[0]} start with DAYNUM = {DAYNUM}  and  image_index = {image_index}")    



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



listofimages="../all_visitsdispersers_gen3/visitdispersers_20220216_filt_empty-ronchi170lpmm.list"
#listofimages="../all_visitsdispersers_gen3/visitdispersers_20220216_filt_empty-holo4_003.list"

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


