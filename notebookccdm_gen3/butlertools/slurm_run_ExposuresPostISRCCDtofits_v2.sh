#!/bin/sh

# SLURM options:

#SBATCH --job-name=convertfits    # Job name
#SBATCH --output=convertfits_%j.log   # Standard output and error log

#SBATCH --partition=htc               # Partition choice
#SBATCH --ntasks=1                    # Run a single task (by default tasks == CPU)
#SBATCH --mem=3000                    # Memory in MB per default
#SBATCH --time=1-00:00:00             # 7 days by default on htc partition


# Commands to be submitted:

# srun -p htc_interactive -n 8 --pty bash -i
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST.bash 
setup lsst_distrib

python ExposuresPostISRCCDtofits.py

