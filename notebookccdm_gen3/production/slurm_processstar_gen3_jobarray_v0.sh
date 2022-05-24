#!/bin/bash
####################################
# SLURM options
###################################
#SBATCH --job-name=procsstar
#SBATCH --output=array_%A_%a.out
#SBATCH --error=array_%A_%a.err
#SBATCH --array=1-18
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



# visitdispersers_20211102_filt_BG40-holo4_003.list
# visitdispersers_20211102_filt_BG40-ronchi170lpmm.list
# visitdispersers_20211102_filt_FELH0600-holo4_003.list
# visitdispersers_20211102_filt_FELH0600-ronchi170lpmm.list
# visitdispersers_20211102_filt_SDSSg-holo4_003.list
# visitdispersers_20211102_filt_SDSSg-ronchi170lpmm.list
# visitdispersers_20211102_filt_empty-holo4_003.list
# visitdispersers_20211102_filt_empty-ronchi170lpmm.list

# visitdispersers_20211103_filt_BG40-holo4_003.list
# visitdispersers_20211103_filt_FELH0600-holo4_003.list
# visitdispersers_20211103_filt_SDSSg-holo4_003.list
# visitdispersers_20211103_filt_empty-holo4_003.list


# visitdispersers_20211104_filt_BG40-holo4_003.list
# visitdispersers_20211104_filt_BG40-ronchi170lpmm.list
# visitdispersers_20211104_filt_FELH0600-holo4_003.list
# visitdispersers_20211104_filt_FELH0600-ronchi170lpmm.list
# visitdispersers_20211104_filt_empty-holo4_003.list
# visitdispersers_20211104_filt_empty-ronchi170lpmm.list


export NEWHOME="/pbs/throng/lsst/users/dagoret"
export AUXTELHOME="/sps/lsst/groups/auxtel"
export AUXTELDM="${AUXTELHOME}/softs/shared/auxteldm"
export AUXTELDM2="${AUXTELHOME}/softs/shared/auxteldm_gen3"
#export PATH=/pbs/throng/lsst/software/desc/bin:${PATH}
#source /pbs/throng/lsst/software/desc/common/miniconda/setup_current_python.sh 


source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_09/loadLSST.bash ; setup lsst_distrib
source ../repos/w_2022_09/user_setup.sh



which python




python processSpectra_holo-newspectractor_v2-configHb.py ${DAYNUM} ${SLURM_ARRAY_TASK_ID}
