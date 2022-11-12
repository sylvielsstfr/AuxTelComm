# /bin/sh

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST.bash
setup lsst_distrib
source /sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3/repos/w_2022_39/user_setup.sh


EXPOSURES='2022031700209, 2022031700211, 2022031700210, 2022031700204,2022031700208, 2022031700205, 2022031700207, 2022031700201,2022031700206, 2022031700202, 2022031700203'
               
    
RERUN=20220317b
BUTLER_REPO='/sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3/data/butler.yaml'


pipetask --long-log run -b $BUTLER_REPO \
          -p $CP_PIPE_DIR/pipelines/Latiss/cpFlat.yaml \
          -i LATISS/calib,LATISS/raw/all \
          -o u/dagoret/myflats.20221108/flatGen.$RERUN \
          -d "instrument='LATISS' AND detector=0 AND exposure IN ($EXPOSURES)" --register-dataset-types \
          >& ./flat.$RERUN.log