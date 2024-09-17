# This script runs the ALMAGAL joint deconvolution script for continuum
#
# This is a template/master script that is updated when running:
# > python createIndividual_scriptForJointDeconvolution.py
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
step_title = {0: 'Create joint-deconvolved continuum image',
              1: 'Combine images using FEATHER'}
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
def my_functionCreateChunks(my_numberOfChunks, my_spw):
    
    """
    help
    
    my_numberOfChunks is fixed to 30 for the 7M+TM2+TM1
    
    """
    
    if (os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_7M.txt') == False) or (os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_TM2.txt') == False) or (os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_TM1.txt') == False):
        
        print("... There seems to be something wrong with the data!")

        if os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_7M.txt') == False:
            print("... CAREFUL! channelsForEachSPW_7M.txt does not exist!")
        if os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_TM2.txt') == False:
            print("... CAREFUL! channelsForEachSPW_TM2.txt does not exist!")
        if os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_TM1.txt') == False:
            print("... CAREFUL! channelsForEachSPW_TM1.txt does not exist!")
    
    else:
        
        print("... Define starting channels and number of channels for each chunk")
        
        print("... Reading information from " + str(my_runningPath)+'/almagal/channelsForEachSPW_7M.txt')        
        lines = [line.rstrip('\n') for line in open(str(my_runningPath)+'/almagal/channelsForEachSPW_7M.txt')]
        my_channelsForEachSPW_7M = []
        for line in lines:
            my_channelsForEachSPW_7M.append(line)
        my_channelsForSPW0_7M = float(my_channelsForEachSPW_7M[0])
        my_channelsForSPW1_7M = float(my_channelsForEachSPW_7M[1])
        my_channelsForSPW2_7M = float(my_channelsForEachSPW_7M[2])
        my_channelsForSPW3_7M = float(my_channelsForEachSPW_7M[3])
        
        print("... Reading information from " + str(my_runningPath)+'/almagal/channelsForEachSPW_TM2.txt')        
        lines = [line.rstrip('\n') for line in open(str(my_runningPath)+'/almagal/channelsForEachSPW_TM2.txt')]
        my_channelsForEachSPW_TM2 = []
        for line in lines:
            my_channelsForEachSPW_TM2.append(line)
        my_channelsForSPW0_TM2 = float(my_channelsForEachSPW_TM2[0])
        my_channelsForSPW1_TM2 = float(my_channelsForEachSPW_TM2[1])
        my_channelsForSPW2_TM2 = float(my_channelsForEachSPW_TM2[2])
        my_channelsForSPW3_TM2 = float(my_channelsForEachSPW_TM2[3])
        
        print("... Reading information from " + str(my_runningPath)+'/almagal/channelsForEachSPW_TM1.txt')        
        lines = [line.rstrip('\n') for line in open(str(my_runningPath)+'/almagal/channelsForEachSPW_TM1.txt')]
        my_channelsForEachSPW_TM1 = []
        for line in lines:
            my_channelsForEachSPW_TM1.append(line)
        my_channelsForSPW0_TM1 = float(my_channelsForEachSPW_TM1[0])
        my_channelsForSPW1_TM1 = float(my_channelsForEachSPW_TM1[1])
        my_channelsForSPW2_TM1 = float(my_channelsForEachSPW_TM1[2])
        my_channelsForSPW3_TM1 = float(my_channelsForEachSPW_TM1[3])
        
        # Create variables to use when cleaning the cube in chunks
        my_numberOfChunks = 30
        my_chunkNameList = range(1, my_numberOfChunks+1)
        
        # for spw 0
        if my_spw == 0:
            my_startingStep = 2
            my_startingChannel = 12
            my_numberOfChannels = 128
            my_currentStepList = []
            my_startingChannelList = []
            my_numberOfChannelsList = []
            for i in range(0, my_numberOfChunks):
                my_currentStepList.append('step'+str(my_startingStep+i))
                my_startingChannelList.append(my_startingChannel+i*my_numberOfChannels)
                if i != my_numberOfChunks-1:
                    my_numberOfChannelsList.append(my_numberOfChannels)
                if i == my_numberOfChunks-1:
                    my_lastSetOfChannels = my_channelsForSPW0_7M-(my_startingChannel+i*my_numberOfChannels)-10
                    my_numberOfChannelsList.append(int(my_lastSetOfChannels))
        
        # for spw 1
        if my_spw == 1:
            my_startingStep = 40
            my_startingChannel = 12
            my_numberOfChannels = 128
            my_currentStepList = []
            my_startingChannelList = []
            my_numberOfChannelsList = []
            for i in range(0, my_numberOfChunks):
                my_currentStepList.append('step'+str(my_startingStep+i))
                my_startingChannelList.append(my_startingChannel+i*my_numberOfChannels)
                if i != my_numberOfChunks-1:
                    my_numberOfChannelsList.append(my_numberOfChannels)
                if i == my_numberOfChunks-1:
                    my_lastSetOfChannels = my_channelsForSPW0_7M-(my_startingChannel+i*my_numberOfChannels)-10
                    my_numberOfChannelsList.append(int(my_lastSetOfChannels))
        
        # for spw 2
        if my_spw == 2:
            my_startingStep = 78
            my_startingChannel = 12
            my_numberOfChannels = 128
            my_currentStepList = []
            my_startingChannelList = []
            my_numberOfChannelsList = []
            for i in range(0, my_numberOfChunks):
                my_currentStepList.append('step'+str(my_startingStep+i))
                my_startingChannelList.append(my_startingChannel+i*my_numberOfChannels)
                if i != my_numberOfChunks-1:
                    my_numberOfChannelsList.append(my_numberOfChannels)
                if i == my_numberOfChunks-1:
                    my_lastSetOfChannels = my_channelsForSPW0_7M-(my_startingChannel+i*my_numberOfChannels)-10
                    my_numberOfChannelsList.append(int(my_lastSetOfChannels))
        
        # for spw 3
        if my_spw == 3:
            my_startingStep = 116
            my_startingChannel = 12
            my_numberOfChannels = 128
            my_currentStepList = []
            my_startingChannelList = []
            my_numberOfChannelsList = []
            for i in range(0, my_numberOfChunks):
                my_currentStepList.append('step'+str(my_startingStep+i))
                my_startingChannelList.append(my_startingChannel+i*my_numberOfChannels)
                if i != my_numberOfChunks-1:
                    my_numberOfChannelsList.append(my_numberOfChannels)
                if i == my_numberOfChunks-1:
                    my_lastSetOfChannels = my_channelsForSPW0_7M-(my_startingChannel+i*my_numberOfChannels)-10
                    my_numberOfChannelsList.append(int(my_lastSetOfChannels))
        
        return my_chunkNameList, my_currentStepList, my_startingChannelList, my_numberOfChannelsList


def my_functionGetCellsizeImsize(my_telescope, my_source):
    
    """
    help
    """
    
    if os.path.isfile(str(my_runningPath) + '/almagal/tcleanParameters.txt') == False:
        
        # Determine the tclean parameters for continuum joint-deconvolution
        #
        my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold, my_gridder = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
        
        # Run TCLEAN task
        #
        
        # Dirty TCLEAN run:
        #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
        #  Key parameters to play with are:
        #   - threshold: right now the value corresponds to 2 times the final threshold
        #   - niter: set to 0
        my_niterNow = 0
        my_number, my_unit = separateNumbersUnits(my_threshold)
        my_thresholdNow = str(2.*my_number) + my_unit
        my_outputImageNow = my_outputImage + '_dirty'
        my_scalesNow = my_scales
        my_smallscalebiasNow = 0.0
        print("Producing dirty image")
        print("... some parameters are")
        print("... ... threshold (from pipeline) = " + str(my_threshold))
        print("... ... threshold (used in current tclean) = " + str(my_thresholdNow))
        print("... ... scales = " + str(my_scalesNow))
        tclean(vis = my_visfilestoclean,
            imagename = my_outputImageNow,
            field = my_source,
            stokes = 'I',
            spw = my_freqs,
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
            pbmask = my_pbmask,
            sidelobethreshold = my_sidelobethreshold,
            noisethreshold = my_noisethreshold,
            minbeamfrac =  my_minbeamfrac,
            lownoisethreshold = my_lownoisethreshold,
            negativethreshold = my_negativethreshold,
            gridder = my_gridder,
            pblimit = my_pblimit,
            pbcor = True,
            threshold = my_thresholdNow,
            interactive = False,
            restoringbeam = 'common',
            smallscalebias = my_smallscalebiasNow)
        
        # Read information of the clean-beam
        #
        ## for Python 2 (CASA 5)
        #my_bmaj = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmaj').items()[0][1]
        #my_bmin = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmin').items()[0][1]
        #my_bpa = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bpa').items()[0][1]
        #my_pxsize = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='cdelt2').items()[0][1]
        #my_imsize = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='naxis2').items()[0][1]
        ## for Python 3 (CASA 6)
        my_bmaj = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmaj')['value']
        my_bmin = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmin')['value']
        my_bpa = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bpa')['value']
        my_pxsize = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='cdelt2')['value']
        my_pxsize = my_pxsize*360.*3600./(2.*np.pi)
        my_imsize = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='shape')[0]
        
        print("Pixel size is " + str(my_pxsize) + " and image size is " + str(my_imsize))
        my_nbpixels = my_bmin/my_pxsize
        print("Number of pixels per beam is " + str(my_nbpixels))
        
        if (my_nbpixels > 6.):
            tmp_imageSize = (my_imsize*my_pxsize)
            my_pxsize = round(1000.*(my_bmin/6.))/1000.
            my_imsize = round((tmp_imageSize/my_pxsize)/10.)*10.
        
        print("New pixel size is " + str(my_pxsize) + " and image size is " + str(my_imsize))
        my_nbpixels = my_bmin/my_pxsize
        print("Number of pixels per beam is " + str(my_nbpixels))
        
        with open(str(my_runningPath)+'/almagal/tcleanParameters.txt', 'w') as f:
            f.write(str(my_pxsize))
            f.write('\n')
            f.write(str(my_imsize))
            f.write('\n')
            f.write(str(my_nbpixels))
            f.write('\n')
        
        # Clean-up created files
        os.system('rm -rf ' + my_outputImageNow + '.*')
        
        return my_pxsize, my_imsize, my_nbpixels
        
    else:
        
        print("Reading information from " + str(my_runningPath)+'/almagal/tcleanParameters.txt')
        
        lines = [line.rstrip('\n') for line in open(str(my_runningPath)+'/almagal/tcleanParameters.txt')]
        my_tcleanParameters = []
        for line in lines:
            my_tcleanParameters.append(line)
        my_pxsize = float(my_tcleanParameters[0])
        my_imsize = int(float(my_tcleanParameters[1]))
        my_nbpixels = float(my_tcleanParameters[2])
        
        print("Pixel size is " + str(my_pxsize) + " and image size is " + str(my_imsize))
        print("Number of pixels per beam is " + str(my_nbpixels))
        
        return my_pxsize, my_imsize, my_nbpixels
    

def my_iCounter(i):
    
    if i < 10:
        itext = "00"+str(i)
    if i >= 10 and i < 100:
        itext = "0"+str(i)
    if i >= 100:
        itext = +str(i)
    
    return itext


def my_functionJointDeconvolutionContinuum(my_telescope, my_source):
    
    """
    help
    """
    keepIntermediates = False
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold, my_gridder = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    my_cell, my_imsize, my_nbpixels = my_functionGetCellsizeImsize(my_telescope, my_source)
    
    ##########################################################################
    #
    # Imaging is divided in different phases depending on the array:
    #
    #  7M:       tclean with auto-multithresh, down to 4xrms from MAD_residual
    #  TM2:      tclean with auto-multithresh, down to 4xrms from MAD_residual
    #  TM1:      tclean with auto-multithresh, down to 4xrms from MAD_residual
    #  7MTM2:    tclean with auto-multithresh, down to 4xrms from MAD_residual
    #            followed by adding 7M mask
    #  TM2TM1:   tclean with auto-multithresh, down to 4xrms from MAD_residual
    #            followed by adding 7M mask
    #  7MTM2TM1: tclean with auto-multithresh, down to 4xrms from MAD_residual
    #            followed by adding TM2 mask
    #            followed by adding 7M mask
    #
    #  all of them followed by adding a PB mask down to 4xrms from MAD_residual
    #  and then another PB mask down to 2xrms from MAD_residual
    #
    ##########################################################################
    #
    # Phase 1: Run TCLEAN task (auto-multithresh with no initial mask)
    #
    # First run of tclean to set up a starting mask and residual image
    #
    # Define iteration name for output files
    #
    itext = my_iCounter(0)
    
    my_niterNow = 100
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(4.0*my_number) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    
    print("... Producing TCLEAN image - multiscale process (source " + str(my_source) + " step " + str(itext) + ")")
    print("... Some parameters are:")
    print("... ... pipeline threshold = " + str(my_threshold))
    print("... ... pipeline niter = " + str(my_niter))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    print("... ... used niter = " + str(my_niterNow))
    
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImageNow,
        field = my_source,
        stokes = 'I',
        spw = my_freqs,
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
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = my_gridder,
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
    # Keep intermediate products (for developing and testing) or skip them (saving only the necessary ones)
    #
    if (keepIntermediates == True):
        exportfits(imagename = my_outputImageNow + '.image',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.image.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.mask',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.mask.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.model',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
            dropdeg = True,
            overwrite = True)
    else:
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.model',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
            dropdeg = True,
            overwrite = True)
    
    #  Calculate the flux contained in the CLEANed model (MOD) and the noise in the residuals (MAD)
    #
    os.system('rm -rf ' + my_outputImageNow + '_MOD.model.fits')
    os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.model.fits ' + my_outputImageNow + '_MOD.model.fits')
    dataModel, headerModel = fits.getdata(my_outputImageNow + '_MOD.model.fits', header=True)
    dataModel_MOD = np.nansum(dataModel)
    print("... ... Flux contained in the model = " + str(dataModel_MOD))
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.model.fits')
    #
    os.system('rm -rf ' + my_outputImageNow + '_MAD.residual.fits')
    os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits ' + my_outputImageNow + '_MAD.residual.fits')
    dataResidual, headerResidual = fits.getdata(my_outputImageNow + '_MAD.residual.fits', header=True)
    dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
    dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
    print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits')
    
    itext = my_iCounter(1)
    
    my_niterNow = 500
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(4.0*dataResidual_MAD) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    
    print("... Producing TCLEAN image - multiscale process (source " + str(my_source) + " step " + str(itext) + ")")
    print("... Some parameters are:")
    print("... ... pipeline threshold = " + str(my_threshold))
    print("... ... pipeline niter = " + str(my_niter))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    print("... ... used niter = " + str(my_niterNow))
    
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImageNow,
        field = my_source,
        stokes = 'I',
        spw = my_freqs,
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
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = my_gridder,
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
    # Keep intermediate products (for developing and testing) or skip them (saving only the necessary ones)
    #
    if (keepIntermediates == True):
        exportfits(imagename = my_outputImageNow + '.image',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.image.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.mask',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.mask.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.model',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
            dropdeg = True,
            overwrite = True)
    else:
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.model',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
            dropdeg = True,
            overwrite = True)
    
    #  Calculate the flux contained in the CLEANed model (MOD) and the noise in the residuals (MAD)
    #
    os.system('rm -rf ' + my_outputImageNow + '_MOD.model.fits')
    os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.model.fits ' + my_outputImageNow + '_MOD.model.fits')
    dataModel, headerModel = fits.getdata(my_outputImageNow + '_MOD.model.fits', header=True)
    dataModel_MOD = np.nansum(dataModel)
    print("... ... Flux contained in the model = " + str(dataModel_MOD))
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.model.fits')
    #
    os.system('rm -rf ' + my_outputImageNow + '_MAD.residual.fits')
    os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits ' + my_outputImageNow + '_MAD.residual.fits')
    dataResidual, headerResidual = fits.getdata(my_outputImageNow + '_MAD.residual.fits', header=True)
    dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
    dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
    print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits')
    
    # Iterate multiscale CLEANing until reaching a non-changing (< 1%) flux model
    # or until the residuals get smaller than 1 x theoretical noise
    #
    # Reset some variables for the loop
    #
    MOD_difference = 1000.0
    MAD_difference = 1000.0
    i = 2
    
    while MOD_difference > 1.0 and dataResidual_MAD > 0.0001:
        
        # Define iteration name for output files
        #
        itext = my_iCounter(i)
        
        my_niterNow = 500
        my_number, my_unit = separateNumbersUnits(my_threshold)
        my_thresholdNow = str(4.0*dataResidual_MAD) + my_unit
        my_outputImageNow = my_outputImage
        my_scalesNow = my_scales
        my_smallscalebiasNow = 0.0
        
        print("... Producing TCLEAN image - continue multiscale to 4xrms_MAD (source " + str(my_source) + " step "+str(itext)+")")
        print("... Some parameters are:")
        print("... ... pipeline threshold = " + str(my_threshold))
        print("... ... pipeline niter = " + str(my_niter))
        print("... ... used threshold = " + str(my_thresholdNow))
        print("... ... used scales = " + str(my_scalesNow))
        print("... ... used niter = " + str(my_niterNow))
        
        tclean(vis = my_visfilestoclean,
            imagename = my_outputImageNow,
            field = my_source,
            stokes = 'I',
            spw = my_freqs,
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
            pbmask = my_pbmask,
            sidelobethreshold = my_sidelobethreshold,
            noisethreshold = my_noisethreshold,
            minbeamfrac =  my_minbeamfrac,
            lownoisethreshold = my_lownoisethreshold,
            negativethreshold = my_negativethreshold,
            gridder = my_gridder,
            pblimit = my_pblimit,
            pbcor = True,
            threshold = my_thresholdNow,
            interactive = False,
            restoringbeam = 'common',
            smallscalebias = my_smallscalebiasNow)
    
        # Keep intermediate products (for developing and testing) or skip them (saving only the necessary ones)
        #
        if (keepIntermediates == True):
            exportfits(imagename = my_outputImageNow + '.image',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.image.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.residual',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.mask',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.mask.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.model',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
                dropdeg = True,
                overwrite = True)
        else:
            exportfits(imagename = my_outputImageNow + '.residual',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.model',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
                dropdeg = True,
                overwrite = True)
    
        #  Calculate the flux contained in the CLEANed model (MOD) and the noise in the residuals (MAD)
        #
        previous_dataModel_MOD = dataModel_MOD
        os.system('rm -rf ' + my_outputImageNow + '_MOD.model.fits')
        os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.model.fits ' + my_outputImageNow + '_MOD.model.fits')
        dataModel, headerModel = fits.getdata(my_outputImageNow + '_MOD.model.fits', header=True)
        dataModel_MOD = np.nansum(dataModel)
        print("... ... Flux contained in the model = " + str(dataModel_MOD))
        if previous_dataModel_MOD != 0.0:
            MOD_difference = 100.*(dataModel_MOD-previous_dataModel_MOD)/previous_dataModel_MOD
            print("... ... MOD has increased by " + str(int(1000.*MOD_difference)/1000.) + "%")
        else:
            MOD_difference = 0.0
        if keepIntermediates == False:
            os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.model.fits')
        #
        previous_dataResidual_MAD = dataResidual_MAD
        os.system('rm -rf ' + my_outputImageNow + '_MAD.residual.fits')
        os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits ' + my_outputImageNow + '_MAD.residual.fits')
        dataResidual, headerResidual = fits.getdata(my_outputImageNow + '_MAD.residual.fits', header=True)
        dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
        dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
        print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
        MAD_difference = 100.*(previous_dataResidual_MAD-dataResidual_MAD)/previous_dataResidual_MAD
        print("... ... MAD has been reduced by " + str(int(1000.*MAD_difference)/1000.) + "%")
        if keepIntermediates == False:
            os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits')
        
        i = i+1
        
        if MOD_difference > 1.0 and dataResidual_MAD > 0.0001:
            print("... ... the multi-scale loop continues")
        else:
            print("... ... the multi-scale loop ends here")
    
    ##########################################################################
    #
    # Phase 4: Use a PB mask and run TCLEAN task (auto-multithresh)
    #
    # First run of tclean after using a PB mask
    #
    # Define iteration name for output files
    #
    itext = my_iCounter(i)
    
    my_niterNow = 500
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(4.0*dataResidual_MAD) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    
    print("... Producing TCLEAN image - multiscale process, with PB mask (source " + str(my_source) + " step " + str(itext) + ")")
    print("... Some parameters are:")
    print("... ... pipeline threshold = " + str(my_threshold))
    print("... ... pipeline niter = " + str(my_niter))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    print("... ... used niter = " + str(my_niterNow))
    
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImageNow,
        field = my_source,
        stokes = 'I',
        spw = my_freqs,
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
        usemask = 'pb',
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = my_gridder,
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
    # Keep intermediate products (for developing and testing) or skip them (saving only the necessary ones)
    #
    if (keepIntermediates == True):
        exportfits(imagename = my_outputImageNow + '.image',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.image.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.mask',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.mask.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.model',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
            dropdeg = True,
            overwrite = True)
    else:
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.model',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
            dropdeg = True,
            overwrite = True)
    
    #  Calculate the flux contained in the CLEANed model (MOD) and the noise in the residuals (MAD)
    #
    os.system('rm -rf ' + my_outputImageNow + '_MOD.model.fits')
    os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.model.fits ' + my_outputImageNow + '_MOD.model.fits')
    dataModel, headerModel = fits.getdata(my_outputImageNow + '_MOD.model.fits', header=True)
    dataModel_MOD = np.nansum(dataModel)
    print("... ... Flux contained in the model = " + str(dataModel_MOD))
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.model.fits')
    #
    os.system('rm -rf ' + my_outputImageNow + '_MAD.residual.fits')
    os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits ' + my_outputImageNow + '_MAD.residual.fits')
    dataResidual, headerResidual = fits.getdata(my_outputImageNow + '_MAD.residual.fits', header=True)
    dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
    dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
    print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits')
        
    # Iterate multiscale CLEANing until reaching a non-changing (< 1%) flux model
    # or until the residuals get smaller than 3/4 x theoretical noise
    #
    # Reset some variables for the loop
    #
    MOD_difference = 1000.0
    MAD_difference = 1000.0
    i = i+1
    
    while MOD_difference > 1.0 and dataResidual_MAD > 0.000075:
        
        # Define iteration name for output files
        #
        itext = my_iCounter(i)
        
        my_niterNow = 500
        my_number, my_unit = separateNumbersUnits(my_threshold)
        my_thresholdNow = str(4.0*dataResidual_MAD) + my_unit
        my_outputImageNow = my_outputImage
        my_scalesNow = my_scales
        my_smallscalebiasNow = 0.0
        
        print("... Producing TCLEAN image - continue multiscale to 4xrms_MAD, with PB mask (source " + str(my_source) + " step "+str(itext)+")")
        print("... Some parameters are:")
        print("... ... pipeline threshold = " + str(my_threshold))
        print("... ... pipeline niter = " + str(my_niter))
        print("... ... used threshold = " + str(my_thresholdNow))
        print("... ... used scales = " + str(my_scalesNow))
        print("... ... used niter = " + str(my_niterNow))
        
        tclean(vis = my_visfilestoclean,
            imagename = my_outputImageNow,
            field = my_source,
            stokes = 'I',
            spw = my_freqs,
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
            usemask = 'pb',
            pbmask = my_pbmask,
            sidelobethreshold = my_sidelobethreshold,
            noisethreshold = my_noisethreshold,
            minbeamfrac =  my_minbeamfrac,
            lownoisethreshold = my_lownoisethreshold,
            negativethreshold = my_negativethreshold,
            gridder = my_gridder,
            pblimit = my_pblimit,
            pbcor = True,
            threshold = my_thresholdNow,
            interactive = False,
            restoringbeam = 'common',
            smallscalebias = my_smallscalebiasNow)
    
        # Keep intermediate products (for developing and testing) or skip them (saving only the necessary ones)
        #
        if (keepIntermediates == True):
            exportfits(imagename = my_outputImageNow + '.image',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.image.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.residual',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.mask',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.mask.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.model',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
                dropdeg = True,
                overwrite = True)
        else:
            exportfits(imagename = my_outputImageNow + '.residual',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.model',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
                dropdeg = True,
                overwrite = True)
    
        #  Calculate the flux contained in the CLEANed model (MOD) and the noise in the residuals (MAD)
        #
        previous_dataModel_MOD = dataModel_MOD
        os.system('rm -rf ' + my_outputImageNow + '_MOD.model.fits')
        os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.model.fits ' + my_outputImageNow + '_MOD.model.fits')
        dataModel, headerModel = fits.getdata(my_outputImageNow + '_MOD.model.fits', header=True)
        dataModel_MOD = np.nansum(dataModel)
        print("... ... Flux contained in the model = " + str(dataModel_MOD))
        if previous_dataModel_MOD != 0.0:
            MOD_difference = 100.*(dataModel_MOD-previous_dataModel_MOD)/previous_dataModel_MOD
            print("... ... MOD has increased by " + str(int(1000.*MOD_difference)/1000.) + "%")
        else:
            MOD_difference = 0.0
        if keepIntermediates == False:
            os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.model.fits')
        #
        previous_dataResidual_MAD = dataResidual_MAD
        os.system('rm -rf ' + my_outputImageNow + '_MAD.residual.fits')
        os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits ' + my_outputImageNow + '_MAD.residual.fits')
        dataResidual, headerResidual = fits.getdata(my_outputImageNow + '_MAD.residual.fits', header=True)
        dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
        dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
        print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
        MAD_difference = 100.*(previous_dataResidual_MAD-dataResidual_MAD)/previous_dataResidual_MAD
        print("... ... MAD has been reduced by " + str(int(1000.*MAD_difference)/1000.) + "%")
        if keepIntermediates == False:
            os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits')
        
        i = i+1
        
        if MOD_difference > 1.0 and dataResidual_MAD > 0.000075:
            print("... ... the multi-scale loop continues")
        else:
            print("... ... the multi-scale loop ends here")
    
    ##########################################################################
    #
    # Phase 5: Use a PB mask and run TCLEAN task (auto-multithresh)
    #
    # First run of tclean after using a PB mask
    #
    # Define iteration name for output files
    #
    itext = my_iCounter(i)
    
    my_niterNow = 500
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(2.0*dataResidual_MAD) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    
    print("... Producing TCLEAN image - multiscale process, with PB mask down to 2xMAD_rms (source " + str(my_source) + " step " + str(itext) + ")")
    print("... Some parameters are:")
    print("... ... pipeline threshold = " + str(my_threshold))
    print("... ... pipeline niter = " + str(my_niter))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    print("... ... used niter = " + str(my_niterNow))
    
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImageNow,
        field = my_source,
        stokes = 'I',
        spw = my_freqs,
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
        usemask = 'pb',
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = my_gridder,
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
    # Keep intermediate products (for developing and testing) or skip them (saving only the necessary ones)
    #
    if (keepIntermediates == True):
        exportfits(imagename = my_outputImageNow + '.image',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.image.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.mask',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.mask.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.model',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
            dropdeg = True,
            overwrite = True)
    else:
        exportfits(imagename = my_outputImageNow + '.residual',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '.model',
            fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
            dropdeg = True,
            overwrite = True)
    
    #  Calculate the flux contained in the CLEANed model (MOD) and the noise in the residuals (MAD)
    #
    os.system('rm -rf ' + my_outputImageNow + '_MOD.model.fits')
    os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.model.fits ' + my_outputImageNow + '_MOD.model.fits')
    dataModel, headerModel = fits.getdata(my_outputImageNow + '_MOD.model.fits', header=True)
    dataModel_MOD = np.nansum(dataModel)
    print("... ... Flux contained in the model = " + str(dataModel_MOD))
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.model.fits')
    #
    os.system('rm -rf ' + my_outputImageNow + '_MAD.residual.fits')
    os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits ' + my_outputImageNow + '_MAD.residual.fits')
    dataResidual, headerResidual = fits.getdata(my_outputImageNow + '_MAD.residual.fits', header=True)
    dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
    dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
    print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits')
        
    # Iterate multiscale CLEANing until reaching a non-changing (< 1%) flux model
    # or until the residuals get smaller than 3/4 x theoretical noise
    #
    # Reset some variables for the loop
    #
    MOD_difference = 1000.0
    MAD_difference = 1000.0
    i = i+1
    
    while MOD_difference > 1.0 and dataResidual_MAD > 0.000075:
        
        # Define iteration name for output files
        #
        itext = my_iCounter(i)
        
        my_niterNow = 500
        my_number, my_unit = separateNumbersUnits(my_threshold)
        my_thresholdNow = str(2.0*dataResidual_MAD) + my_unit
        my_outputImageNow = my_outputImage
        my_scalesNow = my_scales
        my_smallscalebiasNow = 0.0
        
        print("... Producing TCLEAN image - continue multiscale to 2xrms_MAD, with PB mask (source " + str(my_source) + " step "+str(itext)+")")
        print("... Some parameters are:")
        print("... ... pipeline threshold = " + str(my_threshold))
        print("... ... pipeline niter = " + str(my_niter))
        print("... ... used threshold = " + str(my_thresholdNow))
        print("... ... used scales = " + str(my_scalesNow))
        print("... ... used niter = " + str(my_niterNow))
        
        tclean(vis = my_visfilestoclean,
            imagename = my_outputImageNow,
            field = my_source,
            stokes = 'I',
            spw = my_freqs,
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
            usemask = 'pb',
            pbmask = my_pbmask,
            sidelobethreshold = my_sidelobethreshold,
            noisethreshold = my_noisethreshold,
            minbeamfrac =  my_minbeamfrac,
            lownoisethreshold = my_lownoisethreshold,
            negativethreshold = my_negativethreshold,
            gridder = my_gridder,
            pblimit = my_pblimit,
            pbcor = True,
            threshold = my_thresholdNow,
            interactive = False,
            restoringbeam = 'common',
            smallscalebias = my_smallscalebiasNow)
    
        # Keep intermediate products (for developing and testing) or skip them (saving only the necessary ones)
        #
        if (keepIntermediates == True):
            exportfits(imagename = my_outputImageNow + '.image',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.image.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.residual',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.mask',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.mask.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.model',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
                dropdeg = True,
                overwrite = True)
        else:
            exportfits(imagename = my_outputImageNow + '.residual',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.residual.fits',
                dropdeg = True,
                overwrite = True)
            exportfits(imagename = my_outputImageNow + '.model',
                fitsimage = my_outputImageNow + '_i' + str(itext) + '.model.fits',
                dropdeg = True,
                overwrite = True)
    
        #  Calculate the flux contained in the CLEANed model (MOD) and the noise in the residuals (MAD)
        #
        previous_dataModel_MOD = dataModel_MOD
        os.system('rm -rf ' + my_outputImageNow + '_MOD.model.fits')
        os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.model.fits ' + my_outputImageNow + '_MOD.model.fits')
        dataModel, headerModel = fits.getdata(my_outputImageNow + '_MOD.model.fits', header=True)
        dataModel_MOD = np.nansum(dataModel)
        print("... ... Flux contained in the model = " + str(dataModel_MOD))
        if previous_dataModel_MOD != 0.0:
            MOD_difference = 100.*(dataModel_MOD-previous_dataModel_MOD)/previous_dataModel_MOD
            print("... ... MOD has increased by " + str(int(1000.*MOD_difference)/1000.) + "%")
        else:
            MOD_difference = 0.0
        if keepIntermediates == False:
            os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.model.fits')
        #
        previous_dataResidual_MAD = dataResidual_MAD
        os.system('rm -rf ' + my_outputImageNow + '_MAD.residual.fits')
        os.system('cp -rp ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits ' + my_outputImageNow + '_MAD.residual.fits')
        dataResidual, headerResidual = fits.getdata(my_outputImageNow + '_MAD.residual.fits', header=True)
        dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
        dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
        print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))
        MAD_difference = 100.*(previous_dataResidual_MAD-dataResidual_MAD)/previous_dataResidual_MAD
        print("... ... MAD has been reduced by " + str(int(1000.*MAD_difference)/1000.) + "%")
        if keepIntermediates == False:
            os.system('rm -rf ' + my_outputImageNow + '_i' + str(itext) + '.residual.fits')
        
        i = i+1
        
        if MOD_difference > 1.0 and dataResidual_MAD > 0.000075:
            print("... ... the multi-scale loop continues")
        else:
            print("... ... the multi-scale loop ends here")
    
    ##########################################################################
    #
    # Phase 6: Export FITS files, define emission mask and determine JvM factor
    #
    #.........................................................................
    #
    # Export (some) files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '.residual',
        fitsimage = my_outputImageNow + '.residual.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.psf',
        fitsimage = my_outputImageNow + '.psf.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.pb',
        fitsimage = my_outputImageNow + '.pb.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.model',
        fitsimage = my_outputImageNow + '.model.fits',
        dropdeg = True,
        overwrite = True)
    
    #.........................................................................
    #
    # Define emission mask based on the 5.0/3.0 sigma levels
    #
    print("... Defining emission mask")
    #
    # Export key files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '.residual',
        fitsimage = 'forHandMadeMask.residual.fits',
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.image',
        fitsimage = 'forHandMadeMask.image.fits',
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.mask',
        fitsimage = 'forHandMadeMask.mask.fits',
        overwrite = True)
    #
    # Create mask at 5.0/3.0 sigma levels
    # ... mask containing all regions with emission above 5 sigma and extended down to 3 sigma
    #
    dataResidual_MAD = my_maskCreator('forHandMadeMask.image.fits', 'forHandMadeMask.residual.fits', 'forHandMadeMask.mask.fits', 5.0, 3.0)
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/handMade.mask')
    importfits(fitsimage = 'forHandMadeMask.mask.fits',
        imagename = str(my_runningPath) + '/almagal/processing/handMade.mask',
        overwrite = True)
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    exportfits(imagename = str(my_runningPath) + '/almagal/processing/handMade.mask',
        fitsimage = my_outputImageNow + '.mask.fits',
        dropdeg = True,
        overwrite = True)
    
    #.........................................................................
    #
    # Determine RMS noise levels
    #
    exportfits(imagename = my_outputImageNow + '.image',
        fitsimage = my_outputImageNow + '.image.fits',
        dropdeg = True,
        overwrite = True)
    dataImage, headerImage = fits.getdata(my_outputImageNow + '.image.fits', header=True)
    dataResidual, headerResidual = fits.getdata(my_outputImageNow + '.residual.fits', header=True)
    dataMask, headerMask = fits.getdata(my_outputImageNow + '.mask.fits', header=True)
    dataMask[dataMask > 0.5] = np.NaN
    dataMask[dataMask == 0.0] = 1.0

    # ... noise level from all residual (std and MAD)
    dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
    dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
    dataResidual_std = np.std(dataResidual_notNaN)
    print("... ... dataResidual_MAD = " + str(int((dataResidual_MAD*1000.)*10000.)/10000.) + " mJy")
    print("... ... dataResidual_std = " + str(int((dataResidual_std*1000.)*10000.)/10000.) + " mJy")
    
    # ... noise level from masked residual (std and MAD)
    dataResidualMasked = dataResidual*dataMask
    dataResidualMasked_notNaN = dataResidualMasked[np.logical_not(np.isnan(dataResidualMasked))]
    dataResidualMasked_MAD = median_absolute_deviation(dataResidualMasked_notNaN)
    dataResidualMasked_std = np.std(dataResidualMasked_notNaN)
    print("... ... dataResidualMasked_MAD = " + str(int((dataResidualMasked_MAD*1000.)*10000.)/10000.) + " mJy")
    print("... ... dataResidualMasked_std = " + str(int((dataResidualMasked_std*1000.)*10000.)/10000.) + " mJy")
    
    # ... noise level from masked image (std and MAD)
    dataImageMasked = dataImage*dataMask
    dataImageMasked_notNaN = dataImageMasked[np.logical_not(np.isnan(dataImageMasked))]
    dataImageMasked_MAD = median_absolute_deviation(dataImageMasked_notNaN)
    dataImageMasked_std = np.std(dataImageMasked_notNaN)
    print("... ... dataImageMasked_MAD = " + str(int((dataImageMasked_MAD*1000.)*10000.)/10000.) + " mJy")
    print("... ... dataImageMasked_std = " + str(int((dataImageMasked_std*1000.)*10000.)/10000.) + " mJy")
    
    # Update header for .image and future .JvM.image files
    #
    my_outputExtensions = ['.image', '.image.pbcor']
    for my_outputExtension in my_outputExtensions:
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'OBSERVER',
            hdvalue = 'almagal')
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGmadRES',
            hdvalue = dataResidual_MAD)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGstdRES',
            hdvalue = dataResidual_std)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGmadREM',
            hdvalue = dataResidualMasked_MAD)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGstdREM',
            hdvalue = dataResidualMasked_std)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGmadIMM',
            hdvalue = dataImageMasked_MAD)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGstdIMM',
            hdvalue = dataImageMasked_std)
    
    #.........................................................................
    #
    # Read information of the clean-beam
    #
    ## for Python 2 (CASA 5)
    #my_bmaj = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmaj').items()[0][1]
    #my_bmin = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmin').items()[0][1]
    #my_bpa = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bpa').items()[0][1]
    ## for Python 3 (CASA 6)
    my_bmaj = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmaj')['value']
    my_bmin = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmin')['value']
    my_bpa = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bpa')['value']
    print("... clean beam is: " + str(my_bmaj) + " x " + str(my_bmin) + " with PA " + str(my_bpa))
        
    # Convolve (clean-component) model with the clean-beam
    #
    ia.open(my_outputImageNow+'.model')
    im2 = ia.convolve2d(outfile=my_outputImageNow+'.model.convolved', axes=[0, 1], type='gauss', major=str(my_bmaj)+'arcsec', minor=str(my_bmin)+'arcsec', pa=str(my_bpa)+'deg', overwrite=True)
    im2.done()
    ia.close()
    
    # Apply JvM factor to residual
    #
    applyJvMfactor = True
    if (applyJvMfactor == True):
        my_JvMdirtyBeam = my_outputImageNow + '.psf.fits'
        my_JvMimage = my_JvMdirtyBeam
        my_JvMthreshold = 0.02
        my_JvMplots = False
        my_JvM = determineJvMfactor(my_JvMdirtyBeam, my_JvMimage, my_JvMthreshold, my_JvMplots)
        print("... JvM factor is "+str(my_JvM))
        
        os.system('rm -rf ' + my_outputImageNow + '.JvM.image')
        immath(imagename = [my_outputImageNow + '.model.convolved', my_outputImageNow + '.residual'],
            expr = '(IM0 + '+str(my_JvM)+'*IM1)',
            outfile = my_outputImageNow + '.JvM.image')
        
        os.system('rm -rf ' + my_outputImageNow + '.JvM.image.pbcor')
        immath(imagename = [my_outputImageNow + '.JvM.image', my_outputImageNow + '.pb'],
            expr = '(IM0 / IM1)',
            outfile = my_outputImageNow + '.JvM.image.pbcor')
        
        # Update header for .image and future .JvM.image files
        #
        my_outputExtensions = ['.image', '.JvM.image', '.JvM.image.pbcor']
        for my_outputExtension in my_outputExtensions:
            imhead(imagename = my_outputImageNow + my_outputExtension,
                mode = 'put',
                hdkey = 'AGJvM',
                hdvalue = my_JvM)
        
        # Export image files to FITS format
        #
        exportfits(imagename = my_outputImageNow + '.JvM.image',
            fitsimage = my_outputImageNow + '.JvM.image.fits',
            dropdeg = True,
            overwrite = True)
        os.system('rm -rf ' + my_outputImageNow + '.JvM.image')
        exportfits(imagename = my_outputImageNow + '.JvM.image.pbcor',
            fitsimage = my_outputImageNow + '.JvM.image.pbcor.fits',
            dropdeg = True,
            overwrite = True)
        os.system('rm -rf ' + my_outputImageNow + '.JvM.image.pbcor')
    
    exportfits(imagename = my_outputImageNow + '.image',
        fitsimage = my_outputImageNow + '.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.image.pbcor',
        fitsimage = my_outputImageNow + '.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.model.convolved',
        fitsimage = my_outputImageNow + '.model.convolved.fits',
        dropdeg = True,
        overwrite = True)
    os.system('rm -rf ' + my_outputImageNow + '.image')
    os.system('rm -rf ' + my_outputImageNow + '.image.pbcor')
    os.system('rm -rf ' + my_outputImageNow + '.model')
    os.system('rm -rf ' + my_outputImageNow + '.model.convolved')
    os.system('rm -rf ' + my_outputImageNow + '.residual')
    os.system('rm -rf ' + my_outputImageNow + '.pb')
    os.system('rm -rf ' + my_outputImageNow + '.psf')
    os.system('rm -rf ' + my_outputImageNow + '.sumwt')
    os.system('rm -rf ' + my_outputImageNow + '.weight')
    os.system('rm -rf ' + my_outputImageNow + '.sumwt')
    
    ##########################################################################
    #
    # Phase 7: Clean-up files
    #
    #.........................................................................
    #
    # Remove not necessary files
    #
    if keepIntermediates == False:
        os.system('rm -rf ' + my_outputImageNow + '_i*')
        os.system('rm -rf ' + my_outputImageNow + '_MAD.*')
        os.system('rm -rf ' + my_outputImageNow + '_MOD.*')
        os.system('rm -rf forHandMadeMask*')
    os.system('tar -cf combined-cont-fits.tar *image*fits *mask*fits *model*fits *residual.fits *pb.fits *psf.fits *.png')
    os.system('tar -cf auxiliary-cont-fits.tar *beam*fits *beam*png *ellipse-mask*fits *ellipse-mask*png tcleanParameters.txt casa*.log')
    os.system('rm -rf *.fits')
    os.system('rm -rf *.png')


def my_functionUVContinuumSubtractionForJointDeconvolution(my_telescope, my_source):
    
    """
    help
    """
    
    #-----------------------------------------------------------------------
    # Set up infrastructure for array combination
    #
    if (my_telescope == "7MTM2"):
        my_add7M = True
        my_addTM2 = True
        my_addTM1 = False
    
    if (my_telescope == "TM2TM1"):
        my_add7M = False
        my_addTM2 = True
        my_addTM1 = True
    
    if (my_telescope == "7MTM2TM1"):
        my_add7M = True
        my_addTM2 = True
        my_addTM1 = True
    
    #-----------------------------------------------------------------------
    # Get line free channels and prepare variables
    #
    if my_add7M == True:
        my_pipelinePath7M, my_pipelineDirectory7M, my_lineFreeChannels7M, vislist7M, contfile7M = my_functionGetLineFreeChannelsForJointDeconvolution("7M", str(my_source))
    
    if my_addTM2 == True:
        my_pipelinePathTM2, my_pipelineDirectoryTM2, my_lineFreeChannelsTM2, vislistTM2, contfileTM2 = my_functionGetLineFreeChannelsForJointDeconvolution("TM2", str(my_source))
    
    if my_addTM1 == True:
        my_pipelinePathTM1, my_pipelineDirectoryTM1, my_lineFreeChannelsTM1, vislistTM1, contfileTM1 = my_functionGetLineFreeChannelsForJointDeconvolution("TM1", str(my_source))
    
    my_sourceName = str(my_source)
    
    #-----------------------------------------------------------------------
    # Generate continuum subtracted measurement sets for all ms files available (using uvcontsub)
    # and transform data to LSRK frame (using mstransform)
    #
    # For telescope array 7M
    #
    if my_add7M == True:
        
        my_freqsLSRK7Mspw0 = []
        my_freqsLSRK7Mspw1 = []
        my_freqsLSRK7Mspw2 = []
        my_freqsLSRK7Mspw3 = []
        
        for visfile7M in vislist7M:
            #
            # Determine continuum ranges
            #
            my_fitspw = getSPWRanges(visfile7M, contfile7M, my_sourceName)
            #
            # Subtract continuum from visibilities
            #
            uvcontsub(vis = visfile7M,
                fitspw = my_fitspw[0])
            #
            # Transform to LSRK frame
            #
            mstransform(vis = visfile7M+'.contsub',
                outputvis = visfile7M+'.contsub.mstrans',
                spw = '',
                regridms = True,
                outframe = 'LSRK',
                mode = 'channel',
                restfreq = '',
                datacolumn = 'data')
            #
            # Collect frequency information for each SPW for each EB in individual arrays
            #
            msmd.open(visfile7M+'.contsub.mstrans')
            my_freqsLSRK7Mspw0.append(msmd.chanfreqs(0))
            my_freqsLSRK7Mspw1.append(msmd.chanfreqs(1))
            my_freqsLSRK7Mspw2.append(msmd.chanfreqs(2))
            my_freqsLSRK7Mspw3.append(msmd.chanfreqs(3))
            msmd.close()
    
    # For telescope array TM2
    #
    if my_addTM2 == True:
        
        my_freqsLSRKTM2spw0 = []
        my_freqsLSRKTM2spw1 = []
        my_freqsLSRKTM2spw2 = []
        my_freqsLSRKTM2spw3 = []
        
        for visfileTM2 in vislistTM2:
            #
            # Determine continuum ranges
            #
            my_fitspw = getSPWRanges(visfileTM2, contfileTM2, my_sourceName)
            #
            # Subtract continuum from visibilities
            #
            uvcontsub(vis = visfileTM2,
                fitspw = my_fitspw[0])
            #
            # Transform to LSRK frame
            #
            mstransform(vis = visfileTM2+'.contsub',
                outputvis = visfileTM2+'.contsub.mstrans',
                spw = '',
                regridms = True,
                outframe = 'LSRK',
                mode = 'channel',
                restfreq = '',
                datacolumn = 'data')
            #
            # Collect frequency information for each SPW for each EB in individual arrays
            #
            msmd.open(visfileTM2+'.contsub.mstrans')
            my_freqsLSRKTM2spw0.append(msmd.chanfreqs(0))
            my_freqsLSRKTM2spw1.append(msmd.chanfreqs(1))
            my_freqsLSRKTM2spw2.append(msmd.chanfreqs(2))
            my_freqsLSRKTM2spw3.append(msmd.chanfreqs(3))
            msmd.close()
    
    # For telescope array TM1
    #
    if my_addTM1 == True:
        
        my_freqsLSRKTM1spw0 = []
        my_freqsLSRKTM1spw1 = []
        my_freqsLSRKTM1spw2 = []
        my_freqsLSRKTM1spw3 = []
        
        for visfileTM1 in vislistTM1:
            #
            # Determine continuum ranges
            #
            my_fitspw = getSPWRanges(visfileTM1, contfileTM1, my_sourceName)
            #
            # Subtract continuum from visibilities
            #
            uvcontsub(vis = visfileTM1,
                fitspw = my_fitspw[0])
            #
            # Transform to LSRK frame
            #
            mstransform(vis = visfileTM1+'.contsub',
                outputvis = visfileTM1+'.contsub.mstrans',
                spw = '',
                regridms = True,
                outframe = 'LSRK',
                mode = 'channel',
                restfreq = '',
                datacolumn = 'data')
            #
            # Collect frequency information for each SPW for each EB in individual arrays
            #
            msmd.open(visfileTM1+'.contsub.mstrans')
            my_freqsLSRKTM1spw0.append(msmd.chanfreqs(0))
            my_freqsLSRKTM1spw1.append(msmd.chanfreqs(1))
            my_freqsLSRKTM1spw2.append(msmd.chanfreqs(2))
            my_freqsLSRKTM1spw3.append(msmd.chanfreqs(3))
            msmd.close()
    
    #-----------------------------------------------------------------------
    # Define SPW range based on the common frequency coverage of the three arrays
    # This SPW range will be used to split out the corresponding frequency range from the 7M, TM2 and TM1 data
    #
    # for spw 0
    my_minimumSPW0 = []
    my_maximumSPW0 = []
    my_minimumSPW1 = []
    my_maximumSPW1 = []
    my_minimumSPW2 = []
    my_maximumSPW2 = []
    my_minimumSPW3 = []
    my_maximumSPW3 = []
    if my_add7M == True:
        my_minimumSPW0.append(np.min(my_freqsLSRK7Mspw0))
        my_maximumSPW0.append(np.max(my_freqsLSRK7Mspw0))
        my_minimumSPW1.append(np.min(my_freqsLSRK7Mspw1))
        my_maximumSPW1.append(np.max(my_freqsLSRK7Mspw1))
        my_minimumSPW2.append(np.min(my_freqsLSRK7Mspw2))
        my_maximumSPW2.append(np.max(my_freqsLSRK7Mspw2))
        my_minimumSPW3.append(np.min(my_freqsLSRK7Mspw3))
        my_maximumSPW3.append(np.max(my_freqsLSRK7Mspw3))
    if my_addTM2 == True:
        my_minimumSPW0.append(np.min(my_freqsLSRKTM2spw0))
        my_maximumSPW0.append(np.max(my_freqsLSRKTM2spw0))
        my_minimumSPW1.append(np.min(my_freqsLSRKTM2spw1))
        my_maximumSPW1.append(np.max(my_freqsLSRKTM2spw1))
        my_minimumSPW2.append(np.min(my_freqsLSRKTM2spw2))
        my_maximumSPW2.append(np.max(my_freqsLSRKTM2spw2))
        my_minimumSPW3.append(np.min(my_freqsLSRKTM2spw3))
        my_maximumSPW3.append(np.max(my_freqsLSRKTM2spw3))
    if my_addTM1 == True:
        my_minimumSPW0.append(np.min(my_freqsLSRKTM1spw0))
        my_maximumSPW0.append(np.max(my_freqsLSRKTM1spw0))
        my_minimumSPW1.append(np.min(my_freqsLSRKTM1spw1))
        my_maximumSPW1.append(np.max(my_freqsLSRKTM1spw1))
        my_minimumSPW2.append(np.min(my_freqsLSRKTM1spw2))
        my_maximumSPW2.append(np.max(my_freqsLSRKTM1spw2))
        my_minimumSPW3.append(np.min(my_freqsLSRKTM1spw3))
        my_maximumSPW3.append(np.max(my_freqsLSRKTM1spw3))
    
    my_commonALLSPWRange = '0:'+str(np.max(my_minimumSPW0))+'~'+str(np.min(my_maximumSPW0))+'Hz,1:'+str(np.max(my_minimumSPW1))+'~'+str(np.min(my_maximumSPW1))+'Hz,2:'+str(np.max(my_minimumSPW2))+'~'+str(np.min(my_maximumSPW2))+'Hz,3:'+str(np.max(my_minimumSPW3))+'~'+str(np.min(my_maximumSPW3))+'Hz'
    
    if my_add7M == True:
        for visfile7M in vislist7M:
            split(vis = visfile7M+'.contsub.mstrans',
                datacolumn = 'data',
                spw = my_commonALLSPWRange,
                outputvis = visfile7M+'.likeALL.contsub.mstrans')
    
    if my_addTM2 == True:
        for visfileTM2 in vislistTM2:
            split(vis = visfileTM2+'.contsub.mstrans',
                datacolumn = 'data',
                spw = my_commonALLSPWRange,
                outputvis = visfileTM2+'.likeALL.contsub.mstrans')
    
    if my_addTM1 == True:
        for visfileTM1 in vislistTM1:
            split(vis = visfileTM1+'.contsub.mstrans',
                datacolumn = 'data',
                spw = my_commonALLSPWRange,
                outputvis = visfileTM1+'.likeALL.contsub.mstrans')
    
    # Clean-up measurement sets that will not be used later on
    # i.e., keep only visfile+'.likeALL.contsub.mstrans files
    #
    if my_add7M == True:
        print(" CLEANING UP 7M")
        print(vislist7M)
        for visfile7M in vislist7M:
            print("... " + visfile7M)
            os.system('rm -rf ' + visfile7M)
            os.system('rm -rf ' + visfile7M + '.contsub')
            os.system('rm -rf ' + visfile7M + '.contsub.mstrans')
    if my_addTM2 == True:
        print(" CLEANING UP TM2")
        print(vislistTM2)
        for visfileTM2 in vislistTM2:
            print("... " + visfileTM2)
            os.system('rm -rf ' + visfileTM2)
            os.system('rm -rf ' + visfileTM2 + '.contsub')
            os.system('rm -rf ' + visfileTM2 + '.contsub.mstrans')
    if my_addTM1 == True:
        print(" CLEANING UP TM1")
        print(vislistTM1)
        for visfileTM1 in vislistTM1:
            print("... " + visfileTM1)
            os.system('rm -rf ' + visfileTM1)
            os.system('rm -rf ' + visfileTM1 + '.contsub')
            os.system('rm -rf ' + visfileTM1 + '.contsub.mstrans')
    
    # Write out the number of channels of each SPW
    #
    if my_add7M == True:
        if os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_7M.txt') == False:
            with open(str(my_runningPath)+'/almagal/channelsForEachSPW_7M.txt', 'w') as f:
                for visfile7M in vislist7M:
                    msmd.open(visfile7M+'.likeALL.contsub.mstrans')
                    f.write(str(len(msmd.chanfreqs(0))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(1))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(2))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(3))))
                    f.write('\n')
                    msmd.close()
    
    if my_addTM2 == True:
        if os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_TM2.txt') == False:
            with open(str(my_runningPath)+'/almagal/channelsForEachSPW_TM2.txt', 'w') as f:
                for visfileTM2 in vislistTM2:
                    msmd.open(visfileTM2+'.likeALL.contsub.mstrans')
                    f.write(str(len(msmd.chanfreqs(0))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(1))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(2))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(3))))
                    f.write('\n')
                    msmd.close()
    
    if my_addTM1 == True:
        if os.path.isfile(str(my_runningPath) + '/almagal/channelsForEachSPW_TM1.txt') == False:
            with open(str(my_runningPath)+'/almagal/channelsForEachSPW_TM1.txt', 'w') as f:
                for visfileTM1 in vislistTM1:
                    msmd.open(visfileTM1+'.likeALL.contsub.mstrans')
                    f.write(str(len(msmd.chanfreqs(0))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(1))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(2))))
                    f.write('\n')
                    f.write(str(len(msmd.chanfreqs(3))))
                    f.write('\n')
                    msmd.close()
    
    '''
    # OLD APPROACH
    #-----------------------------------------------------------------------
    # Define SPW range based on the TM2 frequency coverage
    # This SPW range will be used to split out the corresponding frequency range from the 7M and TM1 data
    #
    my_commonTM2SPWRange = '0:'+str(np.min(my_freqsLSRKTM2spw0))+'~'+str(np.max(my_freqsLSRKTM2spw0))+'Hz,1:'+str(np.min(my_freqsLSRKTM2spw1))+'~'+str(np.max(my_freqsLSRKTM2spw1))+'Hz,2:'+str(np.min(my_freqsLSRKTM2spw2))+'~'+str(np.max(my_freqsLSRKTM2spw2))+'Hz,3:'+str(np.min(my_freqsLSRKTM2spw3))+'~'+str(np.max(my_freqsLSRKTM2spw3))+'Hz'
    
    if my_add7M == True:
        for visfile7M in vislist7M:
            split(vis = visfile7M+'.contsub.mstrans',
                datacolumn = 'data',
                spw = my_commonTM2SPWRange,
                outputvis = visfile7M+'.likeTM2.contsub.mstrans')
    
    if my_addTM1 == True:
        for visfileTM1 in vislistTM1:
            split(vis = visfileTM1+'.contsub.mstrans',
                datacolumn = 'data',
                spw = my_commonTM2SPWRange,
                outputvis = visfileTM1+'.likeTM2.contsub.mstrans')
                
    # Clean-up measurement sets that will not be used later on
    # i.e., keep only visfile7M+'.contsub.mstrans.split and visfileTM2+'.contsub.mstrans files
    # BUGFIX: bjones 21.07.2021 - changed from removing visfile7M/TM2 to all visfiles 
    #
    if my_add7M == True:
        print(" CLEANING UP 7M")
        print(vislist7M)
        for visfile7M in vislist7M:
            print("... " + visfile7M)
            os.system('rm -rf ' + visfile7M)
            os.system('rm -rf ' + visfile7M + '.contsub')
            os.system('rm -rf ' + visfile7M + '.contsub.mstrans')
    if my_addTM2 == True:
        print(" CLEANING UP TM2")
        print(vislistTM2)
        for visfileTM2 in vislistTM2:
            print("... " + visfileTM2)
            os.system('rm -rf ' + visfileTM2)
            os.system('rm -rf ' + visfileTM2 + '.contsub')
    if my_addTM1 == True:
        print(" CLEANING UP TM1")
        print(vislistTM1)
        for visfileTM1 in vislistTM1:
            print("... " + visfileTM1)
            os.system('rm -rf ' + visfileTM1)
            os.system('rm -rf ' + visfileTM1 + '.contsub')
            os.system('rm -rf ' + visfileTM1 + '.contsub.mstrans')
    '''

def my_functionJointDeconvolutionCube(function_spw, function_start, function_nchan, function_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean):
    """
    Function to joint-deconvolve spectral line cubes combining multiple
    ALMA arrays (e.g., 7M, TM2, TM1)
    
    Input parameters:
      function_spw : indicate the spectral window to process
      function_start : indicate the starting channel of the cube
      function_nchan : indicate the number of channels to be imaged
      function_chunkName : indicate the added name to the output image based on the chunk being processed
      and output (return) parameters from my_functionGetTcleanParametersJointDeconbolutionCube
    """
    # Define output image name for this chunk:
    if (function_chunkName == 0):
        my_outputImage = my_outputImage
    else:
        my_outputImage = my_outputImage + '_chunk' + str(function_chunkName)
    #
    # Use the same pixel size and image size as for the continuum
    my_cell, my_imsize, my_nbpixels = my_functionGetCellsizeImsize(my_telescope, my_source)
    #
    # Run TCLEAN task
    os.system('rm -rf ' + my_outputImage + '.*')
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImage,
        field = my_source,
        stokes = 'I',
        spw = str(function_spw),
        outframe = 'LSRK',
        restfreq = '',
        specmode = 'cube',
        width = 1,
        nchan = function_nchan, # default : function_nchan = 3836 # start at channel 2 and end 2 channels before 3840 
        start = function_start, # default : function_start = 2    # so avoid any channels with TM2 only data
        imsize = my_imsize,
        cell = my_cell,
        deconvolver = 'multiscale',
        scales = my_scales,
        niter = my_niter,
        weighting = my_weighting,
        robust = my_robust,
        usemask = 'auto-multithresh',
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_threshold,
        interactive = False,
        restoringbeam = '',
        perchanweightdensity = True,
        fastnoise = False,          # Based on pipeline imaging tclean
        minpercentchange = 1.0)     # Based on pipeline imaging tclean
    
    '''
    #
    # Export image files to FITS format
    #exportfits(imagename = my_outputImage + '.image',
    #    fitsimage = my_outputImage + '.image.fits',
    #    dropdeg = True,
    #    overwrite = True)
    #exportfits(imagename = my_outputImage + '.image.pbcor',
    #    fitsimage = my_outputImage + '.image.pbcor.fits',
    #    dropdeg = True,
    #    overwrite = True)
    '''
    
    print("First TCLEAN DONE")
    print("checking not masked channels")
    # Re-clean those channels for which mask was not defined
    #
    # The outcome is fairly sensitive to the following parameters:
    #
    maskThreshFactor = 2      # Lower limit of the seed mask
    maskThreshFraction = 0.4  # Fraction of line peak line intensity (per channel) to seed the mask
    newGrow = 1               # Number of iterations that can be used in a "grow" sequence.
    #
    # Noise level and cube image
    #
    cleanrms = float(my_threshold.split("J")[0].split("m")[0])
    cubeName = my_outputImage + '.image'
    #
    print("cleanrms")
    print(cleanrms)
    if (cleanrms > 0.0) and os.path.isdir(cubeName+'.mask'):
        os.system('rm -rf ' + cubeName + '.reclean.*')
        print('check 0')
        print(cleanrms)
        print(maskThreshFactor)
        print(maskThreshFraction)
        print('check 1')
        extrachannels=au.amendMaskForCube(cubeName,
                                          intensityThreshold=cleanrms*2.,  # times 2 added by ASM
                                          maskThreshold=cleanrms*maskThreshFactor,
                                          maskThresholdFraction=maskThreshFraction,
                                          npixels=25,pblimit=0.3,overwriteMask=False,cleanup=True,
                                          masknameInsert='.reclean',
                                          verbose=False,dryrun=False)
        print("HOOOLA")
        print(extrachannels)
        print("Starting cleaning of extra channels")
        check_IFmask = 0
        if os.path.isdir(cubeName+'.mask'):
           check_IFmask = 1
        print(cubeName+'.mask')
        print(check_IFmask)
        #if len(extrachannels) != 0 or check_IFmask == 0:
        if check_IFmask == 0:
            print("que tal estas")
            for i in ['.image','.residual','.psf','.model','.pb','.sumwt']:
                shutil.copytree(cubeName.replace('.image',i),cubeName.replace('.image','')+'.reclean'+i)
            tclean(vis = my_visfilestoclean,
                imagename = my_outputImage+'.reclean',
                field = my_source,
                stokes = 'I',
                spw = str(function_spw),
                outframe = 'LSRK',
                restfreq = '',
                specmode = 'cube',
                width = 1,
                nchan = function_nchan, # default : function_nchan = 3836 # start at channel 2 and end 2 channels before 3840 
                start = function_start, # default : function_start = 2    # so avoid any channels with TM2 only data
                imsize = my_imsize,
                cell = my_cell,
                deconvolver = 'multiscale',
                scales = my_scales,
                niter = my_niter,
                weighting = my_weighting,
                robust = my_robust,
                usemask = 'auto-multithresh',
                pbmask = my_pbmask,
                sidelobethreshold = my_sidelobethreshold,
                noisethreshold = my_noisethreshold,
                minbeamfrac =  my_minbeamfrac,
                lownoisethreshold = my_lownoisethreshold,
                negativethreshold = my_negativethreshold,
                gridder = 'mosaic',
                pblimit = my_pblimit,
                pbcor = True,
                threshold = my_threshold,
                interactive = False,
                restoringbeam = '',
                perchanweightdensity = True,
                fastnoise = False,          # Based on pipeline imaging tclean
                minpercentchange = 1.0,     # Based on pipeline imaging tclean
                growiterations = newGrow)
            #
            # Export image files to FITS format
            #exportfits(imagename = my_outputImage + '.reclean.image',
            #    fitsimage = my_outputImage + '.reclean.image.fits',
            #    dropdeg = True,
            #    overwrite = True)
            #exportfits(imagename = my_outputImage + '.reclean.image.pbcor',
            #    fitsimage = my_outputImage + '.reclean.image.pbcor.fits',
            #    dropdeg = True,
            #    overwrite = True)
        print("Ending cleaning of extra channels")


def my_functionJointDeconvolutionCubeV2(function_spw, function_start, function_nchan, function_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean):
    """
    Function to joint-deconvolve spectral line cubes combining multiple
    ALMA arrays (e.g., 7M, TM2, TM1)
    
    Input parameters:
      function_spw : indicate the spectral window to process
      function_start : indicate the starting channel of the cube
      function_nchan : indicate the number of channels to be imaged
      function_chunkName : indicate the added name to the output image based on the chunk being processed
      and output (return) parameters from my_functionGetTcleanParametersJointDeconbolutionCube
    """
    
    # Define output image name for this chunk:
    if (function_chunkName == 0):
        my_outputImage = my_outputImage
    else:
        my_outputImage = my_outputImage + '_chunk' + str(function_chunkName)
    #
    # Use the same pixel size and image size as for the continuum
    my_cell, my_imsize, my_nbpixels = my_functionGetCellsizeImsize(my_telescope, my_source)
    #
    # Run TCLEAN task
    #
    # First TCLEAN run:
    #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
    #  Key parameters to play with are:
    #   - threshold: 
    #   - niter: 
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.0*my_number) + my_unit
    my_scalesNow = my_scales
    my_outputImageNow = my_outputImage
    
    print("... Producing TCLEAN image - starting new mask (step 1)")
    print("... Some parameters are:")
    print("... ... original threshold = " + str(my_threshold))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    
    os.system('rm -rf ' + my_outputImageNow + '.*')
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImageNow,
        field = my_source,
        stokes = 'I',
        spw = str(function_spw),
        outframe = 'LSRK',
        restfreq = '',
        specmode = 'cube',
        width = 1,
        nchan = function_nchan, # default : function_nchan = 3836 # start at channel 2 and end 2 channels before 3840 
        start = function_start, # default : function_start = 2    # so avoid any channels with TM2 only data
        imsize = my_imsize,
        cell = my_cell,
        deconvolver = 'multiscale',
        scales = my_scalesNow,
        niter = my_niterNow,
        weighting = my_weighting,
        robust = my_robust,
        usemask = 'auto-multithresh',
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = '',
        perchanweightdensity = True,
        fastnoise = False,          # Based on pipeline imaging tclean
        minpercentchange = 1.0)     # Based on pipeline imaging tclean
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v01.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v01.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v01.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')
    os.system('cp -rp ' + my_outputImageNow + '.model ' + my_outputImageNow + '_v01.model')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '_v01.image',
        fitsimage = my_outputImageNow + '_v01.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v01.image.pbcor',
        fitsimage = my_outputImageNow + '_v01.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v01.residual',
        fitsimage = my_outputImageNow + '_v01.residual.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v01.mask',
        fitsimage = my_outputImageNow + '_v01.mask.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v01.model',
        fitsimage = my_outputImageNow + '_v01.model.fits',
        dropdeg = True,
        overwrite = True)
    
    # Add the TM2 mask to the newly-created mask
    #
    print("... Adding TM2 mask to the newly-created mask")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/original_TM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    imregrid(imagename = str(my_runningPath) + '/almagal/processing/original_TM2_spw' + str(function_spw) + '.mask',
        template = my_outputImageNow + '_v01.mask',
        output = str(my_runningPath) + '/almagal/processing/original_TM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask',
        axes = [3])
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/TM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_TM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask',
        output = str(my_runningPath) + '/almagal/processing/TM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/TM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v01.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_withTM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask',
        output = my_outputImageNow + '.mask')
    
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/original_TM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/TM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    
    # Second TCLEAN run:
    #  It uses the mask created first with 7M+TM2+TM1 data and the TM2 mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.00*my_number) + my_unit
    my_scalesNow = my_scales
    my_outputImageNow = my_outputImage
    
    print("... Producing TCLEAN image - with TM2 mask added (step 2)")
    print("... Some parameters are:")
    print("... ... original threshold = " + str(my_threshold))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImageNow,
        field = my_source,
        stokes = 'I',
        spw = str(function_spw),
        outframe = 'LSRK',
        restfreq = '',
        specmode = 'cube',
        width = 1,
        nchan = function_nchan, # default : function_nchan = 3836 # start at channel 2 and end 2 channels before 3840 
        start = function_start, # default : function_start = 2    # so avoid any channels with TM2 only data
        imsize = my_imsize,
        cell = my_cell,
        deconvolver = 'multiscale',
        scales = my_scalesNow,
        niter = my_niterNow,
        weighting = my_weighting,
        robust = my_robust,
        usemask = 'auto-multithresh',
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = '',
        perchanweightdensity = True,
        fastnoise = False,          # Based on pipeline imaging tclean
        minpercentchange = 1.0)     # Based on pipeline imaging tclean
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v02.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v02.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v02.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v02.mask')
    os.system('cp -rp ' + my_outputImageNow + '.model ' + my_outputImageNow + '_v02.model')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '_v02.image',
        fitsimage = my_outputImageNow + '_v02.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v02.image.pbcor',
        fitsimage = my_outputImageNow + '_v02.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v02.residual',
        fitsimage = my_outputImageNow + '_v02.residual.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v02.mask',
        fitsimage = my_outputImageNow + '_v02.mask.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v02.model',
        fitsimage = my_outputImageNow + '_v02.model.fits',
        dropdeg = True,
        overwrite = True)
    
    # Add the 7M mask to the newly-created mask
    #
    print("... Adding 7M mask to the mask")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/original_7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    imregrid(imagename = str(my_runningPath) + '/almagal/processing/original_7M_spw' + str(function_spw) + '.mask',
        template = my_outputImageNow + '_v02.mask',
        output = str(my_runningPath) + '/almagal/processing/original_7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask',
        axes = [3])
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask',
        output = str(my_runningPath) + '/almagal/processing/7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v02.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_with7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M_normalized_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_with7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask',
        output = my_outputImageNow + '.mask')
    
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/original_7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M_normalized_spw' + str(function_spw) + '_chunk' + str(function_chunkName) + '.mask')
    
    # Third TCLEAN run:
    #  It uses the mask created from the previous cleaning step plus the 7M mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.00*my_number) + my_unit
    my_scalesNow = my_scales
    my_outputImageNow = my_outputImage
    
    print("... Producing TCLEAN image - with 7M mask added (step 3)")
    print("... Some parameters are:")
    print("... ... original threshold = " + str(my_threshold))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImageNow,
        field = my_source,
        stokes = 'I',
        spw = str(function_spw),
        outframe = 'LSRK',
        restfreq = '',
        specmode = 'cube',
        width = 1,
        nchan = function_nchan, # default : function_nchan = 3836 # start at channel 2 and end 2 channels before 3840 
        start = function_start, # default : function_start = 2    # so avoid any channels with TM2 only data
        imsize = my_imsize,
        cell = my_cell,
        deconvolver = 'multiscale',
        scales = my_scalesNow,
        niter = my_niterNow,
        weighting = my_weighting,
        robust = my_robust,
        usemask = 'auto-multithresh',
        pbmask = my_pbmask,
        sidelobethreshold = my_sidelobethreshold,
        noisethreshold = my_noisethreshold,
        minbeamfrac =  my_minbeamfrac,
        lownoisethreshold = my_lownoisethreshold,
        negativethreshold = my_negativethreshold,
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = '',
        perchanweightdensity = True,
        fastnoise = False,          # Based on pipeline imaging tclean
        minpercentchange = 1.0)     # Based on pipeline imaging tclean
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '.residual',
        fitsimage = my_outputImageNow + '.residual.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.mask',
        fitsimage = my_outputImageNow + '.mask.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.psf',
        fitsimage = my_outputImageNow + '.psf.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.pb',
        fitsimage = my_outputImageNow + '.pb.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.model',
        fitsimage = my_outputImageNow + '.model.fits',
        dropdeg = True,
        overwrite = True)
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v03.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v03.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v03.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v03.mask')
    os.system('cp -rp ' + my_outputImageNow + '.model ' + my_outputImageNow + '_v03.model')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '_v03.image',
        fitsimage = my_outputImageNow + '_v03.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v03.image.pbcor',
        fitsimage = my_outputImageNow + '_v03.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v03.residual',
        fitsimage = my_outputImageNow + '_v03.residual.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v03.mask',
        fitsimage = my_outputImageNow + '_v03.mask.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v03.model',
        fitsimage = my_outputImageNow + '_v03.model.fits',
        dropdeg = True,
        overwrite = True)
    
    '''
    #
    # Export image files to FITS format
    #exportfits(imagename = my_outputImage + '.image',
    #    fitsimage = my_outputImage + '.image.fits',
    #    dropdeg = True,
    #    overwrite = True)
    #exportfits(imagename = my_outputImage + '.image.pbcor',
    #    fitsimage = my_outputImage + '.image.pbcor.fits',
    #    dropdeg = True,
    #    overwrite = True)
    '''
    
    print("... Producing TCLEAN image - checking for NOT masked channels")
    #
    # Re-clean those channels for which mask was not defined
    #
    # The outcome is fairly sensitive to the following parameters:
    #
    maskThreshFactor = 2      # Lower limit of the seed mask
    maskThreshFraction = 0.4  # Fraction of line peak line intensity (per channel) to seed the mask
    newGrow = 1               # Number of iterations that can be used in a "grow" sequence.
    #
    # Noise level and cube image
    #
    cleanrms = float(my_threshold.split("J")[0].split("m")[0])
    cubeName = my_outputImageNow + '.image'
    #
    print("... Some parameters are:")
    print("... ... cleanrms = " + str(cleanrms))
    print("... ... cubeName = " + str(my_outputImageNow) + ".image")
    #if (cleanrms > 0.0) and os.path.isdir(cubeName+'.mask'):
    if (cleanrms > 0.0):
        os.system('rm -rf ' + cubeName + '.reclean.*')
        extrachannels=au.amendMaskForCube(cubeName,
                                          intensityThreshold=cleanrms*2.,  # times 2 added by ASM
                                          maskThreshold=cleanrms*maskThreshFactor,
                                          maskThresholdFraction=maskThreshFraction,
                                          npixels=25,pblimit=0.3,overwriteMask=False,cleanup=True,
                                          masknameInsert='.reclean',
                                          verbose=False,dryrun=False)
        print("... Starting cleaning of extra channels:")
        print(extrachannels)
        check_IFmask = 0
        if os.path.isdir(cubeName+'.mask'):
           check_IFmask = 1
        print("... ... cubeMask = " + str(cubeName) + ".mask")
        print("... ... check_IFmask = " + str(check_IFmask))
        #if len(extrachannels) != 0 or check_IFmask == 0:
        if len(extrachannels) != 0:
            print("... processing")
            for i in ['.image','.residual','.psf','.model','.pb','.sumwt']:
                shutil.copytree(cubeName.replace('.image',i),cubeName.replace('.image','')+'.reclean'+i)
            tclean(vis = my_visfilestoclean,
                imagename = my_outputImageNow+'.reclean',
                field = my_source,
                stokes = 'I',
                spw = str(function_spw),
                outframe = 'LSRK',
                restfreq = '',
                specmode = 'cube',
                width = 1,
                nchan = function_nchan, # default : function_nchan = 3836 # start at channel 2 and end 2 channels before 3840 
                start = function_start, # default : function_start = 2    # so avoid any channels with TM2 only data
                imsize = my_imsize,
                cell = my_cell,
                deconvolver = 'multiscale',
                scales = my_scalesNow,
                niter = my_niterNow,
                weighting = my_weighting,
                robust = my_robust,
                usemask = 'auto-multithresh',
                pbmask = my_pbmask,
                sidelobethreshold = my_sidelobethreshold,
                noisethreshold = my_noisethreshold,
                minbeamfrac =  my_minbeamfrac,
                lownoisethreshold = my_lownoisethreshold,
                negativethreshold = my_negativethreshold,
                gridder = 'mosaic',
                pblimit = my_pblimit,
                pbcor = True,
                threshold = my_thresholdNow,
                interactive = False,
                restoringbeam = '',
                perchanweightdensity = True,
                fastnoise = False,          # Based on pipeline imaging tclean
                minpercentchange = 1.0,     # Based on pipeline imaging tclean
                growiterations = newGrow)
            #
            # Export image files to FITS format
            #exportfits(imagename = my_outputImage + '.reclean.image',
            #    fitsimage = my_outputImage + '.reclean.image.fits',
            #    dropdeg = True,
            #    overwrite = True)
            #exportfits(imagename = my_outputImage + '.reclean.image.pbcor',
            #    fitsimage = my_outputImage + '.reclean.image.pbcor.fits',
            #    dropdeg = True,
            #    overwrite = True)
        print("... Ending cleaning of extra channels")
    
    print("Clean up intermediate files")
    os.system('rm -rf ' + my_outputImageNow + '_v01.image')
    os.system('rm -rf ' + my_outputImageNow + '_v01.image.pbcor')
    os.system('rm -rf ' + my_outputImageNow + '_v01.residual')
    os.system('rm -rf ' + my_outputImageNow + '_v01.mask')
    os.system('rm -rf ' + my_outputImageNow + '_v01.model')
    os.system('rm -rf ' + my_outputImageNow + '_v02.image')
    os.system('rm -rf ' + my_outputImageNow + '_v02.image.pbcor')
    os.system('rm -rf ' + my_outputImageNow + '_v02.residual')
    os.system('rm -rf ' + my_outputImageNow + '_v02.mask')
    os.system('rm -rf ' + my_outputImageNow + '_v02.model')
    os.system('rm -rf ' + my_outputImageNow + '_v03.image')
    os.system('rm -rf ' + my_outputImageNow + '_v03.image.pbcor')
    os.system('rm -rf ' + my_outputImageNow + '_v03.residual')
    os.system('rm -rf ' + my_outputImageNow + '_v03.mask')
    os.system('rm -rf ' + my_outputImageNow + '_v03.model')


########################################################################
#
# STEP 0: 
# Create joint-deconvolved continuum image
#
mystep = 0
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    my_functionGetCellsizeImsize(my_telescope, my_source)
    my_functionJointDeconvolutionContinuum(my_telescope, my_source)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 1: 
# UV continuum subtraction for line cubes
#
mystep = 1
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    my_functionUVContinuumSubtractionForJointDeconvolution(my_telescope, my_source)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEPS 2 to 31: 
# Joint deconvolution for line cubes (spw 0) chunks 1/30 to 30/30
#
if (mycurrentstep == "step2") or (mycurrentstep == "step3") or (mycurrentstep == "step4") or (mycurrentstep == "step5") or (mycurrentstep == "step6") or (mycurrentstep == "step7") or (mycurrentstep == "step8") or (mycurrentstep == "step9") or (mycurrentstep == "step10") or (mycurrentstep == "step11") or (mycurrentstep == "step12") or (mycurrentstep == "step13") or (mycurrentstep == "step14") or (mycurrentstep == "step15") or (mycurrentstep == "step16") or (mycurrentstep == "step17") or (mycurrentstep == "step18") or (mycurrentstep == "step19") or (mycurrentstep == "step20") or (mycurrentstep == "step21") or (mycurrentstep == "step22") or (mycurrentstep == "step23") or (mycurrentstep == "step24") or (mycurrentstep == "step25") or (mycurrentstep == "step26") or (mycurrentstep == "step27") or (mycurrentstep == "step28") or (mycurrentstep == "step29") or (mycurrentstep == "step30") or (mycurrentstep == "step31"):

    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mycurrentstep))
    
    # Joint deconvolution of 7M, TM2 and TM1 for cube spw 0 chunks 1/30 to 30/30
    #
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        
        my_chunkNameList, my_currentStepList, my_startingChannelList, my_numberOfChannelsList = my_functionCreateChunks(30, my_spw)
        #my_currentStepList = ['step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8', 'step9', 'step10', 'step11', 'step12', 'step13', 'step14', 'step15', 'step16', 'step17', 'step18', 'step19', 'step20', 'step21', 'step22', 'step23', 'step24', 'step25', 'step26', 'step27', 'step28', 'step29', 'step30', 'step31']
        #my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        #my_startingChannelList =  [  12,  140,  268,  396,  524,  652,  780,  908, 1036, 1164, 1292, 1420, 1548, 1676, 1804, 1932, 2060, 2188, 2316, 2444, 2572, 2700, 2828, 2956, 3084, 3212, 3340, 3468, 3596, 3724]
        #my_numberOfChannelsList = [ 128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  114]
        
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
        
        print("... processing " + str(mycurrentstep) + " corresponding to chunk " + str(my_chunkName) + " with starting channel " + str(my_startingChannel) + " and total number of channels " + str(my_numberOfChannels))
        
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        ##my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        #ASM#my_functionJointDeconvolutionCube(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        my_functionJointDeconvolutionCubeV2(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 32: 
# Merge joint-deconvolved chunk cubes (spw 0)
#
mystep = 32
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 0)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk1' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk1' + my_extension + ' ' + my_outputImage + '_chunk2' + my_extension + ' ' + my_outputImage + '_chunk3' + my_extension + ' ' + my_outputImage + '_chunk4' + my_extension + ' ' + my_outputImage + '_chunk5' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk1' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 33: 
# Merge joint-deconvolved chunk cubes (spw 0)
#
mystep = 33
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 0)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk6' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk6' + my_extension + ' ' + my_outputImage + '_chunk7' + my_extension + ' ' + my_outputImage + '_chunk8' + my_extension + ' ' + my_outputImage + '_chunk9' + my_extension + ' ' + my_outputImage + '_chunk10' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk2' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 34: 
# Merge joint-deconvolved chunk cubes (spw 0)
#
mystep = 34
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 0)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk11' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk11' + my_extension + ' ' + my_outputImage + '_chunk12' + my_extension + ' ' + my_outputImage + '_chunk13' + my_extension + ' ' + my_outputImage + '_chunk14' + my_extension + ' ' + my_outputImage + '_chunk15' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk3' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 35: 
# Merge joint-deconvolved chunk cubes (spw 0)
#
mystep = 35
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 0)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk16' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk16' + my_extension + ' ' + my_outputImage + '_chunk17' + my_extension + ' ' + my_outputImage + '_chunk18' + my_extension + ' ' + my_outputImage + '_chunk19' + my_extension + ' ' + my_outputImage + '_chunk20' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk4' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 36: 
# Merge joint-deconvolved chunk cubes (spw 0)
#
mystep = 36
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 0)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk21' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk21' + my_extension + ' ' + my_outputImage + '_chunk22' + my_extension + ' ' + my_outputImage + '_chunk23' + my_extension + ' ' + my_outputImage + '_chunk24' + my_extension + ' ' + my_outputImage + '_chunk25' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk5' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 37: 
# Merge joint-deconvolved chunk cubes (spw 0)
#
mystep = 37
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 0)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk26' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk26' + my_extension + ' ' + my_outputImage + '_chunk27' + my_extension + ' ' + my_outputImage + '_chunk28' + my_extension + ' ' + my_outputImage + '_chunk29' + my_extension + ' ' + my_outputImage + '_chunk30' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk6' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 38: 
# Merge joint-deconvolved chunk cubes (spw 0)
#
mystep = 38
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 0)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chonk1' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chonk1' + my_extension + ' ' + my_outputImage + '_chonk2' + my_extension + ' ' + my_outputImage + '_chonk3' + my_extension + ' ' + my_outputImage + '_chonk4' + my_extension + ' ' + my_outputImage + '_chonk5' + my_extension + ' ' + my_outputImage + '_chonk6' + my_extension
                my_outfileImageConcat = my_outputImage + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 39: 
# Smooth to common beam joint-deconvolved cubes (spw 0)
#

mystep = 39
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 0
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Smooth the images to a common beam for all channels
        # Apply also a mask based on the primary beam response
        #
        # Crete mask based on primary beam
        print("... creating mask using primary beam")
        os.system('rm -rf ' + str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask')
        immath(imagename = [str(my_runningPath) + '/almagal/' + my_outputImage + '.pb', str(my_runningPath) + '/almagal/' + my_outputImage + '.pb'],
            expr = 'IM0/IM1',
            outfile = str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask')
        #
        print("... convolving images to a common beam")
        for my_extension in ['.image', '.image.pbcor']:
            #
            # Smooth to common beam
            print("... convolving images to a common beam / step imsmooth")
            os.system('mv ' + str(my_runningPath) + '/almagal/' + my_outputImage + my_extension + ' ' + str(my_runningPath) + '/almagal/' + my_outputImage + '_multiBeam' + my_extension)
            imsmooth(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '_multiBeam' + my_extension,
                outfile = str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension,
                kernel = 'commonbeam')
            #
            # Mask based on primary beam
            print("... convolving images to a common beam / step immath")
            immath(imagename = [str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension, str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask'],
                expr = 'IM0*IM1',
                imagemd = str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension,
                outfile = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension)
            #
            # Export to fits format
            print("... convolving images to a common beam / step exportfits")
            exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension,
                fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension + '.fits',
                dropdeg = True,
                overwrite = True)
        
        exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '.residual',
            fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + '.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '.mask',
            fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + '.mask.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '.psf',
            fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + '.psf.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '.pb',
            fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + '.pb.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '.model',
            fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + '.model.fits',
            dropdeg = True,
            overwrite = True)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEPS 40 to 69: 
# Joint deconvolution for line cubes (spw 1) chunks 1/30 to 30/30
#
if (mycurrentstep == "step40") or (mycurrentstep == "step41") or (mycurrentstep == "step42") or (mycurrentstep == "step43") or (mycurrentstep == "step44") or (mycurrentstep == "step45") or (mycurrentstep == "step46") or (mycurrentstep == "step47") or (mycurrentstep == "step48") or (mycurrentstep == "step49") or (mycurrentstep == "step50") or (mycurrentstep == "step51") or (mycurrentstep == "step52") or (mycurrentstep == "step53") or (mycurrentstep == "step54") or (mycurrentstep == "step55") or (mycurrentstep == "step56") or (mycurrentstep == "step57") or (mycurrentstep == "step58") or (mycurrentstep == "step59") or (mycurrentstep == "step60") or (mycurrentstep == "step61") or (mycurrentstep == "step62") or (mycurrentstep == "step63") or (mycurrentstep == "step64") or (mycurrentstep == "step65") or (mycurrentstep == "step66") or (mycurrentstep == "step67") or (mycurrentstep == "step68") or (mycurrentstep == "step69"):

    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mycurrentstep))
    
    # Joint deconvolution of 7M, TM2 and TM1 for cube spw 1 chunks 1/30 to 30/30
    #
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        
        my_chunkNameList, my_currentStepList, my_startingChannelList, my_numberOfChannelsList = my_functionCreateChunks(30, my_spw)
        #my_currentStepList = ['step34', 'step35', 'step36', 'step37', 'step38', 'step39', 'step40', 'step41', 'step42', 'step43', 'step44', 'step45', 'step46', 'step47', 'step48', 'step49', 'step50', 'step51', 'step52', 'step53', 'step54', 'step55', 'step56', 'step57', 'step58', 'step59', 'step60', 'step61', 'step62', 'step63']
        #my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        #my_startingChannelList =  [  12,  140,  268,  396,  524,  652,  780,  908, 1036, 1164, 1292, 1420, 1548, 1676, 1804, 1932, 2060, 2188, 2316, 2444, 2572, 2700, 2828, 2956, 3084, 3212, 3340, 3468, 3596, 3724]
        #my_numberOfChannelsList = [ 128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  114]
        ##my_currentStepList = ['step14', 'step15', 'step16', 'step17', 'step18', 'step19', 'step20', 'step21', 'step22', 'step23']
        ##my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ##my_startingChannelList = [12, 382, 762, 1142, 1522, 1902, 2282, 2662, 3042, 3422]
        ##my_numberOfChannelsList = [370, 380, 380, 380, 380, 380, 380, 380, 380, 416]
        
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
        
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        ##my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        #ASM#my_functionJointDeconvolutionCube(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        my_functionJointDeconvolutionCubeV2(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 70: 
# Merge joint-deconvolved chunk cubes (spw 1)
#
mystep = 70
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 1)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk1' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk1' + my_extension + ' ' + my_outputImage + '_chunk2' + my_extension + ' ' + my_outputImage + '_chunk3' + my_extension + ' ' + my_outputImage + '_chunk4' + my_extension + ' ' + my_outputImage + '_chunk5' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk1' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 71: 
# Merge joint-deconvolved chunk cubes (spw 1)
#
mystep = 71
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 1)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk6' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk6' + my_extension + ' ' + my_outputImage + '_chunk7' + my_extension + ' ' + my_outputImage + '_chunk8' + my_extension + ' ' + my_outputImage + '_chunk9' + my_extension + ' ' + my_outputImage + '_chunk10' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk2' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 72: 
# Merge joint-deconvolved chunk cubes (spw 1)
#
mystep = 72
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 1)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk11' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk11' + my_extension + ' ' + my_outputImage + '_chunk12' + my_extension + ' ' + my_outputImage + '_chunk13' + my_extension + ' ' + my_outputImage + '_chunk14' + my_extension + ' ' + my_outputImage + '_chunk15' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk3' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 73: 
# Merge joint-deconvolved chunk cubes (spw 1)
#
mystep = 73
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 1)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk16' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk16' + my_extension + ' ' + my_outputImage + '_chunk17' + my_extension + ' ' + my_outputImage + '_chunk18' + my_extension + ' ' + my_outputImage + '_chunk19' + my_extension + ' ' + my_outputImage + '_chunk20' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk4' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 74: 
# Merge joint-deconvolved chunk cubes (spw 1)
#
mystep = 74
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 1)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk21' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk21' + my_extension + ' ' + my_outputImage + '_chunk22' + my_extension + ' ' + my_outputImage + '_chunk23' + my_extension + ' ' + my_outputImage + '_chunk24' + my_extension + ' ' + my_outputImage + '_chunk25' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk5' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 75: 
# Merge joint-deconvolved chunk cubes (spw 1)
#
mystep = 75
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 1)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk26' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk26' + my_extension + ' ' + my_outputImage + '_chunk27' + my_extension + ' ' + my_outputImage + '_chunk28' + my_extension + ' ' + my_outputImage + '_chunk29' + my_extension + ' ' + my_outputImage + '_chunk30' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk6' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 76: 
# Merge joint-deconvolved chunk cubes (spw 1)
#
mystep = 76
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 1)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chonk1' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chonk1' + my_extension + ' ' + my_outputImage + '_chonk2' + my_extension + ' ' + my_outputImage + '_chonk3' + my_extension + ' ' + my_outputImage + '_chonk4' + my_extension + ' ' + my_outputImage + '_chonk5' + my_extension + ' ' + my_outputImage + '_chonk6' + my_extension
                my_outfileImageConcat = my_outputImage + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 77: 
# Smooth to common beam joint-deconvolved cubes (spw 1)
#

mystep = 77
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 1
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Smooth the images to a common beam for all channels
        # Apply also a mask based on the primary beam response
        #
        # Crete mask based on primary beam
        print("... creating mask using primary beam")
        os.system('rm -rf ' + str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask')
        immath(imagename = [str(my_runningPath) + '/almagal/' + my_outputImage + '.pb', str(my_runningPath) + '/almagal/' + my_outputImage + '.pb'],
            expr = 'IM0/IM1',
            outfile = str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask')
        #
        print("... convolving images to a common beam")
        for my_extension in ['.image', '.image.pbcor']:
            #
            # Smooth to common beam
            print("... convolving images to a common beam / step imsmooth")
            os.system('mv ' + str(my_runningPath) + '/almagal/' + my_outputImage + my_extension + ' ' + str(my_runningPath) + '/almagal/' + my_outputImage + '_multiBeam' + my_extension)
            imsmooth(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '_multiBeam' + my_extension,
                outfile = str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension,
                kernel = 'commonbeam')
            #
            # Mask based on primary beam
            print("... convolving images to a common beam / step immath")
            immath(imagename = [str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension, str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask'],
                expr = 'IM0*IM1',
                imagemd = str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension,
                outfile = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension)
            #
            # Export to fits format
            print("... convolving images to a common beam / step exportfits")
            exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension,
                fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension + '.fits',
                dropdeg = True,
                overwrite = True)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEPS 78 to 107: 
# Joint deconvolution for line cubes (spw 2) chunks 1/30 to 30/30
#
if (mycurrentstep == "step78") or (mycurrentstep == "step79") or (mycurrentstep == "step80") or (mycurrentstep == "step81") or (mycurrentstep == "step82") or (mycurrentstep == "step83") or (mycurrentstep == "step84") or (mycurrentstep == "step85") or (mycurrentstep == "step86") or (mycurrentstep == "step87") or (mycurrentstep == "step88") or (mycurrentstep == "step89") or (mycurrentstep == "step90") or (mycurrentstep == "step91") or (mycurrentstep == "step92") or (mycurrentstep == "step93") or (mycurrentstep == "step94") or (mycurrentstep == "step95") or (mycurrentstep == "step96") or (mycurrentstep == "step97") or (mycurrentstep == "step98") or (mycurrentstep == "step99") or (mycurrentstep == "step100") or (mycurrentstep == "step101") or (mycurrentstep == "step102") or (mycurrentstep == "step103") or (mycurrentstep == "step104") or (mycurrentstep == "step105") or (mycurrentstep == "step106") or (mycurrentstep == "step107"):

    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mycurrentstep))
    
    # Joint deconvolution of 7M, TM2 and TM1 for cube spw 2 chunks 1/30 to 30/30
    #
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        
        my_chunkNameList, my_currentStepList, my_startingChannelList, my_numberOfChannelsList = my_functionCreateChunks(30, my_spw)
        #my_currentStepList = ['step66', 'step67', 'step68', 'step69', 'step70', 'step71', 'step72', 'step73', 'step74', 'step75', 'step76', 'step77', 'step78', 'step79', 'step80', 'step81', 'step82', 'step83', 'step84', 'step85', 'step86', 'step87', 'step88', 'step89', 'step90', 'step91', 'step92', 'step93', 'step94', 'step95']
        #my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        #my_startingChannelList =  [  12,  140,  268,  396,  524,  652,  780,  908, 1036, 1164, 1292, 1420, 1548, 1676, 1804, 1932, 2060, 2188, 2316, 2444, 2572, 2700, 2828, 2956, 3084, 3212, 3340, 3468, 3596, 3724]
        #my_numberOfChannelsList = [ 128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  114]
        ##my_currentStepList = ['step26', 'step27', 'step28', 'step29', 'step30', 'step31', 'step32', 'step33', 'step34', 'step35']
        ##my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ##my_startingChannelList = [12, 382, 762, 1142, 1522, 1902, 2282, 2662, 3042, 3422]
        ##my_numberOfChannelsList = [370, 380, 380, 380, 380, 380, 380, 380, 380, 416]
        
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
        
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        ##my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        #ASM#my_functionJointDeconvolutionCube(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        my_functionJointDeconvolutionCubeV2(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 108: 
# Merge joint-deconvolved chunk cubes (spw 2)
#
mystep = 108
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 2)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk1' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk1' + my_extension + ' ' + my_outputImage + '_chunk2' + my_extension + ' ' + my_outputImage + '_chunk3' + my_extension + ' ' + my_outputImage + '_chunk4' + my_extension + ' ' + my_outputImage + '_chunk5' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk1' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 109: 
# Merge joint-deconvolved chunk cubes (spw 2)
#
mystep = 109
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 2)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk6' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk6' + my_extension + ' ' + my_outputImage + '_chunk7' + my_extension + ' ' + my_outputImage + '_chunk8' + my_extension + ' ' + my_outputImage + '_chunk9' + my_extension + ' ' + my_outputImage + '_chunk10' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk2' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 110: 
# Merge joint-deconvolved chunk cubes (spw 2)
#
mystep = 110
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 2)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk11' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk11' + my_extension + ' ' + my_outputImage + '_chunk12' + my_extension + ' ' + my_outputImage + '_chunk13' + my_extension + ' ' + my_outputImage + '_chunk14' + my_extension + ' ' + my_outputImage + '_chunk15' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk3' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 111: 
# Merge joint-deconvolved chunk cubes (spw 2)
#
mystep = 111
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 2)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk16' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk16' + my_extension + ' ' + my_outputImage + '_chunk17' + my_extension + ' ' + my_outputImage + '_chunk18' + my_extension + ' ' + my_outputImage + '_chunk19' + my_extension + ' ' + my_outputImage + '_chunk20' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk4' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 112: 
# Merge joint-deconvolved chunk cubes (spw 2)
#
mystep = 112
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 2)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk21' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk21' + my_extension + ' ' + my_outputImage + '_chunk22' + my_extension + ' ' + my_outputImage + '_chunk23' + my_extension + ' ' + my_outputImage + '_chunk24' + my_extension + ' ' + my_outputImage + '_chunk25' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk5' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 113: 
# Merge joint-deconvolved chunk cubes (spw 2)
#
mystep = 113
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 2)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk26' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk26' + my_extension + ' ' + my_outputImage + '_chunk27' + my_extension + ' ' + my_outputImage + '_chunk28' + my_extension + ' ' + my_outputImage + '_chunk29' + my_extension + ' ' + my_outputImage + '_chunk30' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk6' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 114: 
# Merge joint-deconvolved chunk cubes (spw 2)
#
mystep = 114
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 2)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chonk1' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chonk1' + my_extension + ' ' + my_outputImage + '_chonk2' + my_extension + ' ' + my_outputImage + '_chonk3' + my_extension + ' ' + my_outputImage + '_chonk4' + my_extension + ' ' + my_outputImage + '_chonk5' + my_extension + ' ' + my_outputImage + '_chonk6' + my_extension
                my_outfileImageConcat = my_outputImage + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 115: 
# Smooth to common beam joint-deconvolved cubes (spw 2)
#

mystep = 115
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 2
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Smooth the images to a common beam for all channels
        # Apply also a mask based on the primary beam response
        #
        # Crete mask based on primary beam
        print("... creating mask using primary beam")
        os.system('rm -rf ' + str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask')
        immath(imagename = [str(my_runningPath) + '/almagal/' + my_outputImage + '.pb', str(my_runningPath) + '/almagal/' + my_outputImage + '.pb'],
            expr = 'IM0/IM1',
            outfile = str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask')
        #
        print("... convolving images to a common beam")
        for my_extension in ['.image', '.image.pbcor']:
            #
            # Smooth to common beam
            print("... convolving images to a common beam / step imsmooth")
            os.system('mv ' + str(my_runningPath) + '/almagal/' + my_outputImage + my_extension + ' ' + str(my_runningPath) + '/almagal/' + my_outputImage + '_multiBeam' + my_extension)
            imsmooth(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '_multiBeam' + my_extension,
                outfile = str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension,
                kernel = 'commonbeam')
            #
            # Mask based on primary beam
            print("... convolving images to a common beam / step immath")
            immath(imagename = [str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension, str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask'],
                expr = 'IM0*IM1',
                imagemd = str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension,
                outfile = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension)
            #
            # Export to fits format
            print("... convolving images to a common beam / step exportfits")
            exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension,
                fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension + '.fits',
                dropdeg = True,
                overwrite = True)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEPS 116 to 145: 
# Joint deconvolution for line cubes (spw 3) chunks 1/30 to 30/30
#
if (mycurrentstep == "step116") or (mycurrentstep == "step117") or (mycurrentstep == "step118") or (mycurrentstep == "step119") or (mycurrentstep == "step120") or (mycurrentstep == "step121") or (mycurrentstep == "step122") or (mycurrentstep == "step123") or (mycurrentstep == "step124") or (mycurrentstep == "step125") or (mycurrentstep == "step126") or (mycurrentstep == "step127") or (mycurrentstep == "step128") or (mycurrentstep == "step129") or (mycurrentstep == "step130") or (mycurrentstep == "step131") or (mycurrentstep == "step132") or (mycurrentstep == "step133") or (mycurrentstep == "step134") or (mycurrentstep == "step135") or (mycurrentstep == "step136") or (mycurrentstep == "step137") or (mycurrentstep == "step138") or (mycurrentstep == "step139") or (mycurrentstep == "step140") or (mycurrentstep == "step141") or (mycurrentstep == "step142") or (mycurrentstep == "step143") or (mycurrentstep == "step144") or (mycurrentstep == "step145"):

    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mycurrentstep))
    
    # Joint deconvolution of 7M, TM2 and TM1 for cube spw 3 chunks 1/30 to 30/30
    #
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        
        my_chunkNameList, my_currentStepList, my_startingChannelList, my_numberOfChannelsList = my_functionCreateChunks(30, my_spw)
        #my_currentStepList = ['step98', 'step99', 'step100', 'step101', 'step102', 'step103', 'step104', 'step105', 'step106', 'step107', 'step108', 'step109', 'step110', 'step111', 'step112', 'step113', 'step114', 'step115', 'step116', 'step117', 'step118', 'step119', 'step120', 'step121', 'step122', 'step123', 'step124', 'step125', 'step126', 'step127']
        #my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        #my_startingChannelList =  [  12,  140,  268,  396,  524,  652,  780,  908, 1036, 1164, 1292, 1420, 1548, 1676, 1804, 1932, 2060, 2188, 2316, 2444, 2572, 2700, 2828, 2956, 3084, 3212, 3340, 3468, 3596, 3724]
        #my_numberOfChannelsList = [ 128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  114]
        ##my_currentStepList = ['step38', 'step39', 'step40', 'step41', 'step42', 'step43', 'step44', 'step45', 'step46', 'step47']
        ##my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ##my_startingChannelList = [12, 382, 762, 1142, 1522, 1902, 2282, 2662, 3042, 3422]
        ##my_numberOfChannelsList = [370, 380, 380, 380, 380, 380, 380, 380, 380, 416]
        
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
        
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        ##my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        #ASM#my_functionJointDeconvolutionCube(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        my_functionJointDeconvolutionCubeV2(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 146: 
# Merge joint-deconvolved chunk cubes (spw 3)
#
mystep = 146
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 3)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk1' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk1' + my_extension + ' ' + my_outputImage + '_chunk2' + my_extension + ' ' + my_outputImage + '_chunk3' + my_extension + ' ' + my_outputImage + '_chunk4' + my_extension + ' ' + my_outputImage + '_chunk5' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk1' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 147: 
# Merge joint-deconvolved chunk cubes (spw 3)
#
mystep = 147
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 3)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk6' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk6' + my_extension + ' ' + my_outputImage + '_chunk7' + my_extension + ' ' + my_outputImage + '_chunk8' + my_extension + ' ' + my_outputImage + '_chunk9' + my_extension + ' ' + my_outputImage + '_chunk10' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk2' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 148: 
# Merge joint-deconvolved chunk cubes (spw 3)
#
mystep = 148
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 3)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk11' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk11' + my_extension + ' ' + my_outputImage + '_chunk12' + my_extension + ' ' + my_outputImage + '_chunk13' + my_extension + ' ' + my_outputImage + '_chunk14' + my_extension + ' ' + my_outputImage + '_chunk15' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk3' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 149: 
# Merge joint-deconvolved chunk cubes (spw 3)
#
mystep = 149
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 3)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk16' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk16' + my_extension + ' ' + my_outputImage + '_chunk17' + my_extension + ' ' + my_outputImage + '_chunk18' + my_extension + ' ' + my_outputImage + '_chunk19' + my_extension + ' ' + my_outputImage + '_chunk20' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk4' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 150: 
# Merge joint-deconvolved chunk cubes (spw 3)
#
mystep = 150
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 3)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk21' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk21' + my_extension + ' ' + my_outputImage + '_chunk22' + my_extension + ' ' + my_outputImage + '_chunk23' + my_extension + ' ' + my_outputImage + '_chunk24' + my_extension + ' ' + my_outputImage + '_chunk25' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk5' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 151: 
# Merge joint-deconvolved chunk cubes (spw 3)
#
mystep = 151
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 3)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk26' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk26' + my_extension + ' ' + my_outputImage + '_chunk27' + my_extension + ' ' + my_outputImage + '_chunk28' + my_extension + ' ' + my_outputImage + '_chunk29' + my_extension + ' ' + my_outputImage + '_chunk30' + my_extension
                my_outfileImageConcat = my_outputImage + '_chonk6' + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 152: 
# Merge joint-deconvolved chunk cubes (spw 3)
#
mystep = 152
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 3)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chonk1' + my_extension):
                print("... processing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chonk1' + my_extension + ' ' + my_outputImage + '_chonk2' + my_extension + ' ' + my_outputImage + '_chonk3' + my_extension + ' ' + my_outputImage + '_chonk4' + my_extension + ' ' + my_outputImage + '_chonk5' + my_extension + ' ' + my_outputImage + '_chonk6' + my_extension
                my_outfileImageConcat = my_outputImage + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 153: 
# Smooth to common beam joint-deconvolved cubes (spw 3)
#

mystep = 153
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2TM1"):
        
        my_spw = 3
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Smooth the images to a common beam for all channels
        # Apply also a mask based on the primary beam response
        #
        # Crete mask based on primary beam
        print("... creating mask using primary beam")
        os.system('rm -rf ' + str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask')
        immath(imagename = [str(my_runningPath) + '/almagal/' + my_outputImage + '.pb', str(my_runningPath) + '/almagal/' + my_outputImage + '.pb'],
            expr = 'IM0/IM1',
            outfile = str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask')
        #
        print("... convolving images to a common beam")
        for my_extension in ['.image', '.image.pbcor']:
            #
            # Smooth to common beam
            print("... convolving images to a common beam / step imsmooth")
            os.system('mv ' + str(my_runningPath) + '/almagal/' + my_outputImage + my_extension + ' ' + str(my_runningPath) + '/almagal/' + my_outputImage + '_multiBeam' + my_extension)
            imsmooth(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + '_multiBeam' + my_extension,
                outfile = str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension,
                kernel = 'commonbeam')
            #
            # Mask based on primary beam
            print("... convolving images to a common beam / step immath")
            immath(imagename = [str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension, str(my_runningPath) + '/almagal/' + my_outputImage + '.pbmask'],
                expr = 'IM0*IM1',
                imagemd = str(my_runningPath) + '/almagal/' + my_outputImage + '_commonBeam' + my_extension,
                outfile = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension)
            #
            # Export to fits format
            print("... convolving images to a common beam / step exportfits")
            exportfits(imagename = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension,
                fitsimage = str(my_runningPath) + '/almagal/' + my_outputImage + my_extension + '.fits',
                dropdeg = True,
                overwrite = True)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")
