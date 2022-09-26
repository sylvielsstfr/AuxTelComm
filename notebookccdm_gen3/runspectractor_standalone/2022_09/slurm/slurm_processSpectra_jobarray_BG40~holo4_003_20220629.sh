#!/bin/bash
# ###################################
# SLURM options
# ##################################
#SBATCH --job-name=holobg
#SBATCH --output=holog.%A_%a.log
#SBATCH --array=1-44
#SBATCH --time=1-00:00:00
#SBATCH --ntasks=1
#SBATCH --mem=20G
#SBATCH --partition htc
# #######################################

# 113 exposures
# Print the task id.
echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

echo "Node: $(hostname)"

echo " Slurm environment variables:"
env | grep SLURM

export NEWHOME="/pbs/throng/lsst/users/dagoret"
export AUXTELHOME="/sps/lsst/groups/auxtel"
export AUXTELDM="${AUXTELHOME}/softs/shared/auxteldm"
export AUXTELDM2="${AUXTELHOME}/softs/shared/auxteldm_gen3"
#export PATH=/pbs/throng/lsst/software/desc/bin:${PATH}
#source /pbs/throng/lsst/software/desc/common/miniconda/setup_current_python.sh 


cd ${AUXTELHOME}/softs
source MySetup_py3_SDC.sh 

which python
cd ${NEWHOME}/desc/AuxTelComm/notebookccdm_gen3/runspectractor_standalone/2022_09


DAYNUM="20220629"
FILTERDISPERSERNAME="BG40~holo4_003"

python processSpectra_holo-newspectractor_v3.py ${DAYNUM} ${FILTERDISPERSERNAME} ${SLURM_ARRAY_TASK_ID}


