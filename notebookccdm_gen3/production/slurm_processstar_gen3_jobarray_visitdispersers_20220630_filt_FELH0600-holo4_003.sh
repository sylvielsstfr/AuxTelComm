#!/bin/bash
####################################
# SLURM options
###################################
#SBATCH --job-name=procstarFEL600
#SBATCH --output=array_%A_%a.out
#SBATCH --error=array_%A_%a.err
#SBATCH --array=1-62
#SBATCH --time=1-00:00:00
#SBATCH --ntasks=1
#SBATCH --mem=20G
#SBATCH --partition htc
########################################

# Print the task id.
echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

echo "Node: $(hostname)"

echo " Slurm environment variables:"
env | grep SLURM



# path configurations
export NEWHOME="/pbs/throng/lsst/users/dagoret"
export AUXTELHOME="/sps/lsst/groups/auxtel"
export AUXTELDM="${AUXTELHOME}/softs/shared/auxteldm"
export AUXTELDM2="${AUXTELHOME}/softs/shared/auxteldm_gen3"

#export REPOSDIR="repos/w_2022_09"
export REPOSDIR="/sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3/repos/w_2022_09"




# list of files
#export MYLISTOFEXPOSURES="all_visitsdispersers_gen3/visitdispersers_20220628_filt_empty-holo4_003.list"
#export MYLISTOFEXPOSURES="all_visitsdispersers_gen3/visitdispersers_20220628_filt_FELH0600-holo4_003.list"
#export MYLISTOFEXPOSURES="all_visitsdispersers_gen3/visitdispersers_20220628_filt_BG40-holo4_003.list"
#export MYLISTOFEXPOSURES="all_visitsdispersers_gen3/visitdispersers_20220629_filt_empty-holo4_003.list"
#export MYLISTOFEXPOSURES="all_visitsdispersers_gen3/visitdispersers_20220630_filt_empty-holo4_003.list"
#export MYLISTOFEXPOSURES="all_visitsdispersers_gen3/visitdispersers_20220630_filt_BG40-holo4_003.list"
export MYLISTOFEXPOSURES="all_visitsdispersers_gen3/visitdispersers_20220630_filt_FELH0600-holo4_003.list"


source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_09/loadLSST.bash ; setup lsst_distrib
#source ../repos/w_2022_09/user_setup.sh
source ${REPOSDIR}/user_setup.sh
which python

cd ${AUXTELDM2}


# execute the processing in parallel
python run_processstarOneImage_gen3_v10.py --reposdir ${REPOSDIR} --listofimages ${MYLISTOFEXPOSURES} --num ${SLURM_ARRAY_TASK_ID}
