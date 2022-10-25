#!/bin/bash
#SBATCH --partition=roma
#
#SBATCH --job-name=procstar
#SBATCH --output=procstar_%A_%a.out
#SBATCH --error=procstar_%A_%a.err
#SBATCH --array=1-63
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=20G
#
#SBATCH --time=24:00:00
# Print the task id.
echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

echo "Node: $(hostname)"

echo " Slurm environment variables:"
env | grep SLURM


export DISPLAY=
export LOGBOOKSPATH=/sdf/home/d/dagoret/notebooks/AuxTelComm/notebooks_usdf/butlertools/all_visitdispersers
export LOGBOOKFILENAME=visitdispersers_20220630_filt_empty-holo4_003.list
export FILTERDISPERSER=empty~holo4
export DATE=20220630
export REPOSDIR=/sdf/home/d/dagoret/repos/repos_w_2022_39
export OUTPUTCOLL=u/dagoret/tests/test_23oct2022_${FILTERDISPERSER}_${DATE} 

# Define the logbook fullfilename
fullfilenamelogbook=${LOGBOOKSPATH}/${DATE}/${LOGBOOKFILENAME}

# Initialisation of DM
source /sdf/group/rubin/sw/tag/w_2022_39/loadLSST.bash
setup lsst_distrib -t w_2022_39
source ~/notebooks/.user_setups

# launch the python script that run DM pipeline
echo "python run_processstarOneImage.py --reposdir ${REPOSDIR} --listofimages ${fullfilenamelogbook} --num ${SLURM_ARRAY_TASK_ID} --outcoll ${OUTPUTCOLL}"
python run_processstarOneImage.py --reposdir ${REPOSDIR} --listofimages ${fullfilenamelogbook} --num ${SLURM_ARRAY_TASK_ID} --outcoll ${OUTPUTCOLL}
