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
config.isr.doFlat = False
config.isr.doFringe = False
config.isr.doDefect = True
config.isr.doCrosstalk = False
config.isr.doSaturationInterpolation = False

#config.isr.doWrite = False
#config.charImage.doWriteExposure = False

#config.charImage.doApCorr = False
#config.charImage.doMeasurePsf = False
#config.charImage.repair.cosmicray.nCrPixelMax = 100000
#config.charImage.repair.doCosmicRay = False
#if config.charImage.doMeasurePsf:
#    config.charImage.measurePsf.starSelector['objectSize'].signalToNoiseMin = 10.0
#    config.charImage.measurePsf.starSelector['objectSize'].fluxMin = 5000.0
#config.charImage.detection.includeThresholdMultiplier = 3
#config.isr.overscan.fitType = 'MEDIAN_PER_ROW'