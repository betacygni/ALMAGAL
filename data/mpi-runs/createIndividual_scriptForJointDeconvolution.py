########################################################################
#
#                   ALMAGAL processing pipeline
#
#
# 
# Script number 6                        created by Alvaro Sanchez-Monge
#
# Previous step:   tarSelfCalibrationProducts.py
# Next step:       tarJointDeconvolutionProducts.py
# 
# Description:     Python script to generate the scripts that are used
#                  to produce combined images of the individual sources
# 
# Required:
#   - database.csv file containing names and MOUS directory tree
#   - calibrated split files produced after evaluting self-calibration
#   - pipeline-weblog tar files stored with tarPipelineProducts.py
#   - master scripts:
#        scriptForJointDeconvolution7M.py
#        run_mainScriptForJointDeconvolution7M
#        mainScriptForJointDeconvolution7M.sh
#        scriptForJointDeconvolutionTM2.py
#        run_mainScriptForJointDeconvolutionTM2
#        mainScriptForJointDeconvolutionTM2.sh
#        scriptForJointDeconvolutionTM1.py
#        run_mainScriptForJointDeconvolutionTM1
#        mainScriptForJointDeconvolutionTM1.sh
#        scriptForJointDeconvolution7MTM2.py
#        run_mainScriptForJointDeconvolution7MTM2
#        mainScriptForJointDeconvolution7MTM2.sh
#        scriptForJointDeconvolutionTM2TM1.py
#        run_mainScriptForJointDeconvolutionTM2TM1
#        mainScriptForJointDeconvolutionTM2TM1.sh
#        scriptForJointDeconvolution7MTM2TM1.py
#        run_mainScriptForJointDeconvolution7MTM2TM1
#        mainScriptForJointDeconvolution7MTM2TM1.sh
#
# Execution:
#   - python createIndividual_scriptForJointDeconvolution.py
#     followed by
#     ./my_executeJointDeconvolution.sh
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
#   --array          : Select array. Options are: 7MTM2, 7MTM2TM1
#   --activeOut      : Remove the active.txt file that exist after wrong execution
#   --fullReset      : Remove the full directory array for selected sources
#   --cleanUp        : Only to be used by Alvaro (be careful!)
#   --noSelfCal      : Only to be used by Alvaro (be careful!)
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
                    help='OPTIONAL: Select array: 7MTM2, 7MTM2TM1')
#
parser.add_argument('--activeOut', action='store_true',
                    help='OPTIONAL: Remove existing active.txt files')
#
parser.add_argument('--fullReset', action='store_true',
                    help='OPTIONAL: Remove the directory of selected array (be careful!)')
#
parser.add_argument('--cleanUp', action='store_true',
                    help='OPTIONAL: Only to be used by Alvaro (be careful!)')
#
parser.add_argument('--noSelfCal', action='store_true',
                    help='OPTIONAL: Only to be used by Alvaro (be careful!)')
#
args = parser.parse_args()
#
########################################################################


########################################################################
#
# SET UP SOURCES AND ARRAY VARIABLES
#
#-----------------------------------------------------------------------
# Define sources to be processed
#
# Create empty lists of sources (do not modify)
#
my_sourceIDs = []

# Method 1.- Define the IDs of the sources
#            e.g.
#            my_sourceIDs = [0, 1, 2]
#            my_sourceIDs = range(0,3)
my_sourceIDs = [0]
#my_sourceIDs = range(0, 1017)

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
# Create empty lists of arrays (do not modify)
#
my_arrays = []

# Method 1.- Define the array as a list
#            e.g.
#            my_arrays = ['7MTM2']
my_arrays = ['7MTM2']

# Method 2.- Define the array via input variables
#            e.g.
#            python SCRIPT.py --array 7MTM2
#
if (args.array == '7MTM2') or (args.array == 'TM2TM1') or (args.array == '7MTM2TM1') or (args.array == '7M') or (args.array == 'TM2') or (args.array == 'TM1') or (args.array == 'likeALL'):
    my_arrays = [args.array]

if (args.array == 'ALL'):
    my_arrays = ['7MTM2', '7MTM2TM1', 'TM2TM1']

########################################################################


########################################################################
#
# MAIN PROCESSING STARTS HERE
#
#-----------------------------------------------------------------------
# Define workstation and main directory paths
#
my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=True)

## Define path where the data for each source are and will be stored
##
#my_individualPath =  my_mainPath + '/2019.1.00195.L/sources'
#
## Define path for cold storage (e.g. almagaldata storage in JSC). Necessary in case data need to be transferred from cold storage to the working computer
##
#my_individualStoragePath = my_storagePath + '/2019.1.00195.L/sources'

#-----------------------------------------------------------------------
# Load the database into Pandas format
#
my_sources, my_indices = my_functionLoadSourcesDatabase(verbose=True)

#-----------------------------------------------------------------------
# Define file that will contain the final EXECUTABLE commands
#
my_executeFile = 'my_executeJointDeconvolution.sh'
os.system('rm -rf ' + my_executeFile)

#-----------------------------------------------------------------------
# Process selected sources
#
my_is = my_sourceIDs
for i in my_is:
    
    my_source = my_sources[i]
    
    print(" ")
    print("Processing (ID: " + str(i) + ") source " + str(my_source) + "...")
    
    for my_array in my_arrays:
        
        if (args.activeOut == True):
            os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array)+'/active.txt')
            os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array)+'/inQueue.txt')
        
        if (args.fullReset == True):
            # pipeline reload (for Cubes)
            #-#os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/calibrated')
            #-#os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/pipeline')
            #os.system('tar -cf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/continuum_'+str(my_array)+'.tar /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array))
            os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array))
            #::#os.system('mv /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array)+' /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/.')
            #::#os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/')
            #::#os.system('mkdir -p /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/')
            #::#os.system('mv /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/'+str(my_array)+' /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/.')
            #::#my_runningTMP = os.getcwd()
            #::#os.chdir('/p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array)+'/almagal')
            #::#os.system('tar -cf processing.tar processing')
            #::#os.system('rm -rf processing')
            #::#os.chdir(my_runningTMP)
            
        
        if (args.cleanUp == True):
            ###print('remove /p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/7MTM2')
            ###os.system('rm -rf /p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/7MTM2')
            ###print('remove /p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/7MTM2TM1')
            ###os.system('rm -rf /p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/7MTM2TM1')
            
            ##os.system('rm -rf /p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/7MTM2/combined-almagal.tar')
            ##os.system('rm -rf /p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/7MTM2TM1')
            ##os.system('rm -rf /p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/7MTM2/combined-visibilities.tar')

            my_runningTMP = os.getcwd()
            os.chdir('/p/largedata/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/TM2')
            
            #os.system('tar -xf almagal.tar -C . finished_step* almagal/REFIND.py almagal/casa-*.log almagal/*ont.dat almagal/*.cont.*.mask almagal/*.cube.*.mask almagal/pipeline-*')
            #os.system('mv almagal.tar all_almagal.tar')
            #os.system('tar -cf almagal.tar almagal finished_step*')
            #os.system('rm -rf almagal finished_step*')
            
            os.system('tar -xf almagal.tar -C . finished_step*')
            os.system('tar -xf almagal.tar -C . almagal/REFIND.py')
            os.system('tar -xf almagal.tar -C . almagal/casa-*.log')
            os.system('tar -xf almagal.tar -C . almagal/*ont.dat')
            os.system('tar -xf almagal.tar -C . almagal/*.cont.*.mask')
            os.system('tar -xf almagal.tar -C . almagal/*.cube.*.mask')
            os.system('tar -xf almagal.tar -C . almagal/pipeline-*')
            
            os.system('mv almagal.tar all_almagal.tar')
            os.system('tar -cf almagal.tar almagal finished_step*')
            os.system('rm -rf almagal')
            os.system('rm -rf finished_step*')
            
            os.chdir(my_runningTMP)
            
        else:
            if (args.noSelfCal == True):
                checkSelfCal = 0.0
                #if (args.fullReset == True):
                #    #os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/selfcalibrated')
                #    #os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/selfcalibrated')
            else:
                checkSelfCal = 1.0
            my_functionPrepareScriptsForJointDeconvolution(i, str(my_source), str(my_array), checkSelfCal)

#            #os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array))
#            #os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/JvM_'+str(my_array)+'.tar')
#            # JvM
#            #os.system('mv /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array)+' /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/JvM_'+str(my_array))
#            #os.system('tar -cf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/JvM_'+str(my_array)+'.tar /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/JvM_'+str(my_array))
#            #os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/JvM_'+str(my_array))
#            # multisteps
#            #os.system('mv /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array)+' /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/multisteps_'+str(my_array))
#            #os.system('tar -cf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/multisteps_'+str(my_array)+'.tar /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/multisteps_'+str(my_array))
#            #os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/multisteps_'+str(my_array))

########################################################################
