# README.md

- author : Sylvie Dagoret-Campagne 
- creation date : 2023/01/05


Purpose : learn using BPS for atmospec pipeline





export DISPLAY=

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST.bash
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST-ext.bash
setup lsst_distrib -t w_2022_39
source ~/notebooks/.user_setups

## launch the pipeline
nohup bps submit survey_singleframe.yaml > bps_test.out &

## check the results

./task_times.py submit/u/dagoret/BPS_testspectro/20230105T131542Z/

Concatenating BPS log files... done!

QuantumGraph contains 8 quanta for 4 tasks.

task                              time                  pass     fail     incomp
--------------------------------------------------------------------------------
isr                               18.88s (~45%)         2        0        0     
characterizeImage                 18.01s (~43%)         2        0        0     
singleStarCentroid                5.24s (~12%)          2        0        0     
processStar                       0.00s (~0%)           0        4        0     
--------------------------------------------------------------------------------


for the moment processStar fails !

