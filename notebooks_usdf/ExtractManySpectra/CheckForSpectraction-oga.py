# # Query for Spectraction Results in OGA

#  work with Weakly_2023_01
# - use jupyter kernel LSST
# 
# 
# - author : Sylvie Dagoret-Campagne
# - affiliation : IJCLab
# - creation date : 2022/10/31
# - update : 2022/01/20




import lsst.daf.butler as dafButler
#import lsst.summit.utils.butlerUtils as butlerUtils


import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
import pandas as pd

import matplotlib.ticker                         # here's where the formatter is
import os
import re
import pandas as pd

plt.rcParams["figure.figsize"] = (4,3)
plt.rcParams["axes.labelsize"] = 'xx-large'
plt.rcParams['axes.titlesize'] = 'xx-large'
plt.rcParams['xtick.labelsize']= 'xx-large'
plt.rcParams['ytick.labelsize']= 'xx-large'


import pickle


from astropy.time import Time
import astropy.units as u


### Config

#### Butler

#repo =  "/sdf/group/rubin/repo/main"
repo = "/sdf/group/rubin/repo/oga/"
butler = dafButler.Butler(repo)
registry = butler.registry


#### Date & Filter & Disperser
# path index for each month
#DATE="20230117" # with "u/dagoret/BPS_manyspectro_v7"
DATE="20230118" # with "u/dagoret/BPS_manyspectro_v8"
#DATE="20230119" # with "u/dagoret/BPS_manyspectro_v9"

filterdispersername = "empty~holo4_003"
#filterdispersername = "BG40~holo4_003"
#filterdispersername = "FELH0600~holo4_003"


# ### Spectractor
configmode = "PSF2DFFM_REBIN2"


# ### The collection

#my_collection = "u/dagoret/spectro/noflat/empty~holo4/"+str(DATE)

#my_collection = "u/dagoret/BPS_manyspectro_v7" # january 20th 2023 (2023/01/17)
#my_collection = "u/dagoret/BPS_manyspectro_v8" # january 23th 2023 (2023/01/18)
#my_collection = "u/dagoret/BPS_manyspectro_v9" # january 23th 2023 (2023/01/19)
my_collection = "u/dagoret/BPS_manyspectro_v10" # january 23th 2023 (2023/01/18), output with the _b

datasetRefs = registry.queryDatasets(datasetType='spectraction', collections=my_collection, where= "instrument='LATISS'")

#butler = butlerUtils.makeDefaultLatissButler(extraCollections=[my_collection])

number_of_references  = len(list(datasetRefs))
print(f"number_of_references = {number_of_references}")

#### Options
FLAG_PLOT = False


#### Loop on exposures
all_dataId = []     # full data id
all_spec = []       # spectra
all_exposures = []  # exposure number
all_num = []        # sequence numbers



for i, ref in enumerate(datasetRefs):

    print(f"==============({i})========== datasetType = spectraction ============================================")
    print("fullId..................:",ref.dataId.full)
    print("visit...................:",ref.dataId["visit"])
    print("band....................:",ref.dataId["band"])
    print("physical filter.........:",ref.dataId["physical_filter"])
    print("run.....................:",ref.run)
    the_exposure = ref.dataId["visit"]
    the_day_obs = ref.dataId["visit"]//100_000
    the_seq_num = ref.dataId["visit"]- the_day_obs*100_000    
    the_dataId = {'day_obs': the_day_obs,'seq_num':the_seq_num,'detector':0}
    print(the_dataId)
    
    # retrieve the spectrum from Butler
    #spec       = butler.get('spectraction',the_dataId)
    spec = butler.get('spectraction', visit=the_exposure, detector=0, collections=my_collection, instrument='LATISS')
    
    # save in collection lists
    all_dataId.append(the_dataId) 
    all_exposures.append(the_exposure)
    all_spec.append(spec)
    all_num.append(the_seq_num)
    #if i > 15:
    #    break



#### Plot


FLAG_ORDER2 = False

infos = []
all_lambdas=[]
all_data=[]
all_data_err=[]

if FLAG_ORDER2:
    all_lambdas_order2=[]
    all_data_order2=[]
    all_data_err_order2=[]



for idx,spec in enumerate(all_spec):
    
    # get spectrum 
    s=spec.spectrum
    label = str(idx) +"):" + str(all_exposures[idx])
    
    try:
    
        if FLAG_PLOT:
            fig=plt.figure(figsize=(16,4))
            ax1 = fig.add_subplot(1, 2, 1)
            s.plot_spectrum(ax=ax1,force_lines=True,label=label)
            ax2 = fig.add_subplot(1, 2, 2)
            s.plot_spectrogram(ax=ax2,scale="log")
            #plt.show()
    
        # fill collections
        all_lambdas.append(s.lambdas)
        all_data.append(s.data)
        all_data_err.append(s.err)
    
        if FLAG_ORDER2:
            all_lambdas_order2.append(s.lambdas_order2)
            all_data_order2.append(s.data_order2)
            all_data_err_order2.append(s.err_order2)
     
        # save info

        infos.append([idx,s.target.label,s.date_obs,s.airmass,s.temperature,s.pressure,s.humidity])
        
    except Exception as inst:
        print(" >>> Exception catched for "+ label )
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        
        
 

#Generate info


df_infos=pd.DataFrame(infos,columns=["idx","object","date_obs","airmass","temperature","pressure","humidity"])

df_infos.set_index('idx',inplace=True)


all_reftime=[ (Time(tt)-Time( df_infos["date_obs"].values[0])).to_value(u.hr) for tt in df_infos["date_obs"].values ]

all_reftime=np.array(all_reftime)

df_infos["reftime"]=all_reftime

NN = len(df_infos)


summary_file = f"summaryspectra_{DATE}-{filterdispersername}-{configmode}_b.csv"
df_infos.to_csv(summary_file)


# ## Main pickle file

#spec.image.target_pixcoords

header = spec.spectrum.header
print(header)



all_rebin=np.zeros(NN)
all_targetx=np.zeros(NN)
all_targety=np.zeros(NN)
all_rotangle=np.zeros(NN)
all_d2ccd=np.zeros(NN)
all_pixshift=np.zeros(NN)
all_chi2_fit=np.zeros(NN)
all_a2_fit=np.zeros(NN)
all_lbda_ref=np.zeros(NN)
all_tagnumber=np.zeros(NN)
all_errors=np.zeros(NN)


for idx in range(NN):
    
    header = all_spec[idx].spectrum.header
    tagnum=str(all_num[idx])
    
    #ROTANGLE=  -0.1367006901184345 / [deg] angle of the dispersion axis             
    #D2CCD   =    179.6778868175837 / [mm] distance between disperser and CCD        
    #TARGETX =    315.9547462941386 / target position on X axis                      
    #TARGETY =    75.06785960446246 / target position on Y axis                      
    #LBDA_REF=    634.9155139280113                                                  
    #PIXSHIFT=  -0.9996981508176748                                                  
    #CHI2_FIT=    1.602115867259752                                                  
    #A2_FIT  =                  1.0                                                  
    #REBIN   =                    2 / original image rebinning factor to get spectrum
    
    try :
        rebin=header["REBIN"]
    except KeyError as e:
        rebin=2
        print(f"KeyError exception for spec {idx} : " + str(e) + f" ! ==> force rebin = {rebin}")
        all_errors[idx]=1
       
        
        
    targetx=header["TARGETX"]*rebin
    targety=header["TARGETY"]*rebin
    rotangle=header["ROTANGLE"]
    d2ccd=header["D2CCD"]
    pixshift=header["PIXSHIFT"]
    
    if header.get("CHI2_FIT") != None:
        chi2_fit=header["CHI2_FIT"]
    else:
        print("Missing CHI2_FIT")
        chi2_fit= -1
        
    if header.get("A2_FIT") != None:
        a2_fit=header["A2_FIT"]
        
    else:
        a2_fit=-1
        print("Missing A2_FIT")
    
    
    if header.get("LBDA_REF") != None:
        lbda_ref=header["LBDA_REF"]
    else:
        lbda_ref=-1
        print("LBDA_REF")
    
    
    all_rebin[idx]=rebin
    all_targetx[idx]=targetx
    all_targety[idx]=targety
    all_rotangle[idx]=rotangle
    all_d2ccd[idx]=d2ccd
    all_pixshift[idx]=pixshift
    
    
    all_chi2_fit[idx]=chi2_fit
    all_a2_fit[idx]=a2_fit
    all_lbda_ref[idx]=lbda_ref
    all_tagnumber[idx]=tagnum
    


# ## Write pickle file

all_out_data = {}

for idx in range(NN):
    if FLAG_ORDER2:
        thedata = {'number':all_tagnumber[idx],
               'object':df_infos.iloc[idx]['object'],
               'dateobs':df_infos.iloc[idx]['date_obs'],
               'refhour':df_infos.iloc[idx]['reftime'],
               'airmass':df_infos.iloc[idx]['airmass'], 
               'pressure':df_infos.iloc[idx]['pressure'], 
               'temperature':df_infos.iloc[idx]['temperature'], 
               'humidity':df_infos.iloc[idx]['humidity'], 
               'targetx_pix':all_targetx[idx],
               'targety_pix':all_targety[idx],
               'rotangle':all_rotangle[idx],
               'd2ccd':all_d2ccd[idx],
               'error':all_errors[idx],   
               'all_lambdas':all_lambdas[idx],
               'all_fluxes':all_data[idx],
               'all_fluxes_err':all_data_err[idx],
               'all_lambdas_order2':all_lambdas_order2[idx],
               'all_fluxes_order2':all_data_order2[idx],
               'all_fluxes_err_order2':all_data_err_order2[idx],
              }
    else:
        thedata = {'number':all_tagnumber[idx],
               'object':df_infos.iloc[idx]['object'],
               'dateobs':df_infos.iloc[idx]['date_obs'],
               'refhour':df_infos.iloc[idx]['reftime'],
               'airmass':df_infos.iloc[idx]['airmass'],
               'pressure':df_infos.iloc[idx]['pressure'], 
               'temperature':df_infos.iloc[idx]['temperature'], 
               'humidity':df_infos.iloc[idx]['humidity'], 
               'targetx_pix':all_targetx[idx],
               'targety_pix':all_targety[idx],
               'rotangle':all_rotangle[idx],
               'd2ccd':all_d2ccd[idx],
               'error':all_errors[idx],   
               'all_lambdas':all_lambdas[idx],
               'all_fluxes':all_data[idx],
               'all_fluxes_err':all_data_err[idx],
            }         
            
    all_out_data[all_exposures[idx]]=thedata


pkl_outfilename=f'run-auxtel-holo-{DATE}-{filterdispersername}-{configmode}.pickle'

with open(pkl_outfilename, 'wb') as pickle_file:
    pickle.dump(all_out_data,pickle_file)


pkl_infilename=pkl_outfilename


with open(pkl_infilename, 'rb') as pickle_file:
    content = pickle.load(pickle_file)


# Get first value of dictionary
print(next(iter(content.items())))






