#! /bin/sh

# author : Sylvie Dagoret-Campagne 
# creation date : 2023/01/18
# last update : 2023/01/18


export DISPLAY=

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST.bash
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST-ext.bash
setup lsst_distrib -t w_2023_01
source ~/notebooks/.user_setups

eups list -s | grep LOCAL
export BPS_WMS_SERVICE=lsst.ctrl.bps.parsl.ParslService



# launch the pipeline
# nohup bps submit survey_singleframe_v6.yaml > bps_test_v6.out &

#with  Data Query :
#dataQuery: "instrument='LATISS' AND exposure.day_obs=20221208 AND exposure.seq_num=44"


# nohup bps submit survey_singleframe_v6.yaml > bps_manyspectra_v6.out &
# with Data Query
# dataQuery: "instrument='LATISS' AND exposure.day_obs=20221208 AND physical_filter.name='empty~holo4_003'"



## check the results
#(lsst-scipipe-5.1.0-ext) [dagoret@sdfrome002 AuxTel_spectro_survey]$ ./task_times.py submit/u/dagoret/BPS_testspectro/20230112T083828Z





