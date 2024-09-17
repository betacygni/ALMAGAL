########################################################################
#
#                   ALMAGAL processing pipeline 
#
#
# 
# Script number 5                        created by Alvaro Sanchez-Monge
#
# Previous step:   createIndividual_scriptForSelfCalibration.py
# Next step:       createIndividual_scriptForJointDeconvolution.py
# 
# Description:      Python script to convert image products into FITS
#                   files and to store the products from self-calibration
#                   processing in the archive directory
# 
# Required:
#   - database.csv file containing names and MOUS directory tree
#   - self-calibration products created by createIndividual_scriptForSelfCalibration.py
#
# Execution:
#   - python tarSelfCalibrationProducts.py
#
# CASA version 6.2.0
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
#            my_arrays = ['7M']
my_arrays = ['7M']
#
# Method 2.- Define the array via input variables
#            e.g.
#            python copyFiles.py --array 7M
if (args.array == '7M') or (args.array == 'TM2') or (args.array == 'TM1'):
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
        
        print("... storing self-calibrated data")
        
        # Create directories where self-calibrated visibilities and images are stored
        #
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated')
        my_selfcalibratedVisibilitiesDirectory = my_individualPath + '/' + str(my_source) + '/selfcalibrated'

        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/selfcalibrated')
        my_selfcalibratedImagesDirectory = my_individualPath + '/' + str(my_source) + '/images/selfcalibrated'
        
        # Evaluate if there are files already avaible for the selected source
        #
        my_sourceSelfcalibratedVisibilitiesPath = my_individualPath + '/' + str(my_source) + '/selfcalibrated'
        my_sourceSelfcalibratedVisibilitiesPaths, my_sourceSelfcalibratedVisibilitiesDirs, my_sourceSelfcalibratedVisibilitiesFiles = next(os.walk(my_sourceSelfcalibratedVisibilitiesPath))
        my_sourceSelfcalibratedImagesPath = my_individualPath + '/' + str(my_source) + '/images/selfcalibrated'
        my_sourceSelfcalibratedImagesPaths, my_sourceSelfcalibratedImagesDirs, my_sourceSelfcalibratedImagesFiles = next(os.walk(my_sourceSelfcalibratedImagesPath))
        
        # If data available
        #
        if len(my_sourceSelfcalibratedImagesFiles) >= 1:
            
            # If data have not been transferred to the storage location
            #
            if (os.path.isfile(my_selfcalibratedImagesDirectory + '/transferred.txt') == False):
            
                my_finishedLastStep = 'finished_step2.txt'
                
                if (os.path.isfile(my_selfcalibratedImagesDirectory + '/' + my_finishedLastStep) == True) or (os.path.isfile(my_selfcalibratedImagesDirectory + '/finished_all.txt') == True):
                    
                    # If self-calibrated products have not been compressed
                    #
                    if (os.path.isfile(my_selfcalibratedImagesDirectory + '/selfcalibrated-fits.tar') == False):
                        
                        my_ImageDirectory = my_individualPath + "/" + str(my_source) + "/images/selfcalibrated/"
                        
                        # Compress the FITS files
                        #
                        if (os.path.isfile(my_selfcalibratedImagesDirectory + '/selfcalibrated-fits.tar') == False):
                            
                            my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_selfcalibratedImagesDirectory+'/almagal/selfcalibration/images'))
                            TMPcountFits = 0
                            for TMPcounter in range(0, len(my_TMPfiles)):
                                if str(my_TMPfiles[TMPcounter][-5:]) == ".fits":
                                    TMPcountFits = TMPcountFits+1
                            print("... number of files available (FITS files): " + str(TMPcountFits))
                            my_runningSelfcalibratedTMP = os.getcwd()
                            os.chdir(my_ImageDirectory)
                            os.system("tar -cf selfcalibrated-fits.tar almagal/selfcalibration/images/*.fits")
                            
                            print("... " + my_array + " clean up the FITS images")
                            os.system("rm -rf almagal/selfcalibration/images/*.fits")
                            os.chdir(my_runningSelfcalibratedTMP)
                            
                        else:
                            
                            print("... FITS self-calibrated images compressed")
                        
                        # Copy self-calibrated visibilities to its storage location
                        #
                        os.system("mkdir -p " + my_selfcalibratedVisibilitiesDirectory + "/7M")
                        os.system("mkdir -p " + my_selfcalibratedVisibilitiesDirectory + "/7M/perEB")
                        os.system("cp -rp " + my_selfcalibratedImagesDirectory + "/almagal/processing/*7M*.tar " + my_selfcalibratedVisibilitiesDirectory + "/7M/perEB/.")
                        os.system("mkdir -p " + my_selfcalibratedVisibilitiesDirectory + "/TM2")
                        os.system("mkdir -p " + my_selfcalibratedVisibilitiesDirectory + "/TM2/perEB")
                        os.system("cp -rp " + my_selfcalibratedImagesDirectory + "/almagal/processing/*TM2*.tar " + my_selfcalibratedVisibilitiesDirectory + "/TM2/perEB/.")
                        os.system("mkdir -p " + my_selfcalibratedVisibilitiesDirectory + "/TM1")
                        os.system("mkdir -p " + my_selfcalibratedVisibilitiesDirectory + "/TM1/perEB")
                        os.system("cp -rp " + my_selfcalibratedImagesDirectory + "/almagal/processing/*TM1*.tar " + my_selfcalibratedVisibilitiesDirectory + "/TM1/perEB/.")
                        
                    else:
                        
                        print("... already compressed")
                        
                        # Transfer to storage directory, only if this is different to the main directory
                        #
                        if (my_storagePath != my_mainPath):
                            
                            print("... storage path is " + my_storagePath)
                            
                            if (os.path.isfile(my_selfcalibratedImagesDirectory + '/transferred.txt') == False):
                                
                                print("... data being transferred")
                                
                                # Copy self-calibrated images to LARGEDATA
                                #
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/images/selfcalibrated')
                                if (args.storageReset == True):
                                    os.system('rm -rf ' + my_individualStoragePath + '/' + str(my_source) + '/images/selfcalibrated')
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/images/selfcalibrated/')
                                os.system('cp -rp ' + my_individualPath + '/' + str(my_source) + '/images/selfcalibrated/*.tar ' + my_individualStoragePath + '/' + str(my_source) + '/images/selfcalibrated/.')
                                
                                # Copy self-calibrated visibilities to LARGEDATA
                                #
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated')
                                if (args.storageReset == True):
                                    os.system('rm -rf ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated')
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/')
                                os.system('cp -rp ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated/* ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/.')
                                
                                # Clean up directory in SCRATCH
                                #
                                os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/images/selfcalibrated/*')
                                os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated/*')
                                os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/calibrated/*')
                                
                                # Create dummy file to indicate that data were transferred
                                #
                                os.system('touch ' + my_selfcalibratedImagesDirectory + '/transferred.txt')
                                os.system('touch ' + my_selfcalibratedVisibilitiesDirectory + '/transferred.txt')
                                
                            else:
                                
                                print("... data already transferred")
                                
                        else:
                            
                            print("... storage path is " + my_storagePath + " No transfer needed")
                            
                else:
                    
                    print("... self-calibration still under processing")
            
            else:
                
                print("... self-calibrated data already transferred")
                print("... storage path is " + my_storagePath)
                
        # If data NOT available
        #
        elif len(my_sourceSelfcalibratedImagesFiles) == 0:
            
            print("... No data yet for source " + str(my_source))
