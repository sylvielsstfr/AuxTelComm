#! /usr/bin/env python3
# -*- Encoding: utf-8 -*-
#
#--------------------------------------------------------
#
# Vera Rubin Oservatory (VRO) / LSST
# Rough stitching procedure for ITL CCD
# Laurent Le Guillou <llg@lpnhe.in2p3.fr> - 2022-05-14
#
#--------------------------------------------------------

import os, sys

import numpy as np
# import pyfits
import astropy.io.fits as pyfits


def parse_slice_str(s):
    """
    Parse slicing string like [2345:1234,567:890] and returns
    the four values in the same order as 2 tuples, eg:
    parse_slice_str('[2345:1234,567:890]') -> (2345,1234),(567,890).
    """
    r = s.replace('[','').replace(']','').strip() # remove brackets

    parts = r.split(',')
    if len(parts) != 2:
        raise ValueError("Invalid format for slice '%s'" % s)

    subparts_first = parts[0].split(':')
    if len(subparts_first) != 2:
        raise ValueError("Invalid format for slice '%s' (first slice)" % s)
    first_values = (int(subparts_first[0]), int(subparts_first[1])) # may raise ValueError, ok

    subparts_second = parts[1].split(':')
    if len(subparts_second) != 2:
        raise ValueError("Invalid format for slice '%s' (second slice)" % s)
    second_values = (int(subparts_second[0]), int(subparts_second[1])) # may raise ValueError, ok

    return first_values, second_values
        


fitsname = "AT_O_20220317_000471-R00S00.fits"
fits = pyfits.open(fitsname)

primhdu = fits[0]
primhdr = primhdu.header

# DETSIZE = '[1:4072,1:4000]'    / Size of sensor                                 
# OVERV   =                   48 / Vert-overscan pix                              
# OVERH   =                   64 / Over-scan pixels                               
## The following is probably wrong, according to the sequencer code used
## for the readout of the ITL CCD and to the resulting geometry: 3 + 509 + 64 = 576
# PREH    =                    0 / Pre-scan pixels                                
## --> here we use instead PREH = 3

## Detector size (illuminated area) 

detsize_str = primhdr['DETSIZE']
(ymin_b1, ymax_b1), (xmin_b1, xmax_b1) = parse_slice_str(detsize_str) # 1-base coordinates
xmin, xmax = xmin_b1-1, xmax_b1-1  # 0-base coordinates
xsize = xmax - xmin + 1
ymin, ymax = ymin_b1-1, ymax_b1-1  # 0-base coordinates
ysize = ymax - ymin + 1

print("Detector size: ")
print("  xsize =", xsize)
print("  ysize =", ysize)

## Prescan and Overscan

amp_prescan_lines    = 0
amp_overscan_lines   = primhdr['OVERV']
amp_prescan_columns  = 3  # primhdr['PREH']  # header is clearly inconsistent here
amp_overscan_columns = primhdr['OVERH']

## Create the large image

ccd = np.zeros(dtype = fits[1].data.dtype, shape = (xsize, ysize))

## Process the HDUs for the 16 amplifiers

for hdu in fits[1:]:
    hdr = hdu.header
    img = hdu.data

    amp_total_xsize, amp_total_ysize = img.shape
    amp_ill_xsize = amp_total_xsize - amp_prescan_lines - amp_overscan_lines
    amp_ill_ysize = amp_total_ysize - amp_prescan_columns - amp_overscan_columns

    
    print("Processing HDU <%s> ..." % hdr['EXTNAME'])

    print("  HDU img.shape = ", img.shape)
    print("  HDU ill_xsize = ", amp_ill_xsize)
    print("  HDU ill_ysize = ", amp_ill_ysize)

    ## illuminated part in the amplifier data...
    # datasec_str = hdu.header['DATASEC']
    # datasec_slice = parse_slice_str(datasec_str)
    # in fact the header DATASEC is wrong.

    amp_ill_xmin = amp_prescan_lines
    amp_ill_xmax = amp_prescan_lines + amp_ill_xsize

    amp_ill_ymin = amp_prescan_columns
    amp_ill_ymax = amp_prescan_columns + amp_ill_ysize

    
    print("  illum area [0-based python-style] = [%d:%d,%d:%d]" % 
          ( amp_ill_xmin, amp_ill_xmax, amp_ill_ymin, amp_ill_ymax ))

    illum = img[amp_ill_xmin:amp_ill_xmax, amp_ill_ymin:amp_ill_ymax]
    print("  illum.shape = ", illum.shape)
    
    ## ... and where it sits in the physical CCD array.
    detsec_str = hdu.header['DETSEC']
    detsec_slice = parse_slice_str(detsec_str)
    # Loading also the transfo vector and matrix (1-based)
    # DTV1    =                  510 / detector transformation vector                 
    # DTV2    =                    0 / detector transformation vector                 
    # DTM1_1  =                  -1. / detector transformation matrix                 
    # DTM2_2  =                   1. / detector transformation matrix                 
    # DTM1_2  =                    0 / detector transformation matrix                 
    # DTM2_1  =                    0 / detector transformation matrix                 
    
    dtv1 = hdr['DTV1']; dtv2 = hdr['DTV2']
    dtm1_1 = hdr['DTM1_1']; dtm1_2 = hdr['DTM1_2']
    dtm2_1 = hdr['DTM2_1']; dtm2_2 = hdr['DTM2_2']

    print("  dtv = ", np.array([dtv1, dtv2]))
    print("  dtm = ")
    print(np.array([[dtm1_1, dtm1_2],[dtm2_1, dtm2_2]]))
    
    ccd_x1 = detsec_slice[1][0]
    ccd_x2 = detsec_slice[1][1]
    # ccd_xstep = int(dtm2_2)
    if ccd_x1 < ccd_x2: 
        ccd_xstep = 1
    else:
        ccd_x1, ccd_x2 = ccd_x2, ccd_x1
        ccd_xstep = -1
    #
    ccd_x1 -= 1

    ccd_y1 = detsec_slice[0][0]
    ccd_y2 = detsec_slice[0][1]
    # ccd_ystep = int(dtm1_1)
    if ccd_y1 < ccd_y2:
        ccd_ystep = 1
    else:
        ccd_y1, ccd_y2 = ccd_y2, ccd_y1
        ccd_ystep = -1
    #
    ccd_y1 -= 1
        
    # print("  DATASEC = ", datasec_slice)
    print("  DETSEC = ", detsec_slice)
    
    print("  CCD area [0-based python-style] = [%d:%d,%d:%d]" % 
          (ccd_x1, ccd_x2, ccd_y1, ccd_y2) )

    # print(ccd[ccd_x1:ccd_x2:ccd_xstep, ccd_y1:ccd_y2:ccd_ystep].shape)
    print(ccd[ccd_x1:ccd_x2, ccd_y1:ccd_y2].shape)

    ccd[ccd_x1:ccd_x2, ccd_y1:ccd_y2] = illum[::ccd_xstep, ::ccd_ystep]


# Save the resulting array in a new FITS file

outfitsname = fitsname.replace(".fits", "-stitched.fits")
outfitshdr = primhdr
pyfits.writeto(outfitsname, ccd, header=primhdr, overwrite=True)




