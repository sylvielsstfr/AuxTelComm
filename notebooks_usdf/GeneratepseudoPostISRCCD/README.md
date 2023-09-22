# Generate fits files from Exposure

- author : Sylvie Dagoret-Campagne
- creation date : September 2023
- last update 2023-09-20


## Purpose

Extract Exposure from butler and generate fits file.
ISR is amplied to get PostISRCCD
A check that good calibration (Master Bias) is taken (calibration date for bais and detect is shown)

This conversion is done through a series of scripts or notebooks.
The differentce between the version is the hierarchy for writing files:

- no version DATE/FILTER
- v2 version FILTER/DATE (used un run_spectractor_standalone)


The choice of DATE and filter is done through the files

## Notebooks

Notebooks can be used when there is a small number of exposures, a flag activate visualisation

- **MakeMyPostISRCCDfromRawForSpectractorSD.ipynb**  
- **MakeMyPostISRCCDfromRawForSpectractorSD_v2.ipynb**, this is what I need


## scripts

Script xan be used for fast running. No visudalisation

- **MakeMyPostISRCCDfromRawForSpectractorSD.py**  
- **MakeMyPostISRCCDfromRawForSpectractorSD_v2.py** this is what I need

## New 

The good procedure is to extract PostISRCCD from PostISRCCD

- **MakeMyPostISRCCDfromDMPostISRCCDForSpectractorSD.ipynb**  