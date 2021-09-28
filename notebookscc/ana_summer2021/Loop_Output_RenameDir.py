#!/bin/sh

#source ${LOADSTACK}
#setup lsst_distrib
#source $HOME/notebooks/.user_setups
#eups list -s | grep LOCAL


# wide scan : HD 160617 
# all_myseq_holo=range(234,310)
# narrow scan :  HD 160617 
# all_myseq_holo=range(317,365)

import os,re

DATE="2021-07-07"
DATE2="2021_07_07"

HOSTCC=False


if HOSTCC:
    path_auxtel="/sps/lsst/groups/auxtel"
    path_spectractor=os.path.join(path_auxtel,"softs/github/desc/Spectractor")
    path_spectractor_config=os.path.join(path_spectractor,"config")
    path_images=os.path.join(path_auxtel,"data/2021/holo/quickLookExp/"+DATE)
else:
    path_auxtel="/Users/dagoret/DATA/AuxTelData2021"
    path_spectractor=os.path.join(path_auxtel,"/users/dagoret/MacOSX/github/LSST/Spectractor")
    path_spectractor_config=os.path.join(path_spectractor,"config")
    path_images=os.path.join(path_auxtel,"holo/quickLookExp/"+DATE)
    path_output_spectractor=os.path.join(path_auxtel,"holo/OutputSpectractor/"+DATE)



#date="2021-07-07"
#datedir="${date}/"
#path_output_dir="/project/shared/auxTel/rerun/dagoret/outputspectr_scan2021_July/spectractorOutput/"
#full_path_output_dir="${path_output_dir}${datedir}"


def file_tag_forsorting(filename):
    # m=re.findall('^Cor_holo4_003_.*([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_.*)[.]fits$',filename)
    m = re.findall('^holo4_003_.*_(.*)_quickLookExp$', filename)
    return m[0]

def file_target(filename):
    m = re.findall('^holo4_003_.*_(.*)_.*_.*_quickLookExp$', filename)
    return m[0]








list_of_files=os.listdir(path_output_spectractor)

for subdir in list_of_files:
    fulldir=os.path.join(path_output_spectractor,subdir)



    if not os.path.isdir(fulldir):
        print("{} is not a directory".format(subdir))

    else:



        print("---------------------------------------------")
        print("{} is a directory".format(subdir))

        tagname=file_tag_forsorting(subdir)
        print("tagname= {}".format(tagname))
        targetname=file_target(subdir)
        print("targetname= {}".format(targetname))

        dir_spectration_in = os.path.join(fulldir, "spectrum")
        dir_spectration_out = os.path.join(fulldir, "basespec")




        if os.path.isdir(dir_spectration_in):
            os.rename(dir_spectration_in,dir_spectration_out)






exit(0)

#




