########################################################################
#
#                   ALMAGAL processing pipeline
#
#
# 
# Script number 1                        created by Alvaro Sanchez-Monge
#
# Previous step:   Download calibrated data from ALMA archive
# Next step:       createIndividual_scriptForImaging.py
# 
# Description:     Python script to split the calibrated data contained
#                  in the MOUS files into individual calibrated files
#                  for each source
# 
# Required:
#   - database.csv file containing names and MOUS directory tree
#   - calibrated MOUS files
#
# Execution:
#   - python scriptToSplitSources.py
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
#            my_arrays = ['7M', 'TM2', 'TM1']
my_arrays = ['7M']
#
# Method 2.- Define the array via input variables
#            e.g.
#            python copyFiles.py --array 7M
if (args.array == '7M') or (args.array == 'TM2') or (args.array == 'TM1'):
    my_arrays = [args.array]

if (args.array == 'ALL'):
    my_arrays = ['7M', 'TM2', 'TM1']
#
########################################################################

#-----------------------------------------------------------------------
# Define the sources to process
#
#my_sourceIDs = [0]
#my_sourceIDs = range(0, 1017)

#-----------------------------------------------------------------------
# Define the arrays to be processed
#
#my_arrays = ['7M']
#my_arrays = ['7M', 'TM2', 'TM1']

########################################################################
#
# MAIN PROCESSING STARTS HERE
#
#-----------------------------------------------------------------------
# Load the database from csv/excel file into Pandas format
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
os.system('mkdir -p ' + my_individualPath)

# Define path for almagaldata storage
#
my_individualStoragePath = my_storagePath + '/2019.1.00195.L/sources'
os.system('mkdir -p ' + my_individualStoragePath)

#-----------------------------------------------------------------------
# Process selected sources
#
my_is = my_sourceIDs
for i in my_is:
    
    my_source = my_sources[i]
    
    print(" ")
    print("Processing source " + str(my_source) + " (source number " + str(i) + ") ...")
    
    # Create directory tree (not necessary once created)
    # These lines can be commented out once the directory structure has been created
    #
    os.system('mkdir -p ' + my_dataPath + '/science_goal.' + df.SGOUS[my_source])
    os.system('mkdir -p ' + my_dataPath + '/science_goal.' + df.SGOUS[my_source] + '/group.' + df.GOUS[my_source])
    os.system('mkdir -p ' + my_dataPath + '/science_goal.' + df.SGOUS[my_source] + '/group.' + df.GOUS[my_source] + '/member.' + df.MOUS_7M[my_source])
    os.system('mkdir -p ' + my_dataPath + '/science_goal.' + df.SGOUS[my_source] + '/group.' + df.GOUS[my_source] + '/member.' + df.MOUS_7M[my_source] + '/calibrated')
    os.system('mkdir -p ' + my_dataPath + '/science_goal.' + df.SGOUS[my_source] + '/group.' + df.GOUS[my_source] + '/member.' + df.MOUS_TM2[my_source])
    os.system('mkdir -p ' + my_dataPath + '/science_goal.' + df.SGOUS[my_source] + '/group.' + df.GOUS[my_source] + '/member.' + df.MOUS_TM2[my_source] + '/calibrated')
    os.system('mkdir -p ' + my_dataPath + '/science_goal.' + df.SGOUS[my_source] + '/group.' + df.GOUS[my_source] + '/member.' + df.MOUS_TM1[my_source])
    os.system('mkdir -p ' + my_dataPath + '/science_goal.' + df.SGOUS[my_source] + '/group.' + df.GOUS[my_source] + '/member.' + df.MOUS_TM1[my_source] + '/calibrated')
    
    # Create a directory for the source being processed
    #
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
    
    # Loop through arrays to be processed
    #
    for my_array in my_arrays:
        
        # Create directories where data will be stored
        #
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + str(my_array))
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB')
        
        # Evaluate and read the number of already processed files
        #
        my_sourceSplitPath = my_individualPath + '/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB'
        my_sourceSplitPaths, my_sourceSplitDirs, my_sourceSplitFiles = next(os.walk(my_sourceSplitPath))
        
        # If files have been processed
        #
        if len(my_sourceSplitFiles) >= 1:
            
            print("... " + str(my_array) + " files already processed")
        
        # If files have not been processed
        #
        elif len(my_sourceSplitFiles) == 0:
            
            # Determine how many files have to be processed (i.e., execution blocks available)
            #
            if (my_array == '7M'):
                my_sourcePath = my_dataPath + '/science_goal.' + df.SGOUS[i] + '/group.' + df.GOUS[i] + '/member.' + df.MOUS_7M[i] + '/calibrated'
            if (my_array == 'TM2'):
                my_sourcePath = my_dataPath + '/science_goal.' + df.SGOUS[i] + '/group.' + df.GOUS[i] + '/member.' + df.MOUS_TM2[i] + '/calibrated'
            if (my_array == 'TM1'):
                my_sourcePath = my_dataPath + '/science_goal.' + df.SGOUS[i] + '/group.' + df.GOUS[i] + '/member.' + df.MOUS_TM1[i] + '/calibrated'
            my_sourcePaths, my_sourceDirs, my_sourceFiles = next(os.walk(my_sourcePath))
            
            # If data available
            #
            if len(my_sourceDirs) >= 1:
                
                print("... " + str(len(my_sourceDirs)) + " file(s) for source " + str(my_source) + " with the " + str(my_array) + " array")
                
                # Split per source (keep all spectral windows in the same file)
                # Scientific spectral windows are:
                #   7M:  16, 18, 20 and 22
                #   TM2: 25, 27, 29 and 31
                #   TM1: 25, 27, 29 and 31
                #
                if (my_array == '7M'):
                    my_spws = '16, 18, 20, 22'
                if (my_array == 'TM2'):
                    my_spws = '25, 27, 29, 31'
                if (my_array == 'TM1'):
                    my_spws = '25, 27, 29, 31'
                
                my_individualFileList = []
                for my_sourceDir in my_sourceDirs:
                    my_sourceFile = my_sourcePath + '/' + my_sourceDir
                    my_individualFile = my_individualPath + '/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB/' + str(my_source) + '_' + str(my_array) + '_' + my_sourceDir
                    my_individualFileList.append(str(my_individualFile))
                    
                    os.system('rm -rf ' + my_individualFile)
                    #split(vis = str(my_sourceFile),
                    #    outputvis = str(my_individualFile),
                    #    field = str(my_source),
                    #    spw = my_spws,
                    #    datacolumn = 'data')
                    #
                    # Create a CASA python script to convert IMAGE files into FITS files
                    #
                    my_CASAscriptFileName = "tmpExecute_" + str(my_source) + ".py"
                    os.system("rm -rf " + my_CASAscriptFileName)
                    os.system("touch " + my_CASAscriptFileName)
                    
                    with open(my_CASAscriptFileName, 'w') as writer:
                        writer.write("split(vis='"+str(my_sourceFile)+"', outputvis='"+str(my_individualFile)+"', field='"+str(my_source)+"', spw='"+str(my_spws)+"', datacolumn='data')\n")
                    
                    os.system(my_softwarePath + "/casa-pipeline-release-5.6.1-8.el7/bin/casa --nologger --nogui -c "+ my_CASAscriptFileName)
                    
                    # Compressing the created directories into .tar file
                    # 
                    my_runningDirectoryTMP = os.getcwd()
                    os.chdir(my_mainPath)
                    os.system('tar -cf ' + str(my_individualFile) + '.tar ' + str(my_individualFile[len(my_mainPath)+1:]))
                    os.chdir(my_runningDirectoryTMP)
                    
                    os.system('rm -rf ' + str(my_individualFile))
                    
                    # Copy .tar file in the data directory (for storage and backup)
                    #
                    os.system('mkdir -p ' + str(my_storagePath) + '/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array))
                    os.system('mkdir -p ' + str(my_storagePath) + '/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB')
                    os.system('scp -rp ' + str(my_individualFile) + '.tar ' + str(my_storagePath) + '/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB/.')
                    #
                    # Old script: saving data in the archive directory. This was modified.
                    #os.system('mkdir -p /p/data1/almagaldata/data/archive/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array))
                    #os.system('mkdir -p /p/data1/almagaldata/data/archive/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB')
                    #os.system('scp -rp ' + str(my_individualFile) + '.tar /p/data1/almagaldata/data/archive/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB/.')
                
                '''
                # OLD APPROACH, MAINTAINED HERE FOR FUTURE REFERENCE
                #
                # Split per source and spectral window
                # Scientific spectral windows are:
                #   7M:  16, 18, 20 and 22
                #   TM2: 25, 27, 29 and 31
                #   TM1: 25, 27, 29 and 31
                #
                if (my_array == '7M'):
                    my_spws = ['16', '18', '20', '22']
                if (my_array == 'TM2'):
                    my_spws = ['25', '27', '29', '31']
                if (my_array == 'TM1'):
                    my_spws = ['25', '27', '29', '31']
                
                for my_spw in range(0, 4):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB/spw' + str(my_spw))
                    my_individualFileList = []
                    for my_sourceDir in my_sourceDirs:
                        my_sourceFile = my_sourcePath + '/' + my_sourceDir
                        my_individualFile = my_individualPath + '/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB/spw' + str(my_spw) + '/' + str(my_source) + '_' + str(my_array) + '_spw' + str(my_spw) + '_' + my_sourceDir
                        my_individualFileList.append(str(my_individualFile))
                        
                        os.system('rm -rf ' + my_individualFile)
                        split(vis = str(my_sourceFile),
                            outputvis = str(my_individualFile),
                            field = str(my_source),
                            spw = my_spws[my_spw],
                            datacolumn = 'data')
                        
                        # Compressing the created directories into .tar file
                        # 
                        os.system('tar -cvf ' + str(my_individualFile) + '.tar ' + str(my_individualFile))
                        os.system('rm -rf ' + str(my_individualFile))
                        
                        # Copy .tar file in the data directory (for storage and backup)
                        #
                        os.system('mkdir -p /p/data1/almagaldata/data/archive/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array))
                        os.system('mkdir -p /p/data1/almagaldata/data/archive/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB')
                        os.system('mkdir -p /p/data1/almagaldata/data/archive/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB/spw' + str(my_spw))
                        os.system('scp -rp ' + str(my_individualFile) + '.tar /p/data1/almagaldata/data/archive/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + str(my_array) + '/perEB/spw' + str(my_spw) + '/.')
                '''
            
            # If data not available
            #
            elif len(my_sourceDirs) == 0:
                
                print("... " + "No data yet for source " + str(my_source) + " with the " + str(my_array) + " array")
