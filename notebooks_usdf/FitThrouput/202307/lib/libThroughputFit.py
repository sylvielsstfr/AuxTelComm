# libThroughputFit
#
# Author          : Sylvie Dagoret-Campagne
# Affiliaton      : IJCLab/IN2P3/CNRS
# Creation Date   : 2023/08/04
# Last update     : 2023/08/05 
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



print("libThroughputFit.py :: Use atmosphtransmemullsst.__path__[0],'../data/simplegrid as the path to data")
data_path = os.path.join(atmosphtransmemullsst.__path__[0],'../data/simplegrid')
print(f"libThroughputFit.py :: data_path = {data_path}")

       
# The emulator as a global variable
emul = SimpleAtmEmulator(data_path)

#need those two global variables
g_airmass = 0
g_sedxthrouput = None


# Dictionnary of absorption band
Dict_Absbands = {} 
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


class ThrouputCut(Throughput):
   
    def __init__(self,path,absband_list) :
          """
          Remove points in the absband_list
          """
          super().__init__(path)
   
          self.absband_list = absband_list
          self.bandindexes_list = np.array([],dtype=int)
          self.removedbands = {}
   
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
                      points_list = {}
                      points_list["wl"] = self.wl[indexes_to_remove]
                      points_list["th"] = self.th[indexes_to_remove]
                      points_list["eth"] = self.eth[indexes_to_remove]
                      self.removedbands[key] =  points_list

              self.bandindexes_list = np.sort(self.bandindexes_list)
              # remove all points from each band
              self.wl = np.delete(self.wl,self.bandindexes_list )
              self.th = np.delete(self.th,self.bandindexes_list )
              self.eth = np.delete(self.eth,self.bandindexes_list )


class ThrouputAddPointsReso(ThrouputCut):
   
    def __init__(self,path,absband_list,reso=10.0) :
          super().__init__(path,absband_list)

          # list of throughput points that can be recalculated
          self.pointsinbands = {}
   
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


class ThrouputAddPointsN(ThrouputCut):
   
    def __init__(self,path,absband_list,npoints_list) :
          super().__init__(path,absband_list)

          # number of points per band
          self.dict_npoints = dict(zip(absband_list, npoints_list))

        
           # list of throughput points that can be recalculated
          self.pointsinbands = {}
   
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

class ThrouputParamsAddPointsN(ThrouputAddPointsN):

      
    def __init__(self,path,absband_list,npoints_list) :
          super().__init__(path,absband_list,npoints_list)

          self.throughputscale = {} 

          # set the relative throuput scale for added points
          for item in self.pointsinbands.items():
              key = item[0]
              val = item[1]
              npts = len(val["th"])
              self.throughputscale[key] = np.ones(npts)

          self.newpointsinbands = self.pointsinbands.copy()

    def setnewscales(self,dict_new_scale):
          for item in self.newpointsinbands.items():
              key = item[0]
              val = item[1]
              xx = val["wl"]
              yy = val["th"]
              yynew = yy*dict_new_scale[key]
              val["th"] = yynew

    def fitthrouputwithgp(self,x):
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

          kernel = kernels.RBF(0.5, (20, 150.0))
          gp = GaussianProcessRegressor(kernel=kernel, alpha=(EY)** 2 ,random_state=0)


          gp.fit(X[:, None], Y)
          f, f_err = gp.predict(x[:, None], return_std=True)
          return f,f_err

        
          
        


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

        # atmospheric parameters
        self.grey0 = 0
        self.pwv0 = 4.0
        self.oz0 = 300.
        self.aer0 = 0.
        self.tau0 = 0.
        self.beta0 = 1.
        

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
        """
        nobs = len(self.airmasses)
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
        Compute throughput
        """
        
        self.th.setnewscales(newscales)

      
        nobs = len(self.airmasses)
        count = 0
        for iobs in range(nobs):
            npts_obs = self.npts[iobs]
            wl = self.wl[count:count+npts_obs]
            y_th,ey_th = self.th.fitthrouputwithgp(wl)

            if iobs == 0:
                all_th = y_th
            else:
                all_th = np.append(all_th, y_th ) 
        return all_th
    

    def computeatmosphere(self,*atmparams):
        """
        Compute atmospheric attenuation
        """

        # decode atmospheric parameters
        pwv  = atmparams[0]
        oz   = atmparams[1]
        vaod = atmparams[2]
        beta = atmparams[3]
        greyod = atmparams[4:]


        nobs = len(self.airmasses)
        count = 0
        for iobs in range(nobs):

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


        




    def fitmultievent_greypwvo3aer(self , X,Y,EY,ninfo):
        """
        Do the fit
        """

        # first flatten the data before the fit
        X,Y,EY,am,npts = FitThroughputandAtmosphericParamsCov.flattendatacurve(X,Y,EY,ninfo,self.wlmin,self.wlmax)

        self.wl        = X         # 1D wavelength array for all observations 
        self.fl        = Y         # 1D fluxarray for all observations 
        self.efl       = EY       # 1D error on flux array for all observations
        self.airmasses = am # 1D array of airmass for all observations
        self.npts      = npts    # 1D array of the number of wl/flux points for each observation
        self.nobs      = len(am)


        assert self.npts.sum()    == self.wl.shape[0] 
        assert self.wl.shape[0]   == self.fl.shape[0] 
        assert self.efl.shape[0]  == self.fl.shape[0] 
        assert self.airmasses.shape[0]  == self.npts.shape[0]

        # Compute SED
        self.all_seds = self.computetheseds()

        # Compute the throughputs

        #set the throughput parameters to fit
        newscales = { "O3": [1.0,1.0,1.0],"O2_2": [1.0],"H2O_2": [1.0],"H2O_3": [1.,1.,1.,1. ]}
        self.all_throughputs = self.computethethroughputs(newscales)


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

        self.all_atmtransm = self.computeatmosphere(*atmparams)

        self.all_specmodel =  self.all_seds * self.all_throughputs * self.all_atmtransm 



        



        popt = []
        pcov= []
        res= []
        myfit = []

        return popt,pcov,res,myfit


   
        
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