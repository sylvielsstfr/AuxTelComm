#! /bin/sh
#
#
# run_multiprocessstar.sh

# configuration to be edited each time
#------------------------------------
export DISPLAY=
export DATE=20220630
export FILTERDISPERSER="empty~holo4"
export LOGBOOKSPATH=/sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers
export LOGBOOKFILENAME=visitdispersers_${DATE}_filt_empty-holo4_003.list
export OUTPUTCOLL=u/dagoret/tests/test_25oct2022c/${FILTERDISPERSER}/${DATE} 

# Initialisation of DM
#----------------------
export REPOSDIR=/sdf/home/d/dagoret/repos/repos_w_2022_39
source /sdf/group/rubin/sw/tag/w_2022_39/loadLSST.bash
setup lsst_distrib -t w_2022_39
source ~/notebooks/.user_setups

# Define the logbook fullfilename
fullfilenamelogbook=${LOGBOOKSPATH}/${DATE}/${LOGBOOKFILENAME}

# range of processing
VALUEMIN=10
VALUEMAX=64
COUNTER=0

# loop on entries in the logbookfilename
while IFS=: read -r line; do
  COUNTER=$(( COUNTER + 1 ))
  # process the fields
  # if the line has less than three fields, the missing fields will be set to an empty string
  # if the line has more than three fields, `field3` will get all the values, including the third field plus the delimiter(s)
 
  datestr=`echo $line | cut -d " " -f1`
  seqstr=`echo $line | cut -d " " -f2`
  logfile="logs/log_${COUNTER}_${datestr}_${seqstr}.log"
  echo "----${COUNTER}--- : ${datestr} , ${seqstr}---${logfile}-------"
  if [ "$COUNTER" -lt $VALUEMIN ]   
  then
   echo "SKIP ${COUNTER}" 
   continue      # Skip rest of this particular loop iteration.
  fi
  if [ "$COUNTER" -gt $VALUEMAX ]   
  then
   echo "SKIP ${COUNTER}"
   continue      # Skip rest of this particular loop iteration.
  fi

  # launch the python script that run DM pipeline
  python run_processstarOneImage.py --reposdir ${REPOSDIR} --listofimages ${fullfilenamelogbook} --num=${COUNTER} --outcoll=${OUTPUTCOLL} &> ${logfile}
done < ${fullfilenamelogbook} 
