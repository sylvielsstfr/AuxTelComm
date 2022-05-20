#/bin/sh


export PATH=${PATH}:/pbs/throng/lsst/users/dagoret/desc/astrometry_install/bin

ra=91.53909041666665
dec=-66.03962083333333

path="/sps/lsst/groups/auxtel/data/2022/empty~ronchi170lpmm/20220316"
image="exposure_2022031600334_postisrccd.fits"

cmd="solve-field --scale-units arcsecperpix --scale-low 0.01 --scale-high 0.1 --ra $ra --dec $dec --radius 0.076 --overwrite --ext 1 $path/$image"

echo $cmd


`$cmd`

