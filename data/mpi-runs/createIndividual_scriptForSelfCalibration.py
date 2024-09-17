########################################################################
#
#                   ALMAGAL processing pipeline
#
#
# 
# Script number 4                        created by Alvaro Sanchez-Monge
#
# Previous step:   tarPipelineProducts.py
# Next step:       tarPipelineSelfCalibrationProducts.py
# 
# Description:     Python script to generate the scripts that are used
#                  to self-calibrate the data (of all arrays)
# 
# Required:
#   - database.csv file containing names and MOUS directory tree
#   - calibrated split files produced with scriptToSplitSources.py
#   - pipeline-weblog tar file produced with scriptToSplitSources.py
#     and stored with tarPipelineProducts.py
#   - master scripts:
#        scriptForSelfCalibration.py
#
# Execution:
#   - python createIndividual_scriptForSelfCalibration.py
#     followed by
#     ./my_executeSelfCalibration.sh
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
from functionsALMAGAL import *

########################################################################
#
# DEFINE LIST OF ARGUMENTS TO BE PROVIDED AT THE EXECUTION TIME
#
# Commands to select sources to be processed. Sources can be selected
# either by their ID number or by their source name with the following
# python arguments:
#   --id,            : Single ID number (e.g., 0)
#   --idrange        : ID range (e.g., 0 10 to give the range (0, 10))
#
# Additional commands:
#   --activeOut      : Remove the active.txt file that exist after wrong execution
#   --fullReset      : Remove the full directory for selected sources
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
parser.add_argument('--activeOut', action='store_true',
                    help='OPTIONAL: Remove existing active.txt files')
#
parser.add_argument('--fullReset', action='store_true',
                    help='OPTIONAL: Remove the directory of selected source (be careful!)')
#
args = parser.parse_args()
#
########################################################################


########################################################################
#
# SET UP SOURCES AND VARIABLES
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
my_executeFile = 'my_executeSelfCalibration.sh'
os.system('rm -rf ' + my_executeFile)

#-----------------------------------------------------------------------
# Process selected sources
#
my_is = my_sourceIDs
for i in my_is:
    
    my_source = my_sources[i]
    
    print(" ")
    print("Processing (ID: " + str(i) + ") source " + str(my_source) + "...")
    
    if (args.activeOut == True):
        os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/selfcalibrated/active.txt')
    
    if (args.fullReset == True):
        # pipeline reload (for Cubes)
        os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/pipeline')
        os.system('rm -rf /p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/'+str(my_source)+'/images/selfcalibrated')
    
    my_functionPrepareScriptsForSelfCalibration(i, str(my_source))

########################################################################
