#!/usr/bin/env python
# coding: utf-8

# # Run Spectractor from notebooks
# 
# - adapted from https://github.com/stubbslab/PCWG-AuxTel/blob/main/Run_Spectractor_example.ipynb
# 
# - author : Sylvie Dagoret-campagne
# - affiliation : IJCLab/IN2P3/CNRS
# - update : September 2021 13th
# - DM-Stack version : **w_2021_36**
# - Big CPU

# In[ ]:


# wide scan : HD 160617 
all_myseq_holo=range(234,310)
# narrow scan :  HD 160617 
#all_myseq_holo=range(317,365)
all_myseq=all_myseq_holo


# In[1]:


#Check your stack container version matches the setup instructions!
#version = get_ipython().getoutput('eups list -s lsst_distrib')
#print(f'You are running {version[0].split()[1]} of lsst_distrib')


# Check your packages are setup, as per the setup instructions. Each of the ones setup should appear here. If they don't, you've missed the line in your .user_setups file

# In[2]:


#get_ipython().system(' eups list -s | grep LOCAL')


# Redirect the logger outputs (stack and Spectractor) to the notebook:

# In[3]:


#from lsst.log.utils import enable_notebook_logging
#enable_notebook_logging()


# Make a bulter, pick an image, and make a data reference to it:



import lsst.daf.persistence as dafPersist

# SDC :: not working Sept 9th 2021
#butler = dafPersist.Butler('/project/shared/auxTel/')

#repoDir='/project/shared/auxTel/rerun/quickLook'

#recommended from https://github.com/stubbslab/PCWG-AuxTel/blob/main/setup_script.md
#repoDir='/project/shared/auxTel/rerun/mfl/slurmRun/'

#
#After mfl created /project/shared/auxTel/rerun/dagoret (2021/09/09):
#repoDir='/project/shared/auxTel/rerun/dagoret/output'
#repoDir='/project/shared/auxTel/rerun/dagoret'
repoDir='/project/shared/auxTel/rerun/dagoret/outputspectr_scan2021_July'
butler=  dafPersist.Butler(repoDir)

dataId = {'dayObs': '2021-07-07', 'seqNum': 235}
#dataId = {'dayObs': '2021-07-07', 'seqNum': 330}
dataRef = butler.dataRef('raw', **dataId)


# Instantiate the task, set our config options


from lsst.atmospec import ProcessStarTask

config = ProcessStarTask.ConfigClass()
config.doDisplayPlots = False  # show the plots in the notebook
config.spectractorDebugMode = False  # make all the debug plots along the way
config.binning = 4

# pretty minimal ISR because some things we don't have the calib products available for
# most of this would be picked up automatically if running from the command line from config files
config.isr.doLinearize = False
config.isr.doDark = False
config.isr.doFlat = False
config.isr.doFringe = False
config.isr.doDefect = True
config.isr.doCrosstalk = False
config.isr.doSaturationInterpolation = False

task = ProcessStarTask(config=config)


# Set this so that the plots pop up in the notebook
# get_ipython().run_line_magic('matplotlib', 'inline')


# Run, and watch the debug plots roll in. If you've selected a writable rerun above, the result will also be butler.put() in there so you can butler.get() it later, but we can also catch the result as it's returned by the runDataRef() method



result = task.runDataRef(dataRef)




print("hello - END ")



