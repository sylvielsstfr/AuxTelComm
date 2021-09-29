# README.md : How to use processing with Spectractor

- author : Sylvie Dagoret-Campagne
- affiliation : IJCLab/IN2P3/CNRS
- creation date : September 21th 2021
- update : September 29th 2021



The sequence to perform Spectractor reconstruction is to perform in the order

- 1) generation of the logbook for the input images using notebook **make_logbook.ipynb**
- 2) run **processSpectra.ipynb** or **processSpectra.py** to check the position of order 0th using Spectractor and then running the reconstruction
- 3) check the reconstructed spectra using **anaSpectra.ipynb**

The script name above are generic.

- To analyse the Planetary nebula of night 2021-09-09 use:
   1) **makeLogbook_holo-newspectractor.ipynb**
   2) **processSpectra_holo-PNG-newspectractor.ipynb**
   3) **anaSpectra_PNG.ipynb**


- To analyse the XY scan of night 2021-07-07 uses:
   1) **makeLogbook_holo-newspectractor.ipynb**
   2) **processSpectra_holo-newspectractor.ipynb** or **processSpectra_holo-newspectractor.py**
   3) **anaSpectra_holo_newspectractor.ipynb**


The label **newspectractor** means the last version of spectractor (September 2021) where we can prevent the search or dispersion axis rotation.


# 1) makeLoogbook.ipynb
- generate basic logbook from filename and information in header.
It must be regenerated each time a new order 0th positon guess is added. This new guess will be applied in **processSpectra.ipynb**



# 2) processSpectra.ipynb
- try to find position of order 0 target. It must be used to update the logbook.
- finally run the reconstruction

## processSpectra_holo.ipynb
## processSpectra_holo-newspectractor.ipynb
## processSpectra_holo-PNG-newspectractor.ipynb



# 3) reprocessSpectra.ipynb
- final processing with Spectractor (deprecated)



# 4) analyse

- anaSpectra.ipynb
- PlanetaryNebula_2021-09-09.ipynb

# Other or deprecated


## QuickViewMyImages-badwcs.ipynb
## QuickViewMyImages.ipynb
## RawImagesReduction.ipynb (deprecated since we have quickLookExp)
