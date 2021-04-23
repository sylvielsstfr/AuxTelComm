# README.md

- author Sylvie Dagoret-Campagne
- Affiliation : ICLab/IN2P3/CNRS
- date : April 2021

Directory containing notebooks to
create and analyse spectra from Auxtel reconstruted by Spectractor


## production of logbook


- **makeLogbook.ipynb** : make logbook for Holograms    
- **makeLogbook_ronchi.ipynb**  : make logbook for Ronchi

These logbook must be used in two steps:

- first step : the notebook search in a directory the list of images to process and then build a first version of the logbbok
- second step : after building the info structure filename --> guessed position for target (order 0), including a quality flag and a run (spectractor run) flag, 
the logbook is reprocessed to include the reconstrcution result of  **processSpectra.ipynb** and **processSpectraronchi.ipynb**


## Reconstruction by Spectractor

Reconstruct the spectra by spectractor image by image. The goal is to find by hand the guessed position for the central target.

- **processSpectra.ipynb** : call Spectractor for images with Holograms
- **processSpectraronchi.ipynb**  : call Spectractor for images with Ronchi

Using the first version of the logbook constructed by  **makeLogbook.ipynb**  or **makeLogbook_ronchi.ipynb** the guessed target position are written
in the notbook and reported in the info structure in **makeLogbook.ipynb**  or **makeLogbook_ronchi.ipynb**.


## Quality of the PSF

- **anaQualityTargetPSF.ipynb** : skewness and kurtosis for Hologram images
- **anaQualityTargetPSF_ronchi.ipynb** : skewness and kurtosis for Ronchi images


## Analyse spectra

Use the second version of the loggbook containing position and quality flag to compute equivalent width.

- **anaSpectra.ipynb** : Equivalent Width for Holograms 
- **anaSpectra_ronchi.ipynb**   : Equivalent Width Ronchi   

## Other



### **readSpectractSpectra.ipynb**

- read spectra processed by Jeremy in february

###  **makeLogbook.ipynb**
- to generate logbooks. Perhaps later write a quality flag.

###  **processSpectra.ipynb**

- make a first reconstruction finding by hands where the first order is. The good guess and quality flag are
written to be put in logbook generation
- old version of logbook is available to select the file on which one want to reconstruct the spectra


### **reprocessSpectra.ipynb**
- do the same thing as above but the target position is found in the logbook


#### **readMySpectra.ipynb**
- read all the spectra
	



