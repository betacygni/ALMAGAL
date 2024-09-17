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
def my_functionJointDeconvolutionContinuum(my_telescope, my_source):
    
    """
    help
    """
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    
    # Run TCLEAN task
    #
    tclean(vis = my_visfilestoclean,
        imagename = my_outputImage,
        field = my_source,
        stokes = 'I',
        spw = my_freqs,
        outframe = 'LSRK',
        restfreq = '',
        specmode = 'mfs',
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
        restoringbeam = 'common')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImage + '.image',
        fitsimage = my_outputImage + '.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImage + '.image.pbcor',
        fitsimage = my_outputImage + '.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImage + '.residual',
        fitsimage = my_outputImage + '.residual.fits',
        dropdeg = True,
        overwrite = True)


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
    # Define SPW range based on the TM2 frequency coverage
    # This SPW range will be used to split out the corresponding frequency range from the 7M and TM1 data
    #
    my_commongTM2SPWRange = '0:'+str(np.min(my_freqsLSRKTM2spw0))+'~'+str(np.max(my_freqsLSRKTM2spw0))+'Hz,1:'+str(np.min(my_freqsLSRKTM2spw1))+'~'+str(np.max(my_freqsLSRKTM2spw1))+'Hz,2:'+str(np.min(my_freqsLSRKTM2spw2))+'~'+str(np.max(my_freqsLSRKTM2spw2))+'Hz,3:'+str(np.min(my_freqsLSRKTM2spw3))+'~'+str(np.max(my_freqsLSRKTM2spw3))+'Hz'
    
    if my_add7M == True:
        for visfile7M in vislist7M:
            split(vis = visfile7M+'.contsub.mstrans',
                datacolumn = 'data',
                spw = my_commongTM2SPWRange,
                outputvis = visfile7M+'.likeTM2.contsub.mstrans')
    
    if my_addTM1 == True:
        for visfileTM1 in vislistTM1:
            split(vis = visfileTM1+'.contsub.mstrans',
                datacolumn = 'data',
                spw = my_commongTM2SPWRange,
                outputvis = visfileTM1+'.likeTM2.contsub.mstrans')
                
    # Clean-up measurement sets that will not be used later on
    # i.e., keep only visfile7M+'.contsub.mstrans.split and visfileTM2+'.contsub.mstrans files
    # BUGFIX: bjones 21.07.2021 - changed from removing visfile7M/TM2 to all visfiles 
    #
    if my_add7M == True:
        print(" CLEANING UP 7M")
        print(vislist7M)
        for visfile7M in vislist7M:
            os.system('rm -rf ' + visfile7M)
            os.system('rm -rf ' + visfile7M + '.contsub')
            os.system('rm -rf ' + visfile7M + '.contsub.mstrans')
    if my_addTM2 == True:
        print(" CLEANING UP TM2")
        print(vislistTM2)
        for visfileTM2 in vislistTM2:
            os.system('rm -rf ' + visfileTM2)
            os.system('rm -rf ' + visfileTM2 + '.contsub')
    if my_addTM1 == True:
        print(" CLEANING UP TM1")
        print(vislistTM1)
        for visfileTM1 in vislistTM1:
            os.system('rm -rf ' + visfileTM1)
            os.system('rm -rf ' + visfileTM1 + '.contsub')
            os.system('rm -rf ' + visfileTM1 + '.contsub.mstrans')


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
    if (cleanrms > 0.0):
        os.system('rm -rf ' + cubeName + '.reclean.*')
        extrachannels=au.amendMaskForCube(cubeName,
                                          intensityThreshold=cleanrms*2.,  # times 2 added by ASM
                                          maskThreshold=cleanrms*maskThreshFactor,
                                          maskThresholdFraction=maskThreshFraction,
                                          npixels=25,pblimit=0.3,overwriteMask=False,cleanup=True,
                                          masknameInsert='.reclean',
                                          verbose=False,dryrun=False)
        if len(extrachannels) != 0:
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


########################################################################
#
# STEP 0: 
# Create joint-deconvolved continuum image
#
mystep = 0
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
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
# STEPS 2 to 11: 
# Joint deconvolution for line cubes (spw 0) chunks 1/10 to 10/10
#
if (mycurrentstep == "step2") or (mycurrentstep == "step3") or (mycurrentstep == "step4") or (mycurrentstep == "step5") or (mycurrentstep == "step6") or (mycurrentstep == "step7") or (mycurrentstep == "step8") or (mycurrentstep == "step9") or (mycurrentstep == "step10") or (mycurrentstep == "step11"):

    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mycurrentstep))
    
    # Joint deconvolution of 7M and TM2 for cube spw 0 chunks 1/10 to 10/10
    #
    if (my_telescope == "7MTM2"):
        
        my_spw = 0
        
        my_currentStepList = ['step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8', 'step9', 'step10', 'step11']
        my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        my_startingChannelList = [2, 382, 762, 1142, 1522, 1902, 2282, 2662, 3042, 3422]
        my_numberOfChannelsList = [380, 380, 380, 380, 380, 380, 380, 380, 380, 416]
        
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
        
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        ##my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        my_functionJointDeconvolutionCube(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")

########################################################################
#
# STEP 12: 
# Merge joint-deconvolved chunk cubes (spw 0)
#
mystep = 12
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2"):
        
        my_spw = 0
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 0)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk1' + my_extension):
                print("... procssing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk1' + my_extension + ' ' + my_outputImage + '_chunk2' + my_extension + ' ' + my_outputImage + '_chunk3' + my_extension + ' ' + my_outputImage + '_chunk4' + my_extension + ' ' + my_outputImage + '_chunk5' + my_extension + ' ' + my_outputImage + '_chunk6' + my_extension + ' ' + my_outputImage + '_chunk7' + my_extension + ' ' + my_outputImage + '_chunk8' + my_extension + ' ' + my_outputImage + '_chunk9' + my_extension + ' ' + my_outputImage + '_chunk10' + my_extension
                my_outfileImageConcat = my_outputImage + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 13: 
# Smooth to common beam joint-deconvolved cubes (spw 0)
#

mystep = 13
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2"):
        
        my_spw = 0
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
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
# STEPS 14 to 23: 
# Joint deconvolution for line cubes (spw 1) chunks 1/10 to 10/10
#
if (mycurrentstep == "step14") or (mycurrentstep == "step15") or (mycurrentstep == "step16") or (mycurrentstep == "step17") or (mycurrentstep == "step18") or (mycurrentstep == "step19") or (mycurrentstep == "step20") or (mycurrentstep == "step21") or (mycurrentstep == "step22") or (mycurrentstep == "step23"):

    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mycurrentstep))
    
    # Joint deconvolution of 7M and TM2 for cube spw 1 chunks 1/10 to 10/10
    #
    if (my_telescope == "7MTM2"):
        
        my_spw = 1
        
        my_currentStepList = ['step14', 'step15', 'step16', 'step17', 'step18', 'step19', 'step20', 'step21', 'step22', 'step23']
        my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        my_startingChannelList = [2, 382, 762, 1142, 1522, 1902, 2282, 2662, 3042, 3422]
        my_numberOfChannelsList = [380, 380, 380, 380, 380, 380, 380, 380, 380, 416]
        
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
        
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        ##my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        my_functionJointDeconvolutionCube(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 24: 
# Merge joint-deconvolved chunk cubes (spw 1)
#
mystep = 24
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2"):
        
        my_spw = 1
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 1)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk1' + my_extension):
                print("... procssing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk1' + my_extension + ' ' + my_outputImage + '_chunk2' + my_extension + ' ' + my_outputImage + '_chunk3' + my_extension + ' ' + my_outputImage + '_chunk4' + my_extension + ' ' + my_outputImage + '_chunk5' + my_extension + ' ' + my_outputImage + '_chunk6' + my_extension + ' ' + my_outputImage + '_chunk7' + my_extension + ' ' + my_outputImage + '_chunk8' + my_extension + ' ' + my_outputImage + '_chunk9' + my_extension + ' ' + my_outputImage + '_chunk10' + my_extension
                my_outfileImageConcat = my_outputImage + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 25: 
# Smooth to common beam joint-deconvolved cubes (spw 1)
#

mystep = 25
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2"):
        
        my_spw = 1
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
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
# STEPS 26 to 35: 
# Joint deconvolution for line cubes (spw 2) chunks 1/10 to 10/10
#
if (mycurrentstep == "step26") or (mycurrentstep == "step27") or (mycurrentstep == "step28") or (mycurrentstep == "step29") or (mycurrentstep == "step30") or (mycurrentstep == "step31") or (mycurrentstep == "step32") or (mycurrentstep == "step33") or (mycurrentstep == "step34") or (mycurrentstep == "step35"):

    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mycurrentstep))
    
    # Joint deconvolution of 7M and TM2 for cube spw 2 chunks 1/10 to 10/10
    #
    if (my_telescope == "7MTM2"):
        
        my_spw = 2
        
        my_currentStepList = ['step26', 'step27', 'step28', 'step29', 'step30', 'step31', 'step32', 'step33', 'step34', 'step35']
        my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        my_startingChannelList = [2, 382, 762, 1142, 1522, 1902, 2282, 2662, 3042, 3422]
        my_numberOfChannelsList = [380, 380, 380, 380, 380, 380, 380, 380, 380, 416]
        
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
        
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        ##my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        my_functionJointDeconvolutionCube(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 36: 
# Merge joint-deconvolved chunk cubes (spw 2)
#
mystep = 36
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2"):
        
        my_spw = 2
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 2)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk1' + my_extension):
                print("... procssing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk1' + my_extension + ' ' + my_outputImage + '_chunk2' + my_extension + ' ' + my_outputImage + '_chunk3' + my_extension + ' ' + my_outputImage + '_chunk4' + my_extension + ' ' + my_outputImage + '_chunk5' + my_extension + ' ' + my_outputImage + '_chunk6' + my_extension + ' ' + my_outputImage + '_chunk7' + my_extension + ' ' + my_outputImage + '_chunk8' + my_extension + ' ' + my_outputImage + '_chunk9' + my_extension + ' ' + my_outputImage + '_chunk10' + my_extension
                my_outfileImageConcat = my_outputImage + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 37: 
# Smooth to common beam joint-deconvolved cubes (spw 2)
#

mystep = 37
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2"):
        
        my_spw = 2
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
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
# STEPS 38 to 47: 
# Joint deconvolution for line cubes (spw 3) chunks 1/10 to 10/10
#
if (mycurrentstep == "step38") or (mycurrentstep == "step39") or (mycurrentstep == "step40") or (mycurrentstep == "step41") or (mycurrentstep == "step42") or (mycurrentstep == "step43") or (mycurrentstep == "step44") or (mycurrentstep == "step45") or (mycurrentstep == "step46") or (mycurrentstep == "step47"):

    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mycurrentstep))
    
    # Joint deconvolution of 7M and TM2 for cube spw 3 chunks 1/10 to 10/10
    #
    if (my_telescope == "7MTM2"):
        
        my_spw = 3
        
        my_currentStepList = ['step38', 'step39', 'step40', 'step41', 'step42', 'step43', 'step44', 'step45', 'step46', 'step47']
        my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        my_startingChannelList = [2, 382, 762, 1142, 1522, 1902, 2282, 2662, 3042, 3422]
        my_numberOfChannelsList = [380, 380, 380, 380, 380, 380, 380, 380, 380, 416]
        
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
        
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        ##my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        my_functionJointDeconvolutionCube(my_spw, my_startingChannel, my_numberOfChannels, my_chunkName, my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean)
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 48: 
# Merge joint-deconvolved chunk cubes (spw 3)
#
mystep = 48
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2"):
        
        my_spw = 3
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
        #my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean = my_functionGetTcleanParametersJointDeconbolutionCube(my_telescope, my_spw)
        
        # Merge joint-deconvolved chunk cubes (spw 3)
        #
        for my_extension in ['.image', '.image.pbcor', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']:
            
            if os.path.isdir(my_outputImage + '_chunk1' + my_extension):
                print("... procssing file extension " + my_extension)
                my_infilesImageConcat = my_outputImage + '_chunk1' + my_extension + ' ' + my_outputImage + '_chunk2' + my_extension + ' ' + my_outputImage + '_chunk3' + my_extension + ' ' + my_outputImage + '_chunk4' + my_extension + ' ' + my_outputImage + '_chunk5' + my_extension + ' ' + my_outputImage + '_chunk6' + my_extension + ' ' + my_outputImage + '_chunk7' + my_extension + ' ' + my_outputImage + '_chunk8' + my_extension + ' ' + my_outputImage + '_chunk9' + my_extension + ' ' + my_outputImage + '_chunk10' + my_extension
                my_outfileImageConcat = my_outputImage + my_extension
                concatenatedimage = ia.imageconcat(outfile=my_outfileImageConcat, infiles=my_infilesImageConcat, axis=3, tempclose=False, overwrite=True)
                concatenatedimage.done()
        
        os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/images/combined/" + my_telescope + "/worked_" + mycurrentstep + ".txt")


########################################################################
#
# STEP 49: 
# Smooth to common beam joint-deconvolved cubes (spw 3)
#

mystep = 49
if(mystep in thesteps):
    
    print(':: ALMAGAL command :: Starting the joint-deconvolution procedures, step ' + str(mystep))
    
    if (my_telescope == "7MTM2"):
        
        my_spw = 3
        my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw)
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
