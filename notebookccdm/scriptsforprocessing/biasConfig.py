import os

# Reference catalog
#for refObjLoader in (config.calibrate.astromRefObjLoader,
#                     config.calibrate.photoRefObjLoader,
#                     ):
    #refObjLoader.load(os.path.join(obsConfigDir, 'filterMap.py'))
#    refObjLoader.ref_dataset_name = 'gaia_dr2_20191105'

#config.calibrate.connections.astromRefCat = "gaia_dr2_20191105"
#config.calibrate.connections.photoRefCat = "gaia_dr2_20191105"

config.isr.doLinearize = False
#config.isr.doBias = False
config.isr.doDark = False
#config.isr.doFlat = False
config.isr.doFringe = False
config.isr.doDefect = False
config.isr.doCrosstalk = False
config.isr.doSaturationInterpolation = False
