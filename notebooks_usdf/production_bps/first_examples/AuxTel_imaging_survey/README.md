# README.md

- author : Sylvie Dagoret-Campagne 
- creation date : 2023/01/05


Purpose : learn using BPS for the photometry  pipeline


source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST.bash 
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST-ext.bash
setup lsst_distrib
pip install 'parsl[monitoring]' --user
pip uninstall sqlalchemy


## launch the pipeline
nohup bps submit survey_singleframe.yaml > bps_test.out &

## check the results

In Dans /sdf/data/rubin/user/dagoret/AuxTel_imaging_survey


./task_times.py  submit/u/dagoret/BPS_test/20230105T093632Z/

Concatenating BPS log files... done!

QuantumGraph contains 1610 quanta for 5 tasks.

task                              time                  pass     fail     incomp
--------------------------------------------------------------------------------
characterizeImage                 731784.07s (~85%)     317      10       0     
calibrate                         114157.17s (~13%)     286      62       0     
isr                               12842.26s (~1%)       322      11       0     
writeSourceTable                  2835.32s (~0%)        286      0        0     
transformSourceTable              2444.64s (~0%)        286      0        0     
--------------------------------------------------------------------------------
total                             864063.45s            1497     83       0     

Executed 1497 quanta out of a total of 1610 quanta (~93%).

