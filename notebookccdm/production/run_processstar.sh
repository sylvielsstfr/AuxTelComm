#/bin/sh

# source run_processstar.sh all_visitsdispersers/*

#source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2021_44/loadLSST.bash
#setup lsst_distrib


RERUNDIR=dagoret_fordispersers2022_01  
 
for file in "$@"
do
  echo "Processing $file file..."
  # take action on each file. $file store current file name
  cat "$file"
  cmd="processStar.py . --rerun ${RERUNDIR} --configfile processConfig.py @${file}"  
  echo -e "${cmd}"
  `$cmd`
 
done
