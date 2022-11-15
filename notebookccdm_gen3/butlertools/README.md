# README.md

-  author : Sylvie Dagoret-Campagne
- affiliation : IJCLab

- update : 2022-11-15
- current DM version w_2022_39


Butler tools to make queruis to Butler for later use.


## Simple Butler queries or examples 

These are example to remember the butler commands.

Interesting commands are reviewed in ths tutorial https://pipelines.lsst.io/


- Query on existing collections : **QueryForCollections.ipynb**
- Example to query results of Spectractor (DM version ) : **QueryForSpectraction.ipynb**   


## Generate list of bias, flats, science exposures into files

- Generate list of bias : **ListOfExposures-bias.ipynb**

- Generate list of flats : **ListOfExposures-flats.ipynb**

- Generate list of hologram exposures :  **ListOfExposures-hologram.ipynb** 

- Generate list of ronchi exposures : **ListOfExposures-ronchi.ipynb**

- Probably deprecated list of exposures : **ListOfExposures.ipynb**   

## Make bookkeeping

Generate excel files, one page per night. Suspect there are missing entries (bug ?) 

-  Book-keeping for bias exposures : **MakeBookKeeping-bias.ipynb**   

-  Book-keeping for flats : **MakeBookKeeping-flat.ipynb** 

-  Book-keeping for holograms : **MakeBookKeeping-hologram.ipynb**  


## Conversion of postISRCCD Exposures inside the Butler into external fits file

- unefficient old way through notebooks :  **ExposuresPostISRCCDtofits.ipynb**
- more efficient conversion through a script : **python ExposuresPostISRCCDtofits.py**
- simple batch job scripts to run above script in batch : **slurm_run_ExposuresPostISRCCDtofits.sh**


## Example to view

remember ds9 att CC is available as 
    
     alias ds9='/pbs/throng/lsst/software/desc/bin/ds9'
     
     
- Example to view bias exposure : **ViewExposures-bias.ipynb**

- Example to view flats exposure : **ListOfExposures-flats.ipynb**    

- Example to view postISRCCD : **ViewExposures-postISRCCD.ipynb** 

- Convert postISRCCD in butler into a fits file : **ViewExposuresPostISRCCDandSaveFits.ipynb** 

- Deprecated, to view results of Spectraction : **ViewSpectractionResults.ipynb**



  




          
   