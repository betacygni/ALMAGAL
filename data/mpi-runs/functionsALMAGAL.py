########################################################################
#
#                      ALMAGAL functions file
#
#
# 
# Auxiliary script number 2              created by Alvaro Sanchez-Monge
#
# Description:      Python script containing main functions used by
#                   other ALMAGAL scripts
# 
#-----------------------------------------------------------------------
#
# Define functions for ALMAGAL
#
import os
import re
import sys
import glob
import numpy as np
import argparse
import astropy
from astropy.io import fits
from astropy.stats import median_absolute_deviation
from scipy import ndimage
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from matplotlib import pyplot as plt
import subprocess
import shutil
import configALMAGAL
from functionsALMAGAL import *
import warnings


def my_functionReadALMAGALConfigFile(verbose=False):
    
    """
    Function to read in the variables of the config file mainly
    containing information on the JSC-username and directories
    and the directories for your working workstation
    
    Input:
      verbose : optional, prints messages
    
    Ouput:
      my_usernameJSC
      my_workstationTransfer
      my_storagePathTransfer
      my_workstation
      my_mainPath
      my_runningPath
      my_softwarePath
      my_storagePath
    
    """
    
    # Define variables related to data transfer
    #
    my_usernameJSC = configALMAGAL.my_usernameJSC
    my_workstationTransfer = configALMAGAL.my_workstationTransfer
    my_storagePathTransfer = configALMAGAL.my_storagePathTransfer
    
    # Define variables related to data processing
    #
    my_workstation = configALMAGAL.my_workstation
    my_mainPath = configALMAGAL.my_mainPath
    my_runningPath = configALMAGAL.my_runningPath
    my_softwarePath = configALMAGAL.my_softwarePath
    my_storagePath = configALMAGAL.my_storagePath
    
    if verbose == True:
        
        print("::: ")
        print("::: ALMAGAL command ::: You are processing ALMAGAL data in " + str(my_workstation))
        print("::: ALMAGAL command ::: Main path is " + str(my_mainPath))
        print("::: ALMAGAL command ::: Running path is " + str(my_runningPath))
        print("::: ALMAGAL command ::: Software path is " + str(my_softwarePath))
        print("::: ALMAGAL command ::: Storage path is " + str(my_storagePath))
        print("::: ALMAGAL command ::: Your JSC username is " + str(my_usernameJSC))
        print("::: ALMAGAL command ::: Your workstation to store data is " + str(my_workstationTransfer))
        print("::: ALMAGAL command ::: Your storage path is " + str(my_storagePathTransfer))
    
    return my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath


def my_functionLoadSourcesDatabase(verbose=False):
    
    """
    Function to read the source database file and store the source
    IDs and source names in list variables
    
    Input:
      verbose : optional, prints messages
    
    Ouput:
      my_sources : list with the names of the ALMAGAL sources
      my_indices : list with the indices of the ALMAGAL sources
    
    """
    
    #-----------------------------------------------------------------------
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Define path where database is stored
    #
    my_databasePath =  my_mainPath + '/database'
    
    if (os.path.isfile(str(my_databasePath)+'/database.csv') == True):
        
        # Read CSV version of the database file
        #
        if verbose == True:
            
            print("::: ")
            print("::: ALMAGAL command ::: Database file used " + str(my_databasePath) + "/database.csv")
        
        df = pd.read_csv(str(my_databasePath) + '/database.csv')
    
    elif (os.path.isfile(str(my_databasePath)+'/database.xlsx') == True):
        
        # Read EXCEL version of the database file
        #
        if verbose == True:
            
            print("::: ")
            print("::: ALMAGAL command ::: Database file used " + str(my_databasePath) + "/database.xlsx")
        
        df = pd.read_excel(str(my_databasePath) + '/database.xlsx', sheet_name='Sheet1')
    
    else:
        
        # No database file exists
        #
        if verbose == True:
            
            print("::: ")
            print("::: ALMAGAL command ::: ERROR! Files database.csv or database.xlsx NOT available!")
    
    df['Index'] = df.index
    df['Source'] = df['Source'].apply(str)
    
    # Create list with all the sources
    #
    my_sources = df['Source']
    my_indices = df['Index']
    
    return my_sources, my_indices


def my_functionCreateDirectoryStructure(my_source):
    
    """
    Function to create the full directory structure for a given source
    within the ALMAGAL project. It initializes all the required 
    directories for calibration, pipeline products and images
    
    After that, it creates a series of variables containing the 
    corresponding paths to these directories
    
    Input variables:
      my_source : string with source name
      
    Ouput:
      my_calibratedDirectory7M
      my_calibratedDirectoryTM2
      my_calibratedDirectoryTM1
      my_pipelineDirectory7M
      my_pipelineDirectoryTM2
      my_pipelineDirectoryTM1
      my_imagesDirectory7M
      my_imagesDirectoryTM2
      my_imagesDirectoryTM1
      my_imagesDirectory7MTM2
      my_imagesDirectory7MTM2TM1
      my_imagesDirectoryTM2TM1
      
    """
    #-----------------------------------------------------------------------
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    my_individualPath =  my_mainPath + '/2019.1.00195.L/sources'
    my_individualStoragePath =  my_storagePath + '/2019.1.00195.L/sources'
    
    #-----------------------------------------------------------------------
    # Create source directory
    #
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source))
    
    # Create directories where calibrated visibilities are stored
    #
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/7M')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/7M/perEB')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/TM2')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/TM2/perEB')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/TM1')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/TM1/perEB')
    #
    my_calibratedDirectory7M = my_individualPath + '/' + str(my_source) + '/calibrated/7M/perEB'
    my_calibratedDirectoryTM2 = my_individualPath + '/' + str(my_source) + '/calibrated/TM2/perEB'
    my_calibratedDirectoryTM1 = my_individualPath + '/' + str(my_source) + '/calibrated/TM1/perEB'
    
    # Create directories where pipeline results are stored
    #
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/7M')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/TM2')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/TM1')
    #
    my_pipelineDirectory7M = my_individualPath + '/' + str(my_source) + '/pipeline/7M'
    my_pipelineDirectoryTM2 = my_individualPath + '/' + str(my_source) + '/pipeline/TM2'
    my_pipelineDirectoryTM1 = my_individualPath + '/' + str(my_source) + '/pipeline/TM1'
    
    # Create directories where images are stored
    #
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/7M')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/TM2')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/TM1')
    #
    my_imagesDirectory7M = my_individualPath + '/' + str(my_source) + '/images/7M'
    my_imagesDirectoryTM2 = my_individualPath + '/' + str(my_source) + '/images/TM2'
    my_imagesDirectoryTM1 = my_individualPath + '/' + str(my_source) + '/images/TM1'
    
    # Create directories where joint-deconvolved images are stored
    #
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/7MTM2')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/7MTM2TM1')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/combined/TM2TM1')
    #
    my_imagesDirectory7MTM2 = my_individualPath + '/' + str(my_source) + '/images/combined/7MTM2'
    my_imagesDirectory7MTM2TM1 = my_individualPath + '/' + str(my_source) + '/images/combined/7MTM2TM1'
    my_imagesDirectoryTM2TM1 = my_individualPath + '/' + str(my_source) + '/images/combined/TM2TM1'
    #
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/contsub')
    my_imagesDirectorylikeALL = my_individualPath + '/' + str(my_source) + '/contsub'
    
    # Create directories where self-calirated products are stored
    #
    os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated')
    os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/7M')
    os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/7M/perEB')
    os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM2')
    os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM2/perEB')
    os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM1')
    os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM1/perEB')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/selfcalibrated')
    #
    my_selfcalibratedDirectory = my_individualPath + '/' + str(my_source) + '/images/selfcalibrated'
    
    return my_calibratedDirectory7M, my_calibratedDirectoryTM2, my_calibratedDirectoryTM1, my_pipelineDirectory7M, my_pipelineDirectoryTM2, my_pipelineDirectoryTM1, my_imagesDirectory7M, my_imagesDirectoryTM2, my_imagesDirectoryTM1, my_imagesDirectory7MTM2, my_imagesDirectory7MTM2TM1, my_imagesDirectoryTM2TM1, my_selfcalibratedDirectory


def my_functionPrepareScriptsForJointDeconvolution(i, my_source, my_array, checkSelfCal):
    
    """
    Function to prepare the scripts necessary to joint deconvolve the
    data of the selected source combining the selected arrays
    
    Input:
      i : ID number of the source
      my_source : source name
      my_array : arrays to be combined (e.g., 7MTM2, 7MTM2TM1)
    
    """
    
    #-----------------------------------------------------------------------
    # Define file that will contain the final EXECUTABLE commands
    #
    my_executeFile = 'my_executeJointDeconvolution.sh'
    
    #-----------------------------------------------------------------------
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    my_individualPath =  my_mainPath + '/2019.1.00195.L/sources'
    my_individualStoragePath =  my_storagePath + '/2019.1.00195.L/sources'
    
    #-----------------------------------------------------------------------
    # Define directory variables for calibrated, pipeline and images data
    #
    my_directoryPaths = my_functionCreateDirectoryStructure(my_source)
    
    my_calibratedDirectory7M = my_directoryPaths[0]
    my_calibratedDirectoryTM2 = my_directoryPaths[1]
    my_calibratedDirectoryTM1 = my_directoryPaths[2]
    my_pipelineDirectory7M = my_directoryPaths[3]
    my_pipelineDirectoryTM2 = my_directoryPaths[4]
    my_pipelineDirectoryTM1 = my_directoryPaths[5]
    my_imagesDirectory7M = my_directoryPaths[6]
    my_imagesDirectoryTM2 = my_directoryPaths[7]
    my_imagesDirectoryTM1 = my_directoryPaths[8]
    my_imagesDirectory7MTM2 = my_directoryPaths[9]
    my_imagesDirectory7MTM2TM1 = my_directoryPaths[10]
    my_imagesDirectoryTM2TM1 = my_directoryPaths[11]
    my_imagesDirectoryTM1 = my_directoryPaths[11][:-6]+'TM1'
    os.system('mkdir -p ' + my_imagesDirectoryTM1)
    my_imagesDirectoryTM2 = my_directoryPaths[11][:-6]+'TM2'
    os.system('mkdir -p ' + my_imagesDirectoryTM2)
    my_imagesDirectory7M = my_directoryPaths[11][:-6]+'7M'
    os.system('mkdir -p ' + my_imagesDirectory7M)
    
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/contsub')
    my_imagesDirectorylikeALL = my_individualPath + '/' + str(my_source) + '/contsub'
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/contsub/7M')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/contsub/7M/perEB')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/contsub/TM2')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/contsub/TM2/perEB')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/contsub/TM1')
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/contsub/TM1/perEB')
    my_imagesDirectorylikeALL = my_individualPath + '/' + str(my_source) + '/contsub'
    
    #-----------------------------------------------------------------------
    # Define arrays that will be combined
    #
    if (my_array == "7MTM2"):
        
        my_add7M = True
        my_addTM2 = True
        my_addTM1 = False
        
        # Define the combination directory based on which data you want to combine
        #
        my_combinedDirectoryJoint = my_imagesDirectory7MTM2
        
        # Processing steps
        #
        my_totalSteps = 187 #50
        
        # Checking if data are available
        #
        my_combinationIsPossible = False
        if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/7M/pipeline-weblog.tar') == True) and (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM2/pipeline-weblog.tar') == True):
            
            my_combinationIsPossible = True
    
    elif (my_array == "TM2TM1"):
        
        my_add7M = False
        my_addTM2 = True
        my_addTM1 = True
        
        # Define the combination directory based on which data you want to combine
        #
        my_combinedDirectoryJoint = my_imagesDirectoryTM2TM1
        
        # Processing steps
        #
        my_totalSteps = 1 #50
        
        # Checking if data are available
        #
        my_combinationIsPossible = False
        if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM2/pipeline-weblog.tar') == True) and (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM1/pipeline-weblog.tar') == True):
            
            my_combinationIsPossible = True
    
    elif (my_array == "7MTM2TM1"):
        
        my_add7M = True
        my_addTM2 = True
        my_addTM1 = True
        
        # Define the combination directory based on which data you want to combine
        #
        my_combinedDirectoryJoint = my_imagesDirectory7MTM2TM1
        
        # Processing steps
        #
        my_totalSteps = 187
        
        # Checking if data are available
        #
        my_combinationIsPossible = False
        if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/7M/pipeline-weblog.tar') == True) and (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM2/pipeline-weblog.tar') == True) and (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM1/pipeline-weblog.tar') == True):
            
            my_combinationIsPossible = True
    
    elif (my_array == "7M"):
        
        my_add7M = True
        my_addTM2 = False
        my_addTM1 = False
        
        # Define the combination directory based on which data you want to combine
        #
        my_combinedDirectoryJoint = my_imagesDirectory7M
        
        # Processing steps
        #
        my_totalSteps = 187
        
        # Checking if data are available
        #
        my_combinationIsPossible = False
        if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/7M/pipeline-weblog.tar') == True):
            
            my_combinationIsPossible = True
    
    elif (my_array == "TM2"):
        
        my_add7M = False
        my_addTM2 = True
        my_addTM1 = False
        
        # Define the combination directory based on which data you want to combine
        #
        my_combinedDirectoryJoint = my_imagesDirectoryTM2
        
        # Processing steps
        #
        my_totalSteps = 187
        
        # Checking if data are available
        #
        my_combinationIsPossible = False
        if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM2/pipeline-weblog.tar') == True):
            
            my_combinationIsPossible = True
    
    elif (my_array == "TM1"):
        
        my_add7M = False
        my_addTM2 = False
        my_addTM1 = True
        
        # Define the combination directory based on which data you want to combine
        #
        my_combinedDirectoryJoint = my_imagesDirectoryTM1
        
        # Processing steps
        #
        my_totalSteps = 1
        
        # Checking if data are available
        #
        my_combinationIsPossible = False
        if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM1/pipeline-weblog.tar') == True):
            
            my_combinationIsPossible = True
    
    elif (my_array == "likeALL"):
        
        my_add7M = True
        my_addTM2 = True
        my_addTM1 = True
        
        # Define the combination directory based on which data you want to combine
        #
        my_combinedDirectoryJoint = my_imagesDirectorylikeALL
        
        # Processing steps
        #
        my_totalSteps = 1
        
        # Checking if data are available
        #
        my_combinationIsPossible = False
        if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/7M/pipeline-weblog.tar') == True) and (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM2/pipeline-weblog.tar') == True) and (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM1/pipeline-weblog.tar') == True):
            
            my_combinationIsPossible = True
    
    else:
        
        print("::: ALMAGAL command ::: ERROR! Possible arrays are 7MTM2, TM2TM1, 7MTM2TM1, 7M, TM2 and TM1")
    
    #-----------------------------------------------------------------------
    # Transfer pipeline weblog (and continuum masks) from storage location to main data location
    #
    # For 7M data
    #
    if (my_mainPath != my_storagePath) and (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == False) and (my_add7M == True):
        
        if my_combinationIsPossible == True:
            
            print("... transfer 7M weblog from storage location")
            os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/7M/pipeline-weblog.tar ' + my_pipelineDirectory7M + '/.')
            
            print("... transfer 7M continuum mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/7M/almagal.tar -C ' + my_pipelineDirectory7M + '/. almagal/*.cont.*mask')
            
            print("... transfer 7M spw0 mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/7M/almagal.tar -C ' + my_pipelineDirectory7M + '/. almagal/*.spw0.cube.*mask')
            
            print("... transfer 7M spw1 mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/7M/almagal.tar -C ' + my_pipelineDirectory7M + '/. almagal/*.spw1.cube.*mask')
            
            print("... transfer 7M spw2 mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/7M/almagal.tar -C ' + my_pipelineDirectory7M + '/. almagal/*.spw2.cube.*mask')
            
            print("... transfer 7M spw3 mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/7M/almagal.tar -C ' + my_pipelineDirectory7M + '/. almagal/*.spw3.cube.*mask')
    
    # For TM2 data
    #
    if (my_mainPath != my_storagePath) and (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == False) and (my_addTM2 == True):
        
        if my_combinationIsPossible == True:
            
            print("... transfer TM2 weblog from storage location")
            os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM2/pipeline-weblog.tar ' + my_pipelineDirectoryTM2 + '/.')
            
            print("... transfer TM2 continuum mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM2/almagal.tar -C ' + my_pipelineDirectoryTM2 + '/. almagal/*.cont.*mask')
            
            print("... transfer TM2 spw0 mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM2/almagal.tar -C ' + my_pipelineDirectoryTM2 + '/. almagal/*.spw0.cube.*mask')
            
            print("... transfer TM2 spw1 mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM2/almagal.tar -C ' + my_pipelineDirectoryTM2 + '/. almagal/*.spw1.cube.*mask')
            
            print("... transfer TM2 spw2 mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM2/almagal.tar -C ' + my_pipelineDirectoryTM2 + '/. almagal/*.spw2.cube.*mask')
            
            print("... transfer TM2 spw3 mask from storage location")
            os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM2/almagal.tar -C ' + my_pipelineDirectoryTM2 + '/. almagal/*.spw3.cube.*mask')
    
    # For TM1 data
    #
    if (my_mainPath != my_storagePath) and (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == False) and (my_addTM1 == True):
        
        if my_combinationIsPossible == True:
            
            print("... transfer TM1 weblog from storage location")
            os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM1/pipeline-weblog.tar ' + my_pipelineDirectoryTM1 + '/.')
    
    
    #-----------------------------------------------------------------------
    # Transfer calibrated visibilities from storage location to main data location
    #
    my_sourceSBPaths7M, my_sourceSBDirs7M, my_sourceSBFiles7M = next(os.walk(my_calibratedDirectory7M))
    my_sourceSBPathsTM2, my_sourceSBDirsTM2, my_sourceSBFilesTM2 = next(os.walk(my_calibratedDirectoryTM2))
    my_sourceSBPathsTM1, my_sourceSBDirsTM1, my_sourceSBFilesTM1 = next(os.walk(my_calibratedDirectoryTM1))
    
    # For 7M data
    #
    if (my_mainPath != my_storagePath) and (len(my_sourceSBFiles7M) < 1) and (my_add7M == True):
        
        if my_combinationIsPossible == True:
            
            # Check if there are self-calibrated visibilities
            my_sourceSelfCalibratedSBPaths7M, my_sourceSelfCalibratedSBDirs7M, my_sourceSelfCalibratedSBFiles7M = next(os.walk(my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/7M/perEB'))
            if len(my_sourceSelfCalibratedSBFiles7M) >= 1 and checkSelfCal == 1.0:
                print("... transfer 7M self-calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/7M/perEB/*.tar ' + my_calibratedDirectory7M + '/.')
            else:
                print("... transfer 7M calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/7M/perEB/*.tar ' + my_calibratedDirectory7M + '/.')
    
    # For TM2 data
    #
    if (my_mainPath != my_storagePath) and (len(my_sourceSBFilesTM2) < 1) and (my_addTM2 == True):
        
        if my_combinationIsPossible == True:
            
            # Check if there are self-calibrated visibilities
            my_sourceSelfCalibratedSBPathsTM2, my_sourceSelfCalibratedSBDirsTM2, my_sourceSelfCalibratedSBFilesTM2 = next(os.walk(my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM2/perEB'))
            if len(my_sourceSelfCalibratedSBFilesTM2) >= 1 and checkSelfCal == 1.0:
                print("... transfer TM2 self-calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM2/perEB/*.tar ' + my_calibratedDirectoryTM2 + '/.')
            else:
                print("... transfer TM2 calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/TM2/perEB/*.tar ' + my_calibratedDirectoryTM2 + '/.')
    
    # For TM1 data
    #
    if (my_mainPath != my_storagePath) and (len(my_sourceSBFilesTM1) < 1) and (my_addTM1 == True):
        
        if my_combinationIsPossible == True:
            
            # Check if there are self-calibrated visibilities
            my_sourceSelfCalibratedSBPathsTM1, my_sourceSelfCalibratedSBDirsTM1, my_sourceSelfCalibratedSBFilesTM1 = next(os.walk(my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM1/perEB'))
            if len(my_sourceSelfCalibratedSBFilesTM1) >= 1 and checkSelfCal == 1.0:
                print("... transfer TM1 self-calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM1/perEB/*.tar ' + my_calibratedDirectoryTM1 + '/.')
            else:
                print("... transfer TM1 calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/TM1/perEB/*.tar ' + my_calibratedDirectoryTM1 + '/.')
    
    #-----------------------------------------------------------------------
    # Evaluate if there are calibrated files produced for the selected source that permit to do joint-deconvolution
    #
    if (my_array == "7MTM2"):
        
        if (len(my_sourceSBFiles7M) >= 1) and (len(my_sourceSBFilesTM2) >= 1) and (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == True) and (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == True):
            
            my_dataAvailableForJointDeconvolution = True
            
            # It was intended to have the same spectral range and channesl for all combined cubes
            # but we are storing the likeALL.contsub.mstrans files.
            # It may be good to try to cover as much frequency range as possible, in case there are
            # interesting lines that may be cutted at the edges of some arrays/observations
            ## If available, use the channelsForEachSPW files used for 7MTM2TM1 data processing
            ##
            #if os.path.isfile(my_individualStoragePath + '/' + str(my_source) + '/images/combined/7MTM2TM1/combined-auxiliary.tar') == True:
            #    print("... using channelsForEachSPW files from 7MTM2TM1 data processing")
            #    my_runningTMP = os.getcwd()
            #    os.chdir(my_mainPath+'/2019.1.00195.L/sources/'+str(my_source)+'/images/combined/'+str(my_array))
            #    os.system('tar -xf ' + my_individualStoragePath + '/' + str(my_source) + '/images/combined/7MTM2TM1/combined-auxiliary.tar -C . almagal/channelsForEachSPW*')
            #    os.chdir(my_runningTMP)
            
        else:
            
            my_dataAvailableForJointDeconvolution = False
            
            if len(my_sourceSBFiles7M) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the 7M array")
            
            elif (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == False):
                print("... 7M not pipeline processed")
            
            if len(my_sourceSBFilesTM2) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM2 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == False):
                print("... TM2 not pipeline processed")
    
    elif (my_array == "TM2TM1"):
        
        if (len(my_sourceSBFilesTM2) >= 1) and (len(my_sourceSBFilesTM1) >= 1) and (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == True) and (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == True):
            
            my_dataAvailableForJointDeconvolution = True
            
        else:
            
            my_dataAvailableForJointDeconvolution = False
            
            if len(my_sourceSBFilesTM2) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM2 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == False):
                print("... TM2 not pipeline processed")
            
            if len(my_sourceSBFilesTM1) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM1 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == False):
                print("... TM1 not pipeline processed")
    
    elif (my_array == "7MTM2TM1"):
        
        if (len(my_sourceSBFiles7M) >= 1) and (len(my_sourceSBFilesTM2) >= 1) and (len(my_sourceSBFilesTM1) >= 1) and (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == True) and (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == True) and (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == True):
            
            my_dataAvailableForJointDeconvolution = True
            
        else:
            
            my_dataAvailableForJointDeconvolution = False
            
            if (len(my_sourceSBFiles7M) == 0):
                print("... " + "No data yet for source " + str(my_source) + " with the 7M array")
            
            elif (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == False):
                print("... 7M not pipeline processed")
            
            if len(my_sourceSBFilesTM2) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM2 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == False):
                print("... TM2 not pipeline processed")
            
            if len(my_sourceSBFilesTM1) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM1 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == False):
                print("... TM1 not pipeline processed")
    
    elif (my_array == "7M"):
        
        if (len(my_sourceSBFiles7M) >= 1) and (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == True):
            
            my_dataAvailableForJointDeconvolution = True
            
        else:
            
            my_dataAvailableForJointDeconvolution = False
            
            if len(my_sourceSBFiles7M) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the 7M array")
            
            elif (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == False):
                print("... 7M not pipeline processed")
    
    elif (my_array == "TM2"):
        
        if (len(my_sourceSBFilesTM2) >= 1) and (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == True):
            
            my_dataAvailableForJointDeconvolution = True
            
        else:
            
            my_dataAvailableForJointDeconvolution = False
            
            if len(my_sourceSBFilesTM2) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM2 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == False):
                print("... TM2 not pipeline processed")
    
    elif (my_array == "TM1"):
        
        if (len(my_sourceSBFilesTM1) >= 1) and (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == True):
            
            my_dataAvailableForJointDeconvolution = True
            
        else:
            
            my_dataAvailableForJointDeconvolution = False
            
            if len(my_sourceSBFilesTM1) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM1 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == False):
                print("... TM1 not pipeline processed")

    elif (my_array == "likeALL"):
        
        if (len(my_sourceSBFiles7M) >= 1) and (len(my_sourceSBFilesTM2) >= 1) and (len(my_sourceSBFilesTM1) >= 1) and (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == True) and (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == True) and (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == True):
            
            my_dataAvailableForJointDeconvolution = True
            
        else:
            
            my_dataAvailableForJointDeconvolution = False
            
            if (len(my_sourceSBFiles7M) == 0):
                print("... " + "No data yet for source " + str(my_source) + " with the 7M array")
            
            elif (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == False):
                print("... 7M not pipeline processed")
            
            if len(my_sourceSBFilesTM2) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM2 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == False):
                print("... TM2 not pipeline processed")
            
            if len(my_sourceSBFilesTM1) == 0:
                print("... " + "No data yet for source " + str(my_source) + " with the TM1 array")
            
            elif (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == False):
                print("... TM1 not pipeline processed")
    
    #-----------------------------------------------------------------------
    # If data have been pipeline-processed and are ready for joint deconvolution
    #
    if my_dataAvailableForJointDeconvolution == True:
        
        if (os.path.isfile(my_combinedDirectoryJoint + '/finished_all.txt') == False) and (os.path.isfile(my_combinedDirectoryJoint + '/inQueue.txt') == False) and (os.path.isfile(my_combinedDirectoryJoint + '/active.txt') == False):
            
            for my_step in range(0, my_totalSteps):
                
                if (os.path.isfile(my_combinedDirectoryJoint + '/finished_step' + str(my_step) + '.txt') == False):
                    
                    print("... joint deconvolution of " + str(my_array) + ", step " + str(my_step) + " has to be applied")
                    
                    #
                    # Create temporary file to indicate the running step
                    #
                    if (str(my_array) != 'likeALL'):
                        os.system("touch " +  my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/images/combined/" + str(my_array) + "/running_step" + str(my_step) + ".txt")
                    else:
                        os.system("touch " +  my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/contsub/running_step" + str(my_step) + ".txt")
                    
                    #
                    # Modify the script that will be executed
                    #
                    os.system("rm -rf scriptForJointDeconvolution"+str(my_array)+"_"+str(i)+"_"+str(my_array)+".py")
                    os.system("cp -rp scriptForJointDeconvolution"+str(my_array)+".py tmp_scriptForJointDeconvolution"+str(my_array)+".py")
                    fin = open("tmp_scriptForJointDeconvolution"+str(my_array)+".py", "rt")
                    data = fin.read()
                    data = data.replace("ToModifySOURCE", str(my_source))
                    data = data.replace("ToModifyTELESCOPE", str(my_array))
                    data = data.replace("ToModifySTEPS", "["+str(my_step)+"]")
                    data = data.replace("ToModifyCURRENTSTEP", "step"+str(my_step))
                    data = data.replace("ToModifyMAINPATH", str(my_mainPath))
                    data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                    data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                    fin.close()
                    fin = open("tmp_scriptForJointDeconvolution"+str(my_array)+".py", "wt")
                    fin.write(data)
                    fin.close()
                    os.system("mv tmp_scriptForJointDeconvolution"+str(my_array)+".py scriptForJointDeconvolution"+str(my_array)+"_"+str(i)+"_"+str(my_array)+".py")
                    
                    #
                    # Modify the mainScriptForJointDeconvolutionARRAY.sh file
                    #
                    os.system("rm -rf mainScriptForJointDeconvolution"+str(my_array)+"_" + str(i) + "_" + str(my_array) + ".sh")
                    os.system("cp -rp mainScriptForJointDeconvolution"+str(my_array)+".sh tmp_mainScriptForJointDeconvolution"+str(my_array)+".sh")
                    fin = open("tmp_mainScriptForJointDeconvolution"+str(my_array)+".sh", "rt")
                    data = fin.read()
                    data = data.replace("ToModifyRCDIR", "myRCDIR_"+str(i)+"_"+str(my_array))
                    data = data.replace("ToModifySCRIPT", "scriptForJointDeconvolution"+str(my_array)+"_"+str(i)+"_"+str(my_array))
                    data = data.replace("ToModifySOURCE", str(my_source))
                    data = data.replace("ToModifyTELESCOPE", str(my_array))
                    data = data.replace("ToModifyCURRENTSTEP", "step"+str(my_step))
                    data = data.replace("ToModifyMAINPATH", str(my_mainPath))
                    data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                    data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                    data = data.replace("ToModifyRUNNINGCOMPUTER", str(my_workstation))
                    fin.close()
                    fin = open("tmp_mainScriptForJointDeconvolution"+str(my_array)+".sh", "wt")
                    fin.write(data)
                    fin.close()
                    os.system("mv tmp_mainScriptForJointDeconvolution"+str(my_array)+".sh mainScriptForJointDeconvolution"+str(my_array)+"_" + str(i) + "_" + str(my_array) + ".sh")
                    os.system("chmod a+x mainScriptForJointDeconvolution"+str(my_array)+"_" + str(i) + "_" + str(my_array) + ".sh")
                    
                    #
                    # Modify the run batch script
                    #
                    ##if (my_step == 6) or (my_step == 7) or (my_step == 12) or (my_step == 13) or (my_step == 18) or (my_step == 19) or (my_step == 24) or (my_step == 25):
                    #if (my_step == 12) or (my_step == 24) or (my_step == 36) or (my_step == 48):
                    #    my_time = '04:00:00'
                    #    my_memory = 'mem192'
                    #else:
                    #    my_time = '14:00:00'
                    #    my_memory = 'batch'
                    #if (my_step == 13) or (my_step == 25) or (my_step == 37) or (my_step == 49):
                    #    my_time = '16:00:00'
                    #    my_memory = 'mem192'
                    my_time = '01:30:00'
                    my_memory = 'batch'
                    if (my_step == 33) or (my_step == 34) or (my_step == 35) or (my_step == 36) or (my_step == 37) or (my_step == 38) or (my_step == 39):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 40):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 41) or (my_step == 42) or (my_step == 43) or (my_step == 44) or (my_step == 45) or (my_step == 46) or (my_step == 47) or (my_step == 48):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 79) or (my_step == 80) or (my_step == 81) or (my_step == 82) or (my_step == 83) or (my_step == 84) or (my_step == 85):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 86):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 87) or (my_step == 88) or (my_step == 89) or (my_step == 90) or (my_step == 91) or (my_step == 92) or (my_step == 93) or (my_step == 94):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 125) or (my_step == 126) or (my_step == 127) or (my_step == 128) or (my_step == 129) or (my_step == 130) or (my_step == 131):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 132):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 133) or (my_step == 134) or (my_step == 135) or (my_step == 136) or (my_step == 137) or (my_step == 138) or (my_step == 139) or (my_step == 140):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 171) or (my_step == 172) or (my_step == 173) or (my_step == 174) or (my_step == 175) or (my_step == 176) or (my_step == 177):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 178):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    if (my_step == 179) or (my_step == 180) or (my_step == 181) or (my_step == 182) or (my_step == 183) or (my_step == 184) or (my_step == 185) or (my_step == 186):
                        my_time = '01:30:00'
                        my_memory = 'batch'
                    #if (my_step == 13) or (my_step == 25) or (my_step == 37) or (my_step == 49):
                    #    my_time = '16:00:00'
                    #    my_memory = 'mem192'
                    os.system("rm -rf run_mainScriptForJointDeconvolution"+str(my_array)+"_" + str(i) + "_" + str(my_array))
                    os.system("cp -rp run_mainScriptForJointDeconvolution"+str(my_array)+" tmp_run_mainScriptForJointDeconvolution"+str(my_array))
                    fin = open("tmp_run_mainScriptForJointDeconvolution"+str(my_array), "rt")
                    data = fin.read()
                    data = data.replace("ToModifyTIME", str(my_time))
                    data = data.replace("ToModifyMEMORY", str(my_memory))
                    data = data.replace("mainScriptForJointDeconvolution"+str(my_array), "mainScriptForJointDeconvolution"+str(my_array)+"_"+str(i)+"_"+str(my_array))
                    fin.close()
                    fin = open("tmp_run_mainScriptForJointDeconvolution"+str(my_array), "wt")
                    fin.write(data)
                    fin.close()
                    os.system("mv tmp_run_mainScriptForJointDeconvolution"+str(my_array)+" run_mainScriptForJointDeconvolution"+str(my_array)+"_" + str(i) + "_" + str(my_array))
                    os.system("chmod a+x run_mainScriptForJointDeconvolution"+str(my_array)+"_" + str(i) + "_" + str(my_array))
                    
                    #
                    # Modify the default-init.py file
                    #
                    os.system("cp -rp default-init.py tmp_default-init.py")
                    fin = open("tmp_default-init.py", "rt")
                    data = fin.read()
                    data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                    data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                    fin.close()
                    fin = open("tmp_default-init.py", "wt")
                    fin.write(data)
                    fin.close()
                    
                    os.system('mkdir -p ' + my_runningPath + '/.myRCDIR_' + str(i) + '_' + str(my_array) + '.mycasa')
                    os.system('cp -rp ' + my_mainPath + '/mpi-runs/tmp_default-init.py ' + my_runningPath + '/.myRCDIR_' + str(i) + '_' + str(my_array) + '.mycasa/init.py')
                    
                    #
                    # Append executable command to main execution file
                    with open(my_executeFile, 'a') as fd:
                        if (str(my_array) != "likeALL"):
                            fd.write("touch  " + my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/images/combined/" + str(my_array) + "/inQueue.txt\n")
                        else:
                            fd.write("touch  " + my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/contsub/inQueue.txt\n")
                        if (my_workstation == "JSC"):
                            fd.write("sbatch run_mainScriptForJointDeconvolution"+str(my_array)+"_"+str(i)+"_"+str(my_array)+"\n")
                        else:
                            fd.write("./mainScriptForJointDeconvolution"+str(my_array)+"_"+str(i)+"_"+str(my_array)+".sh\n")
                    #
                    # Make the run bash script executable
                    os.system("chmod a+x " + my_executeFile)
                    
                    #
                    # Create temporary file to indicate that it is in the queue
                    #os.system("touch " +  my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/pipeline/" + str(my_array) + "/inQueue.txt")
                    
                    break
                
                else:
                    
                    print("... joint deconvolution of " + str(my_array) + ", step " + str(my_step) + " already processed")
                    
        else:
            
            if (os.path.isfile(my_combinedDirectoryJoint + '/finished_all.txt') == True):
                print("... " + my_array + " already joint deconvolved")
            
            if (os.path.isfile(my_combinedDirectoryJoint + '/active.txt') == True):
                print("... " + my_array + " currently active")
            
            if (os.path.isfile(my_combinedDirectoryJoint + '/inQueue.txt') == True):
                print("... " + my_array + " in the queue")


def my_functionPrepareScriptsForSelfCalibration(i, my_source):
    
    """
    Function to prepare the scripts necessary to self-calibrate the
    data of the selected source and array
    
    Input:
      i : ID number of the source
      my_source : source name
    
    """
    
    #-----------------------------------------------------------------------
    # Define file that will contain the final EXECUTABLE commands
    #
    my_executeFile = 'my_executeSelfCalibration.sh'
    
    #-----------------------------------------------------------------------
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    my_individualPath =  my_mainPath + '/2019.1.00195.L/sources'
    my_individualStoragePath =  my_storagePath + '/2019.1.00195.L/sources'
    
    #-----------------------------------------------------------------------
    # Define directory variables for calibrated, pipeline and images data
    #
    my_directoryPaths = my_functionCreateDirectoryStructure(my_source)
    
    my_calibratedDirectory7M = my_directoryPaths[0]
    my_calibratedDirectoryTM2 = my_directoryPaths[1]
    my_calibratedDirectoryTM1 = my_directoryPaths[2]
    my_pipelineDirectory7M = my_directoryPaths[3]
    my_pipelineDirectoryTM2 = my_directoryPaths[4]
    my_pipelineDirectoryTM1 = my_directoryPaths[5]
    my_imagesDirectory7M = my_directoryPaths[6]
    my_imagesDirectoryTM2 = my_directoryPaths[7]
    my_imagesDirectoryTM1 = my_directoryPaths[8]
    my_imagesDirectory7MTM2 = my_directoryPaths[9]
    my_imagesDirectory7MTM2TM1 = my_directoryPaths[10]
    my_imagesDirectoryTM2TM1 = my_directoryPaths[11]
    my_selfcalibratedDirectory = my_directoryPaths[12]
    
    if (os.path.isfile(my_selfcalibratedDirectory + '/transferred.txt') == False):
        #-----------------------------------------------------------------------
        # Define arrays that will be self-calibrated
        #
        my_array = '7M'
        if (my_array == "7M"):
            
            my_add7M = True
            my_addTM2 = False
            my_addTM1 = False
            
            # Define the self-calibration directory based on which data you want to self-calibrate
            #
            #my_selfcalibratedDirectory = my_selfcalibratedDirectory7M
            
            # Processing steps
            #
            my_totalSteps = 3
            
            # Checking if data are available
            #
            my_selfcalibrationIsPossible = False
            if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/7M/pipeline-weblog.tar') == True):
                
                my_selfcalibrationIsPossible = True
        
        my_array = 'TM2'
        if (my_array == "TM2"):
            
            my_add7M = False
            my_addTM2 = True
            my_addTM1 = False
            
            # Define the self-calibration directory based on which data you want to self-calibrate
            #
            #my_selfcalibratedDirectory = my_selfcalibratedDirectoryTM2
            
            # Processing steps
            #
            my_totalSteps = 3
            
            # Checking if data are available
            #
            my_selfcalibrationIsPossible = False
            if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM2/pipeline-weblog.tar') == True):
                
                my_selfcalibrationIsPossible = True
        
        my_array = 'TM1'
        if (my_array == "TM1"):
            
            my_add7M = False
            my_addTM2 = False
            my_addTM1 = True
            
            # Define the self-calibration directory based on which data you want to self-calibrate
            #
            #my_selfcalibratedDirectory = my_selfcalibratedDirectoryTM1
            
            # Processing steps
            #
            my_totalSteps = 3
            
            # Checking if data are available
            #
            my_selfcalibrationIsPossible = False
            if (os.path.isfile(my_storagePath + '/2019.1.00195.L/sources/' + str(my_source) + '/pipeline/TM1/pipeline-weblog.tar') == True):
                
                my_selfcalibrationIsPossible = True
        
        else:
            
            print("::: ALMAGAL command ::: ERROR! Possible arrays are 7M and TM2 and TM1")
        
        #-----------------------------------------------------------------------
        # Transfer pipeline weblog (and continuum masks) from storage location to main data location
        #
        # For 7M data
        #
        if (my_mainPath != my_storagePath) and (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == False) and (my_add7M == True):
            
            if my_selfcalibrationIsPossible == True:
                
                print("... transfer 7M weblog from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/7M/pipeline-weblog.tar ' + my_pipelineDirectory7M + '/.')
        
        # For TM2 data
        #
        if (my_mainPath != my_storagePath) and (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == False) and (my_addTM2 == True):
            
            if my_selfcalibrationIsPossible == True:
                
                print("... transfer TM2 weblog from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM2/pipeline-weblog.tar ' + my_pipelineDirectoryTM2 + '/.')
        
        # For TM1 data
        #
        if (my_mainPath != my_storagePath) and (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == False) and (my_addTM1 == True):
            
            if my_selfcalibrationIsPossible == True:
                
                print("... transfer TM1 weblog from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/TM1/pipeline-weblog.tar ' + my_pipelineDirectoryTM1 + '/.')
        
        
        #-----------------------------------------------------------------------
        # Transfer calibrated visibilities from storage location to main data location
        #
        my_sourceSBPaths7M, my_sourceSBDirs7M, my_sourceSBFiles7M = next(os.walk(my_calibratedDirectory7M))
        my_sourceSBPathsTM2, my_sourceSBDirsTM2, my_sourceSBFilesTM2 = next(os.walk(my_calibratedDirectoryTM2))
        my_sourceSBPathsTM1, my_sourceSBDirsTM1, my_sourceSBFilesTM1 = next(os.walk(my_calibratedDirectoryTM1))
        
        # For 7M data
        #
        if (my_mainPath != my_storagePath) and (len(my_sourceSBFiles7M) < 1) and (my_add7M == True):
            
            if my_selfcalibrationIsPossible == True:
                
                print("... transfer 7M calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/7M/perEB/*.tar ' + my_calibratedDirectory7M + '/.')
        
        # For TM2 data
        #
        if (my_mainPath != my_storagePath) and (len(my_sourceSBFilesTM2) < 1) and (my_addTM2 == True):
            
            if my_selfcalibrationIsPossible == True:
                
                print("... transfer TM2 calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/TM2/perEB/*.tar ' + my_calibratedDirectoryTM2 + '/.')
        
        # For TM1 data
        #
        if (my_mainPath != my_storagePath) and (len(my_sourceSBFilesTM1) < 1) and (my_addTM1 == True):
            
            if my_selfcalibrationIsPossible == True:
                
                print("... transfer TM1 calibrated visibilities from storage location")
                os.system('cp -rp ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/TM1/perEB/*.tar ' + my_calibratedDirectoryTM1 + '/.')
        
        #-----------------------------------------------------------------------
        # Evaluate if there are calibrated files produced for the selected source that permit to do self-calibration
        #
        my_array = '7M'
        if (my_array == "7M"):
            
            if (len(my_sourceSBFiles7M) >= 1) and (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == True):
                
                my_dataAvailableForSelfCalibration = True
                
            else:
                
                my_dataAvailableForSelfCalibration = False
                
                if len(my_sourceSBFiles7M) == 0:
                    print("... " + "No data yet for source " + str(my_source) + " with the 7M array")
                
                elif (os.path.isfile(my_pipelineDirectory7M + '/pipeline-weblog.tar') == False):
                    print("... 7M not pipeline processed")
        
        my_array = 'TM2'
        if (my_array == "TM2"):
            
            if (len(my_sourceSBFilesTM2) >= 1) and (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == True):
                
                my_dataAvailableForSelfCalibration = True
                
            else:
                
                my_dataAvailableForSelfCalibration = False
                
                if len(my_sourceSBFilesTM2) == 0:
                    print("... " + "No data yet for source " + str(my_source) + " with the TM2 array")
                
                elif (os.path.isfile(my_pipelineDirectoryTM2 + '/pipeline-weblog.tar') == False):
                    print("... TM2 not pipeline processed")
        
        my_array = 'TM1'
        if (my_array == "TM1"):
            
            if (len(my_sourceSBFilesTM1) >= 1) and (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == True):
                
                my_dataAvailableForSelfCalibration = True
                
            else:
                
                my_dataAvailableForSelfCalibration = False
                
                if len(my_sourceSBFilesTM1) == 0:
                    print("... " + "No data yet for source " + str(my_source) + " with the TM1 array")
                
                elif (os.path.isfile(my_pipelineDirectoryTM1 + '/pipeline-weblog.tar') == False):
                    print("... TM1 not pipeline processed")
        
        #-----------------------------------------------------------------------
        # If data have been pipeline-processed and are ready for self-calibration
        #
        if my_dataAvailableForSelfCalibration == True:
            
            if (os.path.isfile(my_selfcalibratedDirectory + '/transferred.txt') == False) and (os.path.isfile(my_selfcalibratedDirectory + '/finished_all.txt') == False) and (os.path.isfile(my_selfcalibratedDirectory + '/inQueue.txt') == False) and (os.path.isfile(my_selfcalibratedDirectory + '/active.txt') == False):
                
                for my_step in range(0, my_totalSteps):
                    
                    if (os.path.isfile(my_selfcalibratedDirectory + '/finished_step' + str(my_step) + '.txt') == False):
                        
                        print("... self-calibration, step " + str(my_step) + " has to be applied")
                        
                        #
                        # Create temporary file to indicate the running step
                        #
                        os.system("touch " +  my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/images/selfcalibrated/running_step" + str(my_step) + ".txt")
                        
                        #
                        # Modify the script that will be executed
                        #
                        os.system("cp -rp scriptForSelfCalibration.py tmp_scriptForSelfCalibration.py")
                        fin = open("tmp_scriptForSelfCalibration.py", "rt")
                        data = fin.read()
                        data = data.replace("ToModifySOURCE", str(my_source))
                        data = data.replace("ToModifyTELESCOPE", str(my_array))
                        data = data.replace("ToModifySTEPS", "["+str(my_step)+"]")
                        data = data.replace("ToModifyCURRENTSTEP", "step"+str(my_step))
                        data = data.replace("ToModifyMAINPATH", str(my_mainPath))
                        data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                        data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                        fin.close()
                        fin = open("tmp_scriptForSelfCalibration.py", "wt")
                        fin.write(data)
                        fin.close()
                        os.system("mv tmp_scriptForSelfCalibration.py scriptForSelfCalibration_"+str(i)+".py")
                        
                        #
                        # Modify the mainScriptForSelfCalibrationARRAY.sh file
                        #
                        os.system("cp -rp mainScriptForSelfCalibration.sh tmp_mainScriptForSelfCalibration.sh")
                        fin = open("tmp_mainScriptForSelfCalibration.sh", "rt")
                        data = fin.read()
                        data = data.replace("ToModifyRCDIR", "myRCDIR_"+str(i)+"_"+str(my_array))
                        data = data.replace("ToModifySCRIPT", "scriptForSelfCalibration_"+str(i))
                        data = data.replace("ToModifySOURCE", str(my_source))
                        data = data.replace("ToModifyTELESCOPE", str(my_array))
                        data = data.replace("ToModifyCURRENTSTEP", "step"+str(my_step))
                        data = data.replace("ToModifyMAINPATH", str(my_mainPath))
                        data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                        data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                        data = data.replace("ToModifyRUNNINGCOMPUTER", str(my_workstation))
                        fin.close()
                        fin = open("tmp_mainScriptForSelfCalibration.sh", "wt")
                        fin.write(data)
                        fin.close()
                        os.system("mv tmp_mainScriptForSelfCalibration.sh mainScriptForSelfCalibration_" + str(i) + ".sh")
                        os.system("chmod a+x mainScriptForSelfCalibration_" + str(i) + ".sh")
                        
                        #
                        # Modify the run batch script
                        #
                        my_time = '03:00:00'
                        my_memory = 'batch'
                        if (my_step == 5):
                            my_time = '03:00:00'
                            my_memory = 'mem192'
                        os.system("cp -rp run_mainScriptForSelfCalibration tmp_run_mainScriptForSelfCalibration")
                        fin = open("tmp_run_mainScriptForSelfCalibration", "rt")
                        data = fin.read()
                        data = data.replace("ToModifyTIME", str(my_time))
                        data = data.replace("ToModifyMEMORY", str(my_memory))
                        data = data.replace("mainScriptForSelfCalibration", "mainScriptForSelfCalibration_"+str(i))
                        fin.close()
                        fin = open("tmp_run_mainScriptForSelfCalibration", "wt")
                        fin.write(data)
                        fin.close()
                        os.system("mv tmp_run_mainScriptForSelfCalibration run_mainScriptForSelfCalibration_" + str(i))
                        os.system("chmod a+x run_mainScriptForSelfCalibration_" + str(i))
                        
                        #
                        # Modify the default-init.py file
                        #
                        os.system("cp -rp default-init.py tmp_default-init.py")
                        fin = open("tmp_default-init.py", "rt")
                        data = fin.read()
                        data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                        data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                        fin.close()
                        fin = open("tmp_default-init.py", "wt")
                        fin.write(data)
                        fin.close()
                        
                        os.system('mkdir -p ' + my_runningPath + '/.myRCDIR_' + str(i) + '_' + str(my_array) + '.mycasa')
                        os.system('cp -rp ' + my_mainPath + '/mpi-runs/tmp_default-init.py ' + my_runningPath + '/.myRCDIR_' + str(i) + '_' + str(my_array) + '.mycasa/init.py')
                        
                        #
                        # Append executable command to main execution file
                        with open(my_executeFile, 'a') as fd:
                            fd.write("touch  " + my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/images/selfcalibrated/inQueue.txt\n")
                            if (my_workstation == "JSC"):
                                fd.write("sbatch run_mainScriptForSelfCalibration_"+str(i)+"\n")
                            else:
                                fd.write("./mainScriptForSelfCalibration_"+str(i)+".sh\n")
                        #
                        # Make the run bash script executable
                        os.system("chmod a+x " + my_executeFile)
                        
                        #
                        # Create temporary file to indicate that it is in the queue
                        #os.system("touch " +  my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/pipeline/" + str(my_array) + "/inQueue.txt")
                        
                        break
                    
                    else:
                        
                        print("... self-calibration, step " + str(my_step) + " already processed")
                        
            else:
                
                if (os.path.isfile(my_selfcalibratedDirectory + '/finished_all.txt') == True) or (os.path.isfile(my_selfcalibratedDirectory + '/transferred.txt') == True):
                    print("... " + my_array + " already joint self-calibrated")
                
                if (os.path.isfile(my_selfcalibratedDirectory + '/active.txt') == True):
                    print("... " + my_array + " currently active")
                
                if (os.path.isfile(my_selfcalibratedDirectory + '/inQueue.txt') == True):
                    print("... " + my_array + " in the queue")
    else:
        
        print("... already joint self-calibrated and transferred")


def my_functionFactorizableInteger(n):
    
    """
    Function to determine if a given value is factorizable by the
    integers 2, 3, 5 and 7. This is useful to determine the value
    that has to be used for the variable 'imsize' of tclean
    
    Input variables:
      n : integer value
    
    Output
      my_functionFactorizableIntegerValid : True / False 
    """
    
    if (n%2 == 0) and (n%3 == 0) and (n%5 == 0) and (n%7 == 0):
        my_functionFactorizableIntegerValid = True
    
    else:
        my_functionFactorizableIntegerValid = False
    
    return my_functionFactorizableIntegerValid


def my_functionFindBestFactorizableInteger(value):
    
    """
    Function to find the best higher integer that is factorizable
    according to the function my_functionFactorizableInteger and 
    that can be used as 'imsize' variable in the tclean CASA function
    
    Input variables:
      value : integer value
    
    Output
      my_functionFindBestFactorizableIntegerValid : integer value to be used as imsize
    """
    
    for i in range(value, 5000):
        if my_functionFactorizableInteger(i):
            my_functionFindBestFactorizableIntegerValid = i
            break
    
    return my_functionFindBestFactorizableIntegerValid


'''


def getFreqRangesContinuum(my_visFiles7M, my_visFilesTM2, my_visFilesTM1, my_contFile7M, my_contFileTM2, my_contFileTM1, my_sourceName):
    """
    Function to get the frequency ranges for continuum imaging
    after converting from LSRK frame to TOPO frame
    
    Input variables: 
      my_visFiles7M : list of measurement sets for 7M array
      my_visFilesTM2 : list of measurement sets for TM2 array
      my_visFilesTM1 : list of measurement sets for TM1 array
      my_contFile7M : cont.dat file with LSRK frame frequency ranges for 7M array
      my_contFileTM2 : cont.dat file with LSRK frame frequency ranges for TM2 array
      my_contFileTM1 : cont.dat file with LSRK frame frequency ranges for TM1 array
      my_sourceName : name of the source to be processed
    
    Output
      my_TotalFreqRangesContinuum : list with frequency ranges to use
    """
    
    # Initialize list to contain all frequency ranges
    my_TotalFreqRangesContinuum = []
    
    # Loop through all the measurement sets of array 7M
    for my_visFile in my_visFiles7M:
        
        # For spectral window 0
        my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile7M, 0, field=my_sourceName)
        my_FreqRangesContinuum = my_TOPOranges[my_visFile]
        
        # For spectral window 1
        my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile7M, 1, field=my_sourceName)
        my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
        
        # Append results for both spectral windows in final list
        my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)
    
    # Loop through all the measurement sets of array TM2
    for my_visFile in my_visFilesTM2:
        
        # For spectral window 0
        my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM2, 0, field=my_sourceName)
        my_FreqRangesContinuum = my_TOPOranges[my_visFile]
        
        # For spectral window 1
        my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM2, 1, field=my_sourceName)
        my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
        
        # Append results for both spectral windows in final list
        my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)
    
    # Loop through all the measurement sets of array TM1
    for my_visFile in my_visFilesTM1:
        
        # For spectral window 0
        my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM1, 0, field=my_sourceName)
        my_FreqRangesContinuum = my_TOPOranges[my_visFile]
        
        # For spectral window 1
        my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM1, 1, field=my_sourceName)
        my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
        
        # Append results for both spectral windows in final list
        my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)
    
    # Return final frequency ranges to use for continuum imaging
    return my_TotalFreqRangesContinuum

'''

def getFreqRangesContinuum(my_viscontFiles, my_array, my_sourceName):
    
    """
    Function to get the frequency ranges for continuum imaging
    after converting from LSRK frame to TOPO frame
    
    Input variables: 
      my_viscontFiles : list containing the list of visibility files and continuum ranges
                        if 7MTM2:
                          my_visFiles7M = my_viscontFiles[0]
                          my_visFilesTM2 = my_viscontFiles[1]
                          my_contFile7M = my_viscontFiles[2]
                          my_contFileTM2 = my_viscontFiles[3]
                        if 7MTM2TM1:
                          my_visFiles7M = my_viscontFiles[0]
                          my_visFilesTM2 = my_viscontFiles[1]
                          my_visFilesTM1 = my_viscontFiles[2]
                          my_contFile7M = my_viscontFiles[3]
                          my_contFileTM2 = my_viscontFiles[4]
                          my_contFileTM1 = my_viscontFiles[5]
                        if TM2TM1:
                          my_visFilesTM2 = my_viscontFiles[0]
                          my_visFilesTM1 = my_viscontFiles[1]
                          my_contFileTM2 = my_viscontFiles[2]
                          my_contFileTM1 = my_viscontFiles[3]
      my_array : arrays to be combined (e.g., 7MTM2, 7MTM2TM1)
      my_sourceName : name of the source to be processed
    
    Output
      my_TotalFreqRangesContinuum : list with frequency ranges to use
    """
    
    import analysisUtils as au
    import analysisUtils as aU
    
    # Initialize some variables
    #
    my_visFiles7M = []
    my_visFilesTM2 = []
    my_visFilesTM1 = []
    
    if (my_array == "7MTM2"):
        
        my_visFiles7M = my_viscontFiles[0]
        my_visFilesTM2 = my_viscontFiles[1]
        my_contFile7M = my_viscontFiles[2]
        my_contFileTM2 = my_viscontFiles[3]
    
    elif (my_array == "7MTM2TM1"):
        
        my_visFiles7M = my_viscontFiles[0]
        my_visFilesTM2 = my_viscontFiles[1]
        my_visFilesTM1 = my_viscontFiles[2]
        my_contFile7M = my_viscontFiles[3]
        my_contFileTM2 = my_viscontFiles[4]
        my_contFileTM1 = my_viscontFiles[5]
    
    elif (my_array == "TM2TM1"):
        
        my_visFilesTM2 = my_viscontFiles[0]
        my_visFilesTM1 = my_viscontFiles[1]
        my_contFileTM2 = my_viscontFiles[2]
        my_contFileTM1 = my_viscontFiles[3]
    
    elif (my_array == "TM1"):
        
        my_visFilesTM1 = my_viscontFiles[0]
        my_contFileTM1 = my_viscontFiles[1]
    
    elif (my_array == "TM2"):
        
        my_visFilesTM2 = my_viscontFiles[0]
        my_contFileTM2 = my_viscontFiles[1]
    
    elif (my_array == "7M"):
        
        my_visFiles7M = my_viscontFiles[0]
        my_contFile7M = my_viscontFiles[1]
    
    # Initialize list to contain all frequency ranges
    #
    my_TotalFreqRangesContinuum = []
    
    # Loop through all the measurement sets of array 7M
    #
    if (len(my_visFiles7M) != 0):
        
        for my_visFile in my_visFiles7M:
            
            # For spectral window 0
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile7M, 0, field=my_sourceName)
            my_FreqRangesContinuum = my_TOPOranges[my_visFile]
            
            # For spectral window 1
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile7M, 1, field=my_sourceName)
            my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
            
            # Append results for both spectral windows in final list
            #
            my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)
    
    # Loop through all the measurement sets of array TM2
    #
    if (len(my_visFilesTM2) != 0):
        
        for my_visFile in my_visFilesTM2:
            
            # For spectral window 0
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM2, 0, field=my_sourceName)
            my_FreqRangesContinuum = my_TOPOranges[my_visFile]
            
            # For spectral window 1
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM2, 1, field=my_sourceName)
            my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
            
            # Append results for both spectral windows in final list
            #
            my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)
    
    # Loop through all the measurement sets of array TM1
    #
    if (len(my_visFilesTM1) != 0):
        
        for my_visFile in my_visFilesTM1:
            
            # For spectral window 0
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM1, 0, field=my_sourceName)
            my_FreqRangesContinuum = my_TOPOranges[my_visFile]
            
            # For spectral window 1
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM1, 1, field=my_sourceName)
            my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
            
            # Append results for both spectral windows in final list
            #
            my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)

    # Return final frequency ranges to use for continuum imaging
    #
    return my_TotalFreqRangesContinuum


def getFreqRangesContinuumSelfCalibration(my_viscontFiles, my_array, my_sourceName):
    
    """
    Function to get the frequency ranges for continuum imaging
    after converting from LSRK frame to TOPO frame
    
    Input variables: 
      my_viscontFiles : list containing the list of visibility files and continuum ranges
                        if 7M:
                          my_visFiles7M = my_viscontFiles[0]
                          my_contFile7M = my_viscontFiles[1]
                        if TM2:
                          my_visFilesTM2 = my_viscontFiles[0]
                          my_contFileTM2 = my_viscontFiles[1]
                        if TM1:
                          my_visFilesTM1 = my_viscontFiles[0]
                          my_contFileTM1 = my_viscontFiles[1]
      my_array : arrays to be self-calibrated (e.g., 7M, TM2, TM1)
      my_sourceName : name of the source to be processed
    
    Output
      my_TotalFreqRangesContinuum : list with frequency ranges to use
    """
    
    import analysisUtils as au
    import analysisUtils as aU
    
    # Initialize some variables
    #
    my_visFiles7M = []
    my_visFilesTM2 = []
    my_visFilesTM1 = []
    
    if (my_array == "7M"):
        
        my_visFiles7M = my_viscontFiles[0]
        my_contFile7M = my_viscontFiles[1]
    
    elif (my_array == "TM2"):
        
        my_visFilesTM2 = my_viscontFiles[0]
        my_contFileTM2 = my_viscontFiles[1]
    
    elif (my_array == "TM1"):
        
        my_visFilesTM1 = my_viscontFiles[0]
        my_contFileTM1 = my_viscontFiles[1]
    
    # Initialize list to contain all frequency ranges
    #
    my_TotalFreqRangesContinuum = []
    
    # Loop through all the measurement sets of array 7M
    #
    if (len(my_visFiles7M) != 0):
        
        for my_visFile in my_visFiles7M:
            
            # For spectral window 0
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile7M, 0, field=my_sourceName)
            my_FreqRangesContinuum = my_TOPOranges[my_visFile]
            
            # For spectral window 1
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile7M, 1, field=my_sourceName)
            my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
            
            # Append results for both spectral windows in final list
            #
            my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)
    
    # Loop through all the measurement sets of array TM2
    #
    if (len(my_visFilesTM2) != 0):
        
        for my_visFile in my_visFilesTM2:
            
            # For spectral window 0
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM2, 0, field=my_sourceName)
            my_FreqRangesContinuum = my_TOPOranges[my_visFile]
            
            # For spectral window 1
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM2, 1, field=my_sourceName)
            my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
            
            # Append results for both spectral windows in final list
            #
            my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)
    
    # Loop through all the measurement sets of array TM1
    #
    if (len(my_visFilesTM1) != 0):
        
        for my_visFile in my_visFilesTM1:
            
            # For spectral window 0
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM1, 0, field=my_sourceName)
            my_FreqRangesContinuum = my_TOPOranges[my_visFile]
            
            # For spectral window 1
            #
            my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFileTM1, 1, field=my_sourceName)
            my_FreqRangesContinuum +=  ','+my_TOPOranges[my_visFile]
            
            # Append results for both spectral windows in final list
            #
            my_TotalFreqRangesContinuum.append(my_FreqRangesContinuum)

    # Return final frequency ranges to use for continuum imaging
    #
    return my_TotalFreqRangesContinuum



def getSPWRanges(my_visFile, my_contFile, my_sourceName):
    
    """
    Function to get the frequency ranges of the continuum ranges
    after converting from LSRK frame to TOPO frame
    
    Input variables: 
      my_visFiles : measurement set to be processed
      my_contFile : cont.dat file with LSRK frame frequency ranges
      my_sourceName : name of the source to be processed
    
    Output
      my_TotalSPWRanges : list with frequency ranges to use
    """
    import analysisUtils as au
    import analysisUtils as aU
    
    # Initialize list to contain all frequency ranges
    #
    my_TotalSPWRanges = []
    
    # For spectral window 0
    #
    my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile, 0, field=my_sourceName)
    my_SPWRange = my_TOPOranges[my_visFile]
    
    # For spectral window 1
    #
    my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile, 1, field=my_sourceName)
    my_SPWRange +=  ','+my_TOPOranges[my_visFile]
    
    # For spectral window 2
    #
    my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile, 2, field=my_sourceName)
    my_SPWRange +=  ','+my_TOPOranges[my_visFile]
    
    # For spectral window 3
    #
    my_TOPOranges = aU.LSRKRangesToTopo(my_visFile, my_contFile, 3, field=my_sourceName)
    my_SPWRange +=  ','+my_TOPOranges[my_visFile]
    
    # Append results for both spectral windows in final list
    #
    my_TotalSPWRanges.append(my_SPWRange)

    # Return final frequency ranges
    #
    return my_TotalSPWRanges


def separateNumbersUnits(my_string):
    
    """
    Function to separate the number and the units from a string
    
    Input variables: 
      my_string : string to be processed
    
    Output
      my_number : number (value) of the string
      my_unit   : unit of the string
    """
    
    # Alternative approach: it has problems with scientific notation
    # e.g., 9.55e-05Jy splits at the position of 'e'
    #import re
    #
    #res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', my_string.strip())
    #res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    #
    #my_number = float(res_f[0])
    #my_unit = res_f[1]
    
    # Approach usable only for units mJy and Jy !!
    #
    if "m" in my_string:
        element_l = my_string.split('m')
        element_l[1] = 'm'+element_l[1]
    else:
        element_l = my_string.split('J')
        element_l[1] = 'J'+element_l[1]
    my_number = float(element_l[0])
    my_unit = element_l[1]
    
    return my_number, my_unit


def my_multiBeamAnalyzer(my_fileName, my_trimImage):
    
    """
    Function to determine the median of the beams (when multi-beam)
    and identify channels that may have beams much larger
    than the median value
    
    Input variables:
      my_fileName : name of the image to be investigated
      my_trimImage : set to 1 to remove channels with large beams
    
    Output:
      if my_trimImage is set to 1, the old image is replaced
      by the new one with no channels with large beams
    """
    
    # Read the header of the image
    #
    my_headerSummary = imhead(my_fileName, mode='summary', verbose=True)
    
    # Check if there are multiple beams in the image
    #
    if 'perplanebeams' in my_headerSummary:
        print("The image contains multiple beams")
        
        my_nChannels = my_headerSummary['perplanebeams']['nChannels']
        
        my_beamInHeader0 = my_headerSummary['perplanebeams']['beams']['*0']['*0']
        my_bmaj0 = my_beamInHeader0['major']['value']
        my_bmin0 = my_beamInHeader0['minor']['value']
        my_bmaj = np.array(my_bmaj0)
        my_bmin = np.array(my_bmin0)
        
        for i in range(my_nChannels):
            my_currentChannel = '*%d' % i
            my_beamInHeader1 = my_headerSummary['perplanebeams']['beams'][my_currentChannel]['*0']
            my_bmaj1 = my_beamInHeader1['major']['value']
            my_bmin1 = my_beamInHeader1['minor']['value']
            my_bmaj = np.append(my_bmaj, my_bmaj1)
            my_bmin = np.append(my_bmin, my_bmin1)
        
        print("The median beam is bmaj = " + str(np.median(my_bmaj)) + " and bmin = " + str(np.median(my_bmin)) + " in arcsec")
        
        # Determine the channels that have correct beams
        #
        my_firstChannel = 0
        my_lastChannel = my_nChannels-1
        my_badChannels = 0
        for i in range(my_nChannels):
            my_currentChannel = '*%d' % i
            my_beamInHeader1 = my_headerSummary['perplanebeams']['beams'][my_currentChannel]['*0']
            my_bmaj1 = my_beamInHeader1['major']['value']
            my_bmin1 = my_beamInHeader1['minor']['value']
            
            if (my_bmaj1 > 2.*np.median(my_bmaj)):
                my_badChannels = 1
                print("Large beam! " + str(my_bmaj1) + " for channel " + str(i))
                if i < 500:
                    my_firstChannel = max(my_firstChannel, i)
                if i > 3000:
                    my_lastChannel = min(my_lastChannel, i)
        
        # Create new image removing the channels with large beams:
        #
        if my_badChannels == 1 and my_trimImage == 1:
            print("Creating new image removing channels with large beams")
            my_goodChannels = str(my_firstChannel+1)+"~"+str(my_lastChannel)
            print("Selected channels are " + my_goodChannels)
            
            imsubimage(imagename = my_fileName,
                outfile = my_fileName + '.trimmed',
                chans = my_goodChannels,
                dropdeg = False)
            
            os.system('rm -rf ' + my_fileName)
            os.system('mv ' + my_fileName + '.trimmed ' + my_fileName)
            
        elif my_badChannels == 1 and my_trimImage != 1:
            
            print("No new image is created, but there are channels with large beams!")
            
    else:
        
        print("The image does NOT has multiple beams")

'''
def my_functionGetTcleanParametersJointDeconbolutionCube(function_telescope, function_spw):
    
    """
    Function to get the tclean imaging parameters for joint
    deconvolution combining several arrays. The function reads previous
    casa log files to extract the necessary information and calculates
    the new tclean parameters that are necessary
    
    Input variables:
      function_telescope : indicate the arrays to be combined (e.g., 7MTM2)
      function_spw : indicate the spectral window to be processed
    
    Output (in this order)
      my_imsize
      my_cell
      my_niter
      my_threshold
      my_pbmask
      my_pblimit
      my_weighting
      my_robust
      my_sidelobethreshold
      my_noisethreshold
      my_minbeamfrac
      my_lownoisethreshold
      my_negativethreshold
      my_scales
      my_outputImage
      my_visfilestoclean
    """
    
    if (function_telescope == "7MTM2"):
        
        # Define MS file names
        #
        my_visPath7M = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + '/' + my_source + '/calibrated/7M/perEB'
        my_visFiles7M = sorted(glob.glob(my_visPath7M+'/*.mstrans'))
        #
        my_visPathTM2 = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + '/' + my_source + '/calibrated/TM2/perEB'
        my_visFilesTM2 = sorted(glob.glob(my_visPathTM2+'/*.mstrans'))
        
        # Get maximum recoverable scale (MRS)
        #
        my_bmin = aU.getBaselineLengths(my_visFiles7M[0])[0][1]
        my_MRS = (0.6*((299792458.0/218.9625e9)/my_bmin))*(180.0/np.pi)*3600.0 #--- hard coded max recoverable scale in arcsec. Really should check that 15.1m is min baseline for all TM2 data.
        
        # Get line free channels for continuum imaging
        #
        # For telescope array 7M
        #
        my_pipelinePath7M = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/pipeline/7M'
        my_sourcePipelinePaths, my_sourcePipelineDirs, my_sourcePipelineFiles = next(os.walk(my_pipelinePath7M))
        my_pipelineDirectory = my_sourcePipelineDirs[0]
        my_lineFreeChannels7M = my_pipelinePath7M + '/' + my_sourcePipelineFiles[0]
        #
        # For telescope array TM2
        #
        my_pipelinePathTM2 = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/pipeline/TM2'
        my_sourcePipelinePaths, my_sourcePipelineDirs, my_sourcePipelineFiles = next(os.walk(my_pipelinePathTM2))
        my_pipelineDirectory = my_sourcePipelineDirs[0]
        my_lineFreeChannelsTM2 = my_pipelinePathTM2 + '/' + my_sourcePipelineFiles[0]
        #
        vislist7M = sorted(glob.glob(my_visPath7M+'/*.mstrans'))
        contfile7M = my_lineFreeChannels7M
        vislistTM2 = sorted(glob.glob(my_visPathTM2+'/*.mstrans'))
        contfileTM2 = my_lineFreeChannelsTM2
        my_sourceName = str(my_source)
        
        # Get tclean parameters based on 7M pipeline imaging
        #
        # Inspect tclean for 7M
        #
        my_pipelinePath7M = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/pipeline/7M'
        my_sourcePipelinePaths, my_sourcePipelineDirs, my_sourcePipelineFiles = next(os.walk(my_pipelinePath7M))
        my_pipelineDirectory = my_sourcePipelineDirs[0]
        # 
        # If REFIND continuum was necessary
        if os.path.isfile(my_pipelinePath7M + '/' + my_pipelineDirectory + '/html/stage13/casapy.log'):
            my_casaLog7M = my_pipelinePath7M + '/' + my_pipelineDirectory + '/html/stage13/casapy.log'
        # If only original continuum is available
        elif os.path.isfile(my_pipelinePath7M + '/' + my_pipelineDirectory + '/html/stage7/casapy.log'):
            my_casaLog7M = my_pipelinePath7M + '/' + my_pipelineDirectory + '/html/stage7/casapy.log'
        # No file found - possible error
        else:
            print("::: ALMAGAL ::: No casapy.log file found!")
        #
        my_imsizeCasaLog7M = aU.extractTcleanCommands(my_casaLog7M, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'imsize',
                                                    task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
        my_cellCasaLog7M = aU.extractTcleanCommands(my_casaLog7M, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'cell',
                                                    task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
        
        # Get tclean parameters based on TM2 pipeline imaging
        #
        # Inspect tclean for TM2
        #
        my_pipelinePathTM2 = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/pipeline/TM2'
        my_sourcePipelinePaths, my_sourcePipelineDirs, my_sourcePipelineFiles = next(os.walk(my_pipelinePathTM2))
        my_pipelineDirectory = my_sourcePipelineDirs[0]
        # 
        # If REFIND continuum was necessary
        if os.path.isfile(my_pipelinePathTM2 + '/' + my_pipelineDirectory + '/html/stage19/casapy.log'):
            my_casaLogTM2 = my_pipelinePathTM2 + '/' + my_pipelineDirectory + '/html/stage19/casapy.log'
        # If only original continuum is available
        elif os.path.isfile(my_pipelinePathTM2 + '/' + my_pipelineDirectory + '/html/stage7/casapy.log'):
            my_casaLogTM2 = my_pipelinePathTM2 + '/' + my_pipelineDirectory + '/html/stage7/casapy.log'
        # No file found - possible error
        else:
            print("::: ALMAGAL ::: No casapy.log file found!")
        #
        my_imsizeCasaLogTM2 = aU.extractTcleanCommands(my_casaLogTM2, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'imsize',
                                                    task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
        my_cellCasaLogTM2 = aU.extractTcleanCommands(my_casaLogTM2, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'cell',
                                                    task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
        # 
        # Define stages for each one of the four spectral windows (0, 1, 2, 3)
        my_TM2stagesRefind = ['stage21', 'stage23', 'stage25', 'stage27']
        my_TM2stagesOriginal = ['stage9', 'stage11', 'stage13', 'stage15']
        # 
        # If REFIND continuum was necessary
        if os.path.isfile(my_pipelinePathTM2 + '/' + my_pipelineDirectory + '/html/' + my_TM2stagesRefind[function_spw] + '/casapy.log'):
            my_casaLogTM2 = my_pipelinePathTM2 + '/' + my_pipelineDirectory + '/html/' + my_TM2stagesRefind[function_spw] + '/casapy.log'
        # If only original continuum is available
        elif os.path.isfile(my_pipelinePathTM2 + '/' + my_pipelineDirectory + '/html/' + my_TM2stagesOriginal[function_spw] + '/casapy.log'):
            my_casaLogTM2 = my_pipelinePathTM2 + '/' + my_pipelineDirectory + '/html/' + my_TM2stagesOriginal[function_spw] + '/casapy.log'
        # No file found - possible error
        else:
            print("::: ALMAGAL ::: No casapy.log file found!")
        #
        my_niterCasaLogTM2 = aU.extractTcleanCommands(my_casaLogTM2, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'niter',
                                                    task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
        my_thresholdCasaLogTM2 = aU.extractTcleanCommands(my_casaLogTM2, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'threshold',
                                                    task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
        
        # TCLEAN parameters to be used
        #
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLogTM2[len(my_imsizeCasaLogTM2)-1])))
        #my_imsize7MTM2tmp = 3*my_imsize7MTM2tmp
        my_imsize7MTM2 = my_functionFindBestFactorizableInteger(my_imsize7MTM2tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM2
        my_niterCasaLog = my_niterCasaLogTM2
        my_thresholdCasaLog = my_thresholdCasaLogTM2
        #
        my_imsize = [my_imsize7MTM2, my_imsize7MTM2]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        #
        my_sidelobethreshold = 3.0
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        # Scales after 18 are factors of the Maximum Recoverable Scale
        #
        my_useScales = [0, 6, 18, 0.9]
        my_useScalesARR = np.array(my_useScales)
        my_UseScalesARRtmp = np.copy(my_useScalesARR)
        my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_spw' + str(function_spw) + '_7MTM2_jointdeconv'
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFiles7M + my_visFilesTM2
        
        return my_imsize, my_cell, my_niter, my_threshold, my_pbmask, my_pblimit, my_weighting, my_robust, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_scales, my_outputImage, my_visfilestoclean
'''

def my_functionPrepareWeblogForJointDeconvolution(my_telescope, my_source):
    
    """
    help
    """
    
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Copy and prepare pipeline weblog files for selected source and arrray
    #
    os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/pipeline-weblog.tar " + str(my_runningPath) + "/almagal/processing/.")
    os.system("mkdir -p " + str(my_runningPath) + "/almagal/processing/2019.1.00195.L/sources/" + my_source + "/pipeline")
    os.system("mkdir -p " + str(my_runningPath) + "/almagal/processing/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope)
    os.system('tar -xf ' + str(my_runningPath) + '/almagal/processing/pipeline-weblog.tar -C ' + str(my_runningPath) + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/pipeline/' + my_telescope + '/.')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/pipeline-weblog.tar')
    if (my_telescope == "7M"):
        # Copy mask of continuum
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s13_0._'+str(my_source)+'__sci.spw0_1.cont.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s13*.cont.*mask " + str(my_runningPath) + "/almagal/processing/original_7M.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s7_0._'+str(my_source)+'__sci.spw0_1.cont.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s7*.cont.*mask " + str(my_runningPath) + "/almagal/processing/original_7M.mask")
        # Copy mask of spw0
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw0.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw0.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw0.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw0.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw0.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw0.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw0.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw0.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw0.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw0.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw0.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw0.mask")
        # Copy mask of spw1
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw1.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw1.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw1.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw1.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw1.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw1.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw1.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw1.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw1.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw1.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw1.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw1.mask")
        # Copy mask of spw2
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw2.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw2.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw2.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw2.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw2.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw2.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw2.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw2.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw2.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw2.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw2.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw2.mask")
        # Copy mask of spw3
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw3.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw3.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw3.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw3.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw3.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw3.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw3.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw3.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw3.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw3.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw3.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_7M_spw3.mask")
    if (my_telescope == "TM2"):
        # Copy mask of continuum
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s19_0._'+str(my_source)+'__sci.spw0_1.cont.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s19*.cont.*mask " + str(my_runningPath) + "/almagal/processing/original_TM2.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s7_0._'+str(my_source)+'__sci.spw0_1.cont.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s7*.cont.*mask " + str(my_runningPath) + "/almagal/processing/original_TM2.mask")
        # Copy mask of spw0
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s21_0._'+str(my_source)+'__sci.spw0.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s21*.spw0.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw0.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s21_0._'+str(my_source)+'__sci.spw0.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s21*.spw0.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw0.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw0.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw0.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw0.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s9_0._'+str(my_source)+'__sci.spw0.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s9*.spw0.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw0.mask")
        # Copy mask of spw1
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s23_0._'+str(my_source)+'__sci.spw1.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s23*.spw1.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw1.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s23_0._'+str(my_source)+'__sci.spw1.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s23*.spw1.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw1.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s11_0._'+str(my_source)+'__sci.spw1.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s11*.spw1.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw1.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s11_0._'+str(my_source)+'__sci.spw1.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s11*.spw1.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw1.mask")
        # Copy mask of spw2
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s25_0._'+str(my_source)+'__sci.spw2.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s25*.spw2.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw2.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s25_0._'+str(my_source)+'__sci.spw2.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s25*.spw2.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw2.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s13_0._'+str(my_source)+'__sci.spw2.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s13*.spw2.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw2.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s13_0._'+str(my_source)+'__sci.spw2.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s13*.spw2.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw2.mask")
        # Copy mask of spw3
        if os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s27_0._'+str(my_source)+'__sci.spw3.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s27*.spw3.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw3.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s27_0._'+str(my_source)+'__sci.spw3.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s27*.spw3.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw3.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw3.cube.I.iter1.reclean.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw3.cube.*reclean.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw3.mask")
        elif os.path.isdir(str(my_mainPath)+'/2019.1.00195.L/sources/'+str(my_source)+'/pipeline/'+my_telescope+'/almagal/oussid.s15_0._'+str(my_source)+'__sci.spw3.cube.I.iter1.mask'):
            os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/almagal/*s15*.spw3.cube.*.mask " + str(my_runningPath) + "/almagal/processing/original_TM2_spw3.mask")


def my_functionPrepareWeblogForSelfCalibration(my_telescope, my_source):
    
    """
    help
    """
    
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Copy and prepare pipeline weblog files for selected source and arrray
    #
    os.system("cp -rp " + str(my_mainPath) + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/pipeline-weblog.tar " + str(my_runningPath) + "/almagal/processing/.")
    os.system("mkdir -p " + str(my_runningPath) + "/almagal/processing/2019.1.00195.L/sources/" + my_source + "/pipeline")
    os.system("mkdir -p " + str(my_runningPath) + "/almagal/processing/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope)
    os.system('tar -xf ' + str(my_runningPath) + '/almagal/processing/pipeline-weblog.tar -C ' + str(my_runningPath) + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/pipeline/' + my_telescope + '/.')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/pipeline-weblog.tar')


def my_functionDefineMSFilesForJointDeconvolution(my_telescope, my_source):
    
    """
    help
    """
    
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Define MS file names for selected source and arrray
    #
    my_visPath = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + '/' + my_source + '/calibrated/' + my_telescope + '/perEB'
    my_visFiles = []
    for my_visFile in os.listdir(my_visPath):
        my_visFiles.append(my_visPath+'/'+my_visFile)
    
    return my_visPath, my_visFiles


def my_functionDefineMSFilesForSelfCalibration(my_telescope, my_source):
    
    """
    help
    """
    
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Define MS file names for selected source and arrray
    #
    my_visPath = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + '/' + my_source + '/calibrated/' + my_telescope + '/perEB'
    my_visFiles = []
    for my_visFile in os.listdir(my_visPath):
        my_visFiles.append(my_visPath+'/'+my_visFile)
    
    return my_visPath, my_visFiles


def my_functionGetLineFreeChannelsForJointDeconvolution(my_telescope, my_source):
    
    """
    help
    """
    
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Define MS file names for selected source and arrray
    #
    my_visPath, my_visFiles = my_functionDefineMSFilesForJointDeconvolution(str(my_telescope), str(my_source))
    
    # Get line free channels for continuum imaging
    #
    my_pipelinePath = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + '/' + my_source + '/pipeline/' + my_telescope
    my_sourcePipelinePaths, my_sourcePipelineDirs, my_sourcePipelineFiles = next(os.walk(my_pipelinePath))
    my_pipelineDirectory = my_sourcePipelineDirs[0]
    my_lineFreeChannels = my_pipelinePath + '/' + my_sourcePipelineFiles[0]
    vislist = sorted(glob.glob(my_visPath+'/*.cal'))
    contfile = my_lineFreeChannels
    
    return my_pipelinePath, my_pipelineDirectory, my_lineFreeChannels, vislist, contfile


def my_functionGetLineFreeChannelsForSelfCalibration(my_telescope, my_source):
    
    """
    help
    """
    
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Define MS file names for selected source and arrray
    #
    my_visPath, my_visFiles = my_functionDefineMSFilesForJointDeconvolution(str(my_telescope), str(my_source))
    
    # Get line free channels for continuum imaging
    #
    my_pipelinePath = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + '/' + my_source + '/pipeline/' + my_telescope
    my_sourcePipelinePaths, my_sourcePipelineDirs, my_sourcePipelineFiles = next(os.walk(my_pipelinePath))
    my_pipelineDirectory = my_sourcePipelineDirs[0]
    my_lineFreeChannels = my_pipelinePath + '/' + my_sourcePipelineFiles[0]
    vislist = sorted(glob.glob(my_visPath+'/*.cal'))
    contfile = my_lineFreeChannels
    
    return my_pipelinePath, my_pipelineDirectory, my_lineFreeChannels, vislist, contfile


def my_functionGetTcleanParametersFromPipeline(my_telescope, my_source):
    
    """
    help
    """
    
    import analysisUtils as au
    import analysisUtils as aU
    
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Get pipeline path and directory name
    #
    my_pipelinePath, my_pipelineDirectory, my_lineFreeChannels, vislist, contfile = my_functionGetLineFreeChannelsForJointDeconvolution(str(my_telescope), str(my_source))
    
    # Define stages to be used
    #
    if (my_telescope == "7M"):
        my_stageRefind = 'stage13'
        my_stageOriginal = 'stage7'
    if (my_telescope == "TM2"):
        my_stageRefind = 'stage19'
        my_stageOriginal = 'stage7'
    if (my_telescope == "TM1"):
        my_stageRefind = 'stage19'
        my_stageOriginal = 'stage7'

    # Inspect tclean parameters
    #
    # If REFIND continuum was necessary
    if os.path.isfile(my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stageRefind + '/casapy.log'):
        my_casaLog = my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stageRefind + '/casapy.log'
    # If only original continuum is available
    elif os.path.isfile(my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stageOriginal + '/casapy.log'):
        my_casaLog = my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stageOriginal + '/casapy.log'
    # No file found - possible error
    else:
        print("::: ALMAGAL ::: No casapy.log file found!")
    #
    my_imsizeCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'imsize',
                                                task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
    my_cellCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'cell',
                                                task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
    my_niterCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'niter',
                                                task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
    my_thresholdCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'threshold',
                                                task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
    
    return my_imsizeCasaLog, my_cellCasaLog, my_niterCasaLog, my_thresholdCasaLog


def my_functionGetTcleanParametersCubeFromPipeline(my_telescope, my_source, my_spw):
    
    """
    help
    """
    
    import analysisUtils as au
    import analysisUtils as aU
    
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Get pipeline path and directory name
    #
    my_pipelinePath, my_pipelineDirectory, my_lineFreeChannels, vislist, contfile = my_functionGetLineFreeChannelsForJointDeconvolution(str(my_telescope), str(my_source))
    
    # Inspect tclean parameters (for continuum: imsize and cellsize)
    #
    # Define stages to be used
    #
    if (my_telescope == "7M"):
        my_stageRefind = 'stage13'
        my_stageOriginal = 'stage7'
    if (my_telescope == "TM2"):
        my_stageRefind = 'stage19'
        my_stageOriginal = 'stage7'
    if (my_telescope == "TM1"):
        my_stageRefind = 'stage19'
        my_stageOriginal = 'stage7'
    #
    # If REFIND continuum was necessary
    if os.path.isfile(my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stageRefind + '/casapy.log'):
        my_casaLog = my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stageRefind + '/casapy.log'
    # If only original continuum is available
    elif os.path.isfile(my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stageOriginal + '/casapy.log'):
        my_casaLog = my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stageOriginal + '/casapy.log'
    # No file found - possible error
    else:
        print("::: ALMAGAL ::: No casapy.log file found!")
    #
    my_imsizeCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'imsize',
                                                task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
    my_cellCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'cell',
                                                task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
    
    # Inspect tclean parameters (for the cubes: niter and threshold)
    # 
    # Define stages for each one of the four spectral windows (0, 1, 2, 3)
    #
    if (my_telescope == "7M"):
        my_stagesRefind = ['stage15', 'stage15', 'stage15', 'stage15']
        my_stagesOriginal = ['stage9', 'stage9', 'stage9', 'stage9']
        #
        # If REFIND continuum was necessary
        if os.path.isfile(my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stagesRefind[my_spw] + '/casapy.log'):
            my_casaLog = my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stagesRefind[my_spw] + '/casapy.log'
        # If only original continuum is available
        elif os.path.isfile(my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stagesOriginal[my_spw] + '/casapy.log'):
            my_casaLog = my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stagesOriginal[my_spw] + '/casapy.log'
        # No file found - possible error
        else:
            print("::: ALMAGAL ::: No casapy.log file found!")
        #
        my_niterCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'niter',
                                                    task='tclean', stage=-1, dictionaries=False, spw=str(my_spw), output='', fieldname=None, includeCopyTree=False, vis='')
        my_thresholdCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'threshold',
                                                    task='tclean', stage=-1, dictionaries=False, spw=str(my_spw), output='', fieldname=None, includeCopyTree=False, vis='')
        
    if (my_telescope == "TM2") or (my_telescope == "TM1"):
        if (my_telescope == "TM2"):
            my_stagesRefind = ['stage21', 'stage23', 'stage25', 'stage27']
            my_stagesOriginal = ['stage9', 'stage11', 'stage13', 'stage15']
        if (my_telescope == "TM1"):
            my_stagesRefind = ['stage21', 'stage23', 'stage25', 'stage27']
            my_stagesOriginal = ['stage9', 'stage11', 'stage13', 'stage15']
        #
        # If REFIND continuum was necessary
        if os.path.isfile(my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stagesRefind[my_spw] + '/casapy.log'):
            my_casaLog = my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stagesRefind[my_spw] + '/casapy.log'
        # If only original continuum is available
        elif os.path.isfile(my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stagesOriginal[my_spw] + '/casapy.log'):
            my_casaLog = my_pipelinePath + '/' + my_pipelineDirectory + '/html/' + my_stagesOriginal[my_spw] + '/casapy.log'
        # No file found - possible error
        else:
            print("::: ALMAGAL ::: No casapy.log file found!")
        #
        my_niterCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'niter',
                                                    task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
        my_thresholdCasaLog = aU.extractTcleanCommands(my_casaLog, intent='OBSERVE_TARGET', verbose=True, extractParameter = 'threshold',
                                                    task='tclean', stage=-1, dictionaries=False, spw=None, output='', fieldname=None, includeCopyTree=False, vis='')
    
    return my_imsizeCasaLog, my_cellCasaLog, my_niterCasaLog, my_thresholdCasaLog


def my_functionParametersForJointDeconvolutionContinuum(my_telescope, my_source):
    
    """
    Help
    """
    
    import analysisUtils as au
    import analysisUtils as aU
    
    #-----------------------------------------------------------------------
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Create your running directory
    #
    os.system("mkdir -p " + str(my_runningPath) + "/almagal")
    os.system("mkdir -p " + str(my_runningPath) + "/almagal/processing")

    #-----------------------------------------------------------------------
    # Set up infrastructure for array combination
    #
    if (my_telescope == "7M"):
        my_add7M = True
        my_addTM2 = False
        my_addTM1 = False
    
    if (my_telescope == "TM2"):
        my_add7M = False
        my_addTM2 = True
        my_addTM1 = False
    
    if (my_telescope == "TM1"):
        my_add7M = False
        my_addTM2 = False
        my_addTM1 = True
        
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
    
    if my_add7M == True:
        
        # Check if there are self-calibrated visibilities
        #my_sourceSelfCalibratedSBPaths7M, my_sourceSelfCalibratedSBDirs7M, my_sourceSelfCalibratedSBFiles7M = next(os.walk(my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/7M/perEB'))
        #if len(my_sourceSelfCalibratedSBFiles7M) >= 1:
        #    print("... transfer 7M self-calibrated visibilities from storage location")
        #    os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/selfcalibrated/7M/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
        #else:
        #    print("... transfer 7M calibrated visibilities from storage location")
            os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/calibrated/7M/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
    
    if my_addTM2 == True:
        
        ## Check if there are self-calibrated visibilities
        #my_sourceSelfCalibratedSBPathsTM2, my_sourceSelfCalibratedSBDirsTM2, my_sourceSelfCalibratedSBFilesTM2 = next(os.walk(my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM2/perEB'))
        #if len(my_sourceSelfCalibratedSBFilesTM2) >= 1:
        #    print("... transfer TM2 self-calibrated visibilities from storage location")
        #    os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/selfcalibrated/TM2/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
        #else:
        #    print("... transfer TM2 calibrated visibilities from storage location")
            os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/calibrated/TM2/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
    
    if my_addTM1 == True:
        
        ## Check if there are self-calibrated visibilities
        #my_sourceSelfCalibratedSBPathsTM1, my_sourceSelfCalibratedSBDirsTM1, my_sourceSelfCalibratedSBFilesTM1 = next(os.walk(my_individualStoragePath + '/' + str(my_source) + '/selfcalibrated/TM1/perEB'))
        #if len(my_sourceSelfCalibratedSBFilesTM1) >= 1:
        #    print("... transfer TM1 self-calibrated visibilities from storage location")
        #    os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/selfcalibrated/TM1/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
        #else:
        #    print("... transfer TM1 calibrated visibilities from storage location")
            os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/calibrated/TM1/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
    
    # Evaluate files and directories copied in the processing directory
    #
    my_sourcePaths, my_sourceDirs, my_sourceFiles = next(os.walk(str(my_runningPath)+'/almagal/processing'))
    
    # Untar the visibility files
    #
    for my_sourceFile in my_sourceFiles:
        os.system('tar -xf ' + str(my_runningPath) + '/almagal/processing/' + str(my_sourceFile) + ' -C ' + str(my_runningPath) + '/almagal/processing/.')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/*.tar')
    
    #-----------------------------------------------------------------------
    # Prepare files for 7M
    #
    if my_add7M == True:
        
        # Copy weblogs and cont.dat files to the processing directory
        #
        my_functionPrepareWeblogForJointDeconvolution("7M", str(my_source))
        
        # Define MS file names
        #
        my_visPath7M, my_visFiles7M = my_functionDefineMSFilesForJointDeconvolution("7M", str(my_source))
        
        # Get line free channels for continuum imaging
        #
        my_pipelinePath7M, my_pipelineDirectory7M, my_lineFreeChannels7M, vislist7M, contfile7M = my_functionGetLineFreeChannelsForJointDeconvolution("7M", str(my_source))
    
    #-----------------------------------------------------------------------
    # Prepare files for TM2
    #
    if my_addTM2 == True:
        
        # Copy weblogs and cont.dat files to the processing directory
        #
        my_functionPrepareWeblogForJointDeconvolution("TM2", str(my_source))
        
        # Define MS file names
        #
        my_visPathTM2, my_visFilesTM2 = my_functionDefineMSFilesForJointDeconvolution("TM2", str(my_source))
        
        # Get line free channels for continuum imaging
        #
        my_pipelinePathTM2, my_pipelineDirectoryTM2, my_lineFreeChannelsTM2, vislistTM2, contfileTM2 = my_functionGetLineFreeChannelsForJointDeconvolution("TM2", str(my_source))
    
    #-----------------------------------------------------------------------
    # Prepare files for TM1
    #
    if my_addTM1 == True:
        
        # Copy weblogs and cont.dat files to the processing directory
        #
        my_functionPrepareWeblogForJointDeconvolution("TM1", str(my_source))
        
        # Define MS file names
        #
        my_visPathTM1, my_visFilesTM1 = my_functionDefineMSFilesForJointDeconvolution("TM1", str(my_source))
        
        # Get line free channels for continuum imaging
        #
        my_pipelinePathTM1, my_pipelineDirectoryTM1, my_lineFreeChannelsTM1, vislistTM1, contfileTM1 = my_functionGetLineFreeChannelsForJointDeconvolution("TM1", str(my_source))
    
    #-----------------------------------------------------------------------
    # Define the variable containing the line-free frequency range
    #
    if (my_telescope == "7M"):
        my_viscontFiles = [vislist7M, contfile7M]
        
    if (my_telescope == "TM2"):
        my_viscontFiles = [vislistTM2, contfileTM2]
        
    if (my_telescope == "TM1"):
        my_viscontFiles = [vislistTM1, contfileTM1]

    if (my_telescope == "7MTM2"):
        my_viscontFiles = [vislist7M, vislistTM2, contfile7M, contfileTM2]
        
    if (my_telescope == "TM2TM1"):
        my_viscontFiles = [vislistTM2, vislistTM1, contfileTM2, contfileTM1]
        
    if (my_telescope == "7MTM2TM1"):
        my_viscontFiles = [vislist7M, vislistTM2, vislistTM1, contfile7M, contfileTM2, contfileTM1]
    
    my_sourceName = str(my_source)
    my_freqs = getFreqRangesContinuum(my_viscontFiles, my_telescope, my_sourceName)
    
    #-----------------------------------------------------------------------
    # Get maximum recoverable scale (MRS)
    #
    if my_add7M == True:
        my_bmin = aU.getBaselineLengths(my_visFiles7M[0])[0][1]
        my_MRS = (0.6*((299792458.0/218.9625e9)/my_bmin))*(180.0/np.pi)*3600.0 #--- hard coded max recoverable scale in arcsec. Really should check that 15.1m is min baseline for all TM2 data.
    
    elif my_addTM2 == True:
        my_bmin = aU.getBaselineLengths(my_visFilesTM2[0])[0][1]
        my_MRS = (0.6*((299792458.0/218.9625e9)/my_bmin))*(180.0/np.pi)*3600.0 #--- hard coded max recoverable scale in arcsec. Really should check that 15.1m is min baseline for all TM2 data.
    
    elif my_addTM1 == True:
        my_bmin = aU.getBaselineLengths(my_visFilesTM1[0])[0][1]
        my_MRS = (0.6*((299792458.0/218.9625e9)/my_bmin))*(180.0/np.pi)*3600.0 #--- hard coded max recoverable scale in arcsec. Really should check that 15.1m is min baseline for all TM2 data.
    
    #-----------------------------------------------------------------------
    # Get tclean parameters based on 7M pipeline imaging
    #
    if my_add7M == True:
        
        # Inspect tclean for 7M
        #
        my_imsizeCasaLog7M, my_cellCasaLog7M, my_niterCasaLog7M, my_thresholdCasaLog7M = my_functionGetTcleanParametersFromPipeline("7M", str(my_source))
    
    #-----------------------------------------------------------------------
    # Get tclean parameters based on TM2 pipeline imaging
    #
    if my_addTM2 == True:
        
        # Inspect tclean for TM2
        #
        my_imsizeCasaLogTM2, my_cellCasaLogTM2, my_niterCasaLogTM2, my_thresholdCasaLogTM2 = my_functionGetTcleanParametersFromPipeline("TM2", str(my_source))
    
    #-----------------------------------------------------------------------
    # Get tclean parameters based on TM1 pipeline imaging
    #
    if my_addTM1 == True:
        
        # Inspect tclean for TM1
        #
        my_imsizeCasaLogTM1, my_cellCasaLogTM1, my_niterCasaLogTM1, my_thresholdCasaLogTM1 = my_functionGetTcleanParametersFromPipeline("TM1", str(my_source))
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7M
    #
    if my_telescope == "7M":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsize7Mtmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])))
        my_imsize7M = my_functionFindBestFactorizableInteger(my_imsize7Mtmp)
        my_cellCasaLog = my_cellCasaLog7M
        my_niterCasaLog = my_niterCasaLog7M
        my_thresholdCasaLog = my_thresholdCasaLog7M
        #
        my_imsize = [my_imsize7M, my_imsize7M]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        #
        my_sidelobethreshold = 1.25
        my_noisethreshold = 5.0
        my_minbeamfrac =  0.1
        my_lownoisethreshold = 2.0
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        #
        my_scales = [0, 30, 60]
        #my_useScales = [0, 30, 60, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'standard'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_cont_7M_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFiles7M
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for TM2
    #
    if my_telescope == "TM2":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsizeTM2tmp = int(round(int(my_imsizeCasaLogTM2[len(my_imsizeCasaLogTM2)-1])))
        my_imsizeTM2 = my_functionFindBestFactorizableInteger(my_imsizeTM2tmp)
        my_cellCasaLog = my_cellCasaLogTM2
        my_niterCasaLog = my_niterCasaLogTM2
        my_thresholdCasaLog = my_thresholdCasaLogTM2
        #
        my_imsize = [my_imsizeTM2, my_imsizeTM2]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        #
        my_sidelobethreshold = 2.0
        my_noisethreshold = 4.25
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        #
        my_scales = [0, 6, 18, 30]
        #my_useScales = [0, 6, 18, 30, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'standard'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_cont_TM2_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFilesTM2
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for TM1
    #
    if my_telescope == "TM1":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsizeTM1tmp = int(round(int(my_imsizeCasaLogTM1[len(my_imsizeCasaLogTM1)-1])))
        my_imsizeTM1 = my_functionFindBestFactorizableInteger(my_imsizeTM1tmp)
        my_cellCasaLog = my_cellCasaLogTM1
        my_niterCasaLog = my_niterCasaLogTM1
        my_thresholdCasaLog = my_thresholdCasaLogTM1
        #
        my_imsize = [my_imsizeTM1, my_imsizeTM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        #
        my_sidelobethreshold = 3.0
        my_noisethreshold = 5.0
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        #
        my_scales = [0, 6, 18, 30]
        #my_useScales = [0, 6, 18, 30, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'standard'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_cont_TM1_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFilesTM1
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7MTM2
    #
    if my_telescope == "7MTM2":
        
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLogTM2[len(my_imsizeCasaLogTM2)-1])))
        my_imsize7MTM2 = my_functionFindBestFactorizableInteger(my_imsize7MTM2tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM2
        my_niterCasaLog = my_niterCasaLogTM2
        my_thresholdCasaLog = my_thresholdCasaLogTM2
        #
        my_imsize = [my_imsize7MTM2, my_imsize7MTM2]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        my_sidelobethreshold = 3.0
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        my_scales = [0, 6, 18, 30, 60]
        #my_useScales = [0, 6, 18, 30, 60, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'mosaic'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_cont_7MTM2_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFiles7M + my_visFilesTM2
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7MTM2TM1
    #
    if my_telescope == "7MTM2TM1":
        
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsize7MTM2TM1tmp = int(round(int(my_imsizeCasaLogTM1[len(my_imsizeCasaLogTM1)-1])))
        my_imsize7MTM2TM1 = my_functionFindBestFactorizableInteger(my_imsize7MTM2TM1tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM1
        my_niterCasaLog = my_niterCasaLogTM1
        my_thresholdCasaLog = my_thresholdCasaLogTM1
        #
        my_imsize = [my_imsize7MTM2TM1, my_imsize7MTM2TM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        ##my_thresholdTMP = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        ##print("MY THRESHOLD")
        ##print(my_thresholdTMP)
        ##my_threshold = str(float(my_thresholdTMP[:-2])/2.)+"Jy"
        ##print(my_threshold)
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        ### my_sidelobethreshold = 3.0
        ### my_noisethreshold = 4.5
        ### my_minbeamfrac =  0.3
        ### my_lownoisethreshold = 1.5
        ### my_negativethreshold = 0.0
        # new tests to recover the faint emission visible with 7M
        # testing in source 470
        my_sidelobethreshold = 1.25
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        my_scales = [0, 6, 18, 30, 60]
        #my_useScales = [0, 6, 18, 30, 60, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'mosaic'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_cont_7MTM2TM1_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFiles7M + my_visFilesTM2 + my_visFilesTM1
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for TM2TM1
    #
    if my_telescope == "TM2TM1":
        
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsizeTM2TM1tmp = int(round(int(my_imsizeCasaLogTM1[len(my_imsizeCasaLogTM1)-1])))
        my_imsizeTM2TM1 = my_functionFindBestFactorizableInteger(my_imsizeTM2TM1tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM1
        my_niterCasaLog = my_niterCasaLogTM1
        my_thresholdCasaLog = my_thresholdCasaLogTM1
        #
        my_imsize = [my_imsizeTM2TM1, my_imsizeTM2TM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        ##my_thresholdTMP = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        ##print("MY THRESHOLD")
        ##print(my_thresholdTMP)
        ##my_threshold = str(float(my_thresholdTMP[:-2])/2.)+"Jy"
        ##print(my_threshold)
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        ### my_sidelobethreshold = 3.0
        ### my_noisethreshold = 4.5
        ### my_minbeamfrac =  0.3
        ### my_lownoisethreshold = 1.5
        ### my_negativethreshold = 0.0
        # new tests to recover the faint emission visible with 7M
        # testing in source 470
        my_sidelobethreshold = 1.25
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        my_scales = [0, 6, 18, 30]
        #my_useScales = [0, 6, 18, 30, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'mosaic'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_cont_TM2TM1_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFilesTM2 + my_visFilesTM1

    return my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold, my_gridder


##def my_functionGetTcleanParametersJointDeconbolutionCube(function_telescope, function_spw):
def my_functionParametersForJointDeconvolutionCube(my_telescope, my_source, my_spw):
    
    """
    help
    """
    
    import analysisUtils as au
    import analysisUtils as aU 
    
    #-----------------------------------------------------------------------
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Create your running directory
    #
    os.system("mkdir -p " + str(my_runningPath) + "/almagal")
    os.system("mkdir -p " + str(my_runningPath) + "/almagal/processing")

    #-----------------------------------------------------------------------
    # Set up infrastructure for array combination
    #
    if (my_telescope == "7M"):
        my_add7M = True
        my_addTM2 = False
        my_addTM1 = False
    
    if (my_telescope == "TM2"):
        my_add7M = False
        my_addTM2 = True
        my_addTM1 = False
    
    if (my_telescope == "TM1"):
        my_add7M = False
        my_addTM2 = False
        my_addTM1 = True
        
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
    # Prepare files for 7M
    #
    if my_add7M == True:
        
        # Define MS file names
        #
        my_visPath7M = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/calibrated/7M/perEB'
        my_visFiles7M = sorted(glob.glob(my_visPath7M+'/*.mstrans'))
    
    #-----------------------------------------------------------------------
    # Prepare files for TM2
    #
    if my_addTM2 == True:
        
        # Define MS file names
        #
        my_visPathTM2 = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/calibrated/TM2/perEB'
        my_visFilesTM2 = sorted(glob.glob(my_visPathTM2+'/*.mstrans'))
    
    #-----------------------------------------------------------------------
    # Prepare files for TM1
    #
    if my_addTM1 == True:
        
        # Define MS file names
        #
        my_visPathTM1 = my_runningPath + '/almagal/processing/2019.1.00195.L/sources/' + my_source + '/calibrated/TM1/perEB'
        my_visFilesTM1 = sorted(glob.glob(my_visPathTM1+'/*.mstrans'))
    
    #-----------------------------------------------------------------------
    # Get maximum recoverable scale (MRS)
    #
    if my_add7M == True:
        my_bmin = aU.getBaselineLengths(my_visFiles7M[0])[0][1]
        my_MRS = (0.6*((299792458.0/218.9625e9)/my_bmin))*(180.0/np.pi)*3600.0 #--- hard coded max recoverable scale in arcsec. Really should check that 15.1m is min baseline for all TM2 data.
    
    elif my_addTM2 == True:
        my_bmin = aU.getBaselineLengths(my_visFilesTM2[0])[0][1]
        my_MRS = (0.6*((299792458.0/218.9625e9)/my_bmin))*(180.0/np.pi)*3600.0 #--- hard coded max recoverable scale in arcsec. Really should check that 15.1m is min baseline for all TM2 data.
    
    elif my_addTM1 == True:
        my_bmin = aU.getBaselineLengths(my_visFilesTM1[0])[0][1]
        my_MRS = (0.6*((299792458.0/218.9625e9)/my_bmin))*(180.0/np.pi)*3600.0 #--- hard coded max recoverable scale in arcsec. Really should check that 15.1m is min baseline for all TM2 data.
    
    #-----------------------------------------------------------------------
    # Get tclean parameters based on 7M pipeline imaging
    #
    if my_add7M == True:
        
        # Inspect tclean for 7M
        #
        my_imsizeCasaLog7M, my_cellCasaLog7M, my_niterCasaLog7M, my_thresholdCasaLog7M = my_functionGetTcleanParametersCubeFromPipeline("7M", str(my_source), my_spw)
        
    #-----------------------------------------------------------------------
    # Get tclean parameters based on TM2 pipeline imaging
    #
    if my_addTM2 == True:
        
        # Inspect tclean for TM2
        #
        my_imsizeCasaLogTM2, my_cellCasaLogTM2, my_niterCasaLogTM2, my_thresholdCasaLogTM2 = my_functionGetTcleanParametersCubeFromPipeline("TM2", str(my_source), my_spw)
    
    #-----------------------------------------------------------------------
    # Get tclean parameters based on TM1 pipeline imaging
    #
    if my_addTM1 == True:
        
        # Inspect tclean for TM1
        #
        my_imsizeCasaLogTM1, my_cellCasaLogTM1, my_niterCasaLogTM1, my_thresholdCasaLogTM1 = my_functionGetTcleanParametersCubeFromPipeline("TM1", str(my_source), my_spw)
    
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7M
    #
    if my_telescope == "7M":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsize7Mtmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])))
        my_imsize7M = my_functionFindBestFactorizableInteger(my_imsize7Mtmp)
        my_cellCasaLog = my_cellCasaLog7M
        my_niterCasaLog = my_niterCasaLog7M
        my_thresholdCasaLog = my_thresholdCasaLog7M
        #
        my_imsize = [my_imsize7M, my_imsize7M]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        #
        my_sidelobethreshold = 1.25
        my_noisethreshold = 5.0
        my_minbeamfrac =  0.1
        my_lownoisethreshold = 2.0
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        #
        my_scales = [0, 30, 60]
        #my_useScales = [0, 30, 60, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'standard'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFiles7M
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for TM2
    #
    if my_telescope == "TM2":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsizeTM2tmp = int(round(int(my_imsizeCasaLogTM2[len(my_imsizeCasaLogTM2)-1])))
        my_imsizeTM2 = my_functionFindBestFactorizableInteger(my_imsizeTM2tmp)
        my_cellCasaLog = my_cellCasaLogTM2
        my_niterCasaLog = my_niterCasaLogTM2
        my_thresholdCasaLog = my_thresholdCasaLogTM2
        #
        my_imsize = [my_imsizeTM2, my_imsizeTM2]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        #
        my_sidelobethreshold = 2.0
        my_noisethreshold = 4.25
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        #
        my_scales = [0, 6, 18, 30]
        #my_useScales = [0, 6, 18, 30, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'standard'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFilesTM2
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for TM1
    #
    if my_telescope == "TM1":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsizeTM1tmp = int(round(int(my_imsizeCasaLogTM1[len(my_imsizeCasaLogTM1)-1])))
        my_imsizeTM1 = my_functionFindBestFactorizableInteger(my_imsizeTM1tmp)
        my_cellCasaLog = my_cellCasaLogTM1
        my_niterCasaLog = my_niterCasaLogTM1
        my_thresholdCasaLog = my_thresholdCasaLogTM1
        #
        my_imsize = [my_imsizeTM1, my_imsizeTM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        #
        my_sidelobethreshold = 3.0
        my_noisethreshold = 5.0
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        #
        my_scales = [0, 6, 18, 30]
        #my_useScales = [0, 6, 18, 30, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'standard'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFilesTM1
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7MTM2
    #
    if my_telescope == "7MTM2":
        
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLogTM2[len(my_imsizeCasaLogTM2)-1])))
        my_imsize7MTM2 = my_functionFindBestFactorizableInteger(my_imsize7MTM2tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM2
        my_niterCasaLog = my_niterCasaLogTM2
        my_thresholdCasaLog = my_thresholdCasaLogTM2
        #
        my_imsize = [my_imsize7MTM2, my_imsize7MTM2]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        my_sidelobethreshold = 3.0
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        my_scales = [0, 6, 18, 30, 60]
        #my_useScales = [0, 6, 18, 30, 60, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'mosaic'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFiles7M + my_visFilesTM2
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7MTM2TM1
    #
    if my_telescope == "7MTM2TM1":
        
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsize7MTM2TM1tmp = int(round(int(my_imsizeCasaLogTM1[len(my_imsizeCasaLogTM1)-1])))
        my_imsize7MTM2TM1 = my_functionFindBestFactorizableInteger(my_imsize7MTM2TM1tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM1
        my_niterCasaLog = my_niterCasaLogTM1
        my_thresholdCasaLog = my_thresholdCasaLogTM1
        #
        my_imsize = [my_imsize7MTM2TM1, my_imsize7MTM2TM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        # The following lines may be necesseray if the CASA log contains more tclean runs than expected
        # This next line was the original code line
        # my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        print(my_niterCasaLog)
        if len(my_niterCasaLog) == 1:
            my_niter = int(my_niterCasaLog[0])
        if len(my_niterCasaLog) == 2:
            my_niter = max(int(my_niterCasaLog[0]), int(my_niterCasaLog[1]))
        if len(my_niterCasaLog) == 3:
            my_niter = max(int(my_niterCasaLog[0]), int(my_niterCasaLog[1]), int(my_niterCasaLog[2]))
        if len(my_niterCasaLog) >= 4:
            my_niter = max(int(my_niterCasaLog[0]), int(my_niterCasaLog[1]), int(my_niterCasaLog[2]), int(my_niterCasaLog[3]))
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        my_imsize = [my_imsize7MTM2TM1, my_imsize7MTM2TM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        ##my_thresholdTMP = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        ##print("MY THRESHOLD")
        ##print(my_thresholdTMP)
        ##my_threshold = str(float(my_thresholdTMP[:-2])/2.)+"Jy"
        ##print(my_threshold)
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        ### my_sidelobethreshold = 3.0
        ### my_noisethreshold = 4.5
        ### my_minbeamfrac =  0.3
        ### my_lownoisethreshold = 1.5
        ### my_negativethreshold = 0.0
        # new tests to recover the faint emission visible with 7M
        # testing in source 470
        my_sidelobethreshold = 1.25
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        my_scales = [0, 6, 18, 30, 60]
        #my_useScales = [0, 6, 18, 30, 60, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'mosaic'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFiles7M + my_visFilesTM2 + my_visFilesTM1
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for TM2TM1
    #
    if my_telescope == "TM2TM1":
        
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsizeTM2TM1tmp = int(round(int(my_imsizeCasaLogTM1[len(my_imsizeCasaLogTM1)-1])))
        my_imsizeTM2TM1 = my_functionFindBestFactorizableInteger(my_imsizeTM2TM1tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM1
        my_niterCasaLog = my_niterCasaLogTM1
        my_thresholdCasaLog = my_thresholdCasaLogTM1
        #
        my_imsize = [my_imsizeTM2TM1, my_imsizeTM2TM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        ##my_thresholdTMP = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        ##print("MY THRESHOLD")
        ##print(my_thresholdTMP)
        ##my_threshold = str(float(my_thresholdTMP[:-2])/2.)+"Jy"
        ##print(my_threshold)
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        ### my_sidelobethreshold = 3.0
        ### my_noisethreshold = 4.5
        ### my_minbeamfrac =  0.3
        ### my_lownoisethreshold = 1.5
        ### my_negativethreshold = 0.0
        # new tests to recover the faint emission visible with 7M
        # testing in source 470
        my_sidelobethreshold = 1.25
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        my_scales = [0, 6, 18, 30]
        #my_useScales = [0, 6, 18, 30, 0.9]
        #my_useScalesARR = np.array(my_useScales)
        #my_UseScalesARRtmp = np.copy(my_useScalesARR)
        #my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        #my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        #my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== GRIGGER ALGORITHM =============#
        #
        my_gridder = 'mosaic'
        #
        #====== OUTPUT FILENAME ===============#
        #
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        #
        my_visfilestoclean = my_visFilesTM2 + my_visFilesTM1
    
    '''
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7MTM2
    #
    if my_telescope == "7MTM2":
        
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLogTM2[len(my_imsizeCasaLogTM2)-1])))
        #my_imsize7MTM2tmp = 3*my_imsize7MTM2tmp
        my_imsize7MTM2 = my_functionFindBestFactorizableInteger(my_imsize7MTM2tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM2
        my_niterCasaLog = my_niterCasaLogTM2
        my_thresholdCasaLog = my_thresholdCasaLogTM2
        #
        my_imsize = [my_imsize7MTM2, my_imsize7MTM2]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        my_sidelobethreshold = 3.0
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        # Scales after 18 are factors of the Maximum Recoverable Scale
        my_useScales = [0, 6, 18, 0.9]
        my_useScalesARR = np.array(my_useScales)
        my_UseScalesARRtmp = np.copy(my_useScalesARR)
        my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== OUTPUT FILENAME ===============#
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #
        #====== INPUT FILENAME ================#
        my_visfilestoclean = my_visFiles7M + my_visFilesTM2
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7MTM2TM1
    #
    if my_telescope == "7MTM2TM1":
        
        #======= GENERAL PARAMETERS ===========#
        #
        # Using the imsize determined according to the 7M field of view (this is the most accurate approach, produces larger images)
        #my_imsize7MTM2tmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])*float(my_cellCasaLog7M[len(my_cellCasaLog7M)-1].split("arc")[0])/float(my_cellCasaLogTM2[len(my_cellCasaLogTM2)-1].split("arc")[0])))
        # Using the imsize determined according to the TM2 field of view (this is intented to make smaller images, for quicker test/production)
        my_imsize7MTM2TM1tmp = int(round(int(my_imsizeCasaLogTM1[len(my_imsizeCasaLogTM1)-1])))
        my_imsize7MTM2TM1 = my_functionFindBestFactorizableInteger(my_imsize7MTM2TM1tmp)
        #if (my_imsize7MTM2tmp % 2) != 0:
        #    my_imsize7MTM2tmp = my_imsize7MTM2tmp+1
        my_cellCasaLog = my_cellCasaLogTM1
        my_niterCasaLog = my_niterCasaLogTM1
        my_thresholdCasaLog = my_thresholdCasaLogTM1
        #
        my_imsize = [my_imsize7MTM2TM1, my_imsize7MTM2TM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        # The following lines may be necesseray if the CASA log contains more tclean runs than expected
        # This next line was the original code line
        # my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        print(my_niterCasaLog)
        if len(my_niterCasaLog) == 1:
            my_niter = int(my_niterCasaLog[0])
        if len(my_niterCasaLog) == 2:
            my_niter = max(int(my_niterCasaLog[0]), int(my_niterCasaLog[1]))
        if len(my_niterCasaLog) == 3:
            my_niter = max(int(my_niterCasaLog[0]), int(my_niterCasaLog[1]), int(my_niterCasaLog[2]))
        if len(my_niterCasaLog) >= 4:
            my_niter = max(int(my_niterCasaLog[0]), int(my_niterCasaLog[1]), int(my_niterCasaLog[2]), int(my_niterCasaLog[3]))
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        my_sidelobethreshold = 3.0
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        # Change scales for multiscale clean
        # Scales after 18 are factors of the Maximum Recoverable Scale
        my_useScales = [0, 6, 18, 0.9]
        my_useScalesARR = np.array(my_useScales)
        my_UseScalesARRtmp = np.copy(my_useScalesARR)
        my_UseScalesARRtmp[-1] = int(np.floor((my_UseScalesARRtmp[-1]*my_MRS)/(float(re.split('a',my_cell[1:])[0]))))
        my_UseScalesARRtmp = my_UseScalesARRtmp.astype(int)
        my_scales = my_UseScalesARRtmp.tolist()
        #
        #====== OUTPUT FILENAME ===============#
        my_outputImage = str(my_source) + '_spw' + str(my_spw) + '_' + my_telescope + '_jointdeconv'
        #
        #====== INPUT FILENAME ================#
        my_visfilestoclean = my_visFiles7M + my_visFilesTM2 + my_visFilesTM1
    '''
    
    return my_visfilestoclean, my_outputImage, my_source, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold, my_gridder


def my_functionParametersForSelfCalibration(my_telescope, my_source):
    
    """
    Help
    """
    
    import analysisUtils as au
    import analysisUtils as aU
    
    #-----------------------------------------------------------------------
    # Define workstation and paths
    #
    my_usernameJSC, my_workstationTransfer, my_storagePathTransfer, my_workstation, my_mainPath, my_runningPath, my_softwarePath, my_storagePath = my_functionReadALMAGALConfigFile(verbose=False)
    
    # Create your running directory
    #
    os.system("mkdir -p " + str(my_runningPath) + "/almagal")
    os.system("mkdir -p " + str(my_runningPath) + "/almagal/processing")

    #-----------------------------------------------------------------------
    # Set up infrastructure for array combination
    #
    if (my_telescope == "7M"):
        my_add7M = True
        my_addTM2 = False
        my_addTM1 = False
    
    if (my_telescope == "TM2"):
        my_add7M = False
        my_addTM2 = True
        my_addTM1 = False
    
    if (my_telescope == "TM1"):
        my_add7M = False
        my_addTM2 = False
        my_addTM1 = True
    
    if my_add7M == True:
        os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/calibrated/7M/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
    
    if my_addTM2 == True:
        os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/calibrated/TM2/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
    
    if my_addTM1 == True:
        os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/calibrated/TM1/perEB/* " + str(my_runningPath) + "/almagal/processing/.")
    
    # Evaluate files and directories copied in the processing directory
    #
    my_sourcePaths, my_sourceDirs, my_sourceFiles = next(os.walk(str(my_runningPath)+'/almagal/processing'))
    
    # Untar the visibility files
    #
    for my_sourceFile in my_sourceFiles:
        os.system('tar -xf ' + str(my_runningPath) + '/almagal/processing/' + str(my_sourceFile) + ' -C ' + str(my_runningPath) + '/almagal/processing/.')
    os.system('rm -rf ' + str(my_runningPath) + '/almagal/processing/*.tar')
    
    #-----------------------------------------------------------------------
    # Prepare files for 7M
    #
    if my_add7M == True:
        
        # Copy weblogs and cont.dat files to the processing directory
        #
        my_functionPrepareWeblogForSelfCalibration("7M", str(my_source))
        
        # Define MS file names
        #
        my_visPath7M, my_visFiles7M = my_functionDefineMSFilesForSelfCalibration("7M", str(my_source))
        
        # Get line free channels for continuum imaging
        #
        my_pipelinePath7M, my_pipelineDirectory7M, my_lineFreeChannels7M, vislist7M, contfile7M = my_functionGetLineFreeChannelsForSelfCalibration("7M", str(my_source))
    
    #-----------------------------------------------------------------------
    # Prepare files for TM2
    #
    if my_addTM2 == True:
        
        # Copy weblogs and cont.dat files to the processing directory
        #
        my_functionPrepareWeblogForSelfCalibration("TM2", str(my_source))
        
        # Define MS file names
        #
        my_visPathTM2, my_visFilesTM2 = my_functionDefineMSFilesForSelfCalibration("TM2", str(my_source))
        
        # Get line free channels for continuum imaging
        #
        my_pipelinePathTM2, my_pipelineDirectoryTM2, my_lineFreeChannelsTM2, vislistTM2, contfileTM2 = my_functionGetLineFreeChannelsForSelfCalibration("TM2", str(my_source))
    
    #-----------------------------------------------------------------------
    # Prepare files for TM1
    #
    if my_addTM1 == True:
        
        # Copy weblogs and cont.dat files to the processing directory
        #
        my_functionPrepareWeblogForSelfCalibration("TM1", str(my_source))
        
        # Define MS file names
        #
        my_visPathTM1, my_visFilesTM1 = my_functionDefineMSFilesForSelfCalibration("TM1", str(my_source))
        
        # Get line free channels for continuum imaging
        #
        my_pipelinePathTM1, my_pipelineDirectoryTM1, my_lineFreeChannelsTM1, vislistTM1, contfileTM1 = my_functionGetLineFreeChannelsForSelfCalibration("TM1", str(my_source))
    
    #-----------------------------------------------------------------------
    # Define the variable containing the line-free frequency range
    #
    if (my_telescope == "7M"):
        my_viscontFiles = [vislist7M, contfile7M]
        
    if (my_telescope == "TM2"):
        my_viscontFiles = [vislistTM2, contfileTM2]
        
    if (my_telescope == "TM1"):
        my_viscontFiles = [vislistTM1, contfileTM1]
    
    my_sourceName = str(my_source)
    my_freqs = getFreqRangesContinuumSelfCalibration(my_viscontFiles, my_telescope, my_sourceName)
    
    #-----------------------------------------------------------------------
    # Get tclean parameters based on 7M pipeline imaging
    #
    if my_add7M == True:
        
        # Inspect tclean for 7M
        #
        my_imsizeCasaLog7M, my_cellCasaLog7M, my_niterCasaLog7M, my_thresholdCasaLog7M = my_functionGetTcleanParametersFromPipeline("7M", str(my_source))
    
    #-----------------------------------------------------------------------
    # Get tclean parameters based on TM2 pipeline imaging
    #
    if my_addTM2 == True:
        
        # Inspect tclean for TM2
        #
        my_imsizeCasaLogTM2, my_cellCasaLogTM2, my_niterCasaLogTM2, my_thresholdCasaLogTM2 = my_functionGetTcleanParametersFromPipeline("TM2", str(my_source))
    
    #-----------------------------------------------------------------------
    # Get tclean parameters based on TM1 pipeline imaging
    #
    if my_addTM1 == True:
        
        # Inspect tclean for TM1
        #
        my_imsizeCasaLogTM1, my_cellCasaLogTM1, my_niterCasaLogTM1, my_thresholdCasaLogTM1 = my_functionGetTcleanParametersFromPipeline("TM1", str(my_source))
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for 7M
    #
    if my_telescope == "7M":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsize7Mtmp = int(round(int(my_imsizeCasaLog7M[len(my_imsizeCasaLog7M)-1])))
        my_imsize7M = my_functionFindBestFactorizableInteger(my_imsize7Mtmp)
        my_cellCasaLog = my_cellCasaLog7M
        my_niterCasaLog = my_niterCasaLog7M
        my_thresholdCasaLog = my_thresholdCasaLog7M
        #
        my_imsize = [my_imsize7M, my_imsize7M]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        my_sidelobethreshold = 3.0
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        my_scales =[0, 6, 12]
        #
        #====== OUTPUT FILENAME ===============#
        my_outputImage = str(my_source) + '_cont_7M_selfcal'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        my_visfilestoclean = my_visFiles7M
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for TM2
    #
    if my_telescope == "TM2":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsizeTM2tmp = int(round(int(my_imsizeCasaLogTM2[len(my_imsizeCasaLogTM2)-1])))
        my_imsizeTM2 = my_functionFindBestFactorizableInteger(my_imsizeTM2tmp)
        my_cellCasaLog = my_cellCasaLogTM2
        my_niterCasaLog = my_niterCasaLogTM2
        my_thresholdCasaLog = my_thresholdCasaLogTM2
        #
        my_imsize = [my_imsizeTM2, my_imsizeTM2]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        ### my_sidelobethreshold = 3.0
        ### my_noisethreshold = 4.5
        ### my_minbeamfrac =  0.3
        ### my_lownoisethreshold = 1.5
        ### my_negativethreshold = 0.0
        # new tests to recover the faint emission visible with 7M
        # testing in source 470
        my_sidelobethreshold = 1.25
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        my_scales = [0, 6, 12]
        #
        #====== OUTPUT FILENAME ===============#
        my_outputImage = str(my_source) + '_cont_TM2_selfcal'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        my_visfilestoclean = my_visFilesTM2
    
    #-----------------------------------------------------------------------
    # TCLEAN parameters to be used for TM1
    #
    if my_telescope == "TM1":
        
        #======= GENERAL PARAMETERS ===========#
        #
        my_imsizeTM1tmp = int(round(int(my_imsizeCasaLogTM1[len(my_imsizeCasaLogTM1)-1])))
        my_imsizeTM1 = my_functionFindBestFactorizableInteger(my_imsizeTM1tmp)
        my_cellCasaLog = my_cellCasaLogTM1
        my_niterCasaLog = my_niterCasaLogTM1
        my_thresholdCasaLog = my_thresholdCasaLogTM1
        #
        my_imsize = [my_imsizeTM1, my_imsizeTM1]
        my_cell = str(my_cellCasaLog[len(my_cellCasaLog)-1])
        my_niter = int(my_niterCasaLog[len(my_niterCasaLog)-1])
        my_threshold = str(my_thresholdCasaLog[len(my_thresholdCasaLog)-1])
        #
        #===== PRIMARY BEAM PARAMETERS ========#
        #
        my_pbmask = 0.3
        my_pblimit = 0.3
        #
        #======= WEIGTHING PARAMETERS =========#
        #
        my_weighting = 'briggs'
        my_robust = 0.5
        #
        #======= MULTISCALE PARAMETERS ========#
        # Parameters for tcleans auto-multithresh parameter
        # CASA GUIDES RECOMMENDS 2.0, 4.25, 0.3, 1.5, 0.0
        # SQUALO 3.0, 4.5, 0.15, 2.0, 0.0
        # Adam/Alvaro tests 3.0, 4.5, 0.3, 1.5, 0.0
        ### my_sidelobethreshold = 3.0
        ### my_noisethreshold = 4.5
        ### my_minbeamfrac =  0.3
        ### my_lownoisethreshold = 1.5
        ### my_negativethreshold = 0.0
        # new tests to recover the faint emission visible with 7M
        # testing in source 470
        my_sidelobethreshold = 1.25
        my_noisethreshold = 4.5
        my_minbeamfrac =  0.3
        my_lownoisethreshold = 1.5
        my_negativethreshold = 0.0
        #
        #====== SCALES PARAMETER ==============#
        my_scales = [0, 6, 12]
        #
        #====== OUTPUT FILENAME ===============#
        my_outputImage = str(my_source) + '_cont_TM1_selfcal'
        os.system('rm -rf ' + my_outputImage + '.*')
        #
        #====== INPUT FILENAME ================#
        my_visfilestoclean = my_visFilesTM1
    
    return my_visfilestoclean, my_outputImage, my_source, my_freqs, my_imsize, my_cell, my_scales, my_niter, my_weighting, my_robust, my_pbmask, my_sidelobethreshold, my_noisethreshold, my_minbeamfrac, my_lownoisethreshold, my_negativethreshold, my_pblimit, my_threshold


'''

def function_chunksCreator(my_startingStep, my_numberOfChunks):
    
    """
    help
    """
    
    my_numberOfChunks = 10
    
    # Define starting and ending channel of the cube
    # The cubes have 3840 channels, we exclude the first and last two channels at the edges
    #
    my_firstChannel = 2 # Channels 0 and 1 are not included in the final cube
    my_lastChannel = 3838 # Channels 3838 and 3839 are not included in the final cube
    my_totalChannels = 3840 # Original total number of channels in the cube
    my_edgeChannels = 2 # Two channels at each edge
    
    my_channelsPerChunk = int(((my_totalChannels-2*my_edgeChannels)/my_numberOfChunks)/10)*10
    
    my_numberOfChannelsList = []
    for i in range(0, my_numberOfChunks):
        my_numberOfChannelsList.append()
    
    
        my_currentStepList = ['step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8', 'step9', 'step10', 'step11']
        my_chunkNameList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        my_startingChannelList = [2, 382, 762, 1142, 1522, 1902, 2282, 2662, 3042, 3422]
        my_numberOfChannelsList = [380, 380, 380, 380, 380, 380, 380, 380, 380, 416]
        
        my_spw = 0
        my_TMPindex = my_currentStepList.index(mycurrentstep)
        my_chunkName = my_chunkNameList[my_TMPindex]
        my_startingChannel = my_startingChannelList[my_TMPindex]
        my_numberOfChannels = my_numberOfChannelsList[my_TMPindex]
'''

def twodgaussian(inpars, circle=0, rotate=1, vheight=1, shape=None):
    """
    Returns a 2d gaussian function of the form:
    x' = np.cos(rota) * x - np.sin(rota) * y
    y' = np.sin(rota) * x + np.cos(rota) * y
    (rota should be in degrees)
    g = b + a * np.exp ( - ( ((x-center_x)/width_x)**2 +
    ((y-center_y)/width_y)**2 ) / 2 )
    
    inpars = [b,a,center_x,center_y,width_x,width_y,rota]
             (b is background height, a is peak amplitude)
    
    where x and y are the input parameters of the returned function,
    and all other parameters are specified by this function
    
    However, the above values are passed by list.  The list should be:
    inpars = (height,amplitude,center_x,center_y,width_x,width_y,rota)
    
    You can choose to ignore / neglect some of the above input parameters 
        unp.sing the following options:
        circle=0 - default is an elliptical gaussian (different x, y
            widths), but can reduce the input by one parameter if it's a
            circular gaussian
        rotate=1 - default allows rotation of the gaussian ellipse.  Can
            remove last parameter by setting rotate=0
        vheight=1 - default allows a variable height-above-zero, i.e. an
            additive constant for the Gaussian function.  Can remove first
            parameter by setting this to 0
        shape=None - if shape is set (to a 2-parameter list) then returns
            an image with the gaussian defined by inpars
    
    Adapted from Adam Ginsburg
    """
    inpars_old = inpars
    inpars = list(inpars)
    if vheight == 1:
        height = inpars.pop(0)
        height = float(height)
    else:
        height = float(0)
    amplitude, center_y, center_x = inpars.pop(0),inpars.pop(0),inpars.pop(0)
    amplitude = float(amplitude)
    center_x = float(center_x)
    center_y = float(center_y)
    if circle == 1:
        width = inpars.pop(0)
        width_x = float(width)
        width_y = float(width)
        rotate = 0
    else:
        width_x, width_y = inpars.pop(0),inpars.pop(0)
        width_x = float(width_x)
        width_y = float(width_y)
    if rotate == 1:
        rota = inpars.pop(0)
        rota = np.pi/180. * float(rota)
        rcen_x = center_x * np.cos(rota) - center_y * np.sin(rota)
        rcen_y = center_x * np.sin(rota) + center_y * np.cos(rota)
    else:
        rcen_x = center_x
        rcen_y = center_y
    if len(inpars) > 0:
        raise ValueError("There are still input parameters:" + str(inpars) + \
                " and you've input: " + str(inpars_old) + \
                " circle=%d, rotate=%d, vheight=%d" % (circle,rotate,vheight) )
            
    def rotgauss(x,y):
        if rotate==1:
            xp = x * np.cos(rota) - y * np.sin(rota)
            yp = x * np.sin(rota) + y * np.cos(rota)
        else:
            xp = x
            yp = y
        g = height+amplitude*np.exp(
            -(((rcen_x-xp)/width_x)**2+
            ((rcen_y-yp)/width_y)**2)/2.)
        return g
    if shape is not None:
        return rotgauss(*np.indices(shape))
    else:
        return rotgauss

def determineJvMfactor(my_psfname, my_imagename, my_JvMthreshold, my_plots):
    '''
    help
    '''

    # Dirty beam analysis
    #
    # Read in FITS file with dirty beam
    psf_file = fits.open(my_psfname)[0]
    if (my_imagename == my_psfname):
        psf_bmaj = psf_file.header['bmaj']*3600. # convert to arcsec
        psf_bmin = psf_file.header['bmin']*3600. # convert to arcsec
        psf_bpa = psf_file.header['bpa']
        print("Beam is " + str(psf_bmaj) + " x " + str(psf_bmin) + " with PA " +str(psf_bpa))
        print("... from " + my_psfname)
    else:
        image_file = fits.open(my_imagename)[0]
        psf_bmaj = image_file.header['bmaj']*3600. # convert to arcsec
        psf_bmin = image_file.header['bmin']*3600. # convert to arcsec
        psf_bpa = image_file.header['bpa']
        print("Beam is " + str(psf_bmaj) + " x " + str(psf_bmin) + " with PA " +str(psf_bpa))
        print("... from " + my_imagename)
    
    # Check if psf FITS file has more than two dimensions (cube) and if so, select a channel
    # ... 2 dimensions
    if (len(psf_file.data.shape) == 2):
        print('... processing 2D PSF image')
        print('    ' + my_psfname)
        hdu_data = psf_file.data[:, :]
    elif (len(psf_file.data.shape) == 3):
        print('... processing 3D PSF image, selecting middle channel')
        print('    ' + my_psfname)
        psf_channels = psf_file.data.shape[0]
        psf_selectedChannel = int(psf_channels/2.)
        hdu_data = psf_file.data[psf_selectedChannel, :, :]
    elif (len(psf_file.data.shape) == 4):
        print('... processing 4D PSF image, selecting middle channel')
        print('    ' + my_psfname)
        psf_channels = psf_file.data.shape[1]
        psf_selectedChannel = int(psf_channels/2.)
        hdu_data = psf_file.data[0, psf_selectedChannel, :, :]

    # Initialize mask for ellipse with shape as original FITS file
    ellipse = np.zeros(shape=hdu_data.shape)

    # Define ellipse parameters
    # ... center of the ellipse (in pixels)
    ellipse_x0 = int(psf_file.header['crpix1']-1)
    ellipse_y0 = int(psf_file.header['crpix2']-1)
    # ... size of ellipse (in pixels)
    ellipse_a = psf_bmaj/(abs(psf_file.header['cdelt1'])*3600.)
    ellipse_b = psf_bmin/(abs(psf_file.header['cdelt1'])*3600.)
    ellipse_ratio = ellipse_a/ellipse_b
    ellipse_a = ellipse_a/(int(ellipse_a)+1)
    ellipse_b = ellipse_a/ellipse_ratio
    # ... angle of the ellipse (in degrees)
    ellipse_alpha = psf_bpa+90.

    # Define coordinates to fill in with ellipse masks
    x = np.linspace(0, ellipse.shape[1]-1, ellipse.shape[1])
    y = np.linspace(0, ellipse.shape[0]-1, ellipse.shape[0])[:, None]

    # Defining masked-bins based on the ellipse (in pixels)
    ellipse = (((x-ellipse_x0)*np.cos(ellipse_alpha*np.pi/180.)+(y-ellipse_y0)*np.sin(ellipse_alpha*np.pi/180.))/ellipse_a)**2 + (((x-ellipse_x0)*np.sin(ellipse_alpha*np.pi/180.)-(y-ellipse_y0)*np.cos(ellipse_alpha*np.pi/180.))/ellipse_b)**2 >= 1
    ellipse = 1*ellipse
    for my_bin in range(2, int(psf_bmaj/(abs(psf_file.header['cdelt1'])*3600.))*30+1, 1):
        ellipse_abin = ellipse_a*(my_bin)
        ellipse_bbin = ellipse_abin/ellipse_ratio
        binellipse = (((x-ellipse_x0)*np.cos(ellipse_alpha*np.pi/180.)+(y-ellipse_y0)*np.sin(ellipse_alpha*np.pi/180.))/ellipse_abin)**2 + (((x-ellipse_x0)*np.sin(ellipse_alpha*np.pi/180.)-(y-ellipse_y0)*np.cos(ellipse_alpha*np.pi/180.))/ellipse_bbin)**2 >= 1
        binellipse = 1*binellipse
        ellipse = ellipse+binellipse

    # Create FITS file and plot of masked ellipse (if requested)
    fits.writeto(my_psfname+'.JvM.ellipse-mask.fits', ellipse, psf_file.header, overwrite=True)
    if (my_plots == True):
        plt.imshow(ellipse, extent=(x[0], x[-1], y[0], y[-1]), origin="lower")
        plt.savefig(my_psfname+'.JvM.ellipse-mask.png')
        plt.close()

    # Create dirty-beam variables for profile plot and calculation
    dirtyBeam_radiusList = []
    dirtyBeam_meanList = []
    dirtyBeam_errorList = []
    for my_bin in range(0, int(psf_bmaj/(abs(psf_file.header['cdelt1'])*3600.))*30):
        dirtyBeam_radiusList.append(my_bin)
        dirtyBeam_meanList.append(np.mean(hdu_data[np.where(ellipse==my_bin)]))
        dirtyBeam_errorList.append(np.std(hdu_data[np.where(ellipse==my_bin)]))
    dirtyBeam_radius = (abs(psf_file.header['cdelt1'])*3600.)*np.array(dirtyBeam_radiusList)
    dirtyBeam_mean = np.array(dirtyBeam_meanList)
    dirtyBeam_error = 1.*np.array(dirtyBeam_errorList)

    # Clean beam analysis
    #
    # Define shape of the array to be built
    my_shape = hdu_data.shape
    # Key parameters of the clean beam
    # ... intensity of the peak (normalized to 1)
    beam_height = 0.0
    beam_amplitude = 1.0
    # ... center of the beam
    beam_x0 = int(psf_file.header['crpix1']-1)
    beam_y0 = int(psf_file.header['crpix2']-1)
    # ... width of the beam
    #     Note that FWHM = 2*sqrt(2 ln2) sigma = 2.355 sigma
    #     and that FWHM is the beam (bmaj and bmin)
    beam_a = (psf_bmaj/(2*np.sqrt(2*np.log(2))))/(abs(psf_file.header['cdelt1'])*3600.)
    beam_b = (psf_bmin/(2*np.sqrt(2*np.log(2))))/(abs(psf_file.header['cdelt1'])*3600.)
    # ... position angle of the beam
    beam_alpha = psf_bpa

    # Input parameters for the function twodgaussian
    inpars = (beam_height, beam_amplitude, beam_x0, beam_y0, beam_a, beam_b, beam_alpha)
    rotgauss = twodgaussian(inpars)

    # Write out FITS file with clean beam (if requested)
    fits.writeto(my_psfname+'.JvM.clean-beam.fits', rotgauss(*np.indices(my_shape)), psf_file.header, overwrite=True)
    #if (my_plots == True):
    #    fits.writeto(my_psfname+'.JvM.clean-beam.fits', rotgauss(*np.indices(my_shape)), psf_file.header, overwrite=True)
    
    # Create variables for profile plot
    cleanBeam_radiusList = []
    cleanBeam_meanList = []
    cleanBeam_errorList = []
    for my_bin in range(0, int(psf_bmaj/(abs(psf_file.header['cdelt1'])*3600.))*30):
        cleanBeam_radiusList.append(my_bin)
        cleanBeam_meanList.append(np.mean(rotgauss(*np.indices(my_shape))[np.where(ellipse==my_bin)]))
        cleanBeam_errorList.append(np.std(rotgauss(*np.indices(my_shape))[np.where(ellipse==my_bin)]))
    cleanBeam_radius = (abs(psf_file.header['cdelt1'])*3600.)*np.array(cleanBeam_radiusList)
    cleanBeam_mean = np.array(cleanBeam_meanList)
    cleanBeam_error = 1.*np.array(cleanBeam_errorList)

    # Calculate JvM factor
    #
    my_valueCheck = np.min(np.where(dirtyBeam_mean <= my_JvMthreshold))

    dirtyBeam_cumulative = 0.0
    dirtyBeam_cumulativeVolumeList = []
    dirtyBeam_volume = dirtyBeam_mean*dirtyBeam_radius*2*np.pi*(dirtyBeam_radius[10]-dirtyBeam_radius[9])
    for i in range(0, len(dirtyBeam_volume)):
        dirtyBeam_cumulative = dirtyBeam_cumulative + dirtyBeam_volume[i]
        dirtyBeam_cumulativeVolumeList.append(dirtyBeam_cumulative)
    dirtyBeam_cumulativeVolume = np.array(dirtyBeam_cumulativeVolumeList)

    cleanBeam_cumulative = 0.0
    cleanBeam_cumulativeVolumeList = []
    cleanBeam_volume = cleanBeam_mean*cleanBeam_radius*2*np.pi*(cleanBeam_radius[10]-cleanBeam_radius[9])
    for i in range(0, len(cleanBeam_volume)):
        cleanBeam_cumulative = cleanBeam_cumulative + cleanBeam_volume[i]
        cleanBeam_cumulativeVolumeList.append(cleanBeam_cumulative)
    cleanBeam_cumulativeVolume = np.array(cleanBeam_cumulativeVolumeList)

    JvMfactor = cleanBeam_cumulativeVolume[my_valueCheck]/dirtyBeam_cumulativeVolume[my_valueCheck]

    # Plot of profiles (if requested)
    #
    if (my_plots == True):
        print("    producing plots")
        figure_xsize = 6.5
        figure_ysize = 14.
        box_xsize = 5.
        box_ysize = 5.
        right_margin = 1.0
        top_margin = 0.8
        interplot = 0.5
        extra_interplot = 0.5
        spectra_xsize = 5.
        spectra_ysize = 2.5
                    
        fig = plt.figure(figsize=(figure_xsize, figure_ysize))
                
        ax11 = fig.add_axes([(1.*right_margin+0.*(spectra_xsize+interplot))/figure_xsize, (figure_ysize-1.*top_margin-1.*(spectra_ysize+interplot))/figure_ysize, spectra_xsize/figure_xsize, spectra_ysize/figure_ysize], aspect='auto', anchor='SW')
        ax21 = fig.add_axes([(1.*right_margin+0.*(spectra_xsize+interplot))/figure_xsize, (figure_ysize-1.*top_margin-2.*(spectra_ysize+interplot))/figure_ysize, spectra_xsize/figure_xsize, spectra_ysize/figure_ysize], aspect='auto', anchor='SW')
        ax31 = fig.add_axes([(1.*right_margin+0.*(spectra_xsize+interplot))/figure_xsize, (figure_ysize-1.*top_margin-3.*(spectra_ysize+interplot))/figure_ysize, spectra_xsize/figure_xsize, spectra_ysize/figure_ysize], aspect='auto', anchor='SW')
        ax41 = fig.add_axes([(1.*right_margin+0.*(spectra_xsize+interplot))/figure_xsize, (figure_ysize-1.*top_margin-4.*(spectra_ysize+interplot))/figure_ysize, spectra_xsize/figure_xsize, spectra_ysize/figure_ysize], aspect='auto', anchor='SW')
        
        ax11.set_ylim([-0.1, 1.1])
        ax11.set_xlim([+0.0, psf_bmaj*7.])
        ax11.axvline(x=dirtyBeam_radius[my_valueCheck], color='black', linestyle='dotted')
        ax11.plot(dirtyBeam_radius, dirtyBeam_mean, color='orange', label='PSF average')
        #ax11.plot(dirtyBeam_radius, dirtyBeam_mean, color='orange', marker='x')
        ax11.fill_between(dirtyBeam_radius, dirtyBeam_mean-1.0*dirtyBeam_error, dirtyBeam_mean+1.0*dirtyBeam_error, color='moccasin', label='PSF range')
        ax11.plot(dirtyBeam_radius, cleanBeam_mean, color='black', linestyle='dashed', label='CLEAN beam')
        #ax11.plot(dirtyBeam_radius, cleanBeam_mean, color='black', marker='x')
        #ax11.set_xlabel('radius (arcsec)', fontsize=12)
        ax11.set_ylabel('normalized profile', fontsize=12)
        ax11.legend(prop={'size': 12})
        my_xboxmin_pixel = ax11.get_xlim()[0]
        my_xboxmax_pixel = ax11.get_xlim()[1]
        my_yboxmin_pixel = ax11.get_ylim()[0]
        my_yboxmax_pixel = ax11.get_ylim()[1]
        my_text = my_psfname
        ax11.text(my_xboxmax_pixel+0.5*(my_xboxmin_pixel-my_xboxmax_pixel), my_yboxmin_pixel+1.15*(my_yboxmax_pixel-my_yboxmin_pixel), my_text, fontsize=12, clip_on=False, horizontalalignment='center', verticalalignment='bottom')
        
        ax21.set_ylim([-0.1*max(np.max(dirtyBeam_volume), np.max(cleanBeam_volume)), 1.1*max(np.max(dirtyBeam_volume), np.max(cleanBeam_volume))])
        ax21.set_xlim([+0.0, psf_bmaj*7.])
        ax21.axvline(x=dirtyBeam_radius[my_valueCheck], color='black', linestyle='dotted')
        ax21.plot(dirtyBeam_radius, dirtyBeam_volume, color='orange')
        ax21.plot(dirtyBeam_radius, cleanBeam_volume, color='black', linestyle='dashed')
        #ax21.set_xlabel('radius (arcsec)', fontsize=12)
        ax21.set_ylabel('differential volume', fontsize=12)
        
        ax31.set_ylim([-0.1*max(np.max(dirtyBeam_cumulativeVolume), np.max(cleanBeam_cumulativeVolume)), 1.1*max(np.max(dirtyBeam_cumulativeVolume), np.max(cleanBeam_cumulativeVolume))])
        ax31.set_xlim([+0.0, psf_bmaj*7.])
        ax31.axvline(x=dirtyBeam_radius[my_valueCheck], color='black', linestyle='dotted')
        ax31.plot(dirtyBeam_radius, dirtyBeam_cumulativeVolume, color='orange')
        ax31.plot(dirtyBeam_radius, cleanBeam_cumulativeVolume, color='black', linestyle='dashed')
        #ax31.set_xlabel('radius (arcsec)', fontsize=12)
        ax31.set_ylabel('cumulative volume', fontsize=12)
        
        if np.nanmax(cleanBeam_cumulativeVolume/dirtyBeam_cumulativeVolume) < 2.0:
            ax41.set_ylim([0.9*np.nanmin(cleanBeam_cumulativeVolume/dirtyBeam_cumulativeVolume), 1.1*np.nanmax(cleanBeam_cumulativeVolume/dirtyBeam_cumulativeVolume)])
        else:
            ax41.set_ylim([0.9*np.nanmin(cleanBeam_cumulativeVolume/dirtyBeam_cumulativeVolume), 1.1])
        ax41.set_xlim([+0.0, psf_bmaj*7.])
        ax41.axvline(x=dirtyBeam_radius[my_valueCheck], color='black', linestyle='dotted')
        ax41.axhline(y=JvMfactor, color='grey', linestyle='solid', label='JvM factor = '+str(round(JvMfactor*1000.)/1000.))
        ax41.plot(dirtyBeam_radius, cleanBeam_cumulativeVolume/dirtyBeam_cumulativeVolume, color='blue', linestyle='solid', label='CLEAN / PSF')
        ax41.set_xlabel('radius (arcsec)', fontsize=12)
        ax41.set_ylabel('ratio cumulative volumes', fontsize=12)
        ax41.legend(prop={'size': 12})
        
        plt.savefig(my_psfname+'.JvM.beam-profile.png')
        plt.close()

    return JvMfactor

def my_scraper(my_source, my_casalog_path, my_general_script):

	def lines_that_equal(line_to_match, fp):
		return [line for line in fp if line == line_to_match]

	def lines_that_contain(string, fp):
		return [line for line in fp if string in line]

	def lines_that_start_with(string, fp):
		return [line for line in fp if line.startswith(string)]

	def lines_that_end_with(string, fp):
		return [line for line in fp if line.endswith(string)]

	def write_out_line(my_fileCheck, my_taskCheck, my_counterCheck):
		with open(my_fileCheck, "r") as fp:
			my_counter = 0
			for line in lines_that_contain(str(my_taskCheck)+"(", fp):
				my_counter+=1
				my_startAt = 34+len(my_taskCheck)
				if (my_counter == my_counterCheck):
					print(line[my_startAt:])

	def write_out_line_replace_one(my_fileCheck, my_taskCheck, my_counterCheck, my_first_input, my_first_output):
		with open(my_fileCheck, "r") as fp:
			my_counter = 0
			for line in lines_that_contain(str(my_taskCheck)+"(", fp):
				my_counter+=1
				my_startAt = 34+len(my_taskCheck)
				if (my_counter == my_counterCheck):
					print(line[my_startAt:].replace(my_first_input, my_first_output))

	def write_out_line_replace_two(my_fileCheck, my_taskCheck, my_counterCheck, my_first_input, my_first_output, my_second_input, my_second_output):
		with open(my_fileCheck, "r") as fp:
			my_counter = 0
			for line in lines_that_contain(str(my_taskCheck)+"(", fp):
				my_counter+=1
				my_startAt = 34+len(my_taskCheck)
				if (my_counter == my_counterCheck):
					tmp1_line = line[my_startAt:].replace(my_first_input, my_first_output)
					print(tmp1_line.replace(my_second_input, my_second_output))

	def write_out_line_replace_three(my_fileCheck, my_taskCheck, my_counterCheck, my_first_input, my_first_output, my_second_input, my_second_output, my_third_input, my_third_output):
		with open(my_fileCheck, "r") as fp:
			my_counter = 0
			for line in lines_that_contain(str(my_taskCheck)+"(", fp):
				my_counter+=1
				my_startAt = 34+len(my_taskCheck)
				if (my_counter == my_counterCheck):
					tmp1_line = line[my_startAt:].replace(my_first_input, my_first_output)
					tmp2_line = tmp1_line.replace(my_second_input, my_second_output)
					print(tmp2_line.replace(my_third_input, my_third_output))

	def write_out_line_replace_four(my_fileCheck, my_taskCheck, my_counterCheck, my_first_input, my_first_output, my_second_input, my_second_output, my_third_input, my_third_output, my_fourth_input, my_fourth_output):
		with open(my_fileCheck, "r") as fp:
			my_counter = 0
			for line in lines_that_contain(str(my_taskCheck)+"(", fp):
				my_counter+=1
				my_startAt = 34+len(my_taskCheck)
				if (my_counter == my_counterCheck):
					tmp1_line = line[my_startAt:].replace(my_first_input, my_first_output)
					tmp2_line = tmp1_line.replace(my_second_input, my_second_output)
					tmp3_line = tmp2_line.replace(my_third_input, my_third_output)
					print(tmp3_line.replace(my_fourth_input, my_fourth_output))

	def write_out_all_lines(my_fileCheck, my_taskCheck):
		with open(my_fileCheck, "r") as fp:
			for line in lines_that_contain(str(my_taskCheck)+"(", fp):
				my_startAt = 34+len(my_taskCheck)
				print(line[my_startAt:])

	def write_out_all_lines_replace_one(my_fileCheck, my_taskCheck, my_first_input, my_first_output):
		with open(my_fileCheck, "r") as fp:
			for line in lines_that_contain(str(my_taskCheck)+"(", fp):
				my_startAt = 34+len(my_taskCheck)
				print(line[my_startAt:].replace(my_first_input, my_first_output))


	my_casalog_files = os.listdir(my_casalog_path)
	sys.stdout = open(my_general_script, "w")

	# Introduction
	#
	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Processing script for ALMAGAL (project ID: 2019.1.00195.L)")
	print("# ")
	print("# ::: ALMAGAL ::: Script developed by Alvaro Sanchez-Monge (contact: asanchez.astro <at> gmail.com)")
	print("# ::: ALMAGAL ::: Continuum and cube imaging production of 7M + TM2 + TM1 arrays")
	print("# ::: ALMAGAL ::: Based on the functions and scripts used for the first data release")
	print("# ")
	print("# ::: ALMAGAL ::: Necessary input files (provided with this script): ")
	print("# ::: ALMAGAL :::   - calibrated and split file for the selected source, all arrays and EBs")
	print("# ::: ALMAGAL :::   - original masks for the TM2 and 7M arrays")
	print("# ")

	# Continuum processing
	#
	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Continuum processing: first step of tclean with no initial mask")
	print("# ")
	write_out_line_replace_one(str(my_casalog_path)+str(my_casalog_files[0]), 'tclean', 2, '/dev/shm/almagal/processing/', '')

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Continuum processing: second step of tclean merging in the TM2 mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_cont_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')")
	write_out_line_replace_two(str(my_casalog_path)+str(my_casalog_files[0]), 'makemask', 1, '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_two(str(my_casalog_path)+str(my_casalog_files[0]), 'immath', 1, '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_two(str(my_casalog_path)+str(my_casalog_files[0]), 'immath', 2, '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_two(str(my_casalog_path)+str(my_casalog_files[0]), 'makemask', 2, '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_one(str(my_casalog_path)+str(my_casalog_files[0]), 'tclean', 3, '/dev/shm/almagal/processing/', '')

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Continuum processing: third step of tclean merging in the 7M mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_cont_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v02.mask')")
	write_out_line_replace_two(str(my_casalog_path)+str(my_casalog_files[0]), 'makemask', 3, '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_two(str(my_casalog_path)+str(my_casalog_files[0]), 'immath', 3, '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_two(str(my_casalog_path)+str(my_casalog_files[0]), 'immath', 4, '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_two(str(my_casalog_path)+str(my_casalog_files[0]), 'makemask', 4, '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_one(str(my_casalog_path)+str(my_casalog_files[0]), 'tclean', 4, '/dev/shm/almagal/processing/', '')

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Continuum processing: apply JvM correction")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_cont_7MTM2TM1_jointdeconv'")
	print("my_bmaj = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmaj')['value']")
	print("my_bmin = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bmin')['value']")
	print("my_bpa = imhead(imagename = my_outputImageNow+'.image', mode='get', hdkey='bpa')['value']")
	print("ia.open(my_outputImageNow+'.model')")
	print("im2 = ia.convolve2d(outfile=my_outputImageNow+'.model.convolved', axes=[0, 1], type='gauss', major=str(my_bmaj)+'arcsec', minor=str(my_bmin)+'arcsec', pa=str(my_bpa)+'deg', overwrite=True)")
	print("im2.done()")
	print("ia.close()")
	print(" ")

	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'exportfits', 11)
	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'exportfits', 12)
	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'exportfits', 13)
	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'exportfits', 14)
	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'exportfits', 15)
	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'immath', 5)
	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'immath', 6)
	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'exportfits', 23)
	write_out_line(str(my_casalog_path)+str(my_casalog_files[0]), 'exportfits', 24)

	# Continuum subtraction
	#
	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Continuum subtraction: subtract continuum and resample to the same frequency frame")
	print("# ")
	write_out_all_lines_replace_one(str(my_casalog_path)+str(my_casalog_files[1]), 'uvcontsub', '/dev/shm/almagal/processing/', '')
	write_out_all_lines_replace_one(str(my_casalog_path)+str(my_casalog_files[1]), 'mstransform', '/dev/shm/almagal/processing/', '')
	write_out_all_lines_replace_one(str(my_casalog_path)+str(my_casalog_files[1]), 'split', '/dev/shm/almagal/processing/', '')

	# Cube (spw 0) processing
	#
	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 0) processing: first step of tclean with no initial mask")
	print("# ")
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[2]), "tclean", 1, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 0) processing: second step of tclean merging in the TM2 mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_spw0_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')")
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[2]), 'makemask', 1, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[2]), 'immath', 1, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[2]), 'immath', 2, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[2]), 'makemask', 2, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[2]), "tclean", 2, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 0) processing: third step of tclean merging in the 7M mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_spw0_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v02.mask')")
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[2]), 'makemask', 3, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[2]), 'immath', 3, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[2]), 'immath', 4, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[2]), 'makemask', 4, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[2]), 'tclean', 3, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	# Cube (spw 1) processing
	#
	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 1) processing: first step of tclean with no initial mask")
	print("# ")
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[40]), "tclean", 1, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 1) processing: second step of tclean merging in the TM2 mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_spw1_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')")
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[40]), 'makemask', 1, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[40]), 'immath', 1, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[40]), 'immath', 2, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[40]), 'makemask', 2, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[40]), "tclean", 2, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 1) processing: third step of tclean merging in the 7M mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_spw1_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v02.mask')")
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[40]), 'makemask', 3, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[40]), 'immath', 3, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[40]), 'immath', 4, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[40]), 'makemask', 4, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[40]), 'tclean', 3, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	# Cube (spw 2) processing
	#
	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 2) processing: first step of tclean with no initial mask")
	print("# ")
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[78]), "tclean", 1, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 2) processing: second step of tclean merging in the TM2 mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_spw2_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')")
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[78]), 'makemask', 1, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[78]), 'immath', 1, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[78]), 'immath', 2, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[78]), 'makemask', 2, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[78]), "tclean", 2, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 2) processing: third step of tclean merging in the 7M mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_spw2_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v02.mask')")
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[78]), 'makemask', 3, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[78]), 'immath', 3, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[78]), 'immath', 4, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[78]), 'makemask', 4, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[78]), 'tclean', 3, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	# Cube (spw 3) processing
	#
	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 3) processing: first step of tclean with no initial mask")
	print("# ")
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[116]), "tclean", 1, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 3) processing: second step of tclean merging in the TM2 mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_spw3_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v01.mask')")
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[116]), 'makemask', 1, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[116]), 'immath', 1, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[116]), 'immath', 2, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[116]), 'makemask', 2, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[116]), "tclean", 2, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

	print("####################################################################################################")
	print("# ")
	print("# ::: ALMAGAL ::: Cube (spw 3) processing: third step of tclean merging in the 7M mask")
	print("# ")
	print("my_outputImageNow = '" + str(my_source) + "_spw3_7MTM2TM1_jointdeconv'")
	print("os.system('cp -rp ' + my_outputImageNow + '.mask ' + my_outputImageNow + '_v02.mask')")
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[116]), 'makemask', 3, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[116]), 'immath', 3, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[116]), 'immath', 4, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_three(str(my_casalog_path)+str(my_casalog_files[116]), 'makemask', 4, "_chunk1", "", '/dev/shm/almagal/processing/', '', '/dev/shm/almagal/', '')
	write_out_line_replace_four(str(my_casalog_path)+str(my_casalog_files[116]), 'tclean', 3, '/dev/shm/almagal/processing/', '', "_chunk1", "", "nchan=128", "nchan=-1", "restoringbeam=''", "restoringbeam='common'")

def my_maskCreator(my_imageFile, my_residualFile, my_maskFile, highSNR, lowSNR):
	
	# Load the image and residual FITS files
	dataImage, headerImage = fits.getdata(my_imageFile, header=True)
	dataResidual, headerResidual = fits.getdata(my_residualFile, header=True)
	dataMask, headerMask = fits.getdata(my_maskFile, header=True)
	
	# Calculate the median absolute deviation of the residual
	dataResidual_notNaN = dataResidual[np.logical_not(np.isnan(dataResidual))]
	dataResidual_MAD = median_absolute_deviation(dataResidual_notNaN)
	print("... ... Median absolute deviation of residual = " + str(dataResidual_MAD))

	# Use a boolean condition to find where pixel values in the image file are aboe highSNR and lowSNR
	blobsHigh = dataImage > highSNR*dataResidual_MAD
	blobsLow = dataImage > lowSNR*dataResidual_MAD
	blobsCheck = dataImage > lowSNR*dataResidual_MAD

	# Label connected regions that satisfy this condition
	labelsHigh, nlabelsHigh = ndimage.label(blobsHigh)
	labelsLow, nlabelsLow = ndimage.label(blobsLow)
	labelsCheck, nlabelsCheck = ndimage.label(blobsCheck)
	
	# Keep only lowSNR regions that contain highSNR regions
	for i in range(1, nlabelsLow+1):
		if np.max(labelsHigh[np.where(labelsLow == i)]) == 0:
			labelsCheck[np.where(labelsLow == i)] = 0
			blobsCheck[np.where(labelsLow == i)] = False
	
	# Write out new mask, using the header of the original mask
	dataMask[dataMask > 0] = 0
	dataMask[np.where(labelsCheck > 0)] = 1
	os.system('rm -rf ' + my_maskFile)
	fits.writeto(my_maskFile, dataMask, headerMask)
	
	return dataResidual_MAD
	
	'''
	# plot
	fig, ax = plt.subplots(1, 4, sharex=True, sharey=True, figsize=(20, 5))
	ax[0].imshow(image)
	ax[1].hold(True)
	ax[1].imshow(np.ma.masked_array(labelsHigh, ~blobsHigh), cmap=plt.cm.rainbow)
	ax[2].hold(True)
	ax[2].imshow(np.ma.masked_array(labelsLow, ~blobsLow), cmap=plt.cm.rainbow)
	ax[3].hold(True)
	ax[3].imshow(np.ma.masked_array(labelsCheck, ~blobsCheck), cmap=plt.cm.rainbow)
	#for ri, ci, di in zip(r, c, d):
	#    ax[1].annotate('', xy=(0, 0), xytext=(ci, ri),
	#                   arrowprops={'arrowstyle':'<-', 'shrinkA':0})
	#    ax[1].annotate('d=%.1f' % di, xy=(ci, ri),  xytext=(0, -5),
	#                   textcoords='offset points', ha='center', va='top',
	#                   fontsize='x-large')
	#for aa in ax.flat:
	#    aa.set_axis_off()
	fig.tight_layout()
	plt.show()
	'''


def my_croppingFits(filename, outfile, my_cropperFile):

    """
    Create a cropped version of a larger FITS file by
    removing the NaN pixels in the region outside the primary beam
    
    Parameters
    ----------
    filename : string
        Name of the FITS file
    outfile : string
        Name of the output FITS file
    my_cropperFile : string
        Name of the output ascii file with cropping coordinates
    
    Returns
    -------
    outfile : string
        Name of the output FITS file
    my_cropperFile : string
        Name of the output ascii file with cropping coordinates
    """
    
    # Read in the FITS file
    #
    my_data, my_header = fits.getdata(filename, header=True)
    print("... Cropping file " + str(filename))
    
    # Get dimmensions of the FITS file (usually: 2, 3 or 4)
    #
    ndim = my_header.get('NAXIS')
    
    # Check if there could be some error in the header
    # e.g. missing information on the x and y-axis coordinates
    #
    if my_header.get('CDELT1') is None or my_header.get('CDELT2') is None:
        raise Exception("Missing CD or CDELT keywords in header")
    
    # If file with cropping coordinates do not exist, determine them
    #
    if os.path.isfile(my_cropperFile) == False:
        
        my_buffer = 10
        my_notnandata = np.where(~np.isnan(my_data))
        xmin = int(np.min(my_notnandata[0])-my_buffer)
        xmax = int(np.max(my_notnandata[0])+my_buffer+1)
        ymin = int(np.min(my_notnandata[1])-my_buffer)
        ymax = int(np.max(my_notnandata[1])+my_buffer+1)
        
        with open(my_cropperFile, 'w') as f:
            f.write(str(xmin))
            f.write('\n')
            f.write(str(xmax))
            f.write('\n')
            f.write(str(ymin))
            f.write('\n')
            f.write(str(ymax))
            f.write('\n')
        
        print("    ... File with cropping coordinates has been created with name " + my_cropperFile)
        print("    ... Cropping coordinates are (" + str(xmin) + ", " + str(ymin) + ") and  (" + str(xmax) + ", " + str(ymax) + ")")
    
    # If file with cropping coordinates already exists, use it
    #
    else:
        
        print("    ... Reading information from " + my_cropperFile)
        
        lines = [line.rstrip('\n') for line in open(my_cropperFile)]
        my_croppingCoordinates = []
        for line in lines:
            my_croppingCoordinates.append(line)
        xmin = int(my_croppingCoordinates[0])
        xmax = int(my_croppingCoordinates[1])
        ymin = int(my_croppingCoordinates[2])
        ymax = int(my_croppingCoordinates[3])
        
        print("    ... Cropping coordinates are (" + str(xmin) + ", " + str(ymin) + ") and  (" + str(xmax) + ", " + str(ymax) + ")")
    
    if ymax >= my_header.get('NAXIS2') or xmax >=  my_header.get('NAXIS1'):
        raise ValueError("Max Coordinate is outside of map: %f, %f." % (xmax, ymax))
    
    if xmin < 0 or ymin < 0:
        raise ValueError("Min Coordinate is outside of map: %f, %f." % (xmin, ymin))
    
    # Modify the header based on the new size of the image
    #
    my_header['CRPIX1'] -= xmin
    my_header['CRPIX2'] -= ymin
    my_header['NAXIS1'] = int(xmax - xmin)
    my_header['NAXIS2'] = int(ymax - ymin)
    
    my_header['AGCRPX1'] = xmin
    my_header['AGCRPX2'] = xmax
    my_header['AGCRPY1'] = ymin
    my_header['AGCRPY2'] = ymax
        
    # Check if the resulting image has no available coordinates in X and Y axes
    #
    if my_header.get('NAXIS1') == 0 or my_header.get('NAXIS2') == 0:
        raise ValueError("Map has a 0 dimension: %i, %i." % (my_header.get('NAXIS1'), my_header.get('NAXIS2')))

    # Create new output file, with cropped size
    #
    if ndim == 4:
        img = my_data[:, :, ymin:ymax, xmin:xmax]
    if ndim == 3:
        img = my_data[:, ymin:ymax, xmin:xmax]
    if ndim == 2:
        img = my_data[ymin:ymax, xmin:xmax]
    newfile = fits.PrimaryHDU(data=img, header=my_header)
    
    if isinstance(outfile, str):
        
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            
            newfile.writeto(outfile, overwrite=True)
    
    return newfile
