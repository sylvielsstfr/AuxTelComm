#/bin/sh

pipetask run -p ${ANALYSIS_TOOLS_DIR}/pipelines/visitQualityCore.yaml -b /sdf/group/rubin/repo/oga -i LATISS/runs/AUXTEL_DRP_IMAGING_2023-11A-10A-09AB-08ABC-07AB-05AB/w_2023_46/PREOPS-4553 -o u/dagoret/analysis_tools_auxtelphotometry2023/visitQualityCoreTest1 --register-dataset-types --prune-replaced=purge --replace-run

