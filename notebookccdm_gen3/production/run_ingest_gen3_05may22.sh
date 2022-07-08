#/bin/sh

# Working directory : /sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3

REPOSDIR="repos/w_2022_09"
DATATOPDIR="/sps/lsst/groups/auxtel/data/raw_ncsa/20220502"
DATASUBDIR="${DATATOPDIR}/*"
for filedir in ${DATASUBDIR}   
 
do 	
  echo $filedir
  cmd="butler ingest-raws --transfer symlink -j 4 ./data ${filedir}/*"
  echo -e "${cmd}"
 ${cmd}
 #break 
done
