# libThroughputFit
#
# Author          : Sylvie Dagoret-Campagne
# Affiliaton      : IJCLab/IN2P3/CNRS
# Creation Date   : 2023/08/04
# Last update     : 2023/08/14 
#
# A python tool to fit quickly atmospheric transmission of Auxtel Spectra with scipy.optimize and
# using the atmospheric emulator atmosphtransmemullsst
# 
#
#
import os
import sys
from pathlib import Path

import atmosphtransmemullsst
from atmosphtransmemullsst.simpleatmospherictransparencyemulator import SimpleAtmEmulator

from scipy.optimize import curve_fit,least_squares
from scipy.interpolate import RegularGridInterpolator
from scipy import interpolate
import numpy as np
import pandas as pd

from sklearn.gaussian_process import GaussianProcessRegressor, kernels

import copy
from collections import OrderedDict

pd.options.display.max_columns = 10
#pd.set_printoptions(precision=6)
# Environment settings: 
pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('expand_frame_repr', True)

print("libThroughputFit.py :: Use atmosphtransmemullsst.__path__[0],'../data/simplegrid as the path to data")
data_path = os.path.join(atmosphtransmemullsst.__path__[0],'../data/simplegrid')
print(f"libThroughputFit.py :: data_path = {data_path}")

       
# The emulator as a global variable
emul = SimpleAtmEmulator(data_path)

#need those two global variables
g_airmass = 0
g_sedxthrouput = None


# Dictionnary of absorption band
Dict_Absbands = OrderedDict() 
Dict_Absbands["O3"] = (550.,650.,0)
Dict_Absbands["O2_1"] = (685.,695.,1)
Dict_Absbands["O2_2"] = (760.,770.,1)
Dict_Absbands["H2O_1"] = (715.,735.,2)
Dict_Absbands["H2O_2"] = (815.,835.,2)
Dict_Absbands["H2O_3"] = (925.,980.,2)
Absbands_Colors = ['yellow','cyan','green']



# ================    Functions for the atmospheric profile airmass, pwv, ozone, aerosols ========
def transmpred_ampwvozaer(params,*arg):
  """
    Model prediction y = f(x) where x is the array of wavelength and y the measured flux
    
    inputs:
      - params : the unknown atmospheric parameters to fit (am,pwv,oz,vaod,beta)
      - *args  : additionnal data provided to compute the model : 
                   1) the wavelength array, 
                  
      
    output:
      - the array of predicted air transmission  at each wavelength data point
      
  """
  global emul
  # decode parameters
  am,pwv,oz,vaod,beta = params   
  # decode the argument
  wl = arg[0]
  transm = emul.GetAllTransparencies(wl ,am,pwv,oz,ncomp=1,taus=[vaod],betas=[beta],flagAerosols=True)
  return transm

##########################################################################################################################
class Throughput:
    """
      Class for throughput
    """
    def __init__(self, path) :
            filtyp = path.split(".")[-1]
            if filtyp == "txt":
              array = np.loadtxt(path)
              x = array[:,0]
              y = array[:,1]
              ey = 0
            else:
              dfin = pd.read_csv(path,index_col=0)
          
              x = dfin["wavelength"].values
              y = dfin["newthrou"].values
              ey = dfin["newthrouerr"].values

              self.wl = x
              self.th = y
              self.eth = ey
              self.totaln = len(x)

    def printinfo(self):
            """
            print information ion the throughput
            """
            print(f"Throughputinfo : {self.__class__.__name__}")
            print(f"Total number of points {self.totaln}")
            print("\t wl  = ",self.wl[:5])
            print("\t th  = ",self.th[:5])
            print("\t eth = ",self.eth[:5])

    def countnumberofparams(self):
            """
            """
            return 0
    

    def fitthrouputwithgp(self,x):
            """
            Do the throuput points interpolation doing a Gaussian Process fit
            
            x : input wavelength
            """
            X = self.wl 
            Y = self.th 
            EY = self.eth

            EYmax = np.max(EY)*10.
         
            # Initialise gaussian process with a kernel RBF
            kernel = kernels.RBF(0.5, (20, 150.0))
            gp = GaussianProcessRegressor(kernel=kernel, alpha=(EY)** 2 ,random_state=0)

            # fit the throughput curve with the gaussian process (interpolation at the required points)
            gp.fit(X[:, None], Y)
            f, f_err = gp.predict(x[:, None], return_std=True)
            return f,f_err

################################################################################################################################

class ThrouputCut(Throughput):
   
    def __init__(self,path,absband_list) :
          """
          Remove points in the absband_list
          """
          super().__init__(path)
   
          self.absband_list = absband_list
          self.bandindexes_list = np.array([],dtype=int)
          self.removedbands = OrderedDict()
   
          if self.absband_list is not None:
              for item in Dict_Absbands.items():
                  
                  key = item[0]
                  val = item[1]
                  idx_abscolor = val[2]
                  the_xmin = val[0]
                  the_xmax = val[1]

                 
                  # Check if this absband is activated 
                  if key in self.absband_list:
                      indexes_to_remove = np.where(np.logical_and(self.wl>=the_xmin,self.wl<=the_xmax))[0]
                      self.bandindexes_list = np.union1d(self.bandindexes_list,indexes_to_remove)
                      points_list = OrderedDict()
                      points_list["wl"] = self.wl[indexes_to_remove]
                      points_list["th"] = self.th[indexes_to_remove]
                      points_list["eth"] = self.eth[indexes_to_remove]
                      self.removedbands[key] =  points_list

              self.bandindexes_list = np.sort(self.bandindexes_list)
              # remove all points from each band
              self.wl = np.delete(self.wl,self.bandindexes_list )
              self.th = np.delete(self.th,self.bandindexes_list )
              self.eth = np.delete(self.eth,self.bandindexes_list )

    
    
    def printinfo(self):
            """
            print information ion the throughput
            """
            print(f"Throughputinfo : {self.__class__.__name__}")
            super().printinfo()


    def countnumberofparams(self):
            """
            """
            return 0
    

    def fitthrouputwithgp(self,x):
            """
            Do the throuput points interpolation doing a Gaussian Process fit
            
            x : input wavelength
            """
            X = self.wl 
            Y = self.th 
            EY = self.eth

            EYmax = np.max(EY)*10.
         
            # Initialise gaussian process with a kernel RBF
            kernel = kernels.RBF(0.5, (20, 150.0))
            gp = GaussianProcessRegressor(kernel=kernel, alpha=(EY)** 2 ,random_state=0)

            # fit the throughput curve with the gaussian process (interpolation at the required points)
            gp.fit(X[:, None], Y)
            f, f_err = gp.predict(x[:, None], return_std=True)
            return f,f_err



################################################################################################################################


class ThrouputAddPointsReso(ThrouputCut):
   
    def __init__(self,path,absband_list,reso=10.0) :
          super().__init__(path,absband_list)

          # list of throughput points that can be recalculated
          self.pointsinbands = OrderedDict()
   
          for item in self.removedbands.items():         
              key = item[0]
              val = item[1]

              xx = val["wl"]
              yy = val["th"]
            
              xmin = xx[0]
              xmax = xx[-1]
              xcenter = (xmin+xmax)/2.

              xright = np.arange(xcenter,xmax,reso)
              xleft = np.arange(-xcenter,-xmin,reso)
              xleft = -xleft
              xleft = xleft[:-1]
              
              xpoints = np.union1d(xleft,xright)
              ypoints = np.interp(xpoints,xx,yy)
              points_list = {}
              points_list["wl"] = xpoints
              points_list["th"] = ypoints
              self.pointsinbands[key] = points_list

    def countnumberofparams(self):
            """
            compute the number of parameters
            """
            countparams = 0
            for item in self.pointsinbands.items():
              key = item[0]
              val = item[1]
              xx = val["wl"]
              yy = val["th"]
              countparams += len(xx)
            return countparams
    
    def printinfo(self):
            """
            print information in the throughput
            """
            super().printinfo()
            print(f"Throughputinfo : {self.__class__.__name__}")
            nparams = self.countnumberofparams()
            print(f"\t number of points in bands = {nparams}")
            for item in self.pointsinbands.items():
                key = item[0]
                val = item[1]
                npts = len(val["th"])
               
                print(f"\t {key} , npts = {npts}")

            
################################################################################################################################

class ThrouputAddPointsN(ThrouputCut):
   
    def __init__(self,path,absband_list,npoints_list) :
          super().__init__(path,absband_list)

          # number of points per band
          self.dict_npoints = OrderedDict(zip(absband_list, npoints_list))

        
           # list of throughput points that can be recalculated
          self.pointsinbands = OrderedDict()
   
          for item in self.removedbands.items():
              
              key = item[0]
              val = item[1]

              xx = val["wl"]
              yy = val["th"]
            
              xmin = xx[0]
              xmax = xx[-1]
              npts = self.dict_npoints[key]
              nintervals = npts+1
              reso = (xmax-xmin)/nintervals
              
              xpoints = np.linspace(xmin+reso,xmax-reso,npts)
              ypoints = np.interp(xpoints,xx,yy)
              points_list = {}
              points_list["wl"] = xpoints
              points_list["th"] = ypoints
              self.pointsinbands[key] = points_list

   
    def countnumberofparams(self):
            """
            compute the number of parameters
            """
            countparams = 0
            for item in self.pointsinbands.items():
              key = item[0]
              val = item[1]
              xx = val["wl"]
              yy = val["th"]
              countparams += len(xx)
            return countparams
    
    def printinfo(self):
            """
            print information in the throughput
            """
            super().printinfo()
            print(f"Throughputinfo : {self.__class__.__name__}")
            nparams = self.countnumberofparams()
            print(f"\t number of points in bands = {nparams}")
            for item in self.pointsinbands.items():
                key = item[0]
                val = item[1]
                npts = len(val["th"])
               
                print(f"\t {key} , npts = {npts}")


################################################################################################################################

class ThrouputParamsAddPointsN(ThrouputAddPointsN):

      
    def __init__(self,path,absband_list,npoints_list) :
          super().__init__(path,absband_list,npoints_list)

          # we have a dict of scales  
          self.throughputscale = OrderedDict()

          # set the relative throuput scale for added points
          for item in self.pointsinbands.items():
              key = item[0]
              val = item[1]
              npts = len(val["th"])
              self.throughputscale[key] = np.ones(npts)

          # new points in band are original ones  
          self.newpointsinbands = self.pointsinbands.copy()

    def getparamsnames(self):
        """
        Retrun the array of throughput params names
        """
        paramsnames = []
        for item in self.pointsinbands.items():
              key = item[0]
              val = item[1]
              npts = len(val["th"])
              indexes = np.arange(npts)
              for index in indexes:
                  paramsnames.append(f"thr{key}_{index}")
        paramsnames = np.array(paramsnames)
        return paramsnames
                  
        
    
    def countnumberofparams(self):
            """
            compute the number of parameters
            """
            countparams = 0
            for item in self.newpointsinbands.items():
                key = item[0]
                val = item[1]
                xx = val["wl"]
                yy = val["th"]
                countparams += len(xx)
            return countparams
    
    def printinfo(self):
            """
            print information on the object
            """
            super().printinfo()
            print(f"Throughputinfo : {self.__class__.__name__}")
            nparams = self.countnumberofparams()
            print(f"\t number of params = {nparams}")
            for item in self.pointsinbands.items():
                key = item[0]
                val = item[1]
                npts = len(val["th"])
                scales = self.throughputscale[key]
                print(f"\t {key} , npts = {npts}, scale parameters = ", scales)
            print("\t \t - original points values : ", self.pointsinbands)
            print("\t \t - new points values : ", self.newpointsinbands)


    def setnewscales(self,dict_new_scale):
            """
            When new setnewscales is called, the new points are updated
            The scale is the factor by which the throuput should be multiplied
            """
            # loop on new points that must be updated
            for item in self.newpointsinbands.items():
                key = item[0] # retrieve the key
                val = item[1] # retrive the previous values that must be updated
                xx = copy.deepcopy(val["wl"])
                yy = copy.deepcopy(val["th"])
                self.throughputscale[key] = dict_new_scale[key]  # keep track of the new scale values
                yynew = copy.deepcopy(self.pointsinbands[key]["th"]) * dict_new_scale[key]
               
                self.newpointsinbands[key] = {"wl":xx,"th":yynew} # update the new throughout values
                #print("\t setnewscales() ::",key," scale:",dict_new_scale[key]," old=", self.pointsinbands[key]["th"]," new=" ,yynew)

            #print("\t setnewscales() ::" ,"old = ",self.pointsinbands)
            #print("\t setnewscales() ::" ,"new = ",self.newpointsinbands)
          

    def setuniscales(self):
            """
            set scale factor to 1 for initialisation
            """
            unitparams = np.array([])
            unitparamsdict = {}  # newscales = { "O3": [0.95,1.05,1.01],"O2_2": [1.05],"H2O_2": [0.97],"H2O_3": [1.1,1.2, 0.9, 0.8 ]}
            for item in self.newpointsinbands.items():
                key = item[0] # retrieve the key
                val = item[1] # retrive the previous values that must be updated
                xx = copy.deepcopy(val["wl"])
                yy = copy.deepcopy(val["th"])
                nn = len(yy)
                scalearray = np.full(nn,1)
                self.throughputscale[key] = scalearray   # keep track of the new scale values
                yynew = copy.deepcopy(self.pointsinbands[key]["th"]) * scalearray
                self.newpointsinbands[key] = {"wl":xx,"th":yynew} # update the new throughout values
                unitparams = np.append(unitparams,scalearray)
                unitparamsdict[key] = scalearray 
                #print("\t setuniscales() ::",key," scale:",scalearray," old=", self.pointsinbands[key]["th"]," new=" ,yynew)
            #print("\t setnewscales() ::" ,"old = ",self.pointsinbands)
            #print("\t setnewscales() ::" ,"new = ",self.newpointsinbands)
            return unitparams,unitparamsdict


    def fitthrouputwithgp(self,x):
            """
            Do the throuput points interpolation doing a Gaussian Process fit
            
            x : input wavelength
            """
            X = self.wl 
            Y = self.th 
            EY = self.eth

            EYmax = np.max(EY)*10.
         
            for item in self.newpointsinbands.items():
                key = item[0]
                val = item[1]
                xx = val["wl"]
                yy = val["th"]
                eyy = np.full(len(yy),EYmax)
                X = np.append(X,xx)
                Y = np.append(Y,yy)
                EY = np.append(EY,eyy)

            indexes_sorted = np.argsort(X)
            X = X[indexes_sorted]
            Y = Y[indexes_sorted]
            EY = EY[indexes_sorted]

            # Initialise gaussian process with a kernel RBF
            kernel = kernels.RBF(0.5, (20, 150.0))
            gp = GaussianProcessRegressor(kernel=kernel, alpha=(EY)** 2 ,random_state=0)

            # fit the throughput curve with the gaussian process (interpolation at the required points)
            gp.fit(X[:, None], Y)
            f, f_err = gp.predict(x[:, None], return_std=True)
            return f,f_err

        
################################################################################################################################          
        


########################## Fitting class with curve_fit method ###################################################### 
# scipy.optimize.curve_fit(f, xdata, ydata, p0=None, sigma=None, 
# absolute_sigma=False, check_finite=True, bounds=(-inf, inf), method=None, jac=None, *, full_output=False, **kwargs)
######################################################################################################################
class FitThroughputandAtmosphericParamsCov:
    """
    Class to handle a buch of different methods for fitting
    This class mainly uses curve_fit method of scipy.optimize

    """
    def __init__(self,sed_wl,sed_fl,throughput,wlmin,wlmax) :
        print("Init FitThroughputandAtmosphericParamsCov")
        
        # wl
        self.wlmin = wlmin
        self.wlmax = wlmax

        # SED
        self.sed_wl = sed_wl
        self.sed_fl = sed_fl
        self.f_sed = interpolate.interp1d(sed_wl,sed_fl,bounds_error=False,fill_value="extrapolate")


        # Throughput model
        self.th = throughput
        self.npts_th = self.th.countnumberofparams()
        self.params_th = np.ones(self.npts_th)

        # atmospheric parameters
        self.grey0 = 0
        self.pwv0 = 4.0
        self.oz0 = 300.
        self.aer0 = 0.
        self.tau0 = 0.
        self.beta0 = 1.

        self.greymin = 0
        self.pwvmin = 0.0
        self.ozmin = 100
        self.aermin = 0.
        self.taumin = 0.
        self.betamin = 0.001

        self.greymax = 1.
        self.pwvmax = 10.
        self.ozmax = 500
        self.aermax = 0.3
        self.taumax = 0.3
        self.betamax = 3.8
        
        #init only
        self.nobs = 0
        self.nparams =  self.npts_th


        self.params0 = np.empty(self.nparams)
        
        # number of calls for fitting
        self.nfitcalls = 0
        self.dfparams = None

    
    def printinfo(self):  
       
        print(f"FitThroughputandAtmosphericParamsCov : {self.__class__.__name__}")

         
         
    @staticmethod
    def flattendatacurve(X,Y,Z,ninfo,wlmin,wlmax):
        """
        Decode the 2D data to flatten them
        Keep the data in the appropriate wavelength range
        """
        am = X[:,2]   # airmasses
        nwl = X[:,3].astype(int)  #number of wl points 
        nwlsel = np.zeros(len(am),dtype=int)
        nspec = X.shape[0]
    
        for idx in range (nspec):
           
            x = X[idx,ninfo:nwl[idx]+ninfo]
            y = Y[idx,:nwl[idx]]
            z = Z[idx,:nwl[idx]]

            indexes_sel = np.where(np.logical_and(x>wlmin,x<wlmax))[0]
            x = x[indexes_sel]
            y = y[indexes_sel]
            z = z[indexes_sel]

            if idx == 0:
                xx = x
                yy = y
                zz = z
            else:
                xx = np.append(xx,x)
                yy = np.append(yy,y)
                zz = np.append(zz,z)

            nwlsel[idx] = len(x)
        
        return xx,yy,zz,am,nwlsel
    
    def computetheseds(self):
        """
        Compute the 1D array for the SED
        """
        nobs = self.nobs
        count = 0
        for iobs in range(nobs):
            npts_obs = self.npts[iobs]
            wl = self.wl[count:count+npts_obs]
            
            if iobs == 0:
                all_sed = self.f_sed(wl)
            else:
                all_sed = np.append(all_sed, self.f_sed(wl ) ) 
        return all_sed
    
    def computethethroughputs(self,newscales):
        """
        Compute the 1D array for the throughput
        """
        #define the new scales for variables points in throughputs
        self.th.setnewscales(newscales)

      
        nobs = self.nobs
        count = 0
        # fit gaussian process on each obs (on a given set of wavelength)
        for iobs in range(nobs):
            npts_obs = self.npts[iobs]
            wl = self.wl[count:count+npts_obs]
            y_th,ey_th = self.th.fitthrouputwithgp(wl)
            #buildup the 1D array of throuputs for all observation
            if iobs == 0:
                all_th = y_th
            else:
                all_th = np.append(all_th, y_th ) 
        return all_th
    

    def computeatmosphere(self,*atmparams):
        """
        Compute the atmospheric attenuation from the atmospheric parameters
        """

        # decode atmospheric parameters
        pwv  = atmparams[0]
        oz   = atmparams[1]
        vaod = atmparams[2]
        beta = atmparams[3]
        greyod = atmparams[4:]


        
        count = 0
        for iobs in range(self.nobs):

            npts_obs = self.npts[iobs]
            wl = self.wl[count:count+npts_obs]
            am = self.airmasses[iobs]


            transm = emul.GetAllTransparencies(wl ,am,pwv,oz,ncomp=1,taus=[vaod],betas=[beta],flagAerosols=True)
            transm_att = np.exp(-greyod[iobs]*am)*transm

           
            if iobs == 0:
                all_transm = transm_att
            else:
                all_transm = np.append(all_transm, transm_att ) 
        return all_transm

    def printparams(self,params):
        """
        Print parameters
        the traching of the parameter values is done in the self.dfparams pandas dataframe
        """
        colname = f'call{self.nfitcalls}'  
        #if self.dfparams == None:        
        #    self.dfparams = pd.DataFrame(params,index = self.params_names,columns=[colname])
        #else:
        #    self.dfparams[colname] = params
        
        self.dfparams[colname] = params
            
        with pd.option_context('display.float_format', '{:,.6f}'.format):
            print(self.dfparams)
            
        
            
            
        
        
    def fitparamsandthroughputfunc(self,x,*params):
        """
        Function  for fitting the model using curve_fit

        - x is the array of wavelengths for all observation 
        - params is the array of parameters to fit
               pwv  = params[0]
               oz   = params[1]
               vaod = params[2]
               beta = params[3]
               greyod = params[4:self.nobs+4]
               params[self.nobs+4:] throughput parameters
               newscales = { "O3": [1.0,1.0,1.0],"O2_2": [1.0],"H2O_2": [1.0],"H2O_3": [1.,1.,1.,1. ]}

        """

        #decode parameters
        self.nfitcalls += 1
        
        if self.nfitcalls % 10 == 0:
            #print(f"fitparamsandthroughputfunc:: ncoalls = {self.nfitcalls} decode params",*params)
            self.printparams(params)

        #atmospheric parameters
        pwv  = params[0]
        oz   = params[1]
        vaod = params[2]
        beta = params[3]
        greyods = params[4:self.nobs+4]
        atmparams = np.zeros(self.nobs+4)
        atmparams[0] = pwv
        atmparams[1] = oz
        atmparams[2] = vaod
        atmparams[3] = beta
        atmparams[4:] = greyods

        #print("decoded atmparams",atmparams)


        #
        thparams = params[self.nobs+4:]
        
        # build the throughput new scales
        newscaledict = OrderedDict()
        ipointer = 0
        # loop on points in bands
        for item in self.th.pointsinbands.items():
              key = item[0]
              val = item[1]
              xx = val["wl"]
              yy = val["th"]
              npts = len(xx)
              newscaledict[key] = thparams[ipointer:ipointer+npts]
              ipointer += npts
        
        
        # compute the new throughput
        self.all_throughputs = self.computethethroughputs(newscaledict)

        # compute the atmosphere
        self.all_atmtransm = self.computeatmosphere(*atmparams)

        # compute the predicted fluxes
        self.all_specmodel =  self.all_seds * self.all_throughputs * self.all_atmtransm 

        return  self.all_specmodel

             

        




    def fitmultievent_greypwvo3aer(self , X,Y,EY,ninfo):
        """
        Do the fit by calling curve_fit
            provide the data 
            X
            Y
            EY
            ninfo

        """

        # first flatten the data before the fit
        X,Y,EY,am,npts = FitThroughputandAtmosphericParamsCov.flattendatacurve(X,Y,EY,ninfo,self.wlmin,self.wlmax)

        self.wl        = X         # 1D wavelength array for all observations 
        self.fl        = Y         # 1D fluxarray for all observations 
        self.efl       = EY       # 1D error on flux array for all observations
        self.airmasses = am # 1D array of airmass for all observations
        self.npts      = npts    # 1D array of the number of wl/flux points for each observation
        self.nobs      = len(am)

        self.nparams = self.nobs + self.npts_th
        self.params_th = np.ones(self.npts_th)

       
        # few checks of data consistency
        assert self.npts.sum()    == self.wl.shape[0] 
        assert self.wl.shape[0]   == self.fl.shape[0] 
        assert self.efl.shape[0]  == self.fl.shape[0] 
        assert self.airmasses.shape[0]  == self.npts.shape[0]


         # initial parameters 
         
         #atmospheric parameters (libradtran params and aerosols)
        params_atm0 = np.array([self.pwv0,self.oz0,self.aer0,self.beta0])
        params_atm_names = np.array(["pwv","oz","tau","beta"])
        
        #grey attenuations
        params_greyatts0 = np.full(self.nobs,self.grey0)
        params_greyatts_names = np.array([f"grey_{idx}" for idx in range(self.nobs)])
        
        #throughput attenuation
        params_throughput0 = self.params_th
        params_throughput_names = self.th.getparamsnames()
        
        self.params0 = np.concatenate((params_atm0,params_greyatts0, params_throughput0))
        self.params_names = np.concatenate((params_atm_names,params_greyatts_names, params_throughput_names))

        params_atmmin = np.array([self.pwvmin,self.ozmin,self.aermin,self.betamin])
        params_grerattsmin = np.full(self.nobs,self.greymin)
        params_throughputmin = np.full(self.npts_th,0.8)
        
        paramsmin = np.concatenate((params_atmmin,params_grerattsmin,  params_throughputmin ))

        params_atmmax = np.array([self.pwvmax,self.ozmax,self.aermax,self.betamax])
        params_grerattsmax = np.full(self.nobs,self.greymax)
        params_throughputmax = np.full(self.npts_th,1.2)
    
        paramsmax= np.concatenate((params_atmmax,params_grerattsmax,  params_throughputmax ))

        #parameters bounds
        self.paramsbounds = (paramsmin,paramsmax)

        

        # Compute SED
        self.all_seds = self.computetheseds()

        # Compute the throughputs

        #set the throughput parameters to fit
        throughput_param_arr, throughput_param_dict = self.th.setuniscales()
        
        self.all_throughputs0 = self.computethethroughputs(throughput_param_dict)


        # compute the atmospheric transmission
        atmparams = np.zeros((self.nobs+4))

        ## set parameters
        atmparams[0] = self.pwv0
        atmparams[1] = self.oz0
        atmparams[2] = self.tau0
        atmparams[3] = self.beta0
        atmparams[4:] = np.full((self.nobs), self.grey0)

        atmparams[6] = 0.1
        atmparams[8] = 0.2
        atmparams[10] = 0.5

        self.all_atmtransm0 = self.computeatmosphere(*atmparams)


        self.all_specmodel0 =  self.all_seds * self.all_throughputs0 * self.all_atmtransm0 
        # compute relative residuals
        self.all_residuals0 =  (self.fl - self.all_specmodel0)/self.efl

        params0 = np.concatenate((atmparams,throughput_param_arr))

        #scipy.optimize.curve_fit(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False, 
        #check_finite=None, bounds=(-inf, inf), method=None, jac=None, *, full_output=False, nan_policy=None, **kwargs)
        
        # before doing the fit reset the number of call fit counter and create the parameter tracking dataframe
        self.nfitcalls = 0
        self.dfparams = pd.DataFrame(index=self.params_names)
        res_fit = curve_fit(self.fitparamsandthroughputfunc,X,Y,p0=params0,sigma=EY,bounds=self.paramsbounds,full_output=True)

        popt = res_fit[0]
        pcov = res_fit[1]
        cf_dict = res_fit[2]
    
        # compute the errors on fitted parameters
        sigmas = np.sqrt(np.diagonal(pcov))
        # compute the normalized residuals  
        normresiduals=cf_dict['fvec']
        # compute the chi2 from the 
        chi2= np.sum(normresiduals**2)
        ndf = len(normresiduals)-len(popt)
        chi2_per_ndf = chi2/ndf
        


         # compute relative residuals
        self.all_residuals =  (self.fl - self.all_specmodel)/self.efl


        return popt,pcov,cf_dict,sigmas,normresiduals,chi2,ndf,chi2_per_ndf


################################################################################################################
#  FitAtmosphericParamsOnlyCov
################################################################################################################

class FitAtmosphericParamsOnlyCov:
    """
    Class to handle a buch of different methods for fitting
    This class mainly uses curve_fit method of scipy.optimize

    """
    def __init__(self,sed_wl,sed_fl,throughput,wlmin,wlmax) :
        """

        Thgroughput without parameters 
        """
        print("Init FitAtmosphericParamsOnlyCov")
        
        # wl
        self.wlmin = wlmin
        self.wlmax = wlmax

        # SED
        self.sed_wl = sed_wl
        self.sed_fl = sed_fl
        self.f_sed = interpolate.interp1d(sed_wl,sed_fl,bounds_error=False,fill_value="extrapolate")


        # Throughput model
        self.th = throughput
        self.npts_th = 0
        self.params_th = 0

        # atmospheric parameters
        self.grey0 = 0
        self.pwv0 = 4.0
        self.oz0 = 300.
        self.aer0 = 0.
        self.tau0 = 0.
        self.beta0 = 1.

        self.greymin = 0
        self.pwvmin = 0.0
        self.ozmin = 100
        self.aermin = 0.
        self.taumin = 0.
        self.betamin = 0.001

        self.greymax = 1.
        self.pwvmax = 10.
        self.ozmax = 500
        self.aermax = 0.3
        self.taumax = 0.3
        self.betamax = 3.8
        
        #init only
        self.nobs = 0
        self.nparams =  self.npts_th


        self.params0 = np.empty(self.nparams)
        
        # number of calls for fitting
        self.nfitcalls = 0
        self.dfparams = None

    
    def printinfo(self):  
       
        print(f"FitAtmosphericParamsOnlyCov : {self.__class__.__name__}")

         
         
    @staticmethod
    def flattendatacurve(X,Y,Z,ninfo,wlmin,wlmax):
        """
        Decode the 2D data to flatten them
        Keep the data in the appropriate wavelength range
        """
        am = X[:,2]   # airmasses
        nwl = X[:,3].astype(int)  #number of wl points 
        nwlsel = np.zeros(len(am),dtype=int)
        nspec = X.shape[0]
    
        for idx in range (nspec):
           
            x = X[idx,ninfo:nwl[idx]+ninfo]
            y = Y[idx,:nwl[idx]]
            z = Z[idx,:nwl[idx]]

            indexes_sel = np.where(np.logical_and(x>wlmin,x<wlmax))[0]
            x = x[indexes_sel]
            y = y[indexes_sel]
            z = z[indexes_sel]

            if idx == 0:
                xx = x
                yy = y
                zz = z
            else:
                xx = np.append(xx,x)
                yy = np.append(yy,y)
                zz = np.append(zz,z)

            nwlsel[idx] = len(x)
        
        return xx,yy,zz,am,nwlsel
    
    def computetheseds(self):
        """
        Compute the 1D array for the SED
        """
        nobs = self.nobs
        count = 0
        for iobs in range(nobs):
            npts_obs = self.npts[iobs]
            wl = self.wl[count:count+npts_obs]
            
            if iobs == 0:
                all_sed = self.f_sed(wl)
            else:
                all_sed = np.append(all_sed, self.f_sed(wl ) ) 
        return all_sed
    
    def computethethroughputs(self):
        """
        Compute the 1D array for the throughput
        """
        
      
        nobs = self.nobs
        count = 0
        # fit gaussian process on each obs (on a given set of wavelength)
        for iobs in range(nobs):
            npts_obs = self.npts[iobs]
            wl = self.wl[count:count+npts_obs]
            y_th,ey_th = self.th.fitthrouputwithgp(wl)
            #buildup the 1D array of throuputs for all observation
            if iobs == 0:
                all_th = y_th
            else:
                all_th = np.append(all_th, y_th ) 
        return all_th
    

    def computeatmosphere(self,*atmparams):
        """
        Compute the atmospheric attenuation from the atmospheric parameters
        """

        # decode atmospheric parameters
        pwv  = atmparams[0]
        oz   = atmparams[1]
        vaod = atmparams[2]
        beta = atmparams[3]
        greyod = atmparams[4:]


        
        count = 0
        for iobs in range(self.nobs):

            npts_obs = self.npts[iobs]
            wl = self.wl[count:count+npts_obs]
            am = self.airmasses[iobs]


            transm = emul.GetAllTransparencies(wl ,am,pwv,oz,ncomp=1,taus=[vaod],betas=[beta],flagAerosols=True)
            transm_att = np.exp(-greyod[iobs]*am)*transm

           
            if iobs == 0:
                all_transm = transm_att
            else:
                all_transm = np.append(all_transm, transm_att ) 
        return all_transm

    def printparams(self,params):
        """
        Print parameters
        the traching of the parameter values is done in the self.dfparams pandas dataframe
        """
        colname = f'call{self.nfitcalls}'  
        #if self.dfparams == None:        
        #    self.dfparams = pd.DataFrame(params,index = self.params_names,columns=[colname])
        #else:
        #    self.dfparams[colname] = params
        
        self.dfparams[colname] = params
            
        with pd.option_context('display.float_format', '{:,.6f}'.format):
            print(self.dfparams)
            
        
            
            
        
        
    def fitparamsfunc(self,x,*params):
        """
        Function  for fitting the model using curve_fit

        - x is the array of wavelengths for all observation 
        - params is the array of parameters to fit
               pwv  = params[0]
               oz   = params[1]
               vaod = params[2]
               beta = params[3]
               greyod = params[4:self.nobs+4]
               params[self.nobs+4:] throughput parameters
               newscales = { "O3": [1.0,1.0,1.0],"O2_2": [1.0],"H2O_2": [1.0],"H2O_3": [1.,1.,1.,1. ]}

        """

        #decode parameters
        self.nfitcalls += 1
        
        if self.nfitcalls % 10 == 0:
            #print(f"fitparamsfunc:: ncoalls = {self.nfitcalls} decode params",*params)
            self.printparams(params)

        #atmospheric parameters
        pwv  = params[0]
        oz   = params[1]
        vaod = params[2]
        beta = params[3]
        greyods = params[4:self.nobs+4]
        atmparams = np.zeros(self.nobs+4)
        atmparams[0] = pwv
        atmparams[1] = oz
        atmparams[2] = vaod
        atmparams[3] = beta
        atmparams[4:] = greyods

        #print("decoded atmparams",atmparams)


        
        
        # compute the new throughput
        self.all_throughputs = self.computethethroughputs()

        # compute the atmosphere
        self.all_atmtransm = self.computeatmosphere(*atmparams)

        # compute the predicted fluxes
        self.all_specmodel =  self.all_seds * self.all_throughputs * self.all_atmtransm 

        return  self.all_specmodel

             

        




    def fitmultievent_greypwvo3aer(self , X,Y,EY,ninfo):
        """
        Do the fit by calling curve_fit
            provide the data 
            X
            Y
            EY
            ninfo

        """

        # first flatten the data before the fit
        X,Y,EY,am,npts = FitAtmosphericParamsOnlyCov.flattendatacurve(X,Y,EY,ninfo,self.wlmin,self.wlmax)

        self.wl        = X         # 1D wavelength array for all observations 
        self.fl        = Y         # 1D fluxarray for all observations 
        self.efl       = EY       # 1D error on flux array for all observations
        self.airmasses = am # 1D array of airmass for all observations
        self.npts      = npts    # 1D array of the number of wl/flux points for each observation
        self.nobs      = len(am)

        self.nparams = self.nobs + self.npts_th
        self.params_th = np.ones(self.npts_th)

       
        # few checks of data consistency
        assert self.npts.sum()    == self.wl.shape[0] 
        assert self.wl.shape[0]   == self.fl.shape[0] 
        assert self.efl.shape[0]  == self.fl.shape[0] 
        assert self.airmasses.shape[0]  == self.npts.shape[0]


         # initial parameters 
         
         #atmospheric parameters (libradtran params and aerosols)
        params_atm0 = np.array([self.pwv0,self.oz0,self.aer0,self.beta0])
        params_atm_names = np.array(["pwv","oz","tau","beta"])
        
        #grey attenuations
        params_greyatts0 = np.full(self.nobs,self.grey0)
        params_greyatts_names = np.array([f"grey_{idx}" for idx in range(self.nobs)])
        
       
        
        self.params0 = np.concatenate((params_atm0,params_greyatts0))
        self.params_names = np.concatenate((params_atm_names,params_greyatts_names))

        params_atmmin = np.array([self.pwvmin,self.ozmin,self.aermin,self.betamin])
        params_grerattsmin = np.full(self.nobs,self.greymin)
       
        paramsmin = np.concatenate((params_atmmin,params_grerattsmin ))

        params_atmmax = np.array([self.pwvmax,self.ozmax,self.aermax,self.betamax])
        params_grerattsmax = np.full(self.nobs,self.greymax)
        
        paramsmax= np.concatenate((params_atmmax,params_grerattsmax ))

        #parameters bounds
        self.paramsbounds = (paramsmin,paramsmax)

        

        # Compute SED
        self.all_seds = self.computetheseds()

        # Compute the throughputs

        
        self.all_throughputs0 = self.computethethroughputs()


        # compute the atmospheric transmission
        atmparams = np.zeros((self.nobs+4))

        ## set parameters
        atmparams[0] = self.pwv0
        atmparams[1] = self.oz0
        atmparams[2] = self.tau0
        atmparams[3] = self.beta0
        atmparams[4:] = np.full((self.nobs), self.grey0)

        #atmparams[6] = 0.1
        #atmparams[8] = 0.2
        #atmparams[10] = 0.5

        self.all_atmtransm0 = self.computeatmosphere(*atmparams)


        self.all_specmodel0 =  self.all_seds * self.all_throughputs0 * self.all_atmtransm0 
        # compute relative residuals
        self.all_residuals0 =  (self.fl - self.all_specmodel0)/self.efl

        params0 = atmparams

        #scipy.optimize.curve_fit(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False, 
        #check_finite=None, bounds=(-inf, inf), method=None, jac=None, *, full_output=False, nan_policy=None, **kwargs)
        
        # before doing the fit reset the number of call fit counter and create the parameter tracking dataframe
        self.nfitcalls = 0
        self.dfparams = pd.DataFrame(index=self.params_names)
        res_fit = curve_fit(self.fitparamsfunc,X,Y,p0=params0,sigma=EY,bounds=self.paramsbounds,full_output=True)

        popt = res_fit[0]
        pcov = res_fit[1]
        cf_dict = res_fit[2]
    
        # compute the errors on fitted parameters
        sigmas = np.sqrt(np.diagonal(pcov))
        # compute the normalized residuals  
        normresiduals=cf_dict['fvec']
        # compute the chi2 from the 
        chi2= np.sum(normresiduals**2)
        ndf = len(normresiduals)-len(popt)
        chi2_per_ndf = chi2/ndf
        


         # compute relative residuals
        self.all_residuals =  (self.fl - self.all_specmodel)/self.efl


        return popt,pcov,cf_dict,sigmas,normresiduals,chi2,ndf,chi2_per_ndf

        
################################################################################################        

def main():
    print("============================================================")
    print("Simple Atmospheric emulator for Rubin-LSST observatory")
    print("============================================================")
    
    # retrieve the path of data
    path_data =  os.path.join(atmosphtransmemullsst.__path__[0],'../data/simplegrid')
    # create emulator  
    emul = SimpleAtmEmulator(path = path_data)
    wl = [400.,800.,900.]
    am=1.2
    pwv =4.0
    oz=300.
    transm = emul.GetAllTransparencies(wl,am,pwv,oz)
    print("wavelengths (nm) \t = ",wl)
    print("transmissions    \t = ",transm)


if __name__ == "__main__":
    main()