#! /bin/sh
#
#
# run_multiprocessstar.sh

# configuration to be edited each time
export DISPLAY=
export LOGBOOKSPATH=/sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers
export LOGBOOKFILENAME=visitdispersers_20220630_filt_empty-holo4_003.list
export DATE=20220630
export REPOSDIR=/sdf/home/d/dagoret/repos/repos_w_2022_39
export OUTPUTCOLL=u/dagoret/tests/test_20oct2022 

# Initialisation of DM
source /sdf/group/rubin/sw/tag/w_2022_39/loadLSST.bash
setup lsst_distrib -t w_2022_39
source ~/notebooks/.user_setups

# Define the logbook fullfilename
fullfilenamelogbook=${LOGBOOKSPATH}/${DATE}/${LOGBOOKFILENAME}

COUNTER=0
while IFS=: read -r line; do
  COUNTER=$(( COUNTER + 1 ))
  # process the fields
  # if the line has less than three fields, the missing fields will be set to an empty string
  # if the line has more than three fields, `field3` will get all the values, including the third field plus the delimiter(s)
 
  datestr=`echo $line | cut -d " " -f1`
  seqstr=`echo $line | cut -d " " -f2`
  echo "----${COUNTER}--- : ${datestr} , ${seqstr}----------"
  
  # launch the python script that run DM pipeline
  python run_processstarOneImage.py --reposdir ${REPOSDIR} --listofimages ${fullfilenamelogbook} --num=${COUNTER} --outcoll=${OUTPUTCOLL}
done < ${fullfilenamelogbook}