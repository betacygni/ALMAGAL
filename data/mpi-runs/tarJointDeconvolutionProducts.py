########################################################################
#
#                   ALMAGAL processing pipeline 
#
#
# 
# Script number 7                        created by Alvaro Sanchez-Monge
#
# Previous step:   createIndividual_scriptForJointDeconvolution.py
# Next step:       xxx
# 
# Description:      Python script to convert image products into FITS
#                   files and to store the products from joint
#                   deconvolution processing in the archive directory
# 
# Required:
#   - database.csv file containing names and MOUS directory tree
#   - joint-deconvolution products created by createIndividual_scriptForJointDeconvolution.py
#
# Execution:
#   - python tarJointDeconvolutionProducts.py
#
# CASA version 5.6.1
#
#-----------------------------------------------------------------------
# Import required packages
#
import os
import sys
import numpy as np
import argparse
import astropy
from astropy.io import fits
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import configALMAGAL
from functionsALMAGAL import *

########################################################################
#
# DEFINE LIST OF ARGUMENTS TO BE PROVIDED AT THE EXECUTION TIME
#
# Commands to select sources to be transferred. Sources can be selected
# either by their ID number or by their source name with the following
# python arguments:
#   --id,            : Single ID number (e.g., 0)
#   --idrange        : ID range (e.g., 0 10 to give the range (0, 10))
#
# Commands to indicate the array to be transferred:
#   --array          : Select array. Options are: 7MTM2
#   --storageReset   : Remove the full directory array in storage location
#
#-----------------------------------------------------------------------
# Create a list of arguments
#
parser = argparse.ArgumentParser(description="+++ ----------------------------------------------------------------------- \
                                              +++ ALMAGAL : Parameters to select sources to be processed")
#
parser.add_argument('--id', nargs=1, type=int,
                    help='OPTIONAL: ID number of the source to be processed')
parser.add_argument('--idrange', nargs=2, type=int,
                    help='OPTIONAL: Range of source ID numbers to be processed. \
                            Two integer numbers are required for this option: \
                            first: first ID in the range of sources to execute \
                            last: last ID in the range of sources to execute')
#
parser.add_argument('--array',
                    help='OPTIONAL: Select array: 7MTM2')
#
parser.add_argument('--storageReset', action='store_true',
                    help='OPTIONAL: Remove the directory of selected array in the soratge place (be careful!)')
#
args = parser.parse_args()
#
########################################################################


########################################################################
#
# SET UP WORKSTATION, SOURCES AND ARRAY VARIABLES
#
#-----------------------------------------------------------------------
# Define workstation and paths
#
my_workstation = configALMAGAL.my_workstation
my_mainPath = configALMAGAL.my_mainPath
my_runningPath = configALMAGAL.my_runningPath
my_softwarePath = configALMAGAL.my_softwarePath
my_storagePath = configALMAGAL.my_storagePath
print("::: ALMAGAL command ::: Processing files in " + str(my_workstation))

#-----------------------------------------------------------------------
# Define sources
#
# Create empty lists of sources (do not modify)
#
my_sourceIDs = []
#
# Define the sources to process
#
# Method 1.- Define the IDs of the sources
#            e.g.
#            my_sourceIDs = [0, 1, 2]
#            my_sourceIDs = range(0,3)
my_sourceIDs = [0]
#my_sourceIDs = range(0, 1017)
#
# Method 2.- Define the IDs of the sources via input variables
#            e.g.
#            python SCRIPT.py --id 0
#            python SCRIPT.py --idrange 0 10
#
if (args.id != None):
    my_sourceIDs = [int(args.id[0])]

if (args.idrange != None):
    my_firstID = int(args.idrange[0])
    my_lastID = int(args.idrange[1])
    if (my_lastID <= my_firstID):
        my_lastID = my_firstID+1
        print("... the last ID in the range is smaller than the first ID")
        print("... ID source range modified to (" + str(my_firstID) + ", " + str(my_lastID) + ")")
    my_sourceIDs = range(my_firstID, my_lastID)

#-----------------------------------------------------------------------
# Define the arrays to be processed
#
# Method 1.- Define the array as a list
#            e.g.
#            my_arrays = ['7MTM2']
my_arrays = ['7MTM2']
#
# Method 2.- Define the array via input variables
#            e.g.
#            python copyFiles.py --array 7M
if (args.array == '7MTM2') or (args.array == 'TM2TM1') or (args.array == '7MTM2TM1'):
    my_arrays = [args.array]

#if (args.array == 'ALL'):
#    #my_arrays = ['7M', 'TM2', 'TM1']
#    my_arrays = ['7M', 'TM2']
#
########################################################################

#-----------------------------------------------------------------------
# Define the sources to process
#
#my_sourceIDs = [0]
#my_sourceIDs = range(600, 610)
#my_sourceIDs = range(600, 850)

#-----------------------------------------------------------------------
# Define the arrays to be processed
#
#my_arrays = ['7M']
#my_arrays = ['TM2']

########################################################################
#
# MAIN PROCESSING STARTS HERE
#
#-----------------------------------------------------------------------
# Load the database from Excel file into Pandas format
#
if (os.path.isfile('../database/database.csv') == True):
    print("::: ALMAGAL command ::: Database file used ../database/database.csv")
    df = pd.read_csv('../database/database.csv')
elif (os.path.isfile('../database/database.xlsx') == True):
    print("::: ALMAGAL command ::: Database file used ../database/database.xlsx")
    df = pd.read_excel('../database/database.xlsx', sheet_name='Sheet1')
else:
    print("::: ALMAGAL command ::: ERROR! No available database.xlsx or database.csv files!")
df['Index'] = df.index
df['Source'] = df['Source'].apply(str)

# Create list with all the sources
#
my_sources = df['Source']
my_indices = df['Index']

#-----------------------------------------------------------------------
# Define the path where original MOUS calibrated data are located
#
my_dataPath = my_mainPath + '/2019.1.00195.L'

# Define path where the data for each source will be stored
#
my_individualPath =  my_mainPath + '/2019.1.00195.L/sources'

# Define path for almagaldata storage
#
my_individualStoragePath = my_storagePath + '/2019.1.00195.L/sources'

#-----------------------------------------------------------------------
# Process selected sources
#
my_is = my_sourceIDs
for i in my_is:
    
    my_source = my_sources[i]
    
    print(" ")
    print("Processing (ID: " + str(i) + ") source " + str(my_source) + "...")
    
    for my_array in my_arrays:
        
        print("... storing data for the " + my_array + " array")
        
        # Create directories where images are stored
        #
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
        my_combinedDirectory = my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array
        
        # Evaluate if there are calibrated files produced for the selected source
        #
        my_sourceCombinedPath = my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array
        my_sourceCombinedPaths, my_sourceCombinedDirs, my_sourceCombinedFiles = next(os.walk(my_sourceCombinedPath))
        
        # If data available
        #
        if len(my_sourceCombinedFiles) >= 1:
            
            # If data have not been transferred to the storage location
            #
            if (os.path.isfile(my_combinedDirectory + '/transferred.txt') == False):
            
                # If joint-deconvolution has been completely processed
                #
                if (my_array == '7MTM2'):
                    my_finishedLastStep = 'finished_step153.txt'
            
                # If joint-deconvolution has been completely processed
                #
                if (my_array == 'TM2TM1'):
                    my_finishedLastStep = 'finished_step153.txt'
            
                # If joint-deconvolution has been completely processed
                #
                if (my_array == '7MTM2TM1'):
                    my_finishedLastStep = 'finished_step153.txt'
                
                if (os.path.isfile(my_combinedDirectory + '/' + my_finishedLastStep) == True) or (os.path.isfile(my_combinedDirectory + '/finished_all.txt') == True):
                    
                    #if (os.path.isfile(my_pipelineDirectory + '/almagal.tar') == True):
                    #    
                    #    print("... " + my_array + " untar file (temporary)")
                    #    my_runningDirectoryTMP = os.getcwd()
                    #    os.chdir(my_pipelineDirectory)
                    #    os.system("tar -xf almagal.tar")
                    #    os.system(" rm -rf almagal.tar")
                    #    os.chdir(my_runningDirectoryTMP)
                    
                    # If pipeline has not been compressed
                    #
                    if (os.path.isfile(my_combinedDirectory + '/combined-auxiliary.tar') == False):
                        
                        my_ImageDirectory = my_individualPath + "/" + str(my_source) + "/images/combined/" + my_array
                        
                        # Compress the visibilities and weblog files
                        #
                        if (os.path.isfile(my_combinedDirectory + '/combined-auxiliary.tar') == False):
                            
                            print("... " + my_array + " compress combined products")
                            
                            my_runningCombinedTMP = os.getcwd()
                            os.chdir(my_ImageDirectory)
                            
                            my_SPWs = ['spw0', 'spw1', 'spw2', 'spw3']
                            my_OUTPUTs = ['image', 'residual', 'psf', 'pb', 'model']
                            for my_SPW in my_SPWs:
                                for my_OUTPUT in my_OUTPUTs:
                                    my_FITSfile = 'almagal/' + str(my_source) + '_' + my_SPW + '_' + my_array + '_jointdeconv.' + my_OUTPUT + '.fits'
                                    fits.setval(my_FITSfile, 'OBSERVER', value='almagal')
                            
                            my_importantCombinedTMP = os.getcwd()
                            os.chdir('almagal')
                            os.system('tar -xf combined-cont-fits.tar')
                            os.system('tar -xf auxiliary-cont-fits.tar')
                            os.chdir(my_importantCombinedTMP)
                            
                            os.system('tar -cf combined-cont-fits.tar almagal/'+str(my_source)+'_cont*')
                            os.system('tar -cf combined-line-fits.tar almagal/*jointdeconv.image.fits')
                            os.system('tar -cf combined-extra-fits.tar almagal/*jointdeconv.pb.fits almagal/*jointdeconv.residual.fits')
                            #os.system('tar -cf combined-auxiliary.tar almagal/processing.tar almagal/auxiliary-cont-fits.tar almagal/casa-*.log almagal/channelsForEachSPW_*.txt almagal/tcleanParameters.txt almagal/scriptForJointDeconvolution*.py almagal/functionsALMAGAL.py almagal/*jointdeconv.psf.fits almagal/*jointdeconv.model.fits almagal/*_multiBeam.image finished_step*')
                            os.system('tar -cf combined-auxiliary.tar almagal/casa-*.log almagal/channelsForEachSPW_*.txt almagal/tcleanParameters.txt almagal/scriptForJointDeconvolution*.py almagal/functionsALMAGAL.py almagal/*jointdeconv.psf.fits almagal/*jointdeconv.model.fits almagal/*_multiBeam.image finished_step*')
                            
                            print("... " + my_array + " clean-up already compressed combined products")
                            os.system("rm -rf almagal")
                            os.system("rm -rf finished*.txt")
                            os.system("touch finished_all.txt")
                            
                            os.chdir(my_runningCombinedTMP)
                        
                        else:
                            
                            print("... " + my_array + " combined products already compressed")
                        
                    else:
                        
                        print("... " + my_array + " already compressed")
                        
                        # Transfer to storage directory, only if this is different to the main directory
                        #
                        if (my_storagePath != my_mainPath):
                            
                            print("... storage path is " + my_storagePath)
                            
                            if (os.path.isfile(my_combinedDirectory + '/transferred.txt') == False):
                                
                                print("... " + my_array + " data being transferred")
                                
                                
                                # Copy image products to LARGEDATA
                                #
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/images/combined')
                                if (args.storageReset == True):
                                    os.system('rm -rf ' + my_individualStoragePath + '/' + str(my_source) + '/images/combined/' + my_array)
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/images/combined/' + my_array)
                                os.system('cp -rp ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array + '/*.* ' + my_individualStoragePath + '/' + str(my_source) + '/images/combined/' + my_array + '/.')
                                
                                # Create dummy file to indicate that data were transferred
                                #
                                os.system('touch ' + my_combinedDirectory + '/transferred.txt')
                                
                                # Clean up directory in SCRATCH
                                os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array + '/*.tar')
                                
                                
                            else:
                                
                                print("..." + my_array + " data already transferred")
                                #os.system('scp -rp ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array + '/*.* ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/' + my_array + '/.')
                                #os.system('rm -rf ' + my_pipelineDirectory + '/transferred.txt')
                                #if (os.path.isfile(my_pipelineDirectory + '/transferred.txt') == False):
                                #    
                                #    print("... " + my_array + " being transferred")
                                #    
                                #    os.system('scp -rp ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array + ' ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/.')
                                #    os.system('scp -rp ' + my_individualPath + '/' + str(my_source) + '/images/' + my_array + ' ' + my_individualStoragePath + '/' + str(my_source) + '/images/.')
                                #    os.system('touch ' + my_pipelineDirectory + '/transferred.txt')
                                #
                                #else:
                                #    
                                #    print("... " + my_array + " already transferred")
                                
                        else:
                            
                            print("... storage path is " + my_storagePath + " No transfer needed")
                            
                else:
                    
                    print("... " + my_array + " pipeline still under processing")
            
            else:
                
                print("... " + my_array + " data already transferred")
                print("... storage path is " + my_storagePath)
                
                # Cropping tarr'ed products
                #
                my_runningTMP = os.getcwd()
                os.chdir('/p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+my_array)
                
                # Processing combined-cont-fits.tar file
                #
                print("::: ALMAGAL ::: Processing combined-cont-fits.tar file")
                os.system('tar -xf combined-cont-fits.tar')
                my_extensions = ['image', 'image.pbcor', 'JvM.image', 'JvM.image.pbcor', 'model', 'model.convolved', 'mask', 'psf', 'pb', 'residual']
                for my_extension in my_extensions:
                    my_cropperFile = str(my_source) + '_' + my_array + '_croppedCoordinates.txt'
                    my_basename = 'almagal/' + str(my_source) + '_cont_' + my_array + '_jointdeconv.' + my_extension
                    my_inputFile = my_basename + '.fits'
                    my_outputFile = my_basename + '.cropped.fits'
                    my_croppingFits(my_inputFile, my_outputFile, my_cropperFile)
                    os.system('rm -rf ' + my_inputFile)
                    os.system('mv ' + my_outputFile + ' ' + my_inputFile)
                os.system('rm -rf combined-cont-fits.tar')
                os.system('tar -cf combined-cont-fits.tar almagal')
                os.system('rm -rf almagal')
                
                # Processing combined-line-fits.tar file
                #
                print("::: ALMAGAL ::: Processing combined-line-fits.tar file")
                os.system('tar -xf combined-line-fits.tar')
                my_spws = ['cont', 'spw0', 'spw1', 'spw2', 'spw3']
                for my_spw in my_spws:
                    my_cropperFile = str(my_source)+'_'+my_array+'_croppedCoordinates.txt'
                    my_extensions = ['image']
                    for my_extension in my_extensions:
                        my_basename = 'almagal/'+str(my_source)+'_' + my_spw + '_' + my_array + '_jointdeconv.' + my_extension
                        my_inputFile = my_basename + '.fits'
                        my_outputFile = my_basename + '.cropped.fits'
                        my_croppingFits(my_inputFile, my_outputFile, my_cropperFile)
                        os.system('rm -rf ' + my_inputFile)
                        os.system('mv ' + my_outputFile + ' ' + my_inputFile)
                os.system('rm -rf combined-line-fits.tar')
                os.system('tar -cf combined-line-fits.tar almagal')
                os.system('rm -rf almagal')
                
                # Processing combined-extra-fits.tar file
                #
                print("::: ALMAGAL ::: Processing combined-extra-fits.tar file")
                os.system('tar -xf combined-extra-fits.tar')
                my_spws = ['cont', 'spw0', 'spw1', 'spw2', 'spw3']
                for my_spw in my_spws:
                    my_cropperFile = str(my_source) + '_' + my_array + '_croppedCoordinates.txt'
                    my_extensions = ['pb', 'residual']
                    for my_extension in my_extensions:
                        my_basename = 'almagal/'+str(my_source)+'_' + my_spw + '_' + my_array + '_jointdeconv.' + my_extension
                        my_inputFile = my_basename + '.fits'
                        my_outputFile = my_basename + '.cropped.fits'
                        my_croppingFits(my_inputFile, my_outputFile, my_cropperFile)
                        os.system('rm -rf ' + my_inputFile)
                        os.system('mv ' + my_outputFile + ' ' + my_inputFile)
                os.system('rm -rf combined-extra-fits.tar')
                os.system('tar -cf combined-extra-fits.tar almagal')
                os.system('rm -rf almagal')
                
                # Processing combined-extra-fits.tar file
                #
                print("::: ALMAGAL ::: Processing combined-auxiliary.tar file")
                os.system('tar -xf combined-auxiliary.tar')
                my_spws = ['cont', 'spw0', 'spw1', 'spw2', 'spw3']
                for my_spw in my_spws:
                    my_cropperFile = str(my_source) + '_' + my_array + '_croppedCoordinates.txt'
                    my_extensions = ['psf', 'model']
                    for my_extension in my_extensions:
                        my_basename = 'almagal/'+str(my_source)+'_' + my_spw + '_' + my_array + '_jointdeconv.' + my_extension
                        my_inputFile = my_basename + '.fits'
                        my_outputFile = my_basename + '.cropped.fits'
                        my_croppingFits(my_inputFile, my_outputFile, my_cropperFile)
                        os.system('rm -rf ' + my_inputFile)
                        os.system('mv ' + my_outputFile + ' ' + my_inputFile)
                os.system('rm -rf combined-auxiliary.tar')
                os.system('mv ' + my_cropperFile + ' almagal/.')
                os.system('tar -cf combined-auxiliary.tar almagal finished_step*')
                os.system('rm -rf almagal')
                os.system('rm -rf finished_step*')
                
                os.chdir(my_runningTMP)
                
        # If data NOT available
        #
        elif len(my_sourceCombinedFiles) == 0:
            
            print("... " + "No data yet for source " + str(my_source) + " with the " + my_array + " array")
