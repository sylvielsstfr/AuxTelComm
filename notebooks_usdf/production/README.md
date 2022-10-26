# README.md

- author Sylvie Dagoret-Campagne
- creation date : 2022/09/20
- update : 2022/10/26 
- version w_2022_39

# to initialize the stack
source  /sdf/group/rubin/sw/tag/w_2022_39/loadLSST.bash
setup lsst_distrib
source /sdf/home/d/dagoret/notebooks/.user_setups
eups list -s | grep LOCAL



# Run ISR (not working)
run_pipeline_ISR.ipynb

# Example of processStar through a notebook (not working)
run_pipeline_processStar.ipynb

# Run from command line with python:
View those scripts to build the args.
It is important to notice that OGA and non OGA data are not handled by the same buffer.
That is why there are two python script, each configured with the right Butler path.


## non OGA data
- run_processstarOneImage.py

## with OGA data
- run_processstarOneImage_oga.py 


# Run a series of reconstruction

## Run from interactive

### scripts

- run_multiprocessstar.sh
- run_multiprocessstar_v2.sh
- run_multiprocessstar_v3-20221025.sh 


### Run from interactive machine

- example :

    nohup ./run_multiprocessstar_v2.sh &


###  switch to interactive mode:

    srun --pty --cpus-per-task=8 --mem-per-cpu=4G --time=23:00:00 --partition=roma /bin/bash
    
- then run 
(cannot use nohup in that case)

    source run_multiprocessstar_v3-20221025.sh 


### SLURM 

#### SLURM with job-array (not working contrary to CCIN2P3, butler bay block)

- slurm_run_multiprocessstar.sh 
- slurm_run_multiprocessstar_20221023.sh  
- slurm_run_multiprocessstar_20221025.sh  


#### SLURM with sequential processing (thus not optimized)

- slurm_runoneseqprocesstar_20221026.sh 
- slurm_runoneseqprocesstar_20221026_notoga.sh
- slurm_runoneseqprocesstar_20221026_oga.sh

          

