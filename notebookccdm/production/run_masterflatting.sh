#/bin/sh

# source run_masterflatting.sh all_visitsflats/*

#source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2021_44/loadLSST.bash
#setup lsst_distrib

#PATH=dirname "$@"
#echo "PATH=$PATH"
 
for file in "$@"
do
  echo "Processing $file file..."
  # take action on each file. $file store current file name
  cat "$file"
  cmd="constructFlat.py . --rerun dagoret_jan22_flats  @${file}  --batch-type none --configfile flatConfig.py --clobber-config"
  echo -e "${cmd}"
  `$cmd`
 
done
