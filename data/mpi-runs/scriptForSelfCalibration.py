# This script runs the ALMAGAL self-calibration script
#
# This is a template/master script that is updated when running:
# > python createIndividual_scriptForSelfCalibration.py
#

#-----------------------------------------------------------------------
#
# Import python packages
#
import os
import sys
sys.path.append("ToModifyRUNNINGPATH/almagal/")
sys.path.append("ToModifyRUNNINGPATH/almagal/python/")
sys.path.append("ToModifyRUNNINGPATH/almagal/analysis_scripts/")
import glob
import numpy as np
import astropy
from astropy.io import fits
import subprocess
import shutil
import analysisUtils as au
import analysisUtils as aU
import configALMAGAL
from functionsALMAGAL import *

#-----------------------------------------------------------------------
# Define main paths, variables and steps to process
#
# Paths:
#
my_mainPath = 'ToModifyMAINPATH'       # e.g. '/p/scratch/almagal/data'
my_runningPath = 'ToModifyRUNNINGPATH' # e.g. '/dev/shm'

# Variables:
#
my_source = 'ToModifySOURCE'           # e.g. '49143'
my_telescope = 'ToModifyTELESCOPE'     # e.g. '7M' or 'TM2'

# Steps to process:
#
mysteps = ToModifySTEPS                # e.g. [0] or [0, 1, 2, 3, 4]
mycurrentstep = 'ToModifyCURRENTSTEP'  # e.g. "step0" or "steps"

#-----------------------------------------------------------------------
# Define steps environment
#
thesteps = [0]
step_title = {0: 'Self-calibrate 7M-array data',
              1: 'Self-calibrate TM2-array data',
              2: 'Self-calibrate TM1-array data'}
try:
  print('List of steps to be executed ...', mysteps)
  thesteps = mysteps
except:
  print('global variable mysteps not set.')
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print('Executing all steps: ', thesteps)

#-----------------------------------------------------------------------
#
# Define functions
#
def my_functionSelfCalibration(my_telescope, my_source):
    
    """
    help help
    """
    
    # Determine the tclean parameters
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForSelfCalibration(my_telescope, my_source)

    my_visFiles = my_visfilestoclean
    my_spwRanges = my_freqs
    my_array = my_telescope
    
    # Define reference antenna
    #
    my_refAntsList = []
    for i in range(0, len(my_visFiles)):
        print('... searching for refant for ' + str(my_visFiles[i]))
        my_refAnt = my_searchRefAnt(my_visFiles[i])
        my_refAntsList.append(my_refAnt)
    my_refAnts = np.asarray(my_refAntsList)
    print(my_refAnts)
    #if (my_telescope == "7M"):
    #    my_refant = 'CM03'
    #if (my_telescope == "TM2"):
    #    my_refant = 'DA48'
    #if (my_telescope == "TM1"):
    #    my_refant = 'DA48'
    
    # Define path for self-calibration products
    #
    os.system('mkdir -p ' + str(my_runningPath) + '/almagal/selfcalibration')
    os.system('mkdir -p ' + str(my_runningPath) + '/almagal/selfcalibration/images')

    # SPLIT out original ms files for SELFCAL iterations
    #
    print("... SPLIT ms files for setting up SELFCAL iterations (SETUP / ITER 1)")
    my_visFiles_iter1 = []
    for i in range(0, len(my_visFiles)):
        os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter1*')
        split(vis = my_visFiles[i],
            datacolumn = 'data',
            outputvis = my_visFiles[i] + '_selfcal.iter1')
        my_visFiles_iter1.append(my_visFiles[i] + '_selfcal.iter1')

    # TCLEAN to generate setup image (to initialize residuals and rms levels)
    #
    my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter0.setup_clean'
    my_scalesNow = [0, 6, 12]
    my_niterNow = 100000
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.0*my_number) + my_unit
    my_smallscalebiasNow = 0.0
    
    print("... TCLEAN setup image")
    print("... Some parameters are:")
    print("... ... original threshold = " + str(my_threshold))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    
    os.system('rm -rf ' + my_outputImageNow + '.*')
    tclean(vis = my_visFiles_iter1,
        imagename = my_outputImageNow,
        datacolumn = 'data',
        field = str(my_source),
        stokes = 'I',
        spw = my_spwRanges,
        outframe = 'LSRK',
        restfreq = '',
        specmode = 'mfs',
        imsize = my_imsize,
        cell = my_cell,
        deconvolver = 'multiscale',
        scales = my_scalesNow,
        niter = my_niterNow,
        weighting = my_weighting,
        robust = my_robust,
        usemask = 'auto-multithresh',
        mask = '',
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = 'standard',
        pblimit = my_pblimit,
        pbcor = False,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    # Calculate the median absolute deviation of the residual
    exportfits(imagename = my_outputImageNow + '.residual',
        fitsimage = my_outputImageNow + '.residual.fits',
        dropdeg = True,
        overwrite = True)
    dataResidual, headerResidual = fits.getdata(my_outputImageNow + '.residual.fits', header=True)
    dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
    dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
    print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
    # Calculate the peak intensity of the image
    exportfits(imagename = my_outputImageNow + '.image',
        fitsimage = my_outputImageNow + '.image.fits',
        dropdeg = True,
        overwrite = True)
    dataImage, headerImage = fits.getdata(my_outputImageNow + '.image.fits', header=True)
    dataImage_notNaN = dataImage[np.logical_not(np.isnan(dataImage))]
    dataImage_Peak = np.amax(dataImage_notNaN)
    print("... ... Peak intensity in the image = " + str(dataImage_Peak))
    # Calculate the SNR ratio to evaluate the possibility of doing self-calibration
    dataImage_SNR = dataImage_Peak/dataResidual_MAD
    print("... ... Signal-to-noise ratio = " + str(int(100000.*dataImage_SNR)/100000.))
    
    # Check details at https://science.nrao.edu/facilities/alma/naasc-workshops/nrao-cd-wm16/Selfcal_Madison.pdf
    # for phase only:
    #  rms_ant = rms x sqrt(N-3) , where N is the number of antennas
    #  rms_self = rms_ant x sqrt(total time / solint)
    #  if S/Nself = peak/rms_self > 3 try phase-only selfcal
    #
    my_exposure_time = 0.0
    my_number_of_antennas = 0
    for i in range(0, len(my_visFiles)):
        msmd.open(my_visFiles[i])
        my_exposure_time = my_exposure_time + abs(msmd.effexposuretime()['value'])
        my_number_of_antennas = max(my_number_of_antennas, msmd.nantennas())
        msmd.done()
    if (my_array == "TM1") or (my_array == "TM2"):
        print("... your array is TM2 or TM1")
        SNR_self = dataImage_Peak/(dataResidual_MAD*np.sqrt(my_number_of_antennas-3)*np.sqrt(my_exposure_time/6.048))
    if (my_array == "7M"):
        print("... your array is 7M")
        SNR_self = dataImage_Peak/(dataResidual_MAD*np.sqrt(my_number_of_antennas-3)*np.sqrt(my_exposure_time/10.08))
    print("... effective exposure time is " + str(int(my_exposure_time*1000.)/1000.))
    print("... number of antennas is " + str(my_number_of_antennas))
    print("... signal to noise for selfcalibration is " + str(int(SNR_self*1000.)/1000.))
    
    # Check if signal-to-noise ratio is large enough to do self-calibration
    #
    #if (dataImage_SNR < 50.):
    if (SNR_self < 3.0):
        
        print("... smaller than 3.0, so")
        print("... not enough SNR for self-calibration")
        
        # Clean-up directory from not necessary ms files
        #
        print("... clean-up some files")
        for i in range(0, len(my_visFiles)):
            print("... ... " + my_visFiles[i] + "_selfcal.iter1*")
            os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter1*')
        
    else:
        
        print("... higher than 3.0, so")
        print("... proceding with self-calibration steps")
        
        # Clean-up directory from not necessary ms files
        #
        print("... clean-up some files")
        for i in range(0, len(my_visFiles)):
            print("... ... " + my_visFiles[i])
            os.system('rm -rf ' + my_visFiles[i])
        
        # TCLEAN to generate iter1 preliminary image
        #
        my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter1.prelim_clean'
        my_scalesNow = [0, 6, 12]
        my_niterNow = 100000
        my_number, my_unit = separateNumbersUnits(my_threshold)
        my_thresholdNow = str(4.0*dataResidual_MAD) + my_unit
        my_smallscalebiasNow = 0.0
        
        print("... TCLEAN iter 1 prelim_clean image")
        print("... Some parameters are:")
        print("... ... original threshold = " + str(dataResidual_MAD))
        print("... ... used threshold = " + str(my_thresholdNow))
        print("... ... used scales = " + str(my_scalesNow))
        
        os.system('rm -rf ' + my_outputImageNow + '.*')
        tclean(vis = my_visFiles_iter1,
            imagename = my_outputImageNow,
            datacolumn = 'data',
            field = str(my_source),
            stokes = 'I',
            spw = my_spwRanges,
            outframe = 'LSRK',
            restfreq = '',
            specmode = 'mfs',
            imsize = my_imsize,
            cell = my_cell,
            deconvolver = 'multiscale',
            scales = my_scalesNow,
            niter = my_niterNow,
            weighting = my_weighting,
            robust = my_robust,
            usemask = 'auto-multithresh',
            mask = '',
            pbmask = my_pbmask,
            sidelobethreshold = my_sidelobethreshold,
            noisethreshold = my_noisethreshold,
            minbeamfrac =  my_minbeamfrac,
            lownoisethreshold = my_lownoisethreshold,
            negativethreshold = my_negativethreshold,
            gridder = 'standard',
            pblimit = my_pblimit,
            pbcor = False,
            threshold = my_thresholdNow,
            interactive = False,
            restoringbeam = 'common',
            smallscalebias = my_smallscalebiasNow)
        exportfits(imagename = my_outputImageNow + '.image',
            fitsimage = my_outputImageNow + '.image.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        # Determine intensity peak, rms and SNR levels
        #
        hdu_image = fits.open(my_outputImageNow + '.image.fits')[0]
        hdu_residual = fits.open(my_outputImageNow + '.residual.fits')[0]
        hdu_peak_image = np.nanmax(hdu_image.data)
        hdu_rms_image = np.nanstd(hdu_residual.data)
        hdu_SNR_image = hdu_peak_image/hdu_rms_image
        hdu_bmaj_image = hdu_image.header['bmaj']*3600.
        hdu_bmin_image = hdu_image.header['bmin']*3600.
        print("... intensity peak = " + str(int(hdu_peak_image*1000.)/1000.))
        print("... rms noise level = " + str(int(hdu_rms_image*1000.)/1000.))
        print("... SNR = " + str(int(hdu_SNR_image*1000.)/1000.))
        print("... beam is " + str(int(hdu_bmaj_image*1000.)/1000.) + " x " + str(int(hdu_bmin_image*1000.)/1000.))
        
        # Add model to ms file
        #
        print("... apply FT for iter 1")
        for i in range(0, len(my_visFiles)):
            ft(vis = my_visFiles_iter1[i],
                field = str(my_source),
                spw = my_spwRanges[i],
                model = my_outputImageNow + '.model',
                usescratch = True)
        
        # Gaincal's
        print("... apply GAINCAL for iter 1")
        for i in range(0, len(my_visFiles)):
            os.system('rm -rf ' + my_visFiles_iter1[i] + '.iter1.selfcal.p1')
            gaincal(vis = my_visFiles_iter1[i],
                caltable = my_visFiles_iter1[i] + '.iter1.selfcal.p1',
                spw = my_spwRanges[i],
                combine = 'spw',
                solint = 'int',
                refant = my_refAnts[i],
                calmode = 'p',
                gaintype = 'T',
                minsnr = 2.5)
        
        # Applycal's
        print("... run APPLYCAL for iter 1")
        for i in range(0, len(my_visFiles)):
            applycal(vis = my_visFiles_iter1[i],
                gaintable = my_visFiles_iter1[i] + '.iter1.selfcal.p1',
                spwmap = [0, 0, 0, 0])
        
        # TCLEAN to generate selfcal p1 image
        #
        my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter1.selfcal.p1_clean'
        my_scalesNow = [0, 6, 12]
        my_niterNow = 100000
        my_number, my_unit = separateNumbersUnits(my_threshold)
        my_thresholdNow = str(4.0*dataResidual_MAD) + my_unit
        my_smallscalebiasNow = 0.0
        
        print("... TCLEAN iter 1 selfcal p1 image")
        print("... Some parameters are:")
        print("... ... original threshold = " + str(dataResidual_MAD))
        print("... ... used threshold = " + str(my_thresholdNow))
        print("... ... used scales = " + str(my_scalesNow))
        
        os.system('rm -rf ' + my_outputImageNow + '.*')
        tclean(vis = my_visFiles_iter1,
            imagename = my_outputImageNow,
            datacolumn = 'corrected',
            field = str(my_source),
            stokes = 'I',
            spw = my_spwRanges,
            outframe = 'LSRK',
            restfreq = '',
            specmode = 'mfs',
            imsize = my_imsize,
            cell = my_cell,
            deconvolver = 'multiscale',
            scales = my_scalesNow,
            niter = my_niterNow,
            weighting = my_weighting,
            robust = my_robust,
            usemask = 'auto-multithresh',
            mask = '',
            pbmask = my_pbmask,
            sidelobethreshold = my_sidelobethreshold,
            noisethreshold = my_noisethreshold,
            minbeamfrac =  my_minbeamfrac,
            lownoisethreshold = my_lownoisethreshold,
            negativethreshold = my_negativethreshold,
            gridder = 'standard',
            pblimit = my_pblimit,
            pbcor = False,
            threshold = my_thresholdNow,
            interactive = False,
            restoringbeam = 'common',
            smallscalebias = my_smallscalebiasNow)
        exportfits(imagename = my_outputImageNow + '.image',
            fitsimage = my_outputImageNow + '.image.fits',
            dropdeg = True,
            overwrite = True)
        # Calculate the median absolute deviation of the residual
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        # Determine intensity peak, rms and SNR levels
        #
        hdu_image = fits.open(my_outputImageNow + '.image.fits')[0]
        hdu_residual = fits.open(my_outputImageNow + '.residual.fits')[0]
        hdu_peak_selfcal = np.nanmax(hdu_image.data)
        hdu_rms_selfcal = np.nanstd(hdu_residual.data)
        hdu_SNR_selfcal = hdu_peak_selfcal/hdu_rms_selfcal
        hdu_bmaj_selfcal = hdu_image.header['bmaj']*3600.
        hdu_bmin_selfcal = hdu_image.header['bmin']*3600.
        print("... original image")
        print("... intensity peak = " + str(int(hdu_peak_image*1000.)/1000.))
        print("... rms noise level = " + str(int(hdu_rms_image*1000.)/1000.))
        print("... SNR = " + str(int(hdu_SNR_image*1000.)/1000.))
        print("... beam is " + str(int(hdu_bmaj_image*1000.)/1000.) + " x " + str(int(hdu_bmin_image*1000.)/1000.))
        print("... self-calibrated image")
        print("... intensity peak = " + str(int(hdu_peak_selfcal*1000.)/1000.))
        print("... rms noise level = " + str(int(hdu_rms_selfcal*1000.)/1000.))
        print("... SNR = " + str(int(hdu_SNR_selfcal*1000.)/1000.))
        print("... beam is " + str(int(hdu_bmaj_selfcal*1000.)/1000.) + " x " + str(int(hdu_bmin_selfcal*1000.)/1000.))
        hdu_improvement = 100.*(hdu_SNR_selfcal-hdu_SNR_image)/hdu_SNR_image
        hdu_beamIncrease = 100.*(hdu_bmaj_selfcal-hdu_bmaj_image)/hdu_bmaj_image
        print("... improvement of " + str(int(hdu_improvement*1000.)/1000.) + "%")
        print("... beam modified by " + str(int(hdu_beamIncrease*1000.)/1000.) + "%")
        print("... ")

        dataResidual, headerResidual = fits.getdata(my_outputImageNow + '.residual.fits', header=True)
        dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
        dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
        print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
        
        # SPLIT out original ms files for SELFCAL iterations
        #
        print("... SPLIT ms files for setting up SELFCAL iterations (ITER 2)")
        my_visFiles_iter2 = []
        for i in range(0, len(my_visFiles)):
            os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter2*')
            split(vis = my_visFiles_iter1[i],
                datacolumn = 'corrected',
                outputvis = my_visFiles[i] + '_selfcal.iter2')
            my_visFiles_iter2.append(my_visFiles[i] + '_selfcal.iter2')
        
        # TCLEAN to generate iter2 preliminary image
        #
        my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter2.prelim_clean'
        my_scalesNow = [0, 6, 12]
        my_niterNow = 100000
        my_number, my_unit = separateNumbersUnits(my_threshold)
        my_thresholdNow = str(3.0*dataResidual_MAD) + my_unit
        my_smallscalebiasNow = 0.0
        
        print("... TCLEAN iter 2 prelim_clean image")
        print("... Some parameters are:")
        print("... ... original threshold = " + str(dataResidual_MAD))
        print("... ... used threshold = " + str(my_thresholdNow))
        print("... ... used scales = " + str(my_scalesNow))
        
        os.system('rm -rf ' + my_outputImageNow + '.*')
        tclean(vis = my_visFiles_iter2,
            imagename = my_outputImageNow,
            datacolumn = 'data',
            field = str(my_source),
            stokes = 'I',
            spw = my_spwRanges,
            outframe = 'LSRK',
            restfreq = '',
            specmode = 'mfs',
            imsize = my_imsize,
            cell = my_cell,
            deconvolver = 'multiscale',
            scales = my_scalesNow,
            niter = my_niterNow,
            weighting = my_weighting,
            robust = my_robust,
            usemask = 'auto-multithresh',
            mask = '',
            pbmask = my_pbmask,
            sidelobethreshold = my_sidelobethreshold,
            noisethreshold = my_noisethreshold,
            minbeamfrac =  my_minbeamfrac,
            lownoisethreshold = my_lownoisethreshold,
            negativethreshold = my_negativethreshold,
            gridder = 'standard',
            pblimit = my_pblimit,
            pbcor = False,
            threshold = my_thresholdNow,
            interactive = False,
            restoringbeam = 'common',
            smallscalebias = my_smallscalebiasNow)
        exportfits(imagename = my_outputImageNow + '.image',
            fitsimage = my_outputImageNow + '.image.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        # Determine intensity peak, rms and SNR levels
        #
        hdu_image = fits.open(my_outputImageNow + '.image.fits')[0]
        hdu_residual = fits.open(my_outputImageNow + '.residual.fits')[0]
        hdu_peak_image = np.nanmax(hdu_image.data)
        hdu_rms_image = np.nanstd(hdu_residual.data)
        hdu_SNR_image = hdu_peak_image/hdu_rms_image
        hdu_bmaj_image = hdu_image.header['bmaj']*3600.
        hdu_bmin_image = hdu_image.header['bmin']*3600.
        print("... intensity peak = " + str(int(hdu_peak_image*1000.)/1000.))
        print("... rms noise level = " + str(int(hdu_rms_image*1000.)/1000.))
        print("... SNR = " + str(int(hdu_SNR_image*1000.)/1000.))
        print("... beam is " + str(int(hdu_bmaj_image*1000.)/1000.) + " x " + str(int(hdu_bmin_image*1000.)/1000.))
        
        # Add model to ms file
        #
        print("... apply FT for iter 2")
        for i in range(0, len(my_visFiles)):
            ft(vis = my_visFiles_iter2[i],
                field = str(my_source),
                spw = my_spwRanges[i],
                model = my_outputImageNow + '.model',
                usescratch = True)
        
        # Gaincal's
        print("... apply GAINCAL for iter 2")
        for i in range(0, len(my_visFiles)):
            os.system('rm -rf ' + my_visFiles_iter2[i] + '.iter2.selfcal.p2')
            gaincal(vis = my_visFiles_iter2[i],
                caltable = my_visFiles_iter2[i] + '.iter2.selfcal.p2',
                spw = my_spwRanges[i],
                combine = 'spw',
                solint = 'int',
                refant = my_refAnts[i],
                calmode = 'p',
                gaintype = 'T',
                minsnr = 3.5)
        
        # Applycal's
        print("... run APPLYCAL for iter 2")
        for i in range(0, len(my_visFiles)):
            applycal(vis = my_visFiles_iter2[i],
                gaintable = my_visFiles_iter2[i] + '.iter2.selfcal.p2',
                spwmap = [0, 0, 0, 0])
        
        # TCLEAN to generate selfcal p2 image
        #
        my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter2.selfcal.p2_clean'
        my_scalesNow = [0, 6, 12]
        my_niterNow = 100000
        my_number, my_unit = separateNumbersUnits(my_threshold)
        my_thresholdNow = str(3.0*dataResidual_MAD) + my_unit
        my_smallscalebiasNow = 0.0
        
        print("... TCLEAN iter 2 selfcal p2 image")
        print("... Some parameters are:")
        print("... ... original threshold = " + str(dataResidual_MAD))
        print("... ... used threshold = " + str(my_thresholdNow))
        print("... ... used scales = " + str(my_scalesNow))
        
        os.system('rm -rf ' + my_outputImageNow + '.*')
        tclean(vis = my_visFiles_iter2,
            imagename = my_outputImageNow,
            datacolumn = 'corrected',
            field = str(my_source),
            stokes = 'I',
            spw = my_spwRanges,
            outframe = 'LSRK',
            restfreq = '',
            specmode = 'mfs',
            imsize = my_imsize,
            cell = my_cell,
            deconvolver = 'multiscale',
            scales = my_scalesNow,
            niter = my_niterNow,
            weighting = my_weighting,
            robust = my_robust,
            usemask = 'auto-multithresh',
            mask = '',
            pbmask = my_pbmask,
            sidelobethreshold = my_sidelobethreshold,
            noisethreshold = my_noisethreshold,
            minbeamfrac =  my_minbeamfrac,
            lownoisethreshold = my_lownoisethreshold,
            negativethreshold = my_negativethreshold,
            gridder = 'standard',
            pblimit = my_pblimit,
            pbcor = False,
            threshold = my_thresholdNow,
            interactive = False,
            restoringbeam = 'common',
            smallscalebias = my_smallscalebiasNow)
        exportfits(imagename = my_outputImageNow + '.image',
            fitsimage = my_outputImageNow + '.image.fits',
            dropdeg = True,
            overwrite = True)
        # Calculate the median absolute deviation of the residual
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        # Determine intensity peak, rms and SNR levels
        #
        hdu_image = fits.open(my_outputImageNow + '.image.fits')[0]
        hdu_residual = fits.open(my_outputImageNow + '.residual.fits')[0]
        hdu_peak_selfcal = np.nanmax(hdu_image.data)
        hdu_rms_selfcal = np.nanstd(hdu_residual.data)
        hdu_SNR_selfcal = hdu_peak_selfcal/hdu_rms_selfcal
        hdu_bmaj_selfcal = hdu_image.header['bmaj']*3600.
        hdu_bmin_selfcal = hdu_image.header['bmin']*3600.
        print("... original image")
        print("... intensity peak = " + str(int(hdu_peak_image*1000.)/1000.))
        print("... rms noise level = " + str(int(hdu_rms_image*1000.)/1000.))
        print("... SNR = " + str(int(hdu_SNR_image*1000.)/1000.))
        print("... beam is " + str(int(hdu_bmaj_image*1000.)/1000.) + " x " + str(int(hdu_bmin_image*1000.)/1000.))
        print("... self-calibrated image")
        print("... intensity peak = " + str(int(hdu_peak_selfcal*1000.)/1000.))
        print("... rms noise level = " + str(int(hdu_rms_selfcal*1000.)/1000.))
        print("... SNR = " + str(int(hdu_SNR_selfcal*1000.)/1000.))
        print("... beam is " + str(int(hdu_bmaj_selfcal*1000.)/1000.) + " x " + str(int(hdu_bmin_selfcal*1000.)/1000.))
        hdu_improvement = 100.*(hdu_SNR_selfcal-hdu_SNR_image)/hdu_SNR_image
        hdu_beamIncrease = 100.*(hdu_bmaj_selfcal-hdu_bmaj_image)/hdu_bmaj_image
        print("... improvement of " + str(int(hdu_improvement*1000.)/1000.) + "%")
        print("... beam modified by " + str(int(hdu_beamIncrease*1000.)/1000.) + "%")
        print("... ")
        
        dataResidual, headerResidual = fits.getdata(my_outputImageNow + '.residual.fits', header=True)
        dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
        dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
        print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
        
        # If improvement is less than 7.5 %, stop self-calibrating
        # otherwise, continue self-calibrating
        #
        if (hdu_improvement < 7.5) or (hdu_beamIncrease > 7.5):
                
            print("... stop self-calibration at iteration 1, not enough improvement afterwards!")
            
            # Clean-up directory from not necessary image files
            #
            print("... clean-up some files *.image *.mask *.model *.pb *.psf *.residual *.sumwt")
            os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.image')
            os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.mask')
            os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.model')
            os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.pb')
            os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.psf')
            os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.residual')
            os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.sumwt')
            
            # SPLIT out original ms files for SELFCAL iterations
            #
            print("... SPLIT and RENAME the final self-calibrated ms files")
            for i in range(0, len(my_visFiles)):
                my_runningName = my_visFiles_iter1[i]
                os.system('rm -rf ' + my_runningName[:-27] + '.selfcal.ms.split.cal')
                split(vis = my_visFiles_iter1[i],
                    datacolumn = 'corrected',
                    outputvis = my_runningName[:-27] + '.selfcal.ms.split.cal')
                print("... ... " + my_visFiles[i] + "_selfcal.iter1*")
                os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter1*')
            
            # Create tar file with self-calibrated ms files
            #
            print("Fun starts here ...")
            my_runningDirectoryTMP = os.getcwd()
            os.chdir(str(my_runningPath) + '/almagal/processing/')
            for i in range(0, len(my_visFiles)):
                my_runningName = my_visFiles_iter1[i]
                print(my_visFiles_iter1[i])
                print(my_runningName[len(my_runningPath)+43+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar')
                print(my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal')
                if (my_array == "7M"):
                    os.system('tar -cf ' + my_runningName[len(my_runningPath)+43+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar ' + my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal*')
                if (my_array == "TM2") or (my_array == "TM1"):
                    os.system('tar -cf ' + my_runningName[len(my_runningPath)+44+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar ' + my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal*')
                os.system('rm -rf ' + my_runningName[:-27] + '.selfcal.ms.split.cal*')
            os.chdir(my_runningDirectoryTMP)
            
            # Clean-up directory from not necessary ms files
            #
            print("... clean-up some files")
            for i in range(0, len(my_visFiles)):
                print("... ... " + my_visFiles[i] + "_selfcal.iter2*")
                os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter2*')
            
        else:
            
            # Clean-up directory from not necessary ms files
            #
            print("... clean-up some files")
            for i in range(0, len(my_visFiles)):
                print("... ... " + my_visFiles[i] + "_selfcal.iter1*")
                os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter1*')
            
            # SPLIT out original ms files for SELFCAL iterations
            #
            print("... SPLIT ms files for setting up SELFCAL iterations (ITER 3)")
            my_visFiles_iter3 = []
            for i in range(0, len(my_visFiles)):
                os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter3*')
                split(vis = my_visFiles_iter2[i],
                    datacolumn = 'corrected',
                    outputvis = my_visFiles[i] + '_selfcal.iter3')
                my_visFiles_iter3.append(my_visFiles[i] + '_selfcal.iter3')
            
            # TCLEAN to generate iter3 preliminary image
            #
            my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter3.prelim_clean'
            my_scalesNow = [0, 6, 12]
            my_niterNow = 100000
            my_number, my_unit = separateNumbersUnits(my_threshold)
            my_thresholdNow = str(3.0*dataResidual_MAD) + my_unit
            my_smallscalebiasNow = 0.0
            
            print("... TCLEAN iter 3 prelim_clean image")
            print("... Some parameters are:")
            print("... ... original threshold = " + str(dataResidual_MAD))
            print("... ... used threshold = " + str(my_thresholdNow))
            print("... ... used scales = " + str(my_scalesNow))
            
            os.system('rm -rf ' + my_outputImageNow + '.*')
            tclean(vis = my_visFiles_iter3,
                imagename = my_outputImageNow,
                datacolumn = 'data',
                field = str(my_source),
                stokes = 'I',
                spw = my_spwRanges,
                outframe = 'LSRK',
                restfreq = '',
                specmode = 'mfs',
                imsize = my_imsize,
                cell = my_cell,
                deconvolver = 'multiscale',
                scales = my_scalesNow,
                niter = my_niterNow,
                weighting = my_weighting,
                robust = my_robust,
                usemask = 'auto-multithresh',
                mask = '',
                pbmask = my_pbmask,
                sidelobethreshold = my_sidelobethreshold,
                noisethreshold = my_noisethreshold,
                minbeamfrac =  my_minbeamfrac,
                lownoisethreshold = my_lownoisethreshold,
                negativethreshold = my_negativethreshold,
                gridder = 'standard',
                pblimit = my_pblimit,
                pbcor = False,
                threshold = my_thresholdNow,
                interactive = False,
                restoringbeam = 'common',
                smallscalebias = my_smallscalebiasNow)
            exportfits(imagename = my_outputImageNow + '.image',
                fitsimage = my_outputImageNow + '.image.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.residual',
                fitsimage = my_outputImageNow + '.residual.fits',
                dropdeg = True,
                overwrite = True)
            # Determine intensity peak, rms and SNR levels
            #
            hdu_image = fits.open(my_outputImageNow + '.image.fits')[0]
            hdu_residual = fits.open(my_outputImageNow + '.residual.fits')[0]
            hdu_peak_image = np.nanmax(hdu_image.data)
            hdu_rms_image = np.nanstd(hdu_residual.data)
            hdu_SNR_image = hdu_peak_image/hdu_rms_image
            hdu_bmaj_image = hdu_image.header['bmaj']*3600.
            hdu_bmin_image = hdu_image.header['bmin']*3600.
            print("... intensity peak = " + str(int(hdu_peak_image*1000.)/1000.))
            print("... rms noise level = " + str(int(hdu_rms_image*1000.)/1000.))
            print("... SNR = " + str(int(hdu_SNR_image*1000.)/1000.))
            print("... beam is " + str(int(hdu_bmaj_image*1000.)/1000.) + " x " + str(int(hdu_bmin_image*1000.)/1000.))
            
            # Add model to ms file
            #
            print("... apply FT for iter 3")
            for i in range(0, len(my_visFiles)):
                ft(vis = my_visFiles_iter3[i],
                    field = str(my_source),
                    spw = my_spwRanges[i],
                    model = my_outputImageNow + '.model',
                    usescratch = True)
            
            # Gaincal's
            print("... apply GAINCAL for iter 3")
            for i in range(0, len(my_visFiles)):
                os.system('rm -rf ' + my_visFiles_iter3[i] + '.iter3.selfcal.p3')
                gaincal(vis = my_visFiles_iter3[i],
                    caltable = my_visFiles_iter3[i] + '.iter3.selfcal.p3',
                    spw = my_spwRanges[i],
                    combine = 'spw',
                    solint = 'int',
                    refant = my_refAnts[i],
                    calmode = 'p',
                    gaintype = 'T',
                    minsnr = 5.0)
            
            # Applycal's
            print("... run APPLYCAL for iter 3")
            for i in range(0, len(my_visFiles)):
                applycal(vis = my_visFiles_iter3[i],
                    gaintable = my_visFiles_iter3[i] + '.iter3.selfcal.p3',
                    spwmap = [0, 0, 0, 0])
            
            # TCLEAN to generate selfcal p3 image
            #
            my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter3.selfcal.p3_clean'
            my_scalesNow = [0, 6, 12]
            my_niterNow = 100000
            my_number, my_unit = separateNumbersUnits(my_threshold)
            my_thresholdNow = str(3.0*dataResidual_MAD) + my_unit
            my_smallscalebiasNow = 0.0
            
            print("... TCLEAN iter 3 selfcal p3 image")
            print("... Some parameters are:")
            print("... ... original threshold = " + str(dataResidual_MAD))
            print("... ... used threshold = " + str(my_thresholdNow))
            print("... ... used scales = " + str(my_scalesNow))
            
            os.system('rm -rf ' + my_outputImageNow + '.*')
            tclean(vis = my_visFiles_iter3,
                imagename = my_outputImageNow,
                datacolumn = 'corrected',
                field = str(my_source),
                stokes = 'I',
                spw = my_spwRanges,
                outframe = 'LSRK',
                restfreq = '',
                specmode = 'mfs',
                imsize = my_imsize,
                cell = my_cell,
                deconvolver = 'multiscale',
                scales = my_scalesNow,
                niter = my_niterNow,
                weighting = my_weighting,
                robust = my_robust,
                usemask = 'auto-multithresh',
                mask = '',
                pbmask = my_pbmask,
                sidelobethreshold = my_sidelobethreshold,
                noisethreshold = my_noisethreshold,
                minbeamfrac =  my_minbeamfrac,
                lownoisethreshold = my_lownoisethreshold,
                negativethreshold = my_negativethreshold,
                gridder = 'standard',
                pblimit = my_pblimit,
                pbcor = False,
                threshold = my_thresholdNow,
                interactive = False,
                restoringbeam = 'common',
                smallscalebias = my_smallscalebiasNow)
            exportfits(imagename = my_outputImageNow + '.image',
                fitsimage = my_outputImageNow + '.image.fits',
                dropdeg = True,
                overwrite = True)
            # Calculate the median absolute deviation of the residual
            exportfits(imagename = my_outputImageNow + '.residual',
                fitsimage = my_outputImageNow + '.residual.fits',
                dropdeg = True,
                overwrite = True)
            # Determine intensity peak, rms and SNR levels
            #
            hdu_image = fits.open(my_outputImageNow + '.image.fits')[0]
            hdu_residual = fits.open(my_outputImageNow + '.residual.fits')[0]
            hdu_peak_selfcal = np.nanmax(hdu_image.data)
            hdu_rms_selfcal = np.nanstd(hdu_residual.data)
            hdu_SNR_selfcal = hdu_peak_selfcal/hdu_rms_selfcal
            hdu_bmaj_selfcal = hdu_image.header['bmaj']*3600.
            hdu_bmin_selfcal = hdu_image.header['bmin']*3600.
            print("... original image")
            print("... intensity peak = " + str(int(hdu_peak_image*1000.)/1000.))
            print("... rms noise level = " + str(int(hdu_rms_image*1000.)/1000.))
            print("... SNR = " + str(int(hdu_SNR_image*1000.)/1000.))
            print("... beam is " + str(int(hdu_bmaj_image*1000.)/1000.) + " x " + str(int(hdu_bmin_image*1000.)/1000.))
            print("... self-calibrated image")
            print("... intensity peak = " + str(int(hdu_peak_selfcal*1000.)/1000.))
            print("... rms noise level = " + str(int(hdu_rms_selfcal*1000.)/1000.))
            print("... SNR = " + str(int(hdu_SNR_selfcal*1000.)/1000.))
            print("... beam is " + str(int(hdu_bmaj_selfcal*1000.)/1000.) + " x " + str(int(hdu_bmin_selfcal*1000.)/1000.))
            hdu_improvement = 100.*(hdu_SNR_selfcal-hdu_SNR_image)/hdu_SNR_image
            hdu_beamIncrease = 100.*(hdu_bmaj_selfcal-hdu_bmaj_image)/hdu_bmaj_image
            print("... improvement of " + str(int(hdu_improvement*1000.)/1000.) + "%")
            print("... beam modified by " + str(int(hdu_beamIncrease*1000.)/1000.) + "%")
            print("... ")
            
            dataResidual, headerResidual = fits.getdata(my_outputImageNow + '.residual.fits', header=True)
            dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
            dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
            print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
            
            # If improvement is less than 7.5 %, stop self-calibrating
            # otherwise, continue self-calibrating
            #
            if (hdu_improvement < 7.5) or (hdu_beamIncrease > 7.5):
                
                print("... stop self-calibration at iteration 2, not enough improvement afterwards!")
                
                # Clean-up directory from not necessary image files
                #
                print("... clean-up some files *.image *.mask *.model *.pb *.psf *.residual *.sumwt")
                os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.image')
                os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.mask')
                os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.model')
                os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.pb')
                os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.psf')
                os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.residual')
                os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.sumwt')
                
                # SPLIT out original ms files for SELFCAL iterations
                #
                print("... SPLIT and RENAME the final self-calibrated ms files")
                for i in range(0, len(my_visFiles)):
                    my_runningName = my_visFiles_iter2[i]
                    os.system('rm -rf ' + my_runningName[:-27] + '.selfcal.ms.split.cal')
                    split(vis = my_visFiles_iter2[i],
                        datacolumn = 'corrected',
                        outputvis = my_runningName[:-27] + '.selfcal.ms.split.cal')
                    print("... ... " + my_visFiles[i] + "_selfcal.iter2*")
                    os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter2*')
                
                # Create tar file with self-calibrated ms files
                #
                print("Fun starts here ...")
                my_runningDirectoryTMP = os.getcwd()
                os.chdir(str(my_runningPath) + '/almagal/processing/')
                for i in range(0, len(my_visFiles)):
                    my_runningName = my_visFiles_iter2[i]
                    print(my_visFiles_iter2[i])
                    print(my_runningName[len(my_runningPath)+43+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar')
                    print(my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal')
                    if (my_array == "7M"):
                        os.system('tar -cf ' + my_runningName[len(my_runningPath)+43+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar ' + my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal*')
                    if (my_array == "TM2") or (my_array == "TM1"):
                        os.system('tar -cf ' + my_runningName[len(my_runningPath)+44+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar ' + my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal*')
                    os.system('rm -rf ' + my_runningName[:-27] + '.selfcal.ms.split.cal*')
                os.chdir(my_runningDirectoryTMP)

                # Clean-up directory from not necessary ms files
                #
                print("... clean-up some files")
                for i in range(0, len(my_visFiles)):
                    print("... ... " + my_visFiles[i] + "_selfcal.iter3*")
                    os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter3*')
                
            else:
                
                # Clean-up directory from not necessary ms files
                #
                print("... clean-up some files")
                for i in range(0, len(my_visFiles)):
                    print("... ... " + my_visFiles[i] + "_selfcal.iter2*")
                    os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter2*')
                
                # SPLIT out original ms files for SELFCAL iterations
                #
                print("... SPLIT ms files for setting up SELFCAL iterations (ITER 4)")
                my_visFiles_iter4 = []
                for i in range(0, len(my_visFiles)):
                    os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter4*')
                    split(vis = my_visFiles_iter3[i],
                        datacolumn = 'corrected',
                        outputvis = my_visFiles[i] + '_selfcal.iter4')
                    my_visFiles_iter4.append(my_visFiles[i] + '_selfcal.iter4')
                
                # TCLEAN to generate iter4 preliminary image
                #
                my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter4.prelim_clean'
                my_scalesNow = [0, 6, 12]
                my_niterNow = 100000
                my_number, my_unit = separateNumbersUnits(my_threshold)
                my_thresholdNow = str(2.0*dataResidual_MAD) + my_unit
                my_smallscalebiasNow = 0.0
                
                print("... TCLEAN iter 4 prelim_clean image")
                print("... Some parameters are:")
                print("... ... original threshold = " + str(dataResidual_MAD))
                print("... ... used threshold = " + str(my_thresholdNow))
                print("... ... used scales = " + str(my_scalesNow))
                
                os.system('rm -rf ' + my_outputImageNow + '.*')
                tclean(vis = my_visFiles_iter4,
                    imagename = my_outputImageNow,
                    datacolumn = 'data',
                    field = str(my_source),
                    stokes = 'I',
                    spw = my_spwRanges,
                    outframe = 'LSRK',
                    restfreq = '',
                    specmode = 'mfs',
                    imsize = my_imsize,
                    cell = my_cell,
                    deconvolver = 'multiscale',
                    scales = my_scalesNow,
                    niter = my_niterNow,
                    weighting = my_weighting,
                    robust = my_robust,
                    usemask = 'auto-multithresh',
                    mask = '',
                    pbmask = my_pbmask,
                    sidelobethreshold = my_sidelobethreshold,
                    noisethreshold = my_noisethreshold,
                    minbeamfrac =  my_minbeamfrac,
                    lownoisethreshold = my_lownoisethreshold,
                    negativethreshold = my_negativethreshold,
                    gridder = 'standard',
                    pblimit = my_pblimit,
                    pbcor = False,
                    threshold = my_thresholdNow,
                    interactive = False,
                    restoringbeam = 'common',
                    smallscalebias = my_smallscalebiasNow)
                exportfits(imagename = my_outputImageNow + '.image',
                    fitsimage = my_outputImageNow + '.image.fits',
                    dropdeg = True,
                    overwrite = True)
                exportfits(imagename = my_outputImageNow + '.residual',
                    fitsimage = my_outputImageNow + '.residual.fits',
                    dropdeg = True,
                    overwrite = True)
                # Determine intensity peak, rms and SNR levels
                #
                hdu_image = fits.open(my_outputImageNow + '.image.fits')[0]
                hdu_residual = fits.open(my_outputImageNow + '.residual.fits')[0]
                hdu_peak_image = np.nanmax(hdu_image.data)
                hdu_rms_image = np.nanstd(hdu_residual.data)
                hdu_SNR_image = hdu_peak_image/hdu_rms_image
                hdu_bmaj_image = hdu_image.header['bmaj']*3600.
                hdu_bmin_image = hdu_image.header['bmin']*3600.
                print("... intensity peak = " + str(int(hdu_peak_image*1000.)/1000.))
                print("... rms noise level = " + str(int(hdu_rms_image*1000.)/1000.))
                print("... SNR = " + str(int(hdu_SNR_image*1000.)/1000.))
                print("... beam is " + str(int(hdu_bmaj_image*1000.)/1000.) + " x " + str(int(hdu_bmin_image*1000.)/1000.))
                
                # Add model to ms file
                #
                print("... apply FT for iter 4")
                for i in range(0, len(my_visFiles)):
                    ft(vis = my_visFiles_iter4[i],
                        field = str(my_source),
                        spw = my_spwRanges[i],
                        model = my_outputImageNow + '.model',
                        usescratch = True)
                
                # Gaincal's
                print("... apply GAINCAL for iter 4")
                for i in range(0, len(my_visFiles)):
                    os.system('rm -rf ' + my_visFiles_iter4[i] + '.iter4.selfcal.p4')
                    gaincal(vis = my_visFiles_iter4[i],
                        caltable = my_visFiles_iter4[i] + '.iter4.selfcal.p4',
                        spw = my_spwRanges[i],
                        combine = 'spw',
                        solint = 'int',
                        refant = my_refAnts[i],
                        calmode = 'p',
                        gaintype = 'T',
                        minsnr = 5.0)
                
                # Applycal's
                print("... run APPLYCAL for iter 4")
                for i in range(0, len(my_visFiles)):
                    applycal(vis = my_visFiles_iter4[i],
                        gaintable = my_visFiles_iter4[i] + '.iter4.selfcal.p4',
                        spwmap = [0, 0, 0, 0])
                
                # TCLEAN to generate selfcal p4 image
                #
                my_outputImageNow = str(my_runningPath) + '/almagal/selfcalibration/images/'+str(my_source)+'_'+str(my_array)+'.iter4.selfcal.p4_clean'
                my_scalesNow = [0, 6, 12]
                my_niterNow = 100000
                my_number, my_unit = separateNumbersUnits(my_threshold)
                my_thresholdNow = str(2.0*dataResidual_MAD) + my_unit
                my_smallscalebiasNow = 0.0
                
                print("... TCLEAN iter 4 selfcal p4 image")
                print("... Some parameters are:")
                print("... ... original threshold = " + str(dataResidual_MAD))
                print("... ... used threshold = " + str(my_thresholdNow))
                print("... ... used scales = " + str(my_scalesNow))
                
                os.system('rm -rf ' + my_outputImageNow + '.*')
                tclean(vis = my_visFiles_iter4,
                    imagename = my_outputImageNow,
                    datacolumn = 'corrected',
                    field = str(my_source),
                    stokes = 'I',
                    spw = my_spwRanges,
                    outframe = 'LSRK',
                    restfreq = '',
                    specmode = 'mfs',
                    imsize = my_imsize,
                    cell = my_cell,
                    deconvolver = 'multiscale',
                    scales = my_scalesNow,
                    niter = my_niterNow,
                    weighting = my_weighting,
                    robust = my_robust,
                    usemask = 'auto-multithresh',
                    mask = '',
                    pbmask = my_pbmask,
                    sidelobethreshold = my_sidelobethreshold,
                    noisethreshold = my_noisethreshold,
                    minbeamfrac =  my_minbeamfrac,
                    lownoisethreshold = my_lownoisethreshold,
                    negativethreshold = my_negativethreshold,
                    gridder = 'standard',
                    pblimit = my_pblimit,
                    pbcor = False,
                    threshold = my_thresholdNow,
                    interactive = False,
                    restoringbeam = 'common',
                    smallscalebias = my_smallscalebiasNow)
                exportfits(imagename = my_outputImageNow + '.image',
                    fitsimage = my_outputImageNow + '.image.fits',
                    dropdeg = True,
                    overwrite = True)
                # Calculate the median absolute deviation of the residual
                exportfits(imagename = my_outputImageNow + '.residual',
                    fitsimage = my_outputImageNow + '.residual.fits',
                    dropdeg = True,
                    overwrite = True)
                # Determine intensity peak, rms and SNR levels
                #
                hdu_image = fits.open(my_outputImageNow + '.image.fits')[0]
                hdu_residual = fits.open(my_outputImageNow + '.residual.fits')[0]
                hdu_peak_selfcal = np.nanmax(hdu_image.data)
                hdu_rms_selfcal = np.nanstd(hdu_residual.data)
                hdu_SNR_selfcal = hdu_peak_selfcal/hdu_rms_selfcal
                hdu_bmaj_selfcal = hdu_image.header['bmaj']*3600.
                hdu_bmin_selfcal = hdu_image.header['bmin']*3600.
                print("... original image")
                print("... intensity peak = " + str(int(hdu_peak_image*1000.)/1000.))
                print("... rms noise level = " + str(int(hdu_rms_image*1000.)/1000.))
                print("... SNR = " + str(int(hdu_SNR_image*1000.)/1000.))
                print("... beam is " + str(int(hdu_bmaj_image*1000.)/1000.) + " x " + str(int(hdu_bmin_image*1000.)/1000.))
                print("... self-calibrated image")
                print("... intensity peak = " + str(int(hdu_peak_selfcal*1000.)/1000.))
                print("... rms noise level = " + str(int(hdu_rms_selfcal*1000.)/1000.))
                print("... SNR = " + str(int(hdu_SNR_selfcal*1000.)/1000.))
                print("... beam is " + str(int(hdu_bmaj_selfcal*1000.)/1000.) + " x " + str(int(hdu_bmin_selfcal*1000.)/1000.))
                hdu_improvement = 100.*(hdu_SNR_selfcal-hdu_SNR_image)/hdu_SNR_image
                hdu_beamIncrease = 100.*(hdu_bmaj_selfcal-hdu_bmaj_image)/hdu_bmaj_image
                print("... improvement of " + str(int(hdu_improvement*1000.)/1000.) + "%")
                print("... beam modified by " + str(int(hdu_beamIncrease*1000.)/1000.) + "%")
                print("... ")
                
                dataResidual, headerResidual = fits.getdata(my_outputImageNow + '.residual.fits', header=True)
                dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
                dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
                print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
            
                # If improvement is less than 7.5 %, stop self-calibrating
                # otherwise, continue self-calibrating
                #
                if (hdu_improvement < 7.5) or (hdu_beamIncrease > 7.5):
                    
                    print("... stop self-calibration at iteration 3, not enough improvement afterwards!")
                    
                    # Clean-up directory from not necessary image files
                    #
                    print("... clean-up some files *.image *.mask *.model *.pb *.psf *.residual *.sumwt")
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.image')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.mask')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.model')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.pb')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.psf')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.residual')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.sumwt')
                    
                    # SPLIT out original ms files for SELFCAL iterations
                    #
                    print("... SPLIT and RENAME the final self-calibrated ms files")
                    for i in range(0, len(my_visFiles)):
                        my_runningName = my_visFiles_iter3[i]
                        os.system('rm -rf ' + my_runningName[:-27] + '.selfcal.ms.split.cal')
                        split(vis = my_visFiles_iter3[i],
                            datacolumn = 'corrected',
                            outputvis = my_runningName[:-27] + '.selfcal.ms.split.cal')
                        print("... ... " + my_visFiles[i] + "_selfcal.iter3*")
                        os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter3*')
                    
                    # Create tar file with self-calibrated ms files
                    #
                    print("Fun starts here ...")
                    my_runningDirectoryTMP = os.getcwd()
                    os.chdir(str(my_runningPath) + '/almagal/processing/')
                    for i in range(0, len(my_visFiles)):
                        my_runningName = my_visFiles_iter3[i]
                        print(my_visFiles_iter3[i])
                        print(my_runningName[len(my_runningPath)+43+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar')
                        print(my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal')
                        if (my_array == "7M"):
                            os.system('tar -cf ' + my_runningName[len(my_runningPath)+43+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar ' + my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal*')
                        if (my_array == "TM2") or (my_array == "TM1"):
                            os.system('tar -cf ' + my_runningName[len(my_runningPath)+44+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar ' + my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal*')
                        os.system('rm -rf ' + my_runningName[:-27] + '.selfcal.ms.split.cal*')
                    os.chdir(my_runningDirectoryTMP)

                    # Clean-up directory from not necessary ms files
                    #
                    print("... clean-up some files")
                    for i in range(0, len(my_visFiles)):
                        print("... ... " + my_visFiles[i] + "_selfcal.iter4*")
                        os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter4*')
                    
                else:
                    
                    print("... stop self-calibration at iteration 4, the last one!")
                    
                    # Clean-up directory from not necessary ms files
                    #
                    print("... clean-up some files")
                    for i in range(0, len(my_visFiles)):
                        print("... ... " + my_visFiles[i] + "_selfcal.iter3*")
                        os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter3*')
                    
                    # Clean-up directory from not necessary image files
                    #
                    print("... clean-up some files *.image *.mask *.model *.pb *.psf *.residual *.sumwt")
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.image')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.mask')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.model')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.pb')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.psf')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.residual')
                    os.system('rm -rf ' + str(my_runningPath) + '/almagal/selfcalibration/images/*.sumwt')
                
                    # SPLIT out original ms files for SELFCAL iterations
                    #
                    print("... SPLIT and RENAME the final self-calibrated ms files")
                    for i in range(0, len(my_visFiles)):
                        my_runningName = my_visFiles_iter4[i]
                        os.system('rm -rf ' + my_runningName[:-27] + '.selfcal.ms.split.cal')
                        split(vis = my_visFiles_iter4[i],
                            datacolumn = 'corrected',
                            outputvis = my_runningName[:-27] + '.selfcal.ms.split.cal')
                        print("... ... " + my_visFiles[i] + "_selfcal.iter4*")
                        os.system('rm -rf ' + my_visFiles[i] + '_selfcal.iter4*')
                    
                    ## Re-name self-calibrated ms files
                    ##        
                    #print("... re-name final self-calibrated ms files")
                    #for i in range(0, len(my_visFiles)):
                    #    my_runningName = my_visFiles_iter4[i]
                    #    os.system('mv ' + my_runningName + ' ' + my_runningName[:-27] + '.selfcal.ms.split.cal')
                    #    my_runningName = my_visFiles_iter4[i] + '.flagversions'
                    #    os.system('mv ' + my_runningName + ' ' + my_runningName[:-40] + '.selfcal.ms.split.cal.flagversions')
                    #    os.system('rm -rf ' + my_visFiles_iter4[i] + '.iter4.selfcal.p4')
                    
                    # Create tar file with self-calibrated ms files
                    #
                    print("Fun starts here ...")
                    my_runningDirectoryTMP = os.getcwd()
                    os.chdir(str(my_runningPath) + '/almagal/processing/')
                    for i in range(0, len(my_visFiles)):
                        my_runningName = my_visFiles_iter4[i]
                        print(my_visFiles_iter4[i])
                        print(my_runningName[len(my_runningPath)+43+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar')
                        print(my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal')
                        if (my_array == "7M"):
                            os.system('tar -cf ' + my_runningName[len(my_runningPath)+43+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar ' + my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal*')
                        if (my_array == "TM2") or (my_array == "TM1"):
                            os.system('tar -cf ' + my_runningName[len(my_runningPath)+44+len(my_source)+22:-27] + '.selfcal.ms.split.cal.tar ' + my_runningName[len(my_runningPath)+20:-27] + '.selfcal.ms.split.cal*')
                        os.system('rm -rf ' + my_runningName[:-27] + '.selfcal.ms.split.cal*')
                    os.chdir(my_runningDirectoryTMP)


def my_searchRefAnt(my_visfile):
    
    """
    help
    """
    
    print('... searching for refAnt')
    msmd.open(my_visfile)
    number_of_antennas = msmd.nantennas()
    print('... number of antennas ' + str(number_of_antennas))
    my_antennaCoordinatesList = []
    my_antennaLongsList = []
    my_antennaLatsList = []
    my_antennaNamesList = []
    for j in range(0, number_of_antennas):
        my_antennaCoordinatesList.append((msmd.antennaoffset(j)['longitude offset']['value'], msmd.antennaoffset(j)['latitude offset']['value']))
        my_antennaLongsList.append(msmd.antennaoffset(j)['longitude offset']['value'])
        my_antennaLatsList.append(msmd.antennaoffset(j)['latitude offset']['value'])
        my_antennaNamesList.append(msmd.antennanames(j)[0])
    my_antennaCoordinates = np.array(my_antennaCoordinatesList)
    my_antennaLongs = np.array(my_antennaLongsList)
    my_antennaLats = np.array(my_antennaLatsList)
    my_antennaNames = np.array(my_antennaNamesList)
    msmd.done()
    my_antennaCenter = np.array((np.mean(my_antennaLongs), np.mean(my_antennaLats)))
   
    distances = np.linalg.norm(my_antennaCoordinates-my_antennaCenter, axis=1)
    my_min_index = np.argmin(distances)
    print(my_min_index)
    print(f"the closest point is {my_antennaCoordinates[my_min_index]}, at a distance of {distances[my_min_index]}")

    my_refAnt = my_antennaNames[my_min_index]
    print(my_refAnt)
    
    return my_refAnt


########################################################################
#
# STEP 0: 
# Self-calibration
#
mystep = 0
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Self-calibration, step ' + str(mystep))
    
    my_functionSelfCalibration('7M', my_source)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/selfcalibrated/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 1: 
# Self-calibration
#
mystep = 1
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Self-calibration, step ' + str(mystep))
    
    my_functionSelfCalibration('TM2', my_source)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/selfcalibrated/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 2: 
# Self-calibration
#
mystep = 2
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Self-calibration, step ' + str(mystep))
    
    my_functionSelfCalibration('TM1', my_source)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/selfcalibrated/worked_" + mycurrentstep + ".txt")
