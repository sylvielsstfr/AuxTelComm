# README.md : ExtractrdSpectra April 2023

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

- **ReadH5file.ipynb** : read H5 file (test)

- **ConvertH5filetoPandas.ipynb** : convert H5 file attributes in pandas file (no spectrum)  


- **AnaPandasFiles.ipynb** : pandas file

- **SearchForBadSpectra.ipynb**: Find criteria to identify a bad spectrum
