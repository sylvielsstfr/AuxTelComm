# libAtmosphericFit
#
# Author          : Sylvie Dagoret-Campagne
# Affiliaton      : IJCLab/IN2P3/CNRS
# Creation Date   : 2023/07/29
# Last update     : 2023/07/29 
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
import pickle




print("libAtmosphericFit.py :: Use atmosphtransmemullsst.__path__[0],'../data/simplegrid as the path to data")
data_path = os.path.join(atmosphtransmemullsst.__path__[0],'../data/simplegrid')
print(f"libAtmosphericFit.py :: data_path = {data_path}")

       
# The emulator as a global variable
emul = SimpleAtmEmulator(data_path)

#need those two global variables
g_airmass = 0
g_sedxthrouput = None



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












########################## Fitting class with curve_fit method ###################################################### 
# scipy.optimize.curve_fit(f, xdata, ydata, p0=None, sigma=None, 
# absolute_sigma=False, check_finite=True, bounds=(-inf, inf), method=None, jac=None, *, full_output=False, **kwargs)
######################################################################################################################
class FitAtmosphericParamsCov:
    """
    Class to handle a buch of different methods for fitting
    This class mainly uses curve_fit method of scipy.optimize

    """
    def __init__(self):
        print("Init FitAtmosphericParamsCov")
        
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