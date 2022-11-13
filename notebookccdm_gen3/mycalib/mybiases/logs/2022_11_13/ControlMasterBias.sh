# /bin/sh

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2022_39/loadLSST.bash
setup lsst_distrib
source /sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3/repos/w_2022_39/user_setup.sh

EXPOSURES='2022031700001, 2022031700003, 2022031700004, 2022031700005, 2022031700006,
2022031700007, 2022031700008, 2022031700009, 2022031700010, 2022031700011,
2022031700012, 2022031700013, 2022031700024, 2022031700025, 2022031700026,
2022031700027, 2022031700028, 2022031700029, 2022031700030, 2022031700031,
2022031700032, 2022031700033, 2022031700034, 2022031700035, 2022031700036,
2022031700037, 2022031700038, 2022031700039, 2022031700040, 2022031700041,
2022031700042, 2022031700043, 2022031700044, 2022031700045, 2022031700046,
2022031700047, 2022031700048, 2022031700049, 2022031700050, 2022031700051,
2022031700052, 2022031700053, 2022031700054, 2022031700055, 2022031700056,
2022031700057, 2022031700058, 2022031700059'

EXPOSURES_VERIFY='2022031700060, 2022031700061, 2022031700062, 2022031700063, 2022031700064,
2022031700065, 2022031700066, 2022031700067, 2022031700068, 2022031700069, 2022031700070, 2022031700071,
2022031700072, 2022031700073'
    
RERUN=20220317a
BUTLER_REPO='/sps/lsst/groups/auxtel/softs/shared/auxteldm_gen3/data/butler.yaml'


pipetask --long-log run -b $BUTLER_REPO \
        -p $CP_VERIFY_DIR/pipelines/VerifyBias.yaml \
        -i u/czw/calibX,LATISS/raw/all,LATISS/calib,u/dagoret/mybias.20221113/biasGen.$RERUN \
        -o u/dagoret/mybias.20221113/verifyBias.$RERUN \
        -d "instrument='LATISS' AND detector=0 AND exposure IN ($EXPOSURES)" \
             >& ./biasVerify.$RERUN.log

