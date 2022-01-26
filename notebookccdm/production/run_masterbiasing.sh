#/bin/sh

# source run_masterbiasing.sh all_visitsbias/*

#source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2021_44/loadLSST.bash
#setup lsst_distrib


RERUNDIR=dagoret_fordispersers2022_01  
 
for file in "$@"
do
  echo "Processing $file file..."
  # take action on each file. $file store current file name
  cat "$file"
  cmd="constructBias.py . --rerun ${RERUNDIR}  @${file}  --batch-type none --configfile biasConfig.py --clobber-config"
  echo -e "${cmd}"
  `$cmd`
 
done
