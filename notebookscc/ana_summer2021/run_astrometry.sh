#!/bin/sh


path_input_dir="/Users/dagoret/DATA/AuxTelData2021/holo/quickLookExp_v2/"
date="2021-07-07/"

full_path_input_dir="${path_input_dir}${date}"

filename="holo4_003_empty_HD160617_20210707_000317_quickLookExp.fits"

fullfilename="${full_path_input_dir}${filename}"

echo ${fullfilename}
#cmd="solve-field --scale-units 0.956 --scale-low 0.005 --scale-high 0.02 ${fullfilename} 2>&1"
#echo $cmd
#output=`$cmd`
#echo $output

cmd="solve-field --scale-units arcsecperpix --scale-low 0.005 --scale-high 0.02 ${fullfilename}[1]"
echo $cmd
`$cmd`

done



