# ALMAGAL script
# 
# Created by Alvaro Sanchez-Monge
# Version 0.4
#
# Python script to transfer data products from ALMAGAL
# Mainly from the Juelich Supercomputer Center to a local computer
#
# Required:
#   - database/database.xlsx
#   - astropy (version tested 2.0.8)
#   - argparse (version tested 1.1)
#   - pandas (version tested 0.18.1)
#
# Optional:
#   - sourcefile.dat
#   - idfile.dat
#
# Execution:
#   - python scriptToFetchData.py --help
#
#     Examples:
#     
#     Transfer the available FITS products for the 7MTM2TM1 array for source 49143
#     > python scriptToFetchData.py --fitsProducts --array 7MTM2TM1  --source 49143
#
#     Transfer the available FITS products for the TM2 array for source 49143
#     > python scriptToFetchData.py --fitsProducts --array TM2 --source 49143
#
#     Transfer the available FITS products for the 7M data for the sources included in the file sourcefile.dat
#     > python scriptToFetchData.py --fitsProducts --array 7M  --srcfile sourcefile.dat
#
#-----------------------------------------------------------------------
# Import required packages
#
import os
import sys
import configALMAGAL
sys.path.insert(0,configALMAGAL.my_softwarePath+'/python/')

import numpy as np
import argparse
import astropy
from astropy.io import fits
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


########################################################################
#
# DEFINE LIST OF ARGUMENTS TO BE PROVIDED AT THE EXECUTION TIME
#
# Commands to select sources to be transferred. Sources can be selected
# either by their ID number or by their source name with the following
# python arguments:
#   --id,               : Single ID number (e.g., 0)
#   --idrange           : ID range (e.g., 0 10 to give the range (0, 10))
#   --idfile            : List of ID numbers stored in a file (e.g., idfile.dat)
#   --source            : Single source name (e.g., 543150)
#   --srcfile           : List of source names stored in a file (e.g., sourcefile.dat)
#
# Commands to indicate the array to be transferred:
#   --array             : Select array. Options are: 7M, TM2, TM1, 7MTM2, TM2TM1, 7MTM2TM1
#
# Commands to select which products will be transferred.
# There are three major groups:
# a) Visibility files, pipelines and weblogs (only valy for individual arrays: 7M, TM2, TM1)
#   --calibratedSource  : Transfer calibrated visibilities per source
#   --webLogs           : Transfer weblogs and cont.dat files (pipeline processing)
#   --entirePipeline    : Transfer entire pipeline output (large disk space!)
#
# b) Products from imaging (FITS files)
#   --fitsProducts      : Transfer FITS images, both continuum and cubes
#   --fitsCont          : Transfer continuum images, for combined arrays
#   --fitsCube          : Transfer cube images, for combined arrays
#   --fitsExtra         : Transfer extra images, for combined arrays
#   --fitsAuxiliary     : Transfer auxiliary data files, for combined arrays
#   --fitsAll           : Transfer all files for combined arrays (disabled)
#
# c) Commands for data processing. Do NOT use if you are a standard user
#   --selfCal           : Transfer self-calibration products (FITS and MS files)
#   --localToJSC        : Transfer pipeline products from local computer to Juelich (JSC) for final storage
#   --removePrevious    : Only for 7MTM2TM1, remove previous transferred data
#   --combine7MTM2TM1   : Only for processing the combination of 7MTM2TM1 cubes
#   --sendBack7MTM2TM1  : Only for transferring back the 7MTM2TM1 combined products
#
#-----------------------------------------------------------------------
# Create a list of arguments
#
parser = argparse.ArgumentParser(description="+++ ----------------------------------------------------------------------- \
                                              +++ ALMAGAL : Fetch and transfer ALMAGAL data products ")
#
parser.add_argument('--id',
                    help='OPTIONAL: ID number of the source to be transferred')
parser.add_argument('--idrange', nargs=2, type=int,
                    help='OPTIONAL: Range of source ID numbers to be processed. \
                            Two integer numbers are required for this option: \
                            first: first ID in the range of sources to execute \
                            last: last ID in the range of sources to execute')
parser.add_argument('--idfile',
                    help='OPTIONAL: File with list of IDs to be transferred')
parser.add_argument('--source',
                    help='OPTIONAL: Name of the source to be transferred')
parser.add_argument('--srcfile',
                    help='OPTIONAL: File with list of sources to be transferred')
#
parser.add_argument('--array',
                    help='OPTIONAL: Select array: 7M, TM2, TM1, 7MTM2, ...')
#
parser.add_argument('--calibratedSource', action='store_true',
                    help='OPTIONAL: Transfer calibrated visibilities per source')
parser.add_argument('--webLogs', action='store_true',
                    help='OPTIONAL: Transfer weblogs and cont.dat files (pipeline processing)')
parser.add_argument('--entirePipeline', action='store_true',
                    help='OPTIONAL: Transfer entire pipeline output (large disk space!)')
#
parser.add_argument('--fitsProducts', action='store_true',
                    help='OPTIONAL: Transfer products: FITS files')
parser.add_argument('--fitsCont', action='store_true',
                    help='OPTIONAL: Transfer continuum files for combined arrays')
parser.add_argument('--fitsCube', action='store_true',
                    help='OPTIONAL: Transfer cubes files for combined arrays')
parser.add_argument('--fitsExtra', action='store_true',
                    help='OPTIONAL: Transfer extra files for combined arrays')
parser.add_argument('--fitsAuxiliary', action='store_true',
                    help='OPTIONAL: Transfer auxiliary files for combined arrays')
parser.add_argument('--fitsAll', action='store_true',
                    help='OPTIONAL: Transfer all files for combined arrays (disabled)')
#
parser.add_argument('--selfCal', action='store_true',
                    help='OPTIONAL: Transfer self-calibration products (FITS and MS files)')
parser.add_argument('--localToJSC', action='store_true',
                    help='OPTIONAL: Transfer pipeline products from local computer to JSC (ask Alvaro)')
parser.add_argument('--removePrevious', action='store_true',
                    help='OPTIONAL: Only for 7MTM2TM1, remove previous transferred data (ask Alvaro)')
parser.add_argument('--combine7MTM2TM1', action='store_true',
                    help='OPTIONAL: Only for processing the combination of 7MTM2TM1 cubes (ask Alvaro)')
parser.add_argument('--sendBack7MTM2TM1', action='store_true',
                    help='OPTIONAL: Only for transferring back the 7MTM2TM1 combined products (ask Alvaro)')
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
my_username = configALMAGAL.my_usernameJSC
my_workstation = configALMAGAL.my_workstationTransfer
my_mainPath = configALMAGAL.my_storagePathTransfer
print("::: ALMAGAL command ::: Transfer data products to " + str(my_workstation))

#-----------------------------------------------------------------------
# Define the sources to transfer
#
# Create empty lists of sources (do not modify)
#
my_sourceIDs = []
my_sourceNAMEs = []

#.......................................................................
#
# Method 1.- Define the IDs of the sources
#            e.g.
#            my_sourceIDs = [0, 1, 2]
#            my_sourceIDs = range(0,3)
my_sourceIDs = [0]
#my_sourceIDs = range(0, 1017)

#.......................................................................
#
# Method 2.- Define the NAMEs of the sources
#            e.g.
#            my_sourceNAMEs = [49143, 561782, 565926]
#my_sourceNAMEs = [49143, 561782, 565926]

#.......................................................................
#
# Method 3.- Define the NAMEs of the sources via input variables
#            e.g.
#            python copyFiles.py --source 49143
#            python copyFiles.py --srcfile sourcefile.dat
#
if (args.source != None):
    my_sourceNAMEs = [args.source]

if (args.srcfile != None):
    lines = [line.rstrip('\n') for line in open(args.srcfile)]
    my_sourceNAMEs = []
    for line in lines:
        my_sourceNAMEs.append(line)

#.......................................................................
#
# Method 4.- Define the IDs of the sources via input variables
#            e.g.
#            python copyFiles.py --id 539
#            python copyFiles.py --idfile idfile.dat
#
if (args.id != None):
    my_sourceIDs = [int(args.id)]

if (args.idrange != None):
    my_firstID = int(args.idrange[0])
    my_lastID = int(args.idrange[1])
    if (my_lastID <= my_firstID):
        my_lastID = my_firstID+1
        print("... the last ID in the range is smaller than the first ID")
        print("... ID source range modified to (" + str(my_firstID) + ", " + str(my_lastID) + ")")
    my_sourceIDs = range(my_firstID, my_lastID)

if (args.idfile != None):
    lines = [line.rstrip('\n') for line in open(args.idfile)]
    my_sourceIDs = []
    for line in lines:
        my_sourceIDs.append(int(line))

#-----------------------------------------------------------------------
# Define the arrays to be processed
#
#.......................................................................
#
# Method 1.- Define the array as a list
#            e.g.
#            my_arrays = ['7M', 'TM2', 'TM1']
my_arrays = ['7M']

#.......................................................................
#
# Method 2.- Define the array via input variables
#            e.g.
#            python copyFiles.py --array 7M
if (args.array == '7M') or (args.array == 'TM2') or (args.array == 'TM1') or (args.array == '7MTM2') or (args.array == 'TM2TM1') or (args.array == '7MTM2TM1'):
    my_arrays = [args.array]

if (args.array == 'ALL'):
    my_arrays = ['7M', 'TM2', 'TM1']
    #my_arrays = ['7M', 'TM2']
#
########################################################################


########################################################################
#
# FUNCTION: fetchData
#
def fetchData(my_sourceIDs, my_sourceNAMEs, my_arrays):
    
    """
    Transfer data from Juelich (JSC) to your local computer. 
    
    Parameters
    ----------
    my_sourceIDs   : list of integers
        One-dimension list with source IDs
    my_sourceNAMEs : list of strings
        One-dimension list with source NAMEs
    my_arrays      : list of strings
        One-dimension list with the selected array
    """

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

    # Create list with all the sources and source indices
    #
    my_sources = df['Source']
    my_indices = df['Index']

    # Create list with indices of selected sources
    #
    if (len(my_sourceNAMEs) > 0):
        my_sourceIDs = []
        for my_sourceNAME in my_sourceNAMEs:
            my_sourceIDs.append(df[df['Source']==str(my_sourceNAME)].index.values[0])

    #-----------------------------------------------------------------------
    # Define path where the data for each source will be stored
    #
    os.system('mkdir -p ' + my_mainPath + '/2019.1.00195.L')
    os.system('mkdir -p ' + my_mainPath + '/2019.1.00195.L/sources')
    my_individualPath =  my_mainPath + '/2019.1.00195.L/sources'
    print("::: ALMAGAL command ::: Files will be transferred to " + my_individualPath)

    #-----------------------------------------------------------------------
    # Process selected sources
    #
    my_is = my_sourceIDs
    for i in my_is:
        
        my_source = my_sources[i]
        my_id = i
        
        print(" ")
        print("Processing (ID: " + str(my_id) + ") source " + str(my_source) + "...")
        
        for my_array in my_arrays:
            
            # Transfer data for individual arrays
            #
            if (my_array == '7M') or (my_array == 'TM2') or (my_array == 'TM1'):

                # Transfer calibrated (and self-calibrated) visibility data per individual source (perEB)
                # The function checks if some files exist already in the destination directory
                #
                if (args.calibratedSource == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array)
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB')
                    
                    my_currentSourceCalibratedPath = '/' + str(my_source) + '/calibrated/' + my_array + '/perEB'
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceCalibratedPath))
                    
                    if (args.calibratedSource == True) and (len(my_TMPfiles) == 0):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceCalibratedPath + '/*.tar ' + my_individualPath + my_currentSourceCalibratedPath + '/.')
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated/' + my_array)
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated/' + my_array + '/perEB')
                    
                    my_currentSourceCalibratedPath = '/' + str(my_source) + '/selfcalibrated/' + my_array + '/perEB'
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceCalibratedPath))
                    
                    if (args.selfCal == True) and (len(my_TMPfiles) == 0):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceCalibratedPath + '/*.tar ' + my_individualPath + my_currentSourceCalibratedPath + '/.')
            
                # Transfer pipeline weblogs and cont.dat files
                # The function checks if the pipeline-weblog.tar file exists already in the destination directory
                #
                if (args.webLogs == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array)
                    
                    my_currentSourcePipelinePath = '/' + str(my_source) + '/pipeline/' + my_array
                    
                    if (args.webLogs == True) and (os.path.isfile(my_individualPath + my_currentSourcePipelinePath + '/pipeline-weblog.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourcePipelinePath + '/pipeline-weblog.tar ' + my_individualPath + my_currentSourcePipelinePath + '/.')
                
                # Transfer the entire output of the pipeline run (requires large storage space)
                # The function checks if the almagal.tar file exists already in the destination directory
                #
                if (args.entirePipeline == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array)
                    
                    my_currentSourcePipelinePath = '/' + str(my_source) + '/pipeline/' + my_array
                    
                    if (args.webLogs == True) and (os.path.isfile(my_individualPath + my_currentSourcePipelinePath + '/almagal.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourcePipelinePath + '/almagal.tar ' + my_individualPath + my_currentSourcePipelinePath + '/.')


            # Transfer products for individual arrays (old) - currently disabled
            #
            if (my_array == 'old-7M') or (my_array == 'old-TM2') or (my_array == 'old-TM1'):

                # Transfer calibrated visibility data per individual source (perEB)
                # The function checks if some files exist already in the destination directory
                #
                if (args.calibratedSource == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array)
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB')
                    
                    my_currentSourceCalibratedPath = '/' + str(my_source) + '/calibrated/' + my_array + '/perEB'
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceCalibratedPath))
                    
                    if (args.calibratedSource == True) and (len(my_TMPfiles) == 0):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceCalibratedPath + '/*.tar ' + my_individualPath + my_currentSourceCalibratedPath + '/.')
                
                # Transfer FITS image products (continuum and cubes) for individual arrays
                # The function checks if the pipeline-fits.tar file exists already in the destination directory
                #
                if (args.fitsProducts == True) or (args.fitsCont == True) or (args.fitsCube == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/' + my_array)
                    
                    my_currentSourceImagePath = '/' + str(my_source) + '/images/' + my_array
                    
                    if (args.fitsProducts == True) and (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/pipeline-fits.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/pipeline-fits.tar ' + my_individualPath + my_currentSourceImagePath + '/.')
                
                # Transfer pipeline weblogs and cont.dat files
                # The function checks if the pipeline-weblog.tar file exists already in the destination directory
                #
                if (args.webLogs == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array)
                    
                    my_currentSourcePipelinePath = '/' + str(my_source) + '/pipeline/' + my_array
                    
                    if (args.webLogs == True) and (os.path.isfile(my_individualPath + my_currentSourcePipelinePath + '/pipeline-weblog.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourcePipelinePath + '/pipeline-weblog.tar ' + my_individualPath + my_currentSourcePipelinePath + '/.')
                
                # Transfer the entire output of the pipeline run (requires large storage space)
                # The function checks if the almagal.tar file exists already in the destination directory
                #
                if (args.entirePipeline == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array)
                    
                    my_currentSourcePipelinePath = '/' + str(my_source) + '/pipeline/' + my_array
                    
                    if (args.webLogs == True) and (os.path.isfile(my_individualPath + my_currentSourcePipelinePath + '/almagal.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourcePipelinePath + '/almagal.tar ' + my_individualPath + my_currentSourcePipelinePath + '/.')
                
                # Transfer FITS image products (continuum) from Joint Deconvolution (beta version)
                #
                if (args.localToJSC == True):
                    
                    if os.path.exists(my_individualPath + '/' + str(my_source) + '/images/' + my_array + '/transferred.txt'):
                        print("... FITS images transferred")
                    else:
                        print("... transferring FITS images")
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_individualPath + '/' + str(my_source) + '/images/' + my_array + ' ' + str(my_username) + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/' + str(my_source) + '/images/' + str(my_username) + '_' + my_array)
                        os.system('touch ' + my_individualPath + '/' + str(my_source) + '/images/' + my_array + '/transferred.txt')
                    
                    if os.path.exists(my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array + '/transferred.txt'):
                        print("... pipeline products transferred")
                    else:
                        print("... transferring pipeline products")
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array + ' ' + str(my_username) + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/' + str(my_username) + '_' + my_array)
                        os.system('touch ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array + '/transferred.txt')

            # Transfer products for combined arrays (old) - currently disabled
            #
            if (my_array == 'old-7MTM2'):
                
                # Transfer all files from Joint Deconvolution
                #
                if (args.fitsAll == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    
                    my_currentSourceImagePath = '/' + str(my_source) + '/images/combined/' + my_array
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceImagePath))
                    
                    if (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/combined-almagal.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/combined-almagal.tar ' + my_individualPath + my_currentSourceImagePath + '/.')
                
                # Transfer FITS image products (continuum) from Joint Deconvolution
                #
                if (args.fitsCont == True) or (args.fitsProducts == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    
                    my_currentSourceImagePath = '/' + str(my_source) + '/images/combined/' + my_array
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceImagePath))
                    
                    if (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/combined-cont-fits.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/combined-cont-fits.tar ' + my_individualPath + my_currentSourceImagePath + '/.')
                    
                # Transfer FITS image products (data cubes) from Joint Deconvolution
                #
                if (args.fitsCube == True) or (args.fitsProducts == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    
                    my_currentSourceImagePath = '/' + str(my_source) + '/images/combined/' + my_array
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceImagePath))
                    
                    if (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/combined-line-fits.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/combined-line-fits.tar ' + my_individualPath + my_currentSourceImagePath + '/.')

            # Transfer products for combined arrays
            #
            if (my_array == '7MTM2TM1') or (my_array == '7MTM2') or (my_array == 'TM2TM1') or (my_array == '7M') or (my_array == 'TM2') or (my_array == 'TM1'):
                
                # Transfer continuum FITS image products from Joint Deconvolution
                #
                if (args.fitsCont == True) or (args.fitsProducts == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined')
                    if (args.removePrevious == True):
                        os.system('rm -r ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    
                    my_currentSourceImagePath = '/' + str(my_source) + '/images/combined/' + my_array
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceImagePath))
                    
                    if (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/combined-cont-fits.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/combined-cont-fits.tar ' + my_individualPath + my_currentSourceImagePath + '/.')
                
                # Transfer cube FITS image products from Joint Deconvolution
                #
                if (args.fitsCube == True) or (args.fitsProducts == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined')
                    if (args.removePrevious == True):
                        os.system('rm -r ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    
                    my_currentSourceImagePath = '/' + str(my_source) + '/images/combined/' + my_array
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceImagePath))
                    
                    if (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/combined-line-fits.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/combined-line-fits.tar ' + my_individualPath + my_currentSourceImagePath + '/.')
                
                # Transfer extra FITS products from Joint Deconvolution
                #
                if (args.fitsExtra == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined')
                    if (args.removePrevious == True):
                        os.system('rm -r ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    
                    my_currentSourceImagePath = '/' + str(my_source) + '/images/combined/' + my_array
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceImagePath))
                    
                    if (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/combined-extra-fits.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/combined-extra-fits.tar ' + my_individualPath + my_currentSourceImagePath + '/.')
                
                # Transfer auxiliary files from Joint Deconvolution
                #
                if (args.fitsAuxiliary == True):
                    
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined')
                    if (args.removePrevious == True):
                        os.system('rm -r ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/' + my_array)
                    
                    my_currentSourceImagePath = '/' + str(my_source) + '/images/combined/' + my_array
                    
                    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceImagePath))
                    
                    if (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/combined-auxiliary.tar') == False):
                        os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/combined-auxiliary.tar ' + my_individualPath + my_currentSourceImagePath + '/.')
    
        # Transfer data for 7MTM2TM1 combination processing in your local computer
        # For data processing only, contact Alvaro Sanchez-Monge if you want to use it
        #
        if (args.combine7MTM2TM1 == True):
            
            os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
            os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/calibrated')
            os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/' + str(my_source) + '/calibrated ' + my_individualPath + '/' + str(my_source) + '/.')
            os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/pipeline')
            os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/' + str(my_source) + '/pipeline ' + my_individualPath + '/' + str(my_source) + '/.')
            os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
            os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined')
            os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/scratch/almagal/ALMAGAL/data/2019.1.00195.L/sources/' + str(my_source) + '/images/combined/7MTM2TM1 ' + my_individualPath + '/' + str(my_source) + '/images/combined/.')
            
            os.system("cp -rp tmp_executeRuns.sh executeRuns.sh")
            fin = open("executeRuns.sh", "rt")
            data = fin.read()
            data = data.replace("ToModifyIDSOURCE", str(my_id))
            fin.close()
            fin = open("executeRuns.sh", "wt")
            fin.write(data)
            fin.close()
        
        # Transfer back processed 7MTM2TM1 combined products
        # For data processing only, contact Alvaro Sanchez-Monge if you want to use it
        #
        if (args.sendBack7MTM2TM1 == True):
            
            if os.path.exists(my_individualPath + '/' + str(my_source) + '/images/combined/7MTM2TM1/transferred.txt'):
                print("... combined products transferred")
            else:
                print("... transferring combined products")
                os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_individualPath + '/' + str(my_source) + '/images/combined/7MTM2TM1 ' + str(my_username) + '@judac.fz-juelich.de:/p/scratch/almagal/transferred/' + str(my_source) + '/.')
                os.system('touch ' + my_individualPath + '/' + str(my_source) + '/images/combined/7MTM2TM1/transferred.txt')
        
        # Transfer self-calibration products (FITS and MS files)
        # The function checks if some files exist already in the destination directory
        # For data processing only, contact Alvaro Sanchez-Monge if you want to use it
        #
        if (args.selfCal == True):
            
            os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
            os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
            os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/selfcalibrated')
            
            my_currentSourceImagePath = '/' + str(my_source) + '/images/selfcalibrated'
            
            if (args.selfCal == True) and (os.path.isfile(my_individualPath + my_currentSourceImagePath + '/selfcalibrated-fits.tar') == False):
                os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceImagePath + '/selfcalibrated-fits.tar ' + my_individualPath + my_currentSourceImagePath + '/.')

            os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
            os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated')
            
            for my_array in ['7M', 'TM2', 'TM1']:
                os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated/' + my_array)
                os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/selfcalibrated/' + my_array + '/perEB')
                
                my_currentSourceCalibratedPath = '/' + str(my_source) + '/selfcalibrated/' + my_array + '/perEB'
                
                my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_individualPath + my_currentSourceCalibratedPath))
                
                if (args.selfCal == True) and (len(my_TMPfiles) == 0):
                    os.system('scp -rp -i ~/.ssh/id_ed25519_jsc ' + my_username + '@judac.fz-juelich.de:/p/data1/almagaldata/ALMAGAL/data/2019.1.00195.L/sources' + my_currentSourceCalibratedPath + '/*.tar ' + my_individualPath + my_currentSourceCalibratedPath + '/.')

    print(" ")
    print("::: ALMAGAL command ::: Files transferred to " + my_individualPath)
#
########################################################################

# Execute main function to transfer data
#
fetchData(my_sourceIDs, my_sourceNAMEs, my_arrays)