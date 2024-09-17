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


def my_functionJointDeconvolutionContinuumV2(my_telescope, my_source):
    
    """
    help
    """
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    
    print("HELLO!!!!! - initial")
    print(my_threshold)
    print("ADIOS!!!!! - initial")
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
    my_outputImageNow = my_outputImage+'_steps'
    print("HELLO!!!!! - step 0")
    print(my_threshold)
    print(my_number)
    print(my_unit)
    print(my_thresholdNow)
    print("ADIOS!!!!! - step 0")
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
        scales = my_scales,
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
        restoringbeam = 'common')
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v00.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v00.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v00.residual')
    os.system('cp -rp ' + my_outputImageNow + '.psf ' + my_outputImageNow + '_v00.psf')
    os.system('cp -rp ' + my_outputImageNow + '.model ' + my_outputImageNow + '_v00.model')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '_v00.image',
        fitsimage = my_outputImageNow + '_v00.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v00.image.pbcor',
        fitsimage = my_outputImageNow + '_v00.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v00.residual',
        fitsimage = my_outputImageNow + '_v00.residual.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v00.psf',
        fitsimage = my_outputImageNow + '_v00.psf.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v00.model',
        fitsimage = my_outputImageNow + '_v00.model.fits',
        dropdeg = True,
        overwrite = True)
    
    # First TCLEAN run:
    #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds to 2 times the final threshold
    #   - niter: right now is 5 times less the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.5*my_number) + my_unit
    my_outputImageNow = my_outputImage+'_steps'
    #my_niterNow = int(my_niter)
    #my_number, my_unit = separateNumbersUnits(my_threshold)
    #my_thresholdNow = str(my_number) + my_unit
    #my_outputImageNow = my_outputImage+'_steps'
    print("HELLO!!!!! - step 1")
    print(my_threshold)
    print(my_number)
    print(my_unit)
    print(my_thresholdNow)
    print(my_scales)
    print("ADIOS!!!!! - step 1")
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
        scales = my_scales,
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
        restoringbeam = 'common')
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v01.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v01.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v01.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')
    os.system('cp -rp ' + my_outputImageNow + '.psf ' + my_outputImageNow + '_v01.psf')
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
    exportfits(imagename = my_outputImageNow + '_v01.psf',
        fitsimage = my_outputImageNow + '_v01.psf.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v01.model',
        fitsimage = my_outputImageNow + '_v01.model.fits',
        dropdeg = True,
        overwrite = True)
    
    # Add the TM2 mask to the newly-created mask
    #
    print("Re-shape the mask")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/TM2.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_TM2.mask',
        output = str(my_runningPath) + '/almagal/processing/TM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/TM2.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v01.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask',
        output = my_outputImageNow + '.mask')
    
    # Second TCLEAN run:
    #  It uses the mask created first with 7M+TM2+TM1 data and the TM2 mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    #my_niterNow = my_niter
    #my_thresholdNow = my_threshold
    #my_outputImageNow = my_outputImage+'_steps'
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.0*my_number) + my_unit
    my_outputImageNow = my_outputImage+'_steps'
    print("HELLO!!!!! - step 2")
    print(my_threshold)
    print(my_number)
    print(my_unit)
    print(my_thresholdNow)
    my_scales = my_scales[3:]
    print(my_scales)
    print("ADIOS!!!!! - step 2")
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
        scales = my_scales,
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
        restoringbeam = 'common')
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v02.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v02.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v02.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v02.mask')
    os.system('cp -rp ' + my_outputImageNow + '.psf ' + my_outputImageNow + '_v02.psf')
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
    exportfits(imagename = my_outputImageNow + '_v02.psf',
        fitsimage = my_outputImageNow + '_v02.psf.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v02.model',
        fitsimage = my_outputImageNow + '_v02.model.fits',
        dropdeg = True,
        overwrite = True)
    
    # Add the TM2 mask to the newly-created mask
    #
    print("Re-shape the mask")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/7M.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_7M.mask',
        output = str(my_runningPath) + '/almagal/processing/7M.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/7M.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v02.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_with7M.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_with7M.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask',
        output = my_outputImageNow + '.mask')
    
    # Third TCLEAN run:
    #  It uses the mask created from the previous cleaning step plus the 7M mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    #my_niterNow = my_niter
    #my_thresholdNow = my_threshold
    #my_outputImageNow = my_outputImage+'_steps'
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.*my_number) + my_unit
    my_outputImageNow = my_outputImage+'_steps'
    print("HELLO!!!!! - step 3")
    print(my_threshold)
    print(my_number)
    print(my_unit)
    print(my_thresholdNow)
    my_scales = my_scales[1:]
    print(my_scales)
    print("ADIOS!!!!! - step 3")
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
        scales = my_scales,
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
        restoringbeam = 'common')
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v03.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v03.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v03.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v03.mask')
    os.system('cp -rp ' + my_outputImageNow + '.psf ' + my_outputImageNow + '_v03.psf')
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
    exportfits(imagename = my_outputImageNow + '_v03.psf',
        fitsimage = my_outputImageNow + '_v03.psf.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v03.model',
        fitsimage = my_outputImageNow + '_v03.model.fits',
        dropdeg = True,
        overwrite = True)
    
    # Fourth TCLEAN run:
    #  It starts with the mask created from the previous cleaning step
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold / 1.5 or 2.0 or 3.0 or 4.0
    #                if the threshold is above 150 microJy/beam
    #   - niter: right now is the final number of iterations x 10
    if (my_number > 150.e-6):
        my_niterNow = my_niter*10
        my_number, my_unit = separateNumbersUnits(my_threshold)
        print("HELLO!!!!! - step 4")
        print(my_threshold)
        print(my_number)
        print(my_unit)
        if (my_number >= 400.e-6):
            my_factor = 1.8
            my_thresholdNow = str(my_number/my_factor) + my_unit
        if (my_number >= 300.e-6) and (my_number < 400.e-6):
            my_factor = 1.5
            my_thresholdNow = str(my_number/my_factor) + my_unit
        if (my_number >= 200.e-6) and (my_number < 300.e-6):
            my_factor = 1.3
            my_thresholdNow = str(my_number/my_factor) + my_unit
        if (my_number < 200.e-6):
            my_factor = 1.0
            my_thresholdNow = str(my_number/my_factor) + my_unit
        my_outputImageNow = my_outputImage+'_steps'
        print("HELLO!!!!! - step 4")
        print(my_threshold)
        print(my_number)
        print(my_unit)
        print(my_thresholdNow)
        print(my_scales)
        print("ADIOS!!!!! - step 4")
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
            scales = my_scales,
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
            restoringbeam = 'common')
        
        os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v04.image')
        os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v04.image.pbcor')
        os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v04.residual')
        os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v04.mask')
        os.system('cp -rp ' + my_outputImageNow + '.psf ' + my_outputImageNow + '_v04.psf')
        os.system('cp -rp ' + my_outputImageNow + '.model ' + my_outputImageNow + '_v04.model')
        
        # Export image files to FITS format
        #
        exportfits(imagename = my_outputImageNow + '_v04.image',
            fitsimage = my_outputImageNow + '_v04.image.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '_v04.image.pbcor',
            fitsimage = my_outputImageNow + '_v04.image.pbcor.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '_v04.residual',
            fitsimage = my_outputImageNow + '_v04.residual.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '_v04.mask',
            fitsimage = my_outputImageNow + '_v04.mask.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '_v04.psf',
            fitsimage = my_outputImageNow + '_v04.psf.fits',
            dropdeg = True,
            overwrite = True)
        exportfits(imagename = my_outputImageNow + '_v04.model',
            fitsimage = my_outputImageNow + '_v04.model.fits',
            dropdeg = True,
            overwrite = True)


def my_functionJointDeconvolutionContinuumJvM(my_telescope, my_source):
    
    """
    help
    """
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    
    # Run TCLEAN task
    #
    # Single TCLEAN run:
    #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds to 1 times the final threshold
    #   - niter: right now is 1 times less than the final number of iterations
    my_niterNow = int(my_niter)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(my_number) + my_unit
    my_outputImageNow = my_outputImage
    print("Some key parameters of TCLEAN")
    print(my_threshold)
    print(my_number)
    print(my_unit)
    print(my_thresholdNow)
    print(my_niterNow)
    print("Some key parameters of TCLEAN")
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
        scales = my_scales,
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
        restoringbeam = 'common')
    
    #os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '.image')
    #os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '.image.pbcor')
    #os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '.residual')
    #os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '.mask')
    #os.system('cp -rp ' + my_outputImageNow + '.psf ' + my_outputImageNow + '.psf')
    #os.system('cp -rp ' + my_outputImageNow + '.model ' + my_outputImageNow + '.model')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '.image',
        fitsimage = my_outputImageNow + '.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.image.pbcor',
        fitsimage = my_outputImageNow + '.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
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
    
    # Apply dirty-beam / clean-beam correction
    # based on https://ui.adsabs.harvard.edu/abs/1995AJ....110.2037J/abstract
    #          https://ui.adsabs.harvard.edu/abs/2021ApJS..257....2C/abstract
    #
    # Read information of the clean-beam
    #
    ## for Python 2
    #my_bmaj = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmaj').items()[0][1]
    #my_bmin = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmin').items()[0][1]
    #my_bpa = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bpa').items()[0][1]
    ## for Python 3
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
    my_JvMdirtyBeam = my_outputImageNow + '.psf.fits'
    my_JvMimage = my_JvMdirtyBeam
    my_JvMthreshold = 0.02
    my_JvMplots = True
    my_JvM = determineJvMfactor(my_JvMdirtyBeam, my_JvMimage, my_JvMthreshold, my_JvMplots)
    print("... JvM factor is "+str(my_JvM))
    
    os.system('rm -rf ' + my_outputImageNow + '.JvM.image')
    immath(imagename = [my_outputImageNow + '.model.convolved', my_outputImageNow + '.residual'],
        expr = '(IM0 + '+str(my_JvM)+'*IM1)',
        outfile = my_outputImageNow + '.JvM.image')
    
    # Update header for .image and future .JvM.image files
    my_outputExtensions = ['.image', '.JvM.image']
    for my_outputExtension in my_outputExtensions:
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'OBSERVER',
            hdvalue = 'almagal')
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGniter',
            hdvalue = my_niterNow)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGthresh',
            hdvalue = str(my_thresholdNow))
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGJvM',
            hdvalue = my_JvM)
    '''
    stringHisto = imhistory(imagename = my_outputImageNow + '.image', mode = 'list')[0]
    for i in range(1, len(imhistory(imagename = my_outputImageNow + '.image', mode = 'list'))):
        stringHisto = stringHisto+','+imhistory(imagename = my_outputImageNow + '.image', mode = 'list')[i]
    stringHisto = stringHisto.replace(" ","")
    firstindex = stringHisto.find("vis=")
    lastindex = stringHisto.find("parallel=False")+14
    print(stringHisto)
    print(firstindex)
    print(lastindex)
    stringHisto = 'tclean('+stringHisto[firstindex:lastindex]+')' 
    print("HELLO")
    print(stringHisto)
    print("SI o NO")
    imhistory(imagename = my_outputImageNow + '.JvM.image',
        mode = 'append',
        message = stringHisto)
    print(imhistory(imagename = my_outputImageNow + '.JvM.image', mode = 'list'))
    print("ADIOS")
    '''
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '.JvM.image',
        fitsimage = my_outputImageNow + '.JvM.image.fits',
        dropdeg = True,
        overwrite = True)


def my_functionGetCellsizeImsize(my_telescope, my_source):
    
    """
    help
    """
    
    if os.path.isfile(str(my_runningPath) + '/almagal/tcleanParameters.txt') == False:
        
        # Determine the tclean parameters for continuum joint-deconvolution
        #
        my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
        
        print("HELLO!!!!! - initial")
        print(my_threshold)
        print("ADIOS!!!!! - initial")
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
        print(my_threshold)
        print(my_thresholdNow)
        print(my_scalesNow)
        print('checks')
        print(my_visfilestoclean)
        print(my_outputImageNow)
        print(my_source)
        print(my_freqs)
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
            gridder = 'mosaic',
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


def my_functionJointDeconvolutionContinuumJvMV2(my_telescope, my_source):
    
    """
    help
    """
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    my_cell, my_imsize, my_nbpixels = my_functionGetCellsizeImsize(my_telescope, my_source)
    
    # Run TCLEAN task
    #
    # First TCLEAN run:
    #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds to 1.5 times the final threshold
    #   - niter: right now is 5 times less the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.5*my_number) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    #
    #--------------------------------------------------
    # For TM1+TM2 testing (Crystal Brogan talk)
    # ... my_scales
    #my_scalesNow = [0, 6, 18]
    my_scalesNow = [0, 6, 18, 36]
    #my_scalesNow = [0, 6, 18, 45] -- not used
    # ... my_niter
    my_niterNow = 10
    # ... my_threshold
    #my_thresholdNow = str(1.5*my_number) + my_unit
    #my_thresholdNow = str(2.0*my_number) + my_unit
    my_thresholdNow = str(2.5*my_number) + my_unit
    #--------------------------------------------------
    print("Producing image - step 1")
    print("... some parameters are")
    print(my_threshold)
    print(my_thresholdNow)
    print(my_scalesNow)
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
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
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
    print("Re-shape the mask - step 1")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/TM2.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_TM2.mask',
        output = str(my_runningPath) + '/almagal/processing/TM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/TM2.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v01.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask',
        output = my_outputImageNow + '.mask')
    
    # Second TCLEAN run:
    #  It uses the mask created first with 7M+TM2+TM1 data and the TM2 mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.0*my_number) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales[3:]
    my_smallscalebiasNow = 0.0
    #--------------------------------------------------
    # For TM1+TM2 testing (Crystal Brogan talk)
    # ... my_scales
    #my_scalesNow = [0, 6, 18]
    my_scalesNow = [0, 6, 18, 36]
    #my_scalesNow = [0, 6, 18, 45] -- not used
    # ... my_niter
    my_niterNow = int(my_niter/1.)
    # ... my_threshold
    #my_thresholdNow = str(1.5*my_number) + my_unit
    #my_thresholdNow = str(2.0*my_number) + my_unit
    my_thresholdNow = str(2.5*my_number) + my_unit
    #--------------------------------------------------
    print("Producing image - step 2")
    print("... some parameters are")
    print(my_threshold)
    print(my_thresholdNow)
    print(my_scalesNow)
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
        usemask = 'user',
        #usemask = 'auto-multithresh',
        pbmask = my_pbmask,
        #sidelobethreshold = my_sidelobethreshold,
        #noisethreshold = my_noisethreshold,
        #minbeamfrac =  my_minbeamfrac,
        #lownoisethreshold = my_lownoisethreshold,
        #negativethreshold = my_negativethreshold,
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
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
    '''
    # Add the TM2 mask to the newly-created mask
    #
    print("Re-shape the mask - step 2")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/7M.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_7M.mask',
        output = str(my_runningPath) + '/almagal/processing/7M.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/7M.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v02.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_with7M.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_with7M.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask',
        output = my_outputImageNow + '.mask')
    
    # Third TCLEAN run:
    #  It uses the mask created from the previous cleaning step plus the 7M mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(2.*my_number) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales[4:]
    my_smallscalebiasNow = 0.0
    print("Producing image - step 3")
    print("... some parameters are")
    print(my_threshold)
    print(my_thresholdNow)
    print(my_scalesNow)
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
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
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
    # Apply dirty-beam / clean-beam correction
    # based on https://ui.adsabs.harvard.edu/abs/1995AJ....110.2037J/abstract
    #          https://ui.adsabs.harvard.edu/abs/2021ApJS..257....2C/abstract
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
    my_JvMdirtyBeam = my_outputImageNow + '.psf.fits'
    my_JvMimage = my_JvMdirtyBeam
    my_JvMthreshold = 0.02
    my_JvMplots = True
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
            hdkey = 'OBSERVER',
            hdvalue = 'almagal')
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGniter',
            hdvalue = my_niterNow)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGthresh',
            hdvalue = str(my_thresholdNow))
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
    exportfits(imagename = my_outputImageNow + '.JvM.image.pbcor',
        fitsimage = my_outputImageNow + '.JvM.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.image',
        fitsimage = my_outputImageNow + '.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.image.pbcor',
        fitsimage = my_outputImageNow + '.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)


def my_functionJointDeconvolutionContinuumJvMV3(my_telescope, my_source):
    
    """
    help
    """
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    my_cell, my_imsize, my_nbpixels = my_functionGetCellsizeImsize(my_telescope, my_source)
    
    # Run TCLEAN task
    #
    # First TCLEAN run:
    #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
    #  Key parameters to play with are:
    #   - threshold: 
    #   - niter: 
    my_niterNow = 10
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(2.75*my_number) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    
    print("... Producing TCLEAN image - starting new mask (step 1)")
    print("... Some parameters are:")
    print("... ... original threshold = " + str(my_threshold))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    
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
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
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
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/TM2.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_TM2.mask',
        output = str(my_runningPath) + '/almagal/processing/TM2.mask')
    if os.path.isfile(my_outputImageNow + '_v01.mask.fits') == True:
        os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
        immath(imagename = [str(my_runningPath) + '/almagal/processing/TM2.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v01.mask'],
            mode = 'evalexpr',
            expr = '( IM0 + IM1 )',
            outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    else:
        os.system('cp -rp ' + str(my_runningPath) + '/almagal/processing/TM2.mask ' + str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask',
        output = my_outputImageNow + '.mask')
    
    # Second TCLEAN run:
    #  It uses the mask created first with 7M+TM2+TM1 data and the TM2 mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(2.0*my_number) + my_unit
    my_outputImageNow = my_outputImage
    #my_scalesNow = my_scales[3:]
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    
    print("... Producing TCLEAN image - with TM2 mask added (step 2)")
    print("... Some parameters are:")
    print("... ... original threshold = " + str(my_threshold))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    
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
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
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
    
    '''
    # Add the 7M mask to the newly-created mask
    #
    print("... Adding 7M mask to the mask")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/7M.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_7M.mask',
        output = str(my_runningPath) + '/almagal/processing/7M.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/7M.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v02.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_with7M.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_with7M.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask',
        output = my_outputImageNow + '.mask')
    
    # Third TCLEAN run:
    #  It uses the mask created from the previous cleaning step plus the 7M mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(2.0*my_number) + my_unit
    my_outputImageNow = my_outputImage
    #my_scalesNow = my_scales[4:]
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    
    print("... Producing TCLEAN image - with 7M mask added (step 3)")
    print("... Some parameters are:")
    print("... ... original threshold = " + str(my_threshold))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    
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
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
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
    # Add the hand-made mask to the newly-created mask
    #
    print("... Adding hand-made mask to the mask")
    #
    # Define new mask for last iteration
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
    # Adapt mask file to correspond to the 4-sigma/2-sigma created one
    #
    dataResidual_MAD = my_maskCreator('forHandMadeMask.image.fits', 'forHandMadeMask.residual.fits', 'forHandMadeMask.mask.fits', 4.0, 2.0)
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/handMade.mask')
    importfits(fitsimage = 'forHandMadeMask.mask.fits',
        imagename = str(my_runningPath) + '/almagal/processing/handMade.mask',
        overwrite = True)
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    #os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/handMade7MTM2TM1.mask')
    #makemask(mode = 'copy',
    #    inpimage = my_outputImageNow + '.image',
    #    inpmask = str(my_runningPath) + '/almagal/processing/handMade.mask',
    #    output = str(my_runningPath) + '/almagal/processing/handMade7MTM2TM1.mask')
    #os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M.mask')
    #immath(imagename = [str(my_runningPath) + '/almagal/processing/7M.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v02.mask'],
    #    mode = 'evalexpr',
    #    expr = '( IM0 + IM1 )',
    #    outfile = str(my_runningPath) + '/almagal/processing/merged_with7M.mask')
    #os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask')
    #immath(imagename = str(my_runningPath) + '/almagal/processing/merged_with7M.mask',
    #    mode = 'evalexpr',
    #    expr = ' iif( IM0 >=0.5, 1.0, IM0)',
    #    outfile = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask')
    #os.system('rm -rf ' + my_outputImageNow + '.mask')
    #makemask(mode = 'copy',
    #    inpimage = my_outputImageNow + '.image',
    #    inpmask = str(my_runningPath) + '/almagal/processing/merged_with7M_normalized.mask',
    #    output = my_outputImageNow + '.mask')
    
    # Fourth TCLEAN run:
    #  It uses a mask defined by the emission of the CLEANed multiscale image
    #   - it contains those regions with 4 sigma, extended to include adjacent regions with 2 sigma
    
    #os.system('rm -rf ' + my_outputImageNow + '.mask')
    #print("IMREGRIDDING")
    #imregrid(imagename = str(my_runningPath) + '/almagal/processing/handMade.mask',
    #    output = my_outputImageNow + '.mask',
    #    template = my_outputImageNow + '_v03.mask')
    #makemask(mode = 'copy',
    #    inpimage = my_outputImageNow + '.image',
    #    inpmask = str(my_runningPath) + '/almagal/processing/handMade.mask',
    #    output = my_outputImageNow + '.mask')
    #os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/handMade_reshaped.mask')
    #makemask(mode = 'copy',
    #    inpimage = my_outputImageNow + '.image',
    #    inpmask = str(my_runningPath) + '/almagal/processing/handMade.mask',
    #    output = str(my_runningPath) + '/almagal/processing/handMade_reshaped.mask')
    #os.system('cp -rp ' + str(my_runningPath) + '/almagal/processing/handMade_reshaped.mask ' + my_outputImageNow + '.mask')
    #makemask(mode = 'copy',
    #    inpimage = my_outputImageNow + '.image',
    #    inpmask = my_outputImageNow + '_handMade.mask',
    #    output = my_outputImageNow + '.mask')
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    #my_thresholdNow = str(0.2*my_number) + my_unit
    my_thresholdNow = str(1.0*dataResidual_MAD) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = [0]
    my_smallscalebiasNow = 0.0
    
    print("... Producing TCLEAN image - single-scale hand-defined mask (step 4)")
    print("... Some parameters are:")
    print("... ... original threshold = " + str(my_threshold))
    print("... ... used threshold = " + str(my_thresholdNow))
    print("... ... used scales = " + str(my_scalesNow))
    
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
        usemask = 'user',
        mask = str(my_runningPath)+'/almagal/processing/handMade.mask',
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
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
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
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v04.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v04.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v04.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v04.mask')
    os.system('cp -rp ' + my_outputImageNow + '.model ' + my_outputImageNow + '_v04.model')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '_v04.image',
        fitsimage = my_outputImageNow + '_v04.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v04.image.pbcor',
        fitsimage = my_outputImageNow + '_v04.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v04.residual',
        fitsimage = my_outputImageNow + '_v04.residual.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v04.mask',
        fitsimage = my_outputImageNow + '_v04.mask.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v04.model',
        fitsimage = my_outputImageNow + '_v04.model.fits',
        dropdeg = True,
        overwrite = True)
    
    print("... Applying JvM correction")
    
    # Apply dirty-beam / clean-beam correction
    # based on https://ui.adsabs.harvard.edu/abs/1995AJ....110.2037J/abstract
    #          https://ui.adsabs.harvard.edu/abs/2021ApJS..257....2C/abstract
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
    my_JvMdirtyBeam = my_outputImageNow + '.psf.fits'
    my_JvMimage = my_JvMdirtyBeam
    my_JvMthreshold = 0.02
    my_JvMplots = True
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
            hdkey = 'OBSERVER',
            hdvalue = 'almagal')
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGniter',
            hdvalue = my_niterNow)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGthresh',
            hdvalue = str(my_thresholdNow))
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
    exportfits(imagename = my_outputImageNow + '.JvM.image.pbcor',
        fitsimage = my_outputImageNow + '.JvM.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
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
    
    print("... Clean up intermediate files")
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
    os.system('rm -rf ' + my_outputImageNow + '_v04.image')
    os.system('rm -rf ' + my_outputImageNow + '_v04.image.pbcor')
    os.system('rm -rf ' + my_outputImageNow + '_v04.residual')
    os.system('rm -rf ' + my_outputImageNow + '_v04.mask')
    os.system('rm -rf ' + my_outputImageNow + '_v04.model')


def my_functionJointDeconvolutionContinuumMTMFS(my_telescope, my_source):
    
    """
    help
    """
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    my_cell, my_imsize, my_nbpixels = my_functionGetCellsizeImsize(my_telescope, my_source)
    
    # Run TCLEAN task
    #
    # First TCLEAN run:
    #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds to 1.5 times the final threshold
    #   - niter: right now is 5 times less the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.5*my_number) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales
    my_smallscalebiasNow = 0.0
    #
    #--------------------------------------------------
    # For TM1+TM2 testing (Crystal Brogan talk)
    # ... my_scales
    my_scalesNow = [0, 6, 18]
    #my_scalesNow = [0, 6, 18, 36]
    #my_scalesNow = [0, 6, 18, 45] -- not used
    # ... my_niter
    my_niterNow = 10
    # ... my_threshold
    my_thresholdNow = str(1.5*my_number) + my_unit
    #my_thresholdNow = str(2.0*my_number) + my_unit
    #my_thresholdNow = str(2.5*my_number) + my_unit
    #--------------------------------------------------
    print("Producing image - step 1")
    print("... some parameters are")
    print(my_threshold)
    print(my_thresholdNow)
    print(my_scalesNow)
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
        deconvolver = 'mtmfs', #multiscale
        nterms = 1,
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
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
    os.system('cp -rp ' + my_outputImageNow + '.image.tt0 ' + my_outputImageNow + '_v01.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.tt0.pbcor ' + my_outputImageNow + '_v01.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual.tt0 ' + my_outputImageNow + '_v01.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')
    os.system('cp -rp ' + my_outputImageNow + '.model.tt0 ' + my_outputImageNow + '_v01.model')
    
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
    print("Re-shape the mask - step 1")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/TM2.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image.tt0',
        inpmask = str(my_runningPath) + '/almagal/processing/original_TM2.mask',
        output = str(my_runningPath) + '/almagal/processing/TM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/TM2.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v01.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image.tt0',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask',
        output = my_outputImageNow + '.mask')
    
    # Second TCLEAN run:
    #  It uses the mask created first with 7M+TM2+TM1 data and the TM2 mask
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds the final threshold
    #   - niter: right now is the final number of iterations
    my_niterNow = int(my_niter/1.)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(1.0*my_number) + my_unit
    my_outputImageNow = my_outputImage
    my_scalesNow = my_scales[3:]
    my_smallscalebiasNow = 0.0
    #--------------------------------------------------
    # For TM1+TM2 testing (Crystal Brogan talk)
    # ... my_scales
    my_scalesNow = [0, 6, 18]
    #my_scalesNow = [0, 6, 18, 36]
    #my_scalesNow = [0, 6, 18, 45] -- not used
    # ... my_niter
    my_niterNow = int(my_niter/1.)
    # ... my_threshold
    my_thresholdNow = str(1.5*my_number) + my_unit
    #my_thresholdNow = str(2.0*my_number) + my_unit
    #my_thresholdNow = str(2.5*my_number) + my_unit
    #--------------------------------------------------
    print("Producing image - step 2")
    print("... some parameters are")
    print(my_threshold)
    print(my_thresholdNow)
    print(my_scalesNow)
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
        deconvolver = 'mtmfs', #multiscale
        nterms = 1,
        scales = my_scalesNow,
        niter = my_niterNow,
        weighting = my_weighting,
        robust = my_robust,
        usemask = 'user',
        #usemask = 'auto-multithresh',
        pbmask = my_pbmask,
        #sidelobethreshold = my_sidelobethreshold,
        #noisethreshold = my_noisethreshold,
        #minbeamfrac =  my_minbeamfrac,
        #lownoisethreshold = my_lownoisethreshold,
        #negativethreshold = my_negativethreshold,
        gridder = 'mosaic',
        pblimit = my_pblimit,
        pbcor = True,
        threshold = my_thresholdNow,
        interactive = False,
        restoringbeam = 'common',
        smallscalebias = my_smallscalebiasNow)
    
    os.system('cp -rp ' + my_outputImageNow + '.image.tt0 ' + my_outputImageNow + '.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.tt0.pbcor ' + my_outputImageNow + '.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual.tt0 ' + my_outputImageNow + '.residual')
    os.system('cp -rp ' + my_outputImageNow + '.model.tt0 ' + my_outputImageNow + '.model')
    os.system('cp -rp ' + my_outputImageNow + '.pb.tt0 ' + my_outputImageNow + '.pb')
    os.system('cp -rp ' + my_outputImageNow + '.psf.tt0 ' + my_outputImageNow + '.psf')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '.residual.tt0',
        fitsimage = my_outputImageNow + '.residual.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.mask',
        fitsimage = my_outputImageNow + '.mask.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.psf.tt0',
        fitsimage = my_outputImageNow + '.psf.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.pb.tt0',
        fitsimage = my_outputImageNow + '.pb.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.model.tt0',
        fitsimage = my_outputImageNow + '.model.fits',
        dropdeg = True,
        overwrite = True)
    
    os.system('cp -rp ' + my_outputImageNow + '.image.tt0 ' + my_outputImageNow + '_v02.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.tt0.pbcor ' + my_outputImageNow + '_v02.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual.tt0 ' + my_outputImageNow + '_v02.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v02.mask')
    os.system('cp -rp ' + my_outputImageNow + '.model.tt0 ' + my_outputImageNow + '_v02.model')
    
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
    
    # Apply dirty-beam / clean-beam correction
    # based on https://ui.adsabs.harvard.edu/abs/1995AJ....110.2037J/abstract
    #          https://ui.adsabs.harvard.edu/abs/2021ApJS..257....2C/abstract
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
    my_JvMdirtyBeam = my_outputImageNow + '.psf.fits'
    my_JvMimage = my_JvMdirtyBeam
    my_JvMthreshold = 0.02
    my_JvMplots = True
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
            hdkey = 'OBSERVER',
            hdvalue = 'almagal')
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGniter',
            hdvalue = my_niterNow)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGthresh',
            hdvalue = str(my_thresholdNow))
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
    exportfits(imagename = my_outputImageNow + '.JvM.image.pbcor',
        fitsimage = my_outputImageNow + '.JvM.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.image',
        fitsimage = my_outputImageNow + '.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.image.pbcor',
        fitsimage = my_outputImageNow + '.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)


def my_functionJointDeconvolutionContinuumJvMout(my_telescope, my_source):
    
    """
    help
    """
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    
    # Run TCLEAN task
    #
    # Single TCLEAN run:
    #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds to 1 times the final threshold
    #   - niter: right now is 1 times less than the final number of iterations
    my_niterNow = int(my_niter)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(my_number) + my_unit
    my_outputImageNow = my_outputImage
    print("Some key parameters of TCLEAN")
    print(my_threshold)
    print(my_number)
    print(my_unit)
    print(my_thresholdNow)
    print(my_niterNow)
    print("Some key parameters of TCLEAN")
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
        scales = my_scales,
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
        restoringbeam = 'common')
    
    os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '_v01.image')
    os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '_v01.image.pbcor')
    os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '_v01.residual')
    os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')
    os.system('cp -rp ' + my_outputImageNow + '.psf ' + my_outputImageNow + '_v01.psf')
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
    exportfits(imagename = my_outputImageNow + '_v01.psf',
        fitsimage = my_outputImageNow + '_v01.psf.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '_v01.model',
        fitsimage = my_outputImageNow + '_v01.model.fits',
        dropdeg = True,
        overwrite = True)
    
    # Add the TM2 mask to the newly-created mask
    #
    print("Re-shape the mask")
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/TM2.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/original_TM2.mask',
        output = str(my_runningPath) + '/almagal/processing/TM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    immath(imagename = [str(my_runningPath) + '/almagal/processing/TM2.mask', str(my_runningPath) + '/almagal/' + my_outputImageNow + '_v01.mask'],
        mode = 'evalexpr',
        expr = '( IM0 + IM1 )',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    immath(imagename = str(my_runningPath) + '/almagal/processing/merged_withTM2.mask',
        mode = 'evalexpr',
        expr = ' iif( IM0 >=0.5, 1.0, IM0)',
        outfile = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask')
    os.system('rm -rf ' + my_outputImageNow + '.mask')
    makemask(mode = 'copy',
        inpimage = my_outputImageNow + '.image',
        inpmask = str(my_runningPath) + '/almagal/processing/merged_withTM2_normalized.mask',
        output = my_outputImageNow + '.mask')
    
    # Apply dirty-beam / clean-beam correction
    # based on https://ui.adsabs.harvard.edu/abs/1995AJ....110.2037J/abstract
    #          https://ui.adsabs.harvard.edu/abs/2021ApJS..257....2C/abstract
    #
    # Read information of the clean-beam
    #
    ## for Python 2
    #my_bmaj = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmaj').items()[0][1]
    #my_bmin = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmin').items()[0][1]
    #my_bpa = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bpa').items()[0][1]
    ## for Python 3
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
    my_JvMdirtyBeam = my_outputImageNow + '.psf.fits'
    my_JvMimage = my_JvMdirtyBeam
    my_JvMthreshold = 0.02
    my_JvMplots = True
    my_JvM = determineJvMfactor(my_JvMdirtyBeam, my_JvMimage, my_JvMthreshold, my_JvMplots)
    print("... JvM factor is "+str(my_JvM))
    
    os.system('rm -rf ' + my_outputImageNow + '.JvM.image')
    immath(imagename = [my_outputImageNow + '.model.convolved', my_outputImageNow + '.residual'],
        expr = '(IM0 + '+str(my_JvM)+'*IM1)',
        outfile = my_outputImageNow + '.JvM.image')
    
    # Update header for .JvM.image files
    
    # Update header for .image and future .JvM.image files
    my_outputExtensions = ['.image', '.JvM.image']
    for my_outputExtension in my_outputExtensions:
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'OBSERVER',
            hdvalue = 'almagal')
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGniter',
            hdvalue = my_niterNow)
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGthresh',
            hdvalue = str(my_thresholdNow))
        imhead(imagename = my_outputImageNow + my_outputExtension,
            mode = 'put',
            hdkey = 'AGJvM',
            hdvalue = my_JvM)
    '''
    stringHisto = imhistory(imagename = my_outputImageNow + '.image', mode = 'list')[0]
    for i in range(1, len(imhistory(imagename = my_outputImageNow + '.image', mode = 'list'))):
        stringHisto = stringHisto+','+imhistory(imagename = my_outputImageNow + '.image', mode = 'list')[i]
    stringHisto = stringHisto.replace(" ","")
    firstindex = stringHisto.find("vis=")
    lastindex = stringHisto.find("parallel=False")+14
    print(stringHisto)
    print(firstindex)
    print(lastindex)
    stringHisto = 'tclean('+stringHisto[firstindex:lastindex]+')' 
    print("HELLO")
    print(stringHisto)
    print("SI o NO")
    imhistory(imagename = my_outputImageNow + '.JvM.image',
        mode = 'append',
        message = stringHisto)
    print(imhistory(imagename = my_outputImageNow + '.JvM.image', mode = 'list'))
    print("ADIOS")
    '''
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '.JvM.image',
        fitsimage = my_outputImageNow + '.JvM.image.fits',
        dropdeg = True,
        overwrite = True)


def my_functionJointDeconvolutionContinuumJvMcircle(my_telescope, my_source):
    
    """
    help
    """
    
    # Determine the tclean parameters for continuum joint-deconvolution
    #
    my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold = my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source)
    
    # Run TCLEAN task
    #
    # Single TCLEAN run:
    #  No mask is defined, and it starts defining a new mask from the 7M+TM2+TM1 combined data
    #  Key parameters to play with are:
    #   - threshold: right now the value corresponds to 1 times the final threshold
    #   - niter: right now is 1 times less than the final number of iterations
    my_niterNow = int(my_niter)
    my_number, my_unit = separateNumbersUnits(my_threshold)
    my_thresholdNow = str(my_number) + my_unit
    my_outputImageNow = my_outputImage
    print("Some key parameters of TCLEAN")
    print(my_threshold)
    print(my_number)
    print(my_unit)
    print(my_thresholdNow)
    print("Some key parameters of TCLEAN")
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
        scales = my_scales,
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
        restoringbeam = 'common')
    
    #os.system('cp -rp ' + my_outputImageNow + '.image ' + my_outputImageNow + '.image')
    #os.system('cp -rp ' + my_outputImageNow + '.image.pbcor ' + my_outputImageNow + '.image.pbcor')
    #os.system('cp -rp ' + my_outputImageNow + '.residual ' + my_outputImageNow + '.residual')
    #os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '.mask')
    #os.system('cp -rp ' + my_outputImageNow + '.psf ' + my_outputImageNow + '.psf')
    #os.system('cp -rp ' + my_outputImageNow + '.model ' + my_outputImageNow + '.model')
    
    # Export image files to FITS format
    #
    exportfits(imagename = my_outputImageNow + '.image',
        fitsimage = my_outputImageNow + '.image.fits',
        dropdeg = True,
        overwrite = True)
    exportfits(imagename = my_outputImageNow + '.image.pbcor',
        fitsimage = my_outputImageNow + '.image.pbcor.fits',
        dropdeg = True,
        overwrite = True)
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
    
    # Apply dirty-beam / clean-beam correction
    # based on https://ui.adsabs.harvard.edu/abs/1995AJ....110.2037J/abstract
    #          https://ui.adsabs.harvard.edu/abs/2021ApJS..257....2C/abstract
    #
    # Read information of the clean-beam
    #
    ## for Python 2
    #my_bmaj = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmaj').items()[0][1]
    #my_bmin = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmin').items()[0][1]
    #my_bpa = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bpa').items()[0][1]
    ## for Python 3
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
    
    # Extract radial profile of the dirty-beam
    #
    os.system('rm -rf ' + my_outputImageNow + '.psf.dat')
    au.extractAzimuthalAverageFromImage(my_outputImageNow+'.psf', binsize=1, outfile=my_outputImageNow+'.psf.dat', normalize=False)
    
    my_fileToRead = open(my_outputImageNow+'.psf.dat', 'r')
    my_headerFileToRead = my_fileToRead.readline()
    my_radiusList = [0.0]
    my_valueList = [1.0]
    my_beamList = [1.0]
    my_iteration = 0
    for line in my_fileToRead:
        my_iteration = my_iteration + 1
        if (my_iteration == 1):
            my_firstStep = float(line.split()[0])
        my_radiusList.append(float(line.split()[0])+my_firstStep)
        my_valueList.append(float(line.split()[1]))
        my_beamList.append(np.exp(-0.5*((float(line.split()[0])+my_firstStep)**2/(np.sqrt(my_bmaj*my_bmin)/2.)**2)))
    my_fileToRead.close()
    my_radius = np.array(my_radiusList)
    my_value = np.array(my_valueList)
    my_beam = np.array(my_beamList)
    
    my_valueCheck = np.min(np.where(my_value <= 0.015))
    print(my_valueCheck, my_radius[my_valueCheck])
    
    my_cumulative = 0.0
    my_cumulativeVolumeList = []
    my_volume = my_value*my_radius*2*np.pi*(my_radius[10]-my_radius[9])
    for i in range(0, len(my_volume)):
        my_cumulative = my_cumulative + my_volume[i]
        my_cumulativeVolumeList.append(my_cumulative)
    my_cumulativeVolume = np.array(my_cumulativeVolumeList)

    my_cumulativeBeam = 0.0
    my_cumulativeBeamVolumeList = []
    my_volumeBeam = my_beam*my_radius*2*np.pi*(my_radius[10]-my_radius[9])
    for i in range(0, len(my_volumeBeam)):
        my_cumulativeBeam = my_cumulativeBeam + my_volumeBeam[i]
        my_cumulativeBeamVolumeList.append(my_cumulativeBeam)
    my_cumulativeBeamVolume = np.array(my_cumulativeBeamVolumeList)
    print(my_cumulativeVolume[my_valueCheck])
    print(my_cumulativeBeamVolume[my_valueCheck])
    print(my_cumulativeBeamVolume[my_valueCheck]/my_cumulativeVolume[my_valueCheck])
    
    # New restored imaged with JvM factor applied
    #
    my_JvM = my_cumulativeBeamVolume[my_valueCheck]/my_cumulativeVolume[my_valueCheck]
    os.system('rm -rf ' + my_outputImageNow + '.JvM.image')
    immath(imagename = [my_outputImageNow + '.model.convolved', my_outputImageNow + '.residual'],
        expr = '(IM0 + '+str(my_JvM)+'*IM1)',
        outfile = my_outputImageNow + '.JvM.image')
    
    exportfits(imagename = my_outputImageNow + '.JvM.image',
        fitsimage = my_outputImageNow + '.JvM.image.fits',
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
    
    if (my_telescope == "TM2TM1"):
        my_add7M = False
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
        print("HOOOLA")
        print(extrachannels)
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
    
    my_functionGetCellsizeImsize(my_telescope, my_source)
    #my_functionJointDeconvolutionContinuumJvMV2(my_telescope, my_source)
    ##my_functionJointDeconvolutionContinuumMTMFS(my_telescope, my_source)
    my_functionJointDeconvolutionContinuumJvMV3(my_telescope, my_source)
    
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
    
    # Joint deconvolution of 7M, TM2 and TM1 for cube spw 0 chunks 1/10 to 10/10
    #
    if (my_telescope == "7MTM2TM1"):
        
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
    
    if (my_telescope == "7MTM2TM1"):
        
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
    
    if (my_telescope == "7MTM2TM1"):
        
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
    
    # Joint deconvolution of 7M, TM2 and TM1 for cube spw 1 chunks 1/10 to 10/10
    #
    if (my_telescope == "7MTM2TM1"):
        
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
    
    if (my_telescope == "7MTM2TM1"):
        
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
    
    if (my_telescope == "7MTM2TM1"):
        
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
    
    # Joint deconvolution of 7M, TM2 and TM1 for cube spw 2 chunks 1/10 to 10/10
    #
    if (my_telescope == "7MTM2TM1"):
        
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
    
    if (my_telescope == "7MTM2TM1"):
        
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
    
    if (my_telescope == "7MTM2TM1"):
        
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
    
    # Joint deconvolution of 7M, TM2 and TM1 for cube spw 3 chunks 1/10 to 10/10
    #
    if (my_telescope == "7MTM2TM1"):
        
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
    
    if (my_telescope == "7MTM2TM1"):
        
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
    
    if (my_telescope == "7MTM2TM1"):
        
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
