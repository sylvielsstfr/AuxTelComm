#! /bin/sh

# author : Sylvie Dagoret-Campagne 
#creation date : 2023/02/03


#Purpose : learn using BPS for the photometry  pipeline


source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST.bash 
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST-ext.bash
setup lsst_distrib
#pip install 'parsl[monitoring]' --user
#pip uninstall sqlalchemy


## launch the pipeline
#nohup bps submit survey_singleframe.yaml > bps_test.out &

## check the results

#In Dans /sdf/data/rubin/user/dagoret/AuxTel_imaging_survey


#./task_times.py  submit/u/dagoret/BPS_test/20230105T093632Z/


#nohup bps submit survey_singleframe_photimagingwithholo_20230117-v0.yaml  > bps_survey_singleframe_photimagingwithholo_20230117-v0.log &
