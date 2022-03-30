#!/bin/sh
########################################
# SLURM options
########################################
#SBATCH --mem=20G # memory in MB per default
#SBATCH --ntasks 1 # Run single task or CPU
#SBATCH --time 7-00:00:00 # time (D-HH:MM)
#SBATCH --partition htc
#SBATCH --job-name=new_confC
####################################≈
####################################

echo "Node: $(hostname)"

echo "Slurm environment variables:"
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
cd ${NEWHOME}/desc/AuxTelComm/notebookccdm_gen3/runspectractor_standalone/2022_03
ls

python loop_processSpectra_holo-newspectractor_v2-multiconfigC.py

