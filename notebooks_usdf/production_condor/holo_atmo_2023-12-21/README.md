# =============================================================
# README.md
# author Sylvie Dagoret-Campagne
# creation date 2023-12-21
# update 2023-12-21
# =============================================================

# set the limit on lambdaMin in processStar.yaml files

export DISPLAY=

source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_44/loadLSST.bash
setup lsst_distrib -t w_2023_44
source ~/notebooks/.user_setups

source batch_settings.sh 

eups list -s | grep LOCAL
eups list -s | grep ctrl_bps_htcondor

export BPS_WMS_SERVICE=lsst.ctrl.bps.htcondor.HTCondorService

allocateNodes.py -n 20 -c 120 -m 1-00:00:00 -q roma,milano -g 900 s3df



### launch the pipeline the 2023/12/21 on /repo/main on data since 2021/01/01

# note the special (visit_system=0) in where clause

nohup bps submit bps_auxtel_atmo_202101_v3.0.3_doGainsNOPTC_rebin2.yaml > bps_auxtel_atmo_202101_v3.0.3_doGainsNOPTC_rebin2_231221.out &




### launch the pipeline the 2023/12/21 on repo/embargo since 2022/09/01


nohup bps submit bps_auxtel_atmo_202209_v3.0.3_doGainsPTC_rebin2.yaml > bps_auxtel_atmo_202209_v3.0.3_doGainsPTC_rebin2_231221.out &


