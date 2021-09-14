#!/bin/sh

source ${LOADSTACK}
setup lsst_distrib
source $HOME/notebooks/.user_setups 
eups list -s | grep LOCAL


# wide scan : HD 160617 
# all_myseq_holo=range(234,310)
# narrow scan :  HD 160617 
# all_myseq_holo=range(317,365)


date="2021-07-07"
datedir="${date}/"
path_output_dir="/project/shared/auxTel/rerun/dagoret/outputspectr_scan2021_July/spectractorOutput/"
full_path_output_dir="${path_output_dir}${datedir}"

echo $full_path_output_dir

# list of sequences
#EXPNUMS=`seq 234 1 309`
EXPNUMS=`seq 234 1 309`

# total number of exposures
NBEXP=0
# total number of exposures without dir
NBEXPNODIR=0
# total number of exposures with dir
NBEXPWTHDIR=0
# total number of exposures with plots
NBEXPWTHPLT=0
# total number of exposures with spectra
NBEXPWTHSPEC=0

# list of exposures
LISTNUM=''
# list of exposure without dir (not run spectraction)
LISTNUMNODIR=''
# list of exposure with dir (spectraction has been run)
LISTNUMWTHDIR=''
# list of exposures with plots (Spectractor has run up to some point)
LISTNUMWTHPLOTS=""
# list of exposures with spectraction output (Spectractor has completed)
LISTNUMWTHSPECTR=""

# loop on exposures
for num in $EXPNUMS
do
NBEXP=$(($NBEXP + 1)) 
LISTNUM="${LISTNUM} $num"
num_str=`printf "%04d\n" $num`
echo "=====================================" ${num_str} "=============================================="
path_exposure_output_dir="${full_path_output_dir}${num_str}"


if [[ -d $path_exposure_output_dir ]]; then
    echo "$path_exposure_output_dir  is a directory "
    
    NBEXPWTHDIR=$(($NBEXPWTHDIR + 1)) 
    LISTNUMWTHDIR="$LISTNUMWTHDIR $num"
    
    ls $path_exposure_output_dir
    
    file1="${path_exposure_output_dir}/plots.pdf"
    file2="${path_exposure_output_dir}/spectraction-${date}-${num_str}.pickle"
    
    if [[ -f $file1 ]]; then
    echo "$file1 exists."
    
    NBEXPWTHPLT=$(($NBEXPWTHPLT + 1))
    LISTNUMWTHPLOTS="$LISTNUMWTHPLOTS $num"
    fi
    
    if [[ -f $file2 ]]; then
    echo "$file2 exists."
    
    LISTNUMWTHSPECTR="$LISTNUMWTHSPECTR $num"
    NBEXPWTHSPEC=$(($NBEXPWTHSPEC + 1))
    fi
      

else
    echo "$path_exposure_output_dir  does not exist "
    
    NBEXPNODIR=$(($NBEXPNODIR + 1)) 
    LISTNUMNODIR="$LISTNUMNODIR $num"
    
fi


done

echo "Full list of Exposures : ......................." $LISTNUM
echo "Full list of Exposures without output dir: ....." $LISTNUMNODIR
echo "Full list of Exposures with output dir: ....... " $LISTNUMWTHDIR
echo "Full list of Exposures with output plots: ..... " $LISTNUMWTHPLOTS
echo "Full list of Exposures with output spectra: ...." $LISTNUMWTHSPECTR




echo "Total number of exposures : ....................." $NBEXP
echo "Total number of exposures without dir : ........." $NBEXPNODIR
echo "Total number of exposures with dir :............." $NBEXPWTHDIR
echo "Total number of exposures with plots : .........." $NBEXPWTHPLT
echo "Total number of exposures with spectra: ........." $NBEXPWTHSPEC
