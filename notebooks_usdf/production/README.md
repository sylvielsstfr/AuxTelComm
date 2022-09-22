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
