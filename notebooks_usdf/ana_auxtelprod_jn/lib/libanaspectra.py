import lsst.daf.butler as dafButler
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.colors as mcolors
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec

from getObsAtmo.getObsAtmo import ObsAtmo

# Spectra

def select_files(butler,collection, where):
    """
    Select all records according the where clause
    """
    # datasetRefs = registry.queryDatasets(datasetType='spectractorSpectrum', collections=my_collection, where=where)
    #records = list(butler.registry.queryDimensionRecords('exposure', where=where))
    records = list(butler.registry.queryDimensionRecords('exposure', datasets='spectractorSpectrum', where=where,  collections=collection))
    records = sorted(records, key=lambda x: x.id, reverse=False)
    return records

def filter_data(butler,collection,dateobs,records, sigma_clip=3,remove_withfilters = True, plot_flag = False):  # pragma: no cover
    """
    Spectrum reconstruction Quality Selection
    """
    from scipy.stats import median_abs_deviation
    D = []
    chi2 = []
    dx = []
    amplitude = []
    regs = []
    times = []
    specs = []
    alpha_0_2 = []
    #parameters.VERBOSE = False
    #parameters.DEBUG = False
    spec_flagfilter = []
    for i, r in enumerate(records):
        times.append(r.day_obs)
        spec = butler.get('spectractorSpectrum', visit=r.id, collections=collection, detector=0, instrument='LATISS')
        spec.dataId = r.id
        spec.physical_filter = r.physical_filter

        if spec.x0[0] > 500: 
            continue
            
        flag_filter = spec.physical_filter == 'empty~holo4_003'
        spec_flagfilter.append(flag_filter)
        
        D.append(spec.header["D2CCD"])
        dx.append(spec.header["PIXSHIFT"])
        regs.append(np.log10(spec.header["PSF_REG"]))
        # what is amplitude[300:]
        amplitude.append(np.sum(np.abs(spec.data[300:])))
        # if "CHI2_FIT" in header:
        chi2.append(spec.header["CHI2_FIT"])
        specs.append(spec)
        p = butler.get('spectrumForwardModelFitParameters', visit=r.id, collections=collection, detector=0, instrument='LATISS')
        alpha_0_2.append(p.values[p.get_index("alpha_0_2")])
        #except:
        #    new_file_names.remove(name)
        #    print(f"fail to open {name}. len(file_names)={len(new_file_names)}")
    params = {'D2CCD': np.array(D),
              'dx': np.array(dx),
              'regs': np.array(regs),
              'chi2': np.array(chi2),
              'amplitude': np.array(amplitude),
              'alpha_0_2': np.array(alpha_0_2)
             }
    k = np.arange(len(D))
    spec_flagfilter = np.array(spec_flagfilter)
    #spec_intfilter = np.array(list(map(lambda x: 1 if x else 0, spec_flagfilter)))
    
    # array of filters , one per file
    if remove_withfilters:     
        filter_indices = spec_flagfilter 
    else:
        filter_indices = np.ones_like(k, dtype=bool)    
    for par in params.keys():
        if par in ['amplitude']: #, 'alpha_0_2']:
            continue
        filter_indices *= np.logical_and(params[par] > np.median(params[par]) - sigma_clip * median_abs_deviation(params[par]),
                                         params[par] < np.median(params[par]) + sigma_clip * median_abs_deviation(params[par]))
    if  plot_flag:
        for par in params.keys():
            fig = plt.figure(figsize=(8,4))
            plt.plot(k, params[par])
            plt.plot(k[filter_indices], params[par][filter_indices], "ko")
            plt.grid()
            plt.title(par)

            suptitle = f"Observations : {dateobs} \n collection = {collection}"
            plt.suptitle(suptitle,fontsize=10,y=1.00)
            plt.tight_layout()
            plt.show()
            
    return [s for i,s in enumerate(specs) if filter_indices[i]]


def plot_spectra(spectra, colorparams,collection,dateobs):
    """
    plot spectra
    """
    
    colormap = cm.Reds
    #colormap = cm.jet 

    normalize = mcolors.Normalize(vmin=np.min(colorparams), vmax=np.max(colorparams))

    all_target_names = [] 

    fig  = plt.figure(figsize=(11,6))
    count = 0
    for spec in spectra:
        target_name = spec.target.label
        if target_name in all_target_names:
            plt.plot(spec.lambdas, spec.data, color = colormap(normalize(spec.airmass)))
        else:
            plt.plot(spec.lambdas, spec.data, color = colormap(normalize(spec.airmass)),label=target_name)
            all_target_names.append(target_name)
        count +=1
            
    plt.grid()
    plt.xlabel("$\lambda$ [nm]")
    plt.ylabel(f"Flux [{spec.units}]")
    plt.legend()
    
    # Colorbar setup
    s_map = cm.ScalarMappable(norm=normalize, cmap=colormap)
    s_map.set_array(colorparams)

    # If color parameters is a linspace, we can set boundaries in this way
    halfdist = (colorparams[1] - colorparams[0])/2.0
    boundaries = np.linspace(colorparams[0] - halfdist, colorparams[-1] + halfdist, len(colorparams) + 1)

    # Use this to emphasize the discrete color values
    cbar = fig.colorbar(s_map) #, spacing='proportional', ticks=colorparams, boundaries=boundaries, format='%2.2g') # format='%2i' for integer

    # Use this to show a continuous colorbar
    #cbar = fig.colorbar(s_map, spacing='proportional', ticks=colorparams, format='%2i')
    cbar.set_label("Airmass $z$")
    title = f"Observations : {dateobs}, nspec = {count}"
    suptitle = f"collection = {collection}"
    plt.title(title)
    plt.suptitle(suptitle,fontsize=10)
    plt.tight_layout()
    plt.show()
    return fig


def plot_atmtransmission(spectra, colorparams,all_calspecs_sm,tel,disp,collection,dateobs):
    """
    plot spectra
    """

    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
    colormap = cm.Reds
    #colormap = cm.jet 
   
    normalize = mcolors.Normalize(vmin=np.min(colorparams), vmax=np.max(colorparams))

    all_shown_target_names = [] 
    
    fig  = plt.figure(figsize=(11,6))
    count = 0
    for spec in spectra:
        
        target_name = spec.target.label

        wls = spec.lambdas
        flx = spec.data
        flx_err = spec.err
        
        #c_dict = all_calspecs[target_name]
        c_dict = all_calspecs_sm[target_name]

        #smooth_data_np_convolve(sed,span)
        
        sed=np.interp(wls, c_dict["WAVELENGTH"]/10.,c_dict["FLUX"]*10.,left=1e-15,right=1e-15)
       
                     
        ratio = flx/tel.transmission(wls)/disp.transmission(wls)/sed
       
        indexes = np.where(np.logical_and(wls>350.,wls<=1000.))[0]
       
        sel_wls = wls[indexes]
        sel_ratio = ratio[indexes]
        
        if target_name in all_shown_target_names:
            plt.plot(sel_wls, sel_ratio, color = colormap(normalize(spec.airmass)))
        else:
            plt.plot(sel_wls,sel_ratio, color = colormap(normalize(spec.airmass)),label=target_name)
            all_shown_target_names.append(target_name)
        count +=1
            
     
            
    plt.grid()
    plt.xlabel("$\lambda$ [nm]")
    #plt.ylabel(f"Flux [{spec.units}]")
    plt.legend()
    plt.xlim(360.,1000.)  
    plt.ylim(0.,1.2)  
    
    # Colorbar setup
    s_map = cm.ScalarMappable(norm=normalize, cmap=colormap)
    s_map.set_array(colorparams)

    # If color parameters is a linspace, we can set boundaries in this way
    halfdist = (colorparams[1] - colorparams[0])/2.0
    boundaries = np.linspace(colorparams[0] - halfdist, colorparams[-1] + halfdist, len(colorparams) + 1)

    # Use this to emphasize the discrete color values
    cbar = fig.colorbar(s_map) #, spacing='proportional', ticks=colorparams, boundaries=boundaries, format='%2.2g') # format='%2i' for integer

    # Use this to show a continuous colorbar
    #cbar = fig.colorbar(s_map, spacing='proportional', ticks=colorparams, format='%2i')
    cbar.set_label("Airmass $z$")
    title = f"Atmospheric transmission at target airmasses)"
    suptitle = f"obs : {dateobs} , nspec = {count} \n coll = {collection}"
    plt.title(title)
    plt.suptitle(suptitle,fontsize=10,y=1.0)
    plt.show()
    

def plot_atmtransmission_zcorr(spectra, colorparams,all_calspecs_sm,tel,disp,collection,dateobs):
    """
    plot atmospheric transmission

    parameters
    
    """

    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
    colormap = cm.Reds
    #colormap = cm.jet 
   

    normalize = mcolors.Normalize(vmin=np.min(colorparams), vmax=np.max(colorparams))
    all_shown_target_names = [] 
    fig  = plt.figure(figsize=(11,6))

    count = 0
    for spec in spectra:
             
        target_name = spec.target.label

        wls = spec.lambdas
        flx = spec.data
        flx_err = spec.err
        
        #c_dict = all_calspecs[target_name]
        c_dict = all_calspecs_sm[target_name]

        #smooth_data_np_convolve(sed,span)
        
        sed=np.interp(wls, c_dict["WAVELENGTH"]/10.,c_dict["FLUX"]*10.,left=1e-15,right=1e-15)
                         
        ratio = flx/tel.transmission(wls)/disp.transmission(wls)/sed
       
        indexes = np.where(np.logical_and(wls>350.,wls<=1000.))[0]
       
        sel_wls = wls[indexes]
        sel_ratio = ratio[indexes]
        sel_ratio_airmas_corr = np.power(sel_ratio,1/spec.airmass)
        
        if target_name in all_shown_target_names:
            plt.plot(sel_wls, sel_ratio_airmas_corr, color = colormap(normalize(spec.airmass)))
        else:
            plt.plot(sel_wls,sel_ratio_airmas_corr, color = colormap(normalize(spec.airmass)),label=target_name)
            all_shown_target_names.append(target_name)
        count += 1
            
     
            
    plt.grid()
    plt.xlabel("$\lambda$ [nm]")
    #plt.ylabel(f"Flux [{spec.units}]")
    plt.legend()
    plt.xlim(360.,1000.)  
    plt.ylim(0.,1.2)  
    
    # Colorbar setup
    s_map = cm.ScalarMappable(norm=normalize, cmap=colormap)
    s_map.set_array(colorparams)

    # If color parameters is a linspace, we can set boundaries in this way
    halfdist = (colorparams[1] - colorparams[0])/2.0
    boundaries = np.linspace(colorparams[0] - halfdist, colorparams[-1] + halfdist, len(colorparams) + 1)

    # Use this to emphasize the discrete color values
    cbar = fig.colorbar(s_map) #, spacing='proportional', ticks=colorparams, boundaries=boundaries, format='%2.2g') # format='%2i' for integer

    # Use this to show a continuous colorbar
    #cbar = fig.colorbar(s_map, spacing='proportional', ticks=colorparams, format='%2i')
    cbar.set_label("Airmass $z$")
    title = f"Atmospheric transmission scaled for airmass=1)"
    suptitle = f"obs : {dateobs} , nspec = {count} \n coll = {collection}"
    plt.title(title)
    plt.suptitle(suptitle,fontsize=10,y=1.0)
    plt.show()
    

def plot_atmtransmission_zcorr_antatmsim(spectra, colorparams,all_calspecs_sm,tel,disp,collection,dateobs,df_atm,am=1,pwv=2,oz=300,vaod=0.01,grey=0.99):
    """
    plot spectra
    """

    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
    colormap = cm.Reds
    #colormap = cm.jet 

    # find average atmospheric parameters
    df_good = df_atm[df_atm.filtered].drop(["id","filtered"],axis=1)
    m_A1 , m_ozone, m_PWV, m_VAOD = df_good.median().values
    print(" mean atm parameters",m_A1 , m_ozone, m_PWV, m_VAOD)

    all_meas_atmtransmissions = []

    normalize = mcolors.Normalize(vmin=np.min(colorparams), vmax=np.max(colorparams))

    all_shown_target_names = [] 
    
    fig  = plt.figure(figsize=(11,6))
    count = 0
    for spec in spectra:
        
        row = df_atm[df_atm.id == spec.dataId]
        (s_id, s_target, s_A1, s_ozone, s_PWV, s_VAOD, s_flag) = row.values[0]
        
        if s_flag:
            pwv=s_PWV
            oz=s_ozone
            vaod=s_VAOD
            grey=m_A1
        else:
            pwv=m_PWV
            oz=m_ozone
            vaod=m_VAOD
            grey=m_A1
            
        target_name = spec.target.label

        wls = spec.lambdas
        flx = spec.data
        flx_err = spec.err
        
        #c_dict = all_calspecs[target_name]
        c_dict = all_calspecs_sm[target_name]

        #smooth_data_np_convolve(sed,span)

        sed=np.interp(wls, c_dict["WAVELENGTH"]/10.,c_dict["FLUX"]*10.,left=1e-15,right=1e-15)                 
        ratio = flx/tel.transmission(wls)/disp.transmission(wls)/sed
        
        indexes = np.where(np.logical_and(wls>350.,wls<=1000.))[0]
       
        sel_wls = wls[indexes]
        sel_ratio = ratio[indexes]
        sel_ratio_airmas_corr = np.power(sel_ratio,am/spec.airmass)/(np.power(grey,am))
        
        if target_name in all_shown_target_names:
            plt.plot(sel_wls, sel_ratio_airmas_corr, color = colormap(normalize(spec.airmass)))
        else:
            plt.plot(sel_wls,sel_ratio_airmas_corr, color = colormap(normalize(spec.airmass)),label=target_name)
            all_shown_target_names.append(target_name)

        all_meas_atmtransmissions.append((sel_wls,sel_ratio_airmas_corr))
        count +=1
    
    textstr = '\n'.join((
    r'$am=%.2f$' % (am, ),
    r'$grey=%.2f$' % (m_A1, ),
    r'$pwv=%.2f$ mm' % (m_PWV, ),
    r'$ozone=%.1f$ DU' % (m_ozone, ),
    r'$vaod=%.3f$' % (m_VAOD,)))
    emul1 =  ObsAtmo("AUXTEL",740.)
    emul2 =  ObsAtmo("AUXTEL",730.)
    transm_sim1 = emul1.GetAllTransparencies(sel_wls,am,m_PWV,m_ozone,tau=m_VAOD)
    transm_sim2 = emul2.GetAllTransparencies(sel_wls,am,m_PWV,m_ozone,tau=m_VAOD)
    
    #plt.plot(sel_wls,transm_sim1,'-g',label=f"simulation P=740. hPa")
    plt.plot(sel_wls,transm_sim2,'-b',label=f"simulation P=730. hPa")

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax = plt.gca()
    # place a text box in upper left in axes coords
    ax.text(0.70, 0.25, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
            
    plt.grid()
    plt.xlabel("$\lambda$ [nm]")
    #plt.ylabel(f"Flux [{spec.units}]")
    plt.legend()
    plt.xlim(360.,1000.)  
    plt.ylim(0.,1.3)  
    
    # Colorbar setup
    s_map = cm.ScalarMappable(norm=normalize, cmap=colormap)
    s_map.set_array(colorparams)

    # If color parameters is a linspace, we can set boundaries in this way
    halfdist = (colorparams[1] - colorparams[0])/2.0
    boundaries = np.linspace(colorparams[0] - halfdist, colorparams[-1] + halfdist, len(colorparams) + 1)

    # Use this to emphasize the discrete color values
    cbar = fig.colorbar(s_map) #, spacing='proportional', ticks=colorparams, boundaries=boundaries, format='%2.2g') # format='%2i' for integer

    # Use this to show a continuous colorbar
    #cbar = fig.colorbar(s_map, spacing='proportional', ticks=colorparams, format='%2i')
    cbar.set_label("Airmass $z$")
    title = f"Atmospheric transmission scaled for airmass={am})"
    suptitle = f"obs : {dateobs} , nspec = {count} \n coll = {collection}"
    plt.title(title)
    plt.suptitle(suptitle,fontsize=10,y=1.0)
    plt.show()
    return all_meas_atmtransmissions
    


def plot_atmtransmission_zcorr_antatmsim_ratio(spectra,colorparams,all_calspecs_sm,tel,disp,collection,dateobs,df_atm,am=1,pwv=2,oz=300,vaod=0.01,grey=0.99):
    """
    plot spectra
    """

    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
    colormap = cm.Reds
    #colormap = cm.jet 

    # find average atmospheric parameters
    df_good = df_atm[df_atm.filtered].drop(["id","filtered"],axis=1)
    m_A1 , m_ozone, m_PWV, m_VAOD = df_good.median().values
    print(" mean parameters",m_A1 , m_ozone, m_PWV, m_VAOD)

    normalize = mcolors.Normalize(vmin=np.min(colorparams), vmax=np.max(colorparams))

    all_shown_target_names = [] 
    
    fig  = plt.figure(figsize=(14,10))

    grid = gridspec.GridSpec(2, 1, height_ratios=[2.5,1])

    ax1 = plt.subplot(grid[0])
    ax2 = plt.subplot(grid[1],sharex=ax1)

    textstr = '\n'.join((
    r'$am=%.2f$' % (am, ),
    r'$grey=%.2f$' % (m_A1, ),
    r'$pwv=%.2f$ mm' % (m_PWV, ),
    r'$ozone=%.1f$ DU' % (m_ozone, ),
    r'$vaod=%.3f$' % (m_VAOD,)))
    emul1 =  ObsAtmo("AUXTEL",740.)
    emul2 =  ObsAtmo("AUXTEL",730.)
    

    count = 0
    for spec in spectra:     

        row = df_atm[df_atm.id == spec.dataId]
        (s_id, s_target, s_A1, s_ozone, s_PWV, s_VAOD, s_flag) = row.values[0]
        if s_flag:
            pwv=s_PWV
            oz=s_ozone
            vaod=s_VAOD
            grey=m_A1
        else:
            pwv=m_PWV
            oz=m_ozone
            vaod=m_VAOD
            grey=m_A1
        
        target_name = spec.target.label

        wls = spec.lambdas
        flx = spec.data
        flx_err = spec.err
        
        #c_dict = all_calspecs[target_name]
        c_dict = all_calspecs_sm[target_name]

        #smooth_data_np_convolve(sed,span)
        
        sed=np.interp(wls, c_dict["WAVELENGTH"]/10.,c_dict["FLUX"]*10.,left=1e-15,right=1e-15)
                      
        ratio = flx/tel.transmission(wls)/disp.transmission(wls)/sed
       
        indexes = np.where(np.logical_and(wls>350.,wls<=1000.))[0]
       
        sel_wls = wls[indexes]
        sel_ratio = ratio[indexes]
        sel_ratio_airmas_corr = np.power(sel_ratio,am/spec.airmass)/(np.power(grey,am))
        
        if target_name in all_shown_target_names:
            ax1.plot(sel_wls, sel_ratio_airmas_corr, color = colormap(normalize(spec.airmass)))
        else:
            ax1.plot(sel_wls,sel_ratio_airmas_corr, color = colormap(normalize(spec.airmass)),label=target_name)
            all_shown_target_names.append(target_name)

        transm_sim1 = emul1.GetAllTransparencies(sel_wls,am,pwv,oz,tau=vaod)
        transm_sim2 = emul2.GetAllTransparencies(sel_wls,am,pwv,oz,tau=vaod)
    
        #ax1.plot(sel_wls,transm_sim1,'-g')
        #ax1.plot(sel_wls,transm_sim2,'-b')

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
   
        # place a text box in upper left in axes coords

        ax2.plot(sel_wls,sel_ratio_airmas_corr/transm_sim1,color = colormap(normalize(spec.airmass)),label=f"simulation P=740. hPa")
        #ax2.plot(sel_wls,sel_ratio_airmas_corr/transm_sim2,'-g',label=f"simulation P=730. hPa")
        ax1.text(0.70, 0.25, textstr, transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)

        count += 1
            
    ax1.grid()

    transm_sim1 = emul1.GetAllTransparencies(sel_wls,am,m_PWV,m_ozone,tau=m_VAOD)
    transm_sim2 = emul2.GetAllTransparencies(sel_wls,am,m_PWV,m_ozone,tau=m_VAOD)

    ax1.plot(sel_wls,transm_sim2,'-b')
    
    #ax1.set_xlabel("$\lambda$ [nm]")
    #plt.ylabel(f"Flux [{spec.units}]")
    ax1.legend()
    ax1.set_xlim(360.,1000.)  
    ax1.set_ylim(0.,1.3)  

    ax2.set_title(f"ratio spectrum/sim at airmass {am:.2f}")
    ax2.set_xlabel("$\lambda$ [nm]")  
    ax2.set_ylim(0.9,1.1)  
    ax2.grid()
    # Colorbar setup
    s_map = cm.ScalarMappable(norm=normalize, cmap=colormap)
    s_map.set_array(colorparams)

    # If color parameters is a linspace, we can set boundaries in this way
    halfdist = (colorparams[1] - colorparams[0])/2.0
    boundaries = np.linspace(colorparams[0] - halfdist, colorparams[-1] + halfdist, len(colorparams) + 1)

    # Use this to emphasize the discrete color values
    #cbar = fig.colorbar(s_map) #, spacing='proportional', ticks=colorparams, boundaries=boundaries, format='%2.2g') # format='%2i' for integer

    # Use this to show a continuous colorbar
    #cbar = fig.colorbar(s_map, spacing='proportional', ticks=colorparams, format='%2i')
    #cbar.set_label("Airmass $z$")
    title = f"Atmospheric transmission scaled for airmass={am})"
    suptitle = f"obs : {dateobs} , nspec= {count} \n coll = {collection}"
    ax1.set_title(title)
    plt.suptitle(suptitle,fontsize=10,y=1.0)

    plt.show()
    







# SMOOTHING

def smooth_data_convolve_my_average(arr, span):
    re = np.convolve(arr, np.ones(span * 2 + 1) / (span * 2 + 1), mode="same")

    # The "my_average" part: shrinks the averaging window on the side that 
    # reaches beyond the data, keeps the other side the same size as given 
    # by "span"
    re[0] = np.average(arr[:span])
    for i in range(1, span + 1):
        re[i] = np.average(arr[:i + span])
        re[-i] = np.average(arr[-i - span:])
    return re

def smooth_data_np_average(arr, span):  # my original, naive approach
    return [np.average(arr[val - span:val + span + 1]) for val in range(len(arr))]

def smooth_data_np_convolve(arr, span):
    return np.convolve(arr, np.ones(span * 2 + 1) / (span * 2 + 1), mode="same")

def smooth_data_np_cumsum_my_average(arr, span):
    cumsum_vec = np.cumsum(arr)
    moving_average = (cumsum_vec[2 * span:] - cumsum_vec[:-2 * span]) / (2 * span)

    # The "my_average" part again. Slightly different to before, because the
    # moving average from cumsum is shorter than the input and needs to be padded
    front, back = [np.average(arr[:span])], []
    for i in range(1, span):
        front.append(np.average(arr[:i + span]))
        back.insert(0, np.average(arr[-i - span:]))
    back.insert(0, np.average(arr[-2 * span:]))
    return np.concatenate((front, moving_average, back))

def smooth_data_lowess(arr, span):
    x = np.linspace(0, 1, len(arr))
    return sm.nonparametric.lowess(arr, x, frac=(5*span / len(arr)), return_sorted=False)

def smooth_data_kernel_regression(arr, span):
    # "span" smoothing parameter is ignored. If you know how to 
    # incorporate that with kernel regression, please comment below.
    kr = KernelReg(arr, np.linspace(0, 1, len(arr)), 'c')
    return kr.fit()[0]

def smooth_data_savgol_0(arr, span):  
    return savgol_filter(arr, span * 2 + 1, 0)

def smooth_data_savgol_1(arr, span):  
    return savgol_filter(arr, span * 2 + 1, 1)

def smooth_data_savgol_2(arr, span):  
    return savgol_filter(arr, span * 2 + 1, 2)

def smooth_data_fft(arr, span):  # the scaling of "span" is open to suggestions
    w = fftpack.rfft(arr)
    spectrum = w ** 2
    cutoff_idx = spectrum < (spectrum.max() * (1 - np.exp(-span / 2000)))
    w[cutoff_idx] = 0
    return fftpack.irfft(w)


# Integrals


def fII0(wl,s):
    """
    Parameters:
    S : is the atmospheric transmission times the instrumental transmission
    wl :is the wavelength transmission

    return:
    II0 integral which is unitless
    """

    # clean
    indexes_sel = np.where(s>0.002)[0]
    wlmin = wl[indexes_sel].min()
    wlmax = wl[indexes_sel].max()

    indexes_sel = np.where(np.logical_and(wl>wlmin,wl<wlmax))[0]
    
    return np.trapz(s[indexes_sel]/wl[indexes_sel],wl[indexes_sel])
      
def fII1(wl,phi,wlb):
    """
    """
    return np.trapz(phi*(wl-wlb),wl)
  
def ZPT(wl,s):
    """
    Parameter:
    S : is the atmospheric transmission times the instrumental transmission
    wl :is the wavelength transmission

    return:
    The Zero point
    """
    return 2.5*np.log10(fII0(wl,s)) + ZPTconst

