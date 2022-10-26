# README.md

- author Sylvie Dagoret-Campagne
- creation date : 2022/09/20
- update : 2022/09/22 
- version w_2022_39

source  /sdf/group/rubin/sw/tag/w_2022_39/loadLSST.bash
setup lsst_distrib
source /sdf/home/d/dagoret/notebooks/.user_setups
eups list -s | grep LOCAL



# Run ISR
run_pipeline_ISR.ipynb

# Example of processStar through a notebook
run_pipeline_processStar.ipynb

# Run from command line
run_processstarOneImage.py


(lsst-scipipe-4.1.0) [dagoret@sdfrome015 production]$ ls *.py
run_processstarOneImage_oga.py  run_processstarOneImage.py
(lsst-scipipe-4.1.0) [dagoret@sdfrome015 production]$ ls *.sh
run_multiprocessstar.sh              slurm_run_multiprocessstar_20221023.sh  slurm_runoneseqprocesstar_20221026_notoga.sh
run_multiprocessstar_v2.sh           slurm_run_multiprocessstar_20221025.sh  slurm_runoneseqprocesstar_20221026_oga.sh
run_multiprocessstar_v3-20221025.sh  slurm_run_multiprocessstar.sh           slurm_runoneseqprocesstar_20221026.sh 
