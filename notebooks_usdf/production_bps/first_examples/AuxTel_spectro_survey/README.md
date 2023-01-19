# README.md

- author : Sylvie Dagoret-Campagne 
- creation date : 2023/01/05
- last update : 2023/01/12

Purpose : learn using BPS for atmospec pipeline





export DISPLAY=

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST.bash
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST-ext.bash
setup lsst_distrib -t w_2023_01
source ~/notebooks/.user_setups

eups list -s | grep LOCAL
export BPS_WMS_SERVICE=lsst.ctrl.bps.parsl.ParslService



## launch the pipeline
> nohup bps submit survey_singleframe_v2.yaml > bps_test.out &

with  Data Query :

    dataQuery: "instrument='LATISS' AND exposure.day_obs=20221208 AND exposure.seq_num=44"


> nohup bps submit survey_singleframe_v3.yaml > bps_manyspectra_v0.out &

with Data Query

    dataQuery: "instrument='LATISS' AND exposure.day_obs=20221208 AND physical_filter.name='empty~holo4_003'"



## check the results

(lsst-scipipe-5.1.0-ext) [dagoret@sdfrome002 AuxTel_spectro_survey]$ ./task_times.py submit/u/dagoret/BPS_testspectro/20230112T083828Z

Concatenating BPS log files... done!

QuantumGraph contains 4 quanta for 4 tasks.

task                              time                  pass     fail     incomp
--------------------------------------------------------------------------------
processStar                       675.60s (~97%)        1        0        0     
characterizeImage                 10.21s (~1%)          1        0        0     
isr                               8.68s (~1%)           1        0        0     
singleStarCentroid                2.95s (~0%)           1        0        0     
--------------------------------------------------------------------------------
total                             697.44s               4        0        0     



or

(lsst-scipipe-5.1.0-ext) [dagoret@sdfrome002 AuxTel_spectro_survey]$ ./task_times.py submit/u/dagoret/BPS_manyspectro_v0/20230112T090722Z

Concatenating BPS log files... done!

QuantumGraph contains 876 quanta for 4 tasks.

task                              time                  pass     fail     incomp
--------------------------------------------------------------------------------
isr                               5808.66s (~54%)       219      0        0     
characterizeImage                 3664.94s (~34%)       219      0        0     
singleStarCentroid                961.36s (~9%)         219      0        0     
processStar                       266.19s (~2%)         1        58       0     
--------------------------------------------------------------------------------
total                             10701.15s             658      58       0     

Executed 658 quanta out of a total of 876 quanta (~75%).





