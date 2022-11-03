# README.md : Generate Photometry of stars

- author Sylvie Dagoret-Campagne
- creation date : 2022/11/03
- update : 2022/11/03 
- version w_2022_39

# to initialize the stack
source  /sdf/group/rubin/sw/tag/w_2022_39/loadLSST.bash
setup lsst_distrib
source /sdf/home/d/dagoret/notebooks/.user_setups
eups list -s | grep LOCAL



      
Baiscally inspired from doc here https://confluence.lsstcorp.org/display/LSSTCOM/AuxTel+Imaging+Survey+Data+Descriptions

To run the command

    pipetask run -b /repo/main -i LATISS/raw/all,refcats,LATISS/calib -o u/edennihy/latiss_singleFrame_test -d "exposure=2022050400274 AND instrument='LATISS' AND detector=0" -p \$DRP_PIPE_DIR/pipelines/LATISS/DRP.yaml#isr,characterizeImage,calibrate --register-dataset-type
