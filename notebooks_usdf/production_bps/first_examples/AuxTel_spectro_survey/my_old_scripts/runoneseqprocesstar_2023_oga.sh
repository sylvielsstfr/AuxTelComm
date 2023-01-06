#!/bin/sh +x
# configuration to be edited each time
#------------------------------------
export DISPLAY=
export DATE=20221208
export DATEEXEC=2023_01_05
export FILTERDISPERSER="empty~holo4"
export LOGBOOKSPATH="/sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers"
export LOGBOOKFILENAME="visitdispersers_${DATE}_filt_empty-holo4_003.list"
export OUTPUTCOLL="u/dagoret/spectro/noflat/${FILTERDISPERSER}/${DATE}" 
# Define the logbook fullfilename
fullfilenamelogbook="${LOGBOOKSPATH}/${DATE}/${LOGBOOKFILENAME}"

echo "SLURM batch job for OGA : " 
echo "date of observation     : ${DATE}"
echo "filter - disperser name : ${FILTERDISPERSER}"
echo "logbook path            : ${fullfilenamelogbook}"
echo "output collection       : ${OUTPUTCOLL}"
echo "date of execution       : ${DATEEXEC}"


# Initialisation of DM
#----------------------
export REPOSDIR=/sdf/home/d/dagoret/repos/repos_w_2022_39

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST.bash
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST-ext.bash
setup lsst_distrib -t w_2022_39

#source /sdf/group/rubin/sw/tag/w_2022_39/loadLSST.bash
#setup lsst_distrib -t w_2022_39
source ~/notebooks/.user_setups

echo "STACK repodir           : ${REPOSDIR}"

#
# September 12/09/22: 
# - 157 exposures with empty~holo4_003 in batches of 10 exposures
# September 13/09/22
# - 137 exposures with empty~holo4_003
# December 8th 2022
#- 84 exposures with emptly-holo4_003

# range of processing
INDEXBATCH=1
INDEXMIN=1
INDEXMAX=84

echo "Batch number            : ${INDEXBATCH} ==> index min : ${INDEXMIN} - index max : ${INDEXMAX}"

# init counter over the indexes
COUNTER=0

# loop on entries in the logbookfilename
while IFS=: read -r line; do
  COUNTER=$(( COUNTER + 1 ))
  # process the fields
  # if the line has less than three fields, the missing fields will be set to an empty string
  # if the line has more than three fields, `field3` will get all the values, including the third field plus the delimiter(s)
 
  datestr=`echo $line | cut -d " " -f1`
  seqstr=`echo $line | cut -d " " -f2`

#  logfiledir="logs/logs_${DATEEXEC}"
#  if [[ ! -e ${logfiledir} ]]; then
#    mkdir -p ${logfiledir}
#  elif [[ ! -d ${logfiledir} ]]; then
#    echo "${logfiledir} already exists but is not a directory"
#  fi

  logfile="logs/logs_${DATEEXEC}/log_${COUNTER}_${datestr}_${seqstr}.log"

  echo "----${COUNTER}--- : ${datestr} , ${seqstr}---${logfile}-------"
  if [ "$COUNTER" -lt $INDEXMIN ]   
  then
   echo "SKIP ${COUNTER}" 
   continue      # Skip rest of this particular loop iteration.
  fi
  if [ "$COUNTER" -gt $INDEXMAX ]   
  then
   echo "SKIP ${COUNTER}"
   continue      # Skip rest of this particular loop iteration.
  fi

  # launch the python script that run DM pipeline
  python run_processstarOneImage_oga.py --reposdir ${REPOSDIR} --listofimages ${fullfilenamelogbook} --num=${COUNTER} --outcoll=${OUTPUTCOLL}
done 
