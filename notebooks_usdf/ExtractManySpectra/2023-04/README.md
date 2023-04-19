# README.md : ExtractrdSpectra April 2023

- last update 2023-04-06

## Config of DM


   ```
   source /sdf/group/rubin/sw/tag/w_2023_11/loadLSST.bash
   setup lsst_distrib -t w_2023_11
   source ~/notebooks/.user_setups
   ```


- User_setups:
   ``` 
  # March 16th 2023 for w_2023_11
  setup -k -r ~/repos/repos_w_2023_11/atmospec
  #setup -k -r ~/repos/repos_w_2023_10/Spectractor



## notebooks

- **CheckForSpectraction-oga-spectractorv2_4.ipynb** : extract spectra from butler and write in h5 file  

- **ViewSpectraction-oga-spectractorv2_4.ipynb** : same, but focused to view order1 and order2 in datafile

- **ReadH5file.ipynb** : read H5 file (test)

- **ConvertH5filetoPandas.ipynb** : convert H5 file attributes in pandas files (no spectrum) , one per night 


- **AnaPandasFiles.ipynb** : Analyse pandas file, one pernight

- **AnaPandasMultiFiles.ipynb** : Aanlyse all pandas files, all nights


- **SearchForBadSpectra.ipynb**: Find criteria to identify what is a  bad spectrum, generate the list of bad numbers

- **SearchForBadSpectraandbadtracking.ipynb**: Study the impact of bad tracking on Spectra 


- **ViewPostISRCCD-oga-spectractorv2_4.ipynb** : Example for extracting the postISRCCD from my collection
