#!/bin/sh
########################################
# SLURM options
########################################
#SBATCH --mem=20G # memory in MB per default
#SBATCH --ntasks 1 # Run single task or CPU
#SBATCH --time 7-00:00:00 # time (D-HH:MM)
#SBATCH --partition htc
#SBATCH --job-name=procstar0
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


source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_09/loadLSST.bash ; setup lsst_distrib
source ../repos/w_2022_09/user_setup.sh



which python

python run_processstar_gen3_v7.py 0
