#!/bin/sh
########################################
# SLURM options
########################################
#SBATCH --mem=10G # memory in MB per default
###SBATCH --time 0-00:01 # time (D-HH:MM)
#SBATCH --partition htc
#SBATCH --job-name=batch_testbigmem
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


