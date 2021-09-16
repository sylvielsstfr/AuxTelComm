#!/bin/sh

source ${LOADSTACK}
setup lsst_distrib
source $HOME/notebooks/.user_setups 
eups list -s | grep LOCAL


# wide scan : HD 160617 
# all_myseq_holo=range(234,310)
# narrow scan :  HD 160617 
# all_myseq_holo=range(317,365)

path_output_dir=/project/shared/auxTel/rerun/dagoret/outputspectr_scan2021_July/spectractorOutput/

date="2021-07-07"

full_path_output_dir="$path_output_dir $date"

# wide scan
#EXPNUMS=`seq 234 1 309`

# narrow scan
EXPNUMS=`seq 317 1 365`
#EXPNUMS=`seq 318 1 365`

LISTNUM=''

# loop on exposures
for num in $EXPNUMS
do
LISTNUM="${LISTNUM} $num"
echo " num = $num"
#output=$(python Run_Spectractor_example_2021-07-07.py -n $num 2>&1) 

cmd="python Run_Spectractor_example.py -n $num -d $date 2>&1"
echo $cmd
output=`$cmd` 
echo $output
done

echo "List of Exposures : " $LISTNUM


