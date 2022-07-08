#/bin/sh

# Working directory : /sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3

REPOSDIR="repos/w_2022_09"
DATATOPDIR="/sps/lsst/groups/auxtel/data/raw_ncsa/20220609"
DATASUBDIR="${DATATOPDIR}/*"

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_09/loadLSST.bash ; setup lsst_distrib
source repos/w_2022_09/user_setup.sh
eups list -s | grep LOCAL

for filedir in ${DATASUBDIR}   
 
do 	
  echo $filedir
  cmd="butler ingest-raws --transfer symlink -j 4 ./data ${filedir}/*"
  echo -e "${cmd}"
 ${cmd}
 #break 
done
