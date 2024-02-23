# =============================================================
# README.md
# author Sylvie Dagoret-Campagne
# creation date 2024-02-01
# update 2024-02-01
# =============================================================



export DISPLAY=

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_44/loadLSST.bash
setup lsst_distrib -t w_2023_44
source ~/notebooks/.user_setups

source batch_settings.sh 

eups list -s | grep LOCAL
eups list -s | grep ctrl_bps_htcondor

export BPS_WMS_SERVICE=lsst.ctrl.bps.htcondor.HTCondorService

allocateNodes.py -n 20 -c 120 -m 1-00:00:00 -q roma,milano -g 900 s3df





### launch the pipeline the 2024/02/01 on repo/embargo since 2024/01/01
# expect to process 2024/01/29,  2024/01/30, 2024/01/31

nohup bps submit bps_auxtel_atmo_202401_v3.0.3_doGainsPTC_rebin2.yaml > bps_auxtel_atmo_202401_v3.0.3_doGainsPTC_rebin2_240201.out &

nohup bps submit bps_auxtel_atmo_202401_v3.0.3_doGainsNOPTC_rebin2.yaml > bps_auxtel_atmo_202401_v3.0.3_doGainsNOPTC_rebin2_240201.out &






pipetask run -b /sdf/group/rubin/repo/oga/ -p ./processStar_auxtel_atmo_202401_v3.0.3_doGainsOPTC_rebin2.yaml -i LATISS/raw/all,refcats,LATISS/calib -o u/dagoret/spectro/w_2023_44_spec3.0.3/holo_2024_01_29 -d "exposure.day_obs=20240129 and visit_system=0 and exposure.seq_num in (293,294,316,317,323,324,330,331,337,338) and instrument='LATISS'" --register-dataset-types -j 8
