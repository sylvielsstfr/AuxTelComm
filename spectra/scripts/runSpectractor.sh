#/bin/sh
dir_spectra="/Users/dagoret/DATA/AuxTelData2021/holo/FlipCleans"
filename_image="Cor_holo4_003_RG610_HD75519_2021-03-11_296.fits"
fullfilename=${dir_spectra}/${filename_image}
output_directory="./outputs/"
guess='[1500,3700]'
disperser_label="holo4_003"
config="config/auxtel_quicklook.ini"
#config = "config/auxtel.ini"
target="HD75519"


python runExtractor.py ${fullfilename} -d -o outputs -c ${config} --xy ${guess} -t ${target} -g ${disperser_label}
