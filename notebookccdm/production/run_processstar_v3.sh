#/bin/sh

# source run_processstar_v3 .sh 
# No arg
# from image-list
#source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2021_36/loadLSST.bash
#setup lsst_distrib

# processStar.py . --rerun dagoret_testfordispersers2022_03 --configfile processConfig.py --id dayObs='2022-02-16' seqNum=748


#RERUNDIR=dagoret_testfordispersers2022_03
RERUNDIR=dagoret_withbiasfordispersers2022_03/


FILEPATH="all_visitsdispersers/visitdispersers_2022-02-16.list"

cat ${FILEPATH} | while read line || [[ -n $line ]];
do
		       
  cmd="processStar.py . --rerun ${RERUNDIR} --configfile processConfig.py ${line}"  
  echo -e "${cmd}"
 `$cmd` 
done
