#/bin/sh

# source run_processstar_v2 .sh 
# No arg

#source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2021_36/loadLSST.bash
#setup lsst_distrib

# processStar.py . --rerun dagoret_testfordispersers2022_03 --configfile processConfig.py --id dayObs='2022-02-16' seqNum=748


RERUNDIR=dagoret_testfordispersers2022_03
MYDATE="2022-02-16"

NUMSTART=700
NUMSTOP=750

NUM=$NUMSTART

while [ $NUM -ne $NUMSTOP ]
do
  NUM=$(($NUM+1))
		       
  echo "Processing $NUM image..."
  # take action on each file. $file store current file name
  cmd="processStar.py . --rerun ${RERUNDIR} --configfile processConfig.py --id dayObs=${MYDATE} seqNum=${NUM}"  
  echo -e "${cmd}"
  `$cmd` 
done
