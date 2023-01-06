#!/bin/sh +x
# configuration to be edited each time
#------------------------------------
export DISPLAY=
export DATE=20221208
export DATEEXEC=2023_01_06
export FILTERDISPERSER="empty~holo4"
export LOGBOOKSPATH="/sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers"
export LOGBOOKFILENAME="visitdispersers_${DATE}_filt_empty-holo4_003.list"
# Define the logbook fullfilename
fullfilenamelogbook="${LOGBOOKSPATH}/${DATE}/${LOGBOOKFILENAME}"

echo "date of observation     : ${DATE}"
echo "filter - disperser name : ${FILTERDISPERSER}"
echo "logbook path            : ${fullfilenamelogbook}"
echo "date of execution       : ${DATEEXEC}"

my_list=`cut -d " " -f2 < $fullfilenamelogbook`
#echo $my_list

array=( $my_list ) # assuming this is filled already
string=""
for i in "${array[@]}" # this exact syntax will preserve array elements even if they have spaces in them
do
    string="$string,$i"
done
# we have a superfluous trailing comma now, remove it:
string="${string%,}"
echo $string
