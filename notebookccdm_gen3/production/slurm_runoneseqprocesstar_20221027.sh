#!/bin/sh +x
#SBATCH --partition=htc
#
#SBATCH --job-name=procsstar_job
#SBATCH --output=procstar_job-%j.log
#SBATCH --error=procstar_job-%j.log
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=4G
#
#SBATCH --time=24:00:00

# configuration to be edited each time
#------------------------------------
export DISPLAY=
export DATE=20211103
export DATEEXEC=2022_10_30
export FILTER="FELH0600"
export FILTERDISPERSER="FELH0600~holo4"
export LOGBOOKSPATH="/sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3/all_visitsdispersers_gen3"
#export LOGBOOKFILENAME="visitdispersers_${DATE}_filt_empty-holo4_003.list"
export LOGBOOKFILENAME="visitdispersers_${DATE}_filt_${FILTER}-holo4_003.list"
#export OUTPUTCOLL="u/dagoret/spectro/noflat/${FILTERDISPERSER}/${DATE}" 
export OUTPUTCOLL="u/dagoret/first_test2"

# Define the logbook fullfilename
#fullfilenamelogbook="${LOGBOOKSPATH}/${DATE}/${LOGBOOKFILENAME}"
fullfilenamelogbook="${LOGBOOKSPATH}/${LOGBOOKFILENAME}"

echo "SLURM batch job         : " 
echo "date of observation     : ${DATE}"
echo "filter - disperser name : ${FILTERDISPERSER}"
echo "logbook path            : ${fullfilenamelogbook}"
echo "output collection       : ${OUTPUTCOLL}"
echo "date of execution       : ${DATEEXEC}"


# Initialisation of DM
#----------------------


export REPOSDIR=/sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3/repos/w_2022_39
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST.bash
setup lsst_distrib -t w_2022_39
source ${REPOSDIR}/user_setup.sh 

echo "STACK repodir           : ${REPOSDIR}"

#
# November 03/11/22: 
# - 43 exposures with FELH0600~holo4_003 in batches of 10 exposures

# range of processing
INDEXBATCH=1
INDEXMIN=1
INDEXMAX=43

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
  python run_processstarOneImage.py --reposdir ${REPOSDIR} --listofimages ${fullfilenamelogbook} --num=${COUNTER} --outcoll=${OUTPUTCOLL} &> ${logfile}
done < ${fullfilenamelogbook} 
