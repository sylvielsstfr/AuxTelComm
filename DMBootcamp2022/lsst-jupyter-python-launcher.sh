#!/bin/bash

# ----------------------------------------------------------------------------#
# File:    lsst-jupyter-kernel-launcher.sh                                    #
#                                                                             #
# Purpose: launch a Python Jupyter kernel configured to use a given release   #
#          the LSST science pipelines (lsst_distrib) distributed via cvmfs    #
#          (see https://sw.lsst.eu)                                           #
#                                                                             #
# Usage:  this file and its companion configuration files must be located     #
#         at                                                                  #
#              ~/.local/share/jupyter/kernels   (Linux)                       #
#              ~/Library/Jupyter/kernels        (macOS)                       #
#                                                                             #
#          To specify the version of the LSST software that you want to use   #
#          in your Jupyter notebook, initialize the environment variable      #
#          LSST_DISTRIB_RELEASE to the value of a given release,              # 
#          e.g. w_2020_05.                                                    #
#                                                                             #
# Source:  https://www.github.com/airnandez/lsst-jupyter-kernel               #
#                                                                             #
# Author: fabio hernandez                                                     #
#         IN2P3/CNRS computing center (CC-IN2P3)                              #
#         https://cc.in2p3.fr                                                 #
# ----------------------------------------------------------------------------#

#
# Save and consume all command line arguments: we don't want them to be passed
# to sourced scripts, such as 'loadLSST.bash'
#
allArgs="$@"
set --

#
# Determine the lsst_distrib top level directory
#
case $(uname) in
    "Linux")
        distribDir='/cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib';;
    "Darwin")
        distribDir='/cvmfs/sw.lsst.eu/darwin-x86_64/lsst_distrib';;
esac

#
# Build the absolute path of the specified release via the environment
# variable "LSST_DISTRIB_RELEASE" or the "latest" available
#
release=${LSST_DISTRIB_RELEASE:-'latest'}
if [[ ${release} == 'latest' ]]; then
    # Select the most recent release among the stables (v*) and weeklies (w_*), 
    # but not development releases (i.e. those ending by '-dev')
    release=$(ls -d ${distribDir}/v*[0-9] ${distribDir}/w_*[0-9] | tail -1)
    release=$(basename ${release})
fi
releaseDir=${distribDir}/${release}

#
# EUPS setup the requested release
#
if [[ -f ${releaseDir}/loadLSST.bash ]]; then
    #
    # Unset ANACONDA, MINICONDA and CONDA environment variables so that
    # the conda environment included in the Rubin's LSST science pipelines
    # takes precedence over the one potentially existing in the
    # Jupyter environment under which this kernel is being executed
    #
    for v in $(env | grep -e '^CONDA' -e '^ANACONDA' -e '^MINICONDA'); do 
        eval $(echo $v | awk -F '=' '{printf "unset %s", $1}')
    done

    #
    # Save the current PYTHONPATH
    #
    savedPythonPath=${PYTHONPATH}
    unset PYTHONPATH

    #
    # Activate the Rubin environment: if the value of the environment variable
    # 'LSST_USE_EXTENDED_CONDA_ENV' is "true", activate the extended conda 
    # environment by using the loader 'loadLSST-ext.bash' instead of 'loadLSST.bash'
    #
    export LSST_DISTRIB_RELEASE=$(basename ${releaseDir})
    loader=${releaseDir}/loadLSST.bash
    if [[ ${LSST_USE_EXTENDED_CONDA_ENV} == "true" ]] && [[ -f ${releaseDir}/loadLSST-ext.bash ]]; then
        loader=${releaseDir}/loadLSST-ext.bash
    fi
    unset LSST_USE_EXTENDED_CONDA_ENV
    source ${loader}
    setup lsst_distrib

    #
    # Restore PYTHONPATH
    #
    if [[ ! -z ${savedPythonPath} ]]; then
        export PYTHONPATH="${PYTHONPATH}:${savedPythonPath}"
    fi
fi

