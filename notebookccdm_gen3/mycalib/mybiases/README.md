# README.md

Gaol understand how to generate a MasterBias and see a Masterbias to be sure that I pick the right MasterFlat later.
Want to compare the Masterbias from imported/ingested calibs in 2022/06 (Bootcamp) / the calib I generate for 2022/03/17


## Shell script to generate a MasterBias and check a Master Bias

- Generate the Masterbias : GenerateMasterBias.sh

- Verify the Masterbias : ControlMasterBias.sh  

## logs outputs

- in logs/



## Notebooks

- 0) View the list of available calib collections : **QueryForCalibCollections.ipynb**
- 1) nb to Select a series of bias to make Master Bias : **ListOfExposures-biases.ipynb**   
- 2) nb to view the indisvidual bias exposures for the date 0210311  : **ViewExposures-biases.ipynb**
- 3) nb to view each individual bias exposures for the date 20220317 : **ViewExposures-biases-20220317.ipynb**  
- 4) Ask to view a Masterbias showing strong effects with columns : **QueryForMasterBias.ipynb**
The question is why I see the same Masterbias with previously ingested calibs wrt the new generated MasterBias on bias exposures of 20220317
- 5) Nb to conptrol the output of **GenerateMasterBias :  **cpp-bias-20220317.ipynb**



