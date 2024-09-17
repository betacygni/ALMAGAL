########################################################################
#
#                   ALMAGAL processing pipeline
#
#
# 
# Script number 2                        created by Alvaro Sanchez-Monge
#
# Previous step:   scriptToSplitSources.py
# Next step:       tarPipelineProducts.py
# 
# Description:     Python script to generate the scripts that are used
#                  to produce images of the individual sources
#                  for individual arrays
# 
# Required:
#   - database.csv file containing names and MOUS directory tree
#   - calibrated split files produced with scriptToSplitSources.py
#   - master scripts:
#        REFIND.py
#        scriptForImaging7M.py
#        run_mainScriptForImaging7M
#        mainScriptForImaging7M.sh
#        scriptForImagingTM2.py
#        run_mainScriptForImagingTM2
#        mainScriptForImagingTM2.sh
#        scriptForImagingTM1.py
#        run_mainScriptForImagingTM1
#        mainScriptForImagingTM1.sh
#        scriptForImagingTM1_serial.py
#        run_mainScriptForImagingTM1_serial
#        mainScriptForImagingTM1_serial.sh
#
# Execution:
#   - gomodule (necessary in JSC processing)
#   - gopython (necessary in JSC processing)
#   - python createIndividual_scriptForImaging.py
#     followed by
#     ./my_executeImaging.sh
#
# CASA version 5.6.1
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
#   --id,            : Single ID number (e.g., 0)
#   --idrange        : ID range (e.g., 0 10 to give the range (0, 10))
#
# Commands to indicate the array to be transferred:
#   --array          : Select array. Options are: 7M, TM2, TM1, ALL
#
# Command to run all processing steps without stopping:
#   --serial         : run all the steps without stopping
#                      currently available for TM1 only
#
# Command to indicate if MPICASA is used (parallel):
#   --mpicores       : N (number of cores; 0 is NOT mpi parallel)
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
                    help='OPTIONAL: Select array: 7M, TM2, TM1, ALL')
#
parser.add_argument('--serial', action='store_true',
                    help='OPTIONAL: Run all steps at once (only for TM1)')
#
parser.add_argument('--mpicores', nargs=1, type=int,
                    help='OPTIONAL: Number of cores (parallel) to use in CASA \
                            0: (default) standard CASA run (NO mpi-parallel) \
                            N: MPI with command mpicasa -n N')
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
    #my_arrays = ['7M', 'TM2']

#-----------------------------------------------------------------------
# Define number of cores to use in mpicasa
#
# Default value is 0
#
if (args.mpicores == None):
    my_mpiCores = 0
    print("... using one single core (no MPI parallel)")

if (args.mpicores != None):
    my_mpiCores = int(args.mpicores[0])
    print("... " + str(my_mpiCores) + " cores selected for MPI parallel")
#
########################################################################


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

#-----------------------------------------------------------------------
# Define file that will contain the final EXECUTABLE commands
#
my_executeFile = 'my_executeImaging.sh'
my_executeFileStep0 = 'my_executeImagingStep0.sh'
os.system('rm -rf ' + my_executeFile)
os.system('rm -rf ' + my_executeFileStep0)

#-----------------------------------------------------------------------
# Process selected sources
#
my_is = my_sourceIDs
for i in my_is:
    
    my_source = my_sources[i]
    
    print(" ")
    print("Processing (ID: " + str(i) + ") source " + str(my_source) + "...")
    
    for my_array in my_arrays:
        
        if my_array == '7M':
            my_totalSteps = 6   # previously it was 5 (0 and 1 together)
        if my_array == 'TM2':
            my_totalSteps = 15  # previously it was 14 (0 and 1 together)
        if my_array == 'TM1':
            my_totalSteps = 11  # 
        
        print("... imaging of the " + my_array + " array")
        
        # Create directories where visibilities are stored
        #
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array)
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB')
        
        # Temporary (after setting up GitHub). This has to be removed after new run
        #os.system('mv /p/scratch/almagal/data/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + my_array + '/perEB/*.tar ' +  my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB/.')
        
        # Create directories where pipeline results will be stored
        #
        #os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/pipeline')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array)
        my_pipelineDirectory = my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array
        
        # Evaluate if there are calibrated files produced for the selected source
        #
        my_sourceSBPath = my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB/'
        my_sourceSBPaths, my_sourceSBDirs, my_sourceSBFiles = next(os.walk(my_sourceSBPath))
        
        # Evaluate if there are calibrated files produced for the selected source in the archived directory
        #
        #my_sourceARCHIVEPath = '/p/largedata/almagaldata/data/archive/2019.1.00195.L/sources/' + str(my_source) + '/calibrated/' + my_array + '/perEB/'
        #my_sourceARCHIVEPaths, my_sourceARCHIVEDirs, my_sourceARCHIVEFiles = next(os.walk(my_sourceARCHIVEPath))
        
        # If data available
        #
        if len(my_sourceSBFiles) >= 1:
        #if len(my_sourceARCHIVEFiles) >= 1:
            
            if (os.path.isfile(my_pipelineDirectory + '/transferred.txt') == True):
                
                # If data have been pipeline-processed and transferred to the storage location
                #
                print("... " + my_array + " data processed and transferred")
                
            else:
                
                # If pipeline has not been completely processed
                #
                if (os.path.isfile(my_pipelineDirectory + '/finished_all.txt') == False) and (os.path.isfile(my_pipelineDirectory + '/active.txt') == False) and (os.path.isfile(my_pipelineDirectory + '/inQueue.txt') == False):
                    
                    for my_step in range(0, my_totalSteps):
                        
                        if (os.path.isfile(my_pipelineDirectory + '/finished_step' + str(my_step) + '.txt') == False):
                            
                            print("... " + my_array + " step " + str(my_step) + " has to be applied")
                            
                            #
                            # Create temporary file to indicate the running step
                            #
                            os.system("touch " +  my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/pipeline/" + str(my_array) + "/running_step" + str(my_step) + ".txt")
                            
                            #
                            # Modify the script that will be executed
                            #
                            if args.serial == True:
                                my_baseScript = "scriptForImaging"+str(my_array)+"_serial"
                            else:
                                my_baseScript = "scriptForImaging"+str(my_array)
                            os.system("cp -rp "+str(my_baseScript)+".py tmp_"+str(my_baseScript)+".py")
                            fin = open("tmp_"+str(my_baseScript)+".py", "rt")
                            data = fin.read()
                            data = data.replace("ToModifySOURCE", str(my_source))
                            data = data.replace("ToModifyTELESCOPE", str(my_array))
                            data = data.replace("ToModifySTEPS", "["+str(my_step)+"]")
                            data = data.replace("ToModifyCURRENTSTEP", "step"+str(my_step))
                            data = data.replace("ToModifyMAINPATH", str(my_mainPath))
                            data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                            data = data.replace("ToModifySTORAGEPATH", str(my_storagePath))
                            fin.close()
                            fin = open("tmp_"+str(my_baseScript)+".py", "wt")
                            fin.write(data)
                            fin.close()
                            os.system("mv tmp_"+str(my_baseScript)+".py "+str(my_baseScript)+"_" + str(i) + "_" + str(my_array) + ".py")
                            
                            #
                            # Modify the mainScriptForImagingARRAY.sh file
                            #
                            if args.serial == True:
                                my_baseMainScript = "mainScriptForImaging"+str(my_array)+"_serial"
                            else:
                                my_baseMainScript = "mainScriptForImaging"+str(my_array)
                            os.system("cp -rp "+str(my_baseMainScript)+".sh tmp_"+str(my_baseMainScript)+".sh")
                            fin = open("tmp_"+str(my_baseMainScript)+".sh", "rt")
                            data = fin.read()
                            data = data.replace("ToModifyRCDIR", "myRCDIR_"+str(i)+"_"+str(my_array))
                            data = data.replace("ToModifySCRIPT", str(my_baseScript)+"_"+str(i)+"_"+str(my_array))
                            data = data.replace("ToModifySOURCE", str(my_source))
                            data = data.replace("ToModifyTELESCOPE", str(my_array))
                            data = data.replace("ToModifyCURRENTSTEP", "step"+str(my_step))
                            data = data.replace("ToModifyMAINPATH", str(my_mainPath))
                            data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                            data = data.replace("ToModifySTORAGEPATH", str(my_storagePath))
                            data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                            data = data.replace("ToModifyRUNNINGCOMPUTER", str(my_workstation))
                            data = data.replace("ToModifyMPICORES", str(my_mpiCores))
                            fin.close()
                            fin = open("tmp_"+str(my_baseMainScript)+".sh", "wt")
                            fin.write(data)
                            fin.close()
                            os.system("mv tmp_"+str(my_baseMainScript)+".sh "+str(my_baseMainScript)+"_" + str(i) + "_" + str(my_array) + ".sh")
                            os.system("chmod a+x "+str(my_baseMainScript)+"_" + str(i) + "_" + str(my_array) + ".sh")
                            
                            #
                            # Modify the run batch script
                            #
                            #
                            os.system("cp -rp run_"+str(my_baseMainScript)+" tmp_run_"+str(my_baseMainScript))
                            fin = open("tmp_run_"+str(my_baseMainScript), "rt")
                            data = fin.read()
                            data = data.replace(str(my_baseMainScript), str(my_baseMainScript)+"_"+str(i)+"_"+str(my_array))
                            fin.close()
                            fin = open("tmp_run_"+str(my_baseMainScript), "wt")
                            fin.write(data)
                            fin.close()
                            os.system("mv tmp_run_"+str(my_baseMainScript)+" run_"+str(my_baseMainScript)+"_" + str(i) + "_" + str(my_array))
                            os.system("chmod a+x run_"+str(my_baseMainScript)+"_" + str(i) + "_" + str(my_array))
                            
                            #
                            # Modify the default-init.py file
                            #
                            os.system("cp -rp default-init.py "+str(my_source)+"_default-init.py")
                            fin = open(str(my_source)+"_default-init.py", "rt")
                            data = fin.read()
                            data = data.replace("ToModifySOURCE", str(my_source))
                            data = data.replace("ToModifyRUNNINGPATH", str(my_runningPath))
                            data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                            fin.close()
                            fin = open(str(my_source)+"_default-init.py", "wt")
                            fin.write(data)
                            fin.close()
                            
                            os.system('mkdir -p ' + my_runningPath + '/.myRCDIR_' + str(i) + '_' + str(my_array) + '.mycasa')
                            os.system('cp -rp ' + my_mainPath + '/mpi-runs/' + str(my_source) + '_default-init.py ' + my_runningPath + '/.myRCDIR_' + str(i) + '_' + str(my_array) + '.mycasa/init.py')

                            #
                            # Append executable command to main execution file
                            #
                            if (my_workstation == "JSC") and (my_step == 0) and (args.serial == False):
                                with open(my_executeFileStep0, 'a') as fd:
                                    #fd.write("touch  " + my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/pipeline/" + str(my_array) + "/inQueue.txt\n")
                                    #if (my_workstation == "JSC"):
                                    #    fd.write("sbatch run_mainScriptForImaging"+str(my_array)+"_"+str(i)+"_"+str(my_array)+"\n")
                                    #else:
                                    fd.write("./"+str(my_baseMainScript)+"_"+str(i)+"_"+str(my_array)+".sh\n")
                                
                            else:
                                with open(my_executeFile, 'a') as fd:
                                    fd.write("touch  " + my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/pipeline/" + str(my_array) + "/inQueue.txt\n")
                                    if (my_workstation == "JSC"):
                                        fd.write("sbatch run_"+str(my_baseMainScript)+"_"+str(i)+"_"+str(my_array)+"\n")
                                    else:
                                        fd.write("./"+str(my_baseMainScript)+"_"+str(i)+"_"+str(my_array)+".sh\n")
                            #
                            # Make the run bash script executable
                            #
                            if (os.path.isfile(my_executeFile) == True):
                                os.system("chmod a+x " + my_executeFile)
                            if (os.path.isfile(my_executeFileStep0) == True):
                                os.system("chmod a+x " + my_executeFileStep0)
                            
                            #
                            # Create temporary file to indicate that it is in the queue
                            #os.system("touch " +  my_mainPath + "/2019.1.00195.L/sources/" + str(my_source) + "/pipeline/" + str(my_array) + "/inQueue.txt")
                            
                            break
                        
                        else:
                            
                            print("... " + my_array + " step " + str(my_step) + " already processed")
                
                else:
                    
                    if (os.path.isfile(my_pipelineDirectory + '/finished_all.txt') == True):
                        print("... " + my_array + " already processed")
                    
                    if (os.path.isfile(my_pipelineDirectory + '/active.txt') == True):
                        print("... " + my_array + " is running, it is currently active")
                    
                    if (os.path.isfile(my_pipelineDirectory + '/inQueue.txt') == True):
                        print("... " + my_array + " in the queue")
        
        # If data NOT available
        #
        elif len(my_sourceSBFiles) == 0:
        #elif len(my_sourceARCHIVEFiles) == 0:
            
            print("... " + "No data yet for source " + str(my_source) + " with the " + my_array + " array")
