# libAtmosphericFit
#
# Author          : Sylvie Dagoret-Campagne
# Affiliaton      : IJCLab/IN2P3/CNRS
# Creation Date   : 2023/07/29
# Last update     : 2023/08/03 
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
    def __init__(self,Nobs,airmasses_list = []):
        print("Init FitThroughputandAtmosphericParamsCov")
        Nobs = Nobs
        airmasses_list = airmasses_list

        
    #######################################################    
    # Static methods defining the model of fluxes    
    # function that calculate y = f(x)
    ######################################################
    @staticmethod
    def func_model_greypwvo3(x, *params):
      """
      Evaluate the flux
  
      Parameters 
         x : the abscisse , ie the wavelength array
         params : array of parameters to fit (amplitude, pwv, ozone)

          Required global variables for the model
          g_airmass :airmass
          g_sedxthroughput : the throughput time SED

      Return
        the array of fluxes

      """

      global emul
  
      #alpha,pwv,oz = params    
      alpha,pwv,oz = params[0],params[1],params[2]
   
      wl = x
      the_sedxthroughput = g_sedxthroughput
      airmass = g_airmass
  
      fl = alpha*emul.GetAllTransparencies(wl ,airmass,pwv,oz,ncomp=0,flagAerosols=False)
      fl *= the_sedxthroughput
      return fl
    
    @staticmethod
    def func_model_greypwv(x, *params):
      """
        Evaluate the flux
        Parameters 
           x : the abscisse , ie the wavelength array
          params : array of parameters to fit (amplitude, pwv)

        Required global variables
          g_airmass : the airmass
           g_sedxthroughput : the sed time throughput

        Return
          the array of fluxes
      """

      global emul
    
      #alpha,pwv = params
      alpha=params[0]
      pwv=params[1]   
      oz=300. 
    
      wl = x
      the_sedxthroughput = g_sedxthroughput
      airmass = g_airmass
      fl = alpha*emul.GetAllTransparencies(wl ,airmass,pwv,oz,ncomp=0,flagAerosols=False)
      fl *= the_sedxthroughput
      return fl
  

    def fit_greypwvo3(self,params0,xdata,ydata,covdata,airmass,sedxthroughput):
        """
        Fit a grey term, precipitable water varpor and ozone.
        It provides the covariance matrix (not the error vector)

        """
        # first pass the global parameters to the func_model_grewpwvo3 function
        global g_airmass 
        g_airmass = airmass
        global g_sedxthroughput 
        g_sedxthroughput = sedxthroughput
 
        #res_fit = curve_fit(func_model_greypwvo3, xdata=xdata, ydata=ydata, p0=params0,sigma = covdata,bounds=([0.1,0.001,50.],[2,9.5,550.]), full_output=True) 
    
        # FOR CLOUDY nights
        res_fit = curve_fit(FitAtmosphericParamsCov.func_model_greypwvo3, xdata=xdata, ydata=ydata, p0=params0,sigma = covdata,bounds=([0.005,0.001,50.],[50,9.5,550.]), full_output=True) 
    
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
        
        #another method to calculate residuals
        pred = FitAtmosphericParamsCov.func_model_greypwvo3(xdata,*popt)
        residuals = ydata-pred
        r=residuals
        chi2 = r.T @ np.linalg.inv(covdata) @ r
        ndf = len(residuals)-len(popt)
        chi2_per_ndf = chi2/ndf
      
        pwv_fit = popt[1]
        oz_fit = popt[2]
        alpha_fit = popt[0]
        
        pwve = sigmas[1]*np.sqrt(chi2_per_ndf)
        oze =sigmas[2]*np.sqrt(chi2_per_ndf)
        greye = sigmas[0]*np.sqrt(chi2_per_ndf)
        
        fit_dict = {"chi2":chi2,"ndeg":ndf,"chi2_per_deg":chi2_per_ndf,"popt":popt,"sigmas":sigmas,"pwv_fit":pwv_fit,"oz_fit":oz_fit,"grey_fit":alpha_fit,"pwve":pwve,"oze":oze,"greye":greye}

        return popt,sigmas,normresiduals,fit_dict
    
    def pred_greypwvo3(self,params,xdata,airmass,sedxthroughput):
        """
        Parameters
          params parameters of the fit , ie alpha, pwv,oz
          xdata : wavelength array
          airmass : airmass
          sedxthroughput : product of the SED by the throughput
          
        Return
          the flux array for the xdata array
        """
        # first pass the global parameters
        global g_airmass 
        g_airmass = airmass
        global g_sedxthroughput 
        g_sedxthroughput = sedxthroughput

        flux_model = FitAtmosphericParamsCov.func_model_greypwvo3(xdata,*params)
        return flux_model
    
    #--------
    
    def fit_greypwv(self,params0,xdata,ydata,covdata,airmass,sedxthroughput):
        """
        Fit a grey term, precipitable water varpor but No  ozone.
        This case applies when fittingg with the red filter.
        It is assumed an ozone value of 300 DB

        """
        # first pass the global parameters
        global g_airmass 
        g_airmass = airmass
        global g_sedxthroughput 
        g_sedxthroughput = sedxthroughput
            
        #res_fit = curve_fit(func_model_greypwv,  xdata=xdata, ydata=ydata, p0=params0,sigma = covdata,bounds=([0.1,0.001],[2,9.5]),full_output=True)
        
        # For Cloudy nights
        res_fit = curve_fit(FitAtmosphericParamsCov.func_model_greypwv,  xdata=xdata, ydata=ydata, p0=params0,sigma = covdata,bounds=([0.005,0.001],[50,9.5]),full_output=True)
        
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
        
        #another method to calculate residuals
        pred = FitAtmosphericParamsCov.func_model_greypwv(xdata,*popt)
        residuals = ydata-pred
        r=residuals
        chi2 = r.T @ np.linalg.inv(covdata) @ r
        ndf = len(residuals)-len(popt)
        chi2_per_ndf = chi2/ndf
      
        pwv_fit = popt[1]
        alpha_fit = popt[0]
        
        
        pwve = sigmas[1]*np.sqrt(chi2_per_ndf)
        greye = sigmas[0]*np.sqrt(chi2_per_ndf)
        
        fit_dict = {"chi2":chi2,"ndeg":ndf,"chi2_per_deg":chi2_per_ndf,"popt":popt,"sigmas":sigmas,"pwv_fit":pwv_fit,"grey_fit":alpha_fit,"pwve":pwve,"greye":greye}

        return popt,sigmas,normresiduals,fit_dict
        
        
    
    
    def pred_greypwv(self,params,xdata,airmass,sedxthroughput):
        """
        """

        # first pass the global parameters
        global g_airmass 
        g_airmass = airmass
        global g_sedxthroughput 
        g_sedxthroughput = sedxthroughput


        flux_model = FitAtmosphericParamsCov.func_model_greypwv(xdata,*params)
        return flux_model
    
    
    #-------------------

    def fit_transmampwvozaer(self,params0,xdata,ydata):
        """
        Fit transmission

        """            
        res_fit = least_squares(FitAtmosphericParamsCov.func_residuals_tramampwvozaer, params0,bounds=([1.001,0.001,0.001,0,-3],[2.499,9.5,599,0.5,0]),args=[xdata,ydata])
        
        # results fo the fit
        popt= res_fit.x
        J = res_fit.jac
        pcov = np.linalg.inv(J.T.dot(J))
        sigmas = np.sqrt(np.diagonal(pcov))
        cost=res_fit.cost
        residuals = res_fit.fun
        chi2=np.sum(residuals**2)
        ndeg = J.shape[0]- popt.shape[0]
        chi2_per_deg = chi2/ndeg
        
        
        fit_dict = {"chi2":chi2,"ndeg":ndeg,"chi2_per_deg":chi2_per_deg,"popt":popt,"sigmas":sigmas}

        return res_fit,fit_dict
    
    
    def pred_transmampwvozaer(self,params,xdata):
        """
        """
        transm_model = transmpred_ampwvozaer(params,xdata)
        return transm_model
        
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