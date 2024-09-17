########################################################################
#
#                   ALMAGAL processing pipeline 
#
#
# 
# Script number 3                        created by Alvaro Sanchez-Monge
#
# Previous step:   createIndividual_scriptForImaging.py
# Next step:       createIndividual_scriptForJointDeconvolution.py
# 
# Description:      Python script to convert image products into FITS
#                   files and to store the products and pipeline
#                   weblogs in the archive directory
# 
# Required:
#   - database.xlsx file containing names and MOUS directory tree
#   - pipeline products created by createIndividual_scriptForImaging.py
#
# Execution:
#   - python tarPipelineProducts.py
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
    #my_arrays = ['7M', 'TM2', 'TM1']
    my_arrays = ['7M', 'TM2']
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
df = pd.read_excel('../database/database.xlsx', sheet_name='Sheet1', index_col=0)
df['Source'] = df.index

# Create list with all the sources
#
my_sources = df['Source']

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
        
        print("... imaging of the " + my_array + " array")
        
        # Create directories where visibilities are stored
        #
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array)
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB')
        
        # Create directories where pipeline results will be stored
        #
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array)
        my_pipelineDirectory = my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array
        
        # Create directories where images are stored
        #
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images')
        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/' + my_array)
        
        # Evaluate if there are calibrated files produced for the selected source
        #
        my_sourceSBPath = my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB/'
        my_sourceSBPaths, my_sourceSBDirs, my_sourceSBFiles = next(os.walk(my_sourceSBPath))
        
        # If data available
        #
        if len(my_sourceSBFiles) >= 1:
            
            # If data have not been transferred to the storage location
            #
            if (os.path.isfile(my_pipelineDirectory + '/transferred.txt') == False):
            
                # If pipeline has been completely processed
                #
                if (my_array == '7M'):
                    my_finishedLastStep = 'finished_step5.txt'
                if (my_array == 'TM2'):
                    my_finishedLastStep = 'finished_step14.txt'
                
                if (os.path.isfile(my_pipelineDirectory + '/' + my_finishedLastStep) == True) or (os.path.isfile(my_pipelineDirectory + '/finished_all.txt') == True):
                    
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
                    if (os.path.isfile(my_pipelineDirectory + '/almagal.tar') == False):
                        
                        print("... " + my_array + " pipeline completed")
                        print("... " + my_array + " images being copied")
                        
                        os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/' + my_array + '/pipeline')
                        os.system("cp -rp " + my_pipelineDirectory + "/almagal/*image " + my_individualPath + "/" + str(my_source) + "/images/" + my_array + "/pipeline/.")
                        os.system("cp -rp " + my_pipelineDirectory + "/almagal/*image.pbcor " + my_individualPath + "/" + str(my_source) + "/images/" + my_array + "/pipeline/.")
                        os.system("cp -rp " + my_pipelineDirectory + "/almagal/cont.dat " + my_individualPath + "/" + str(my_source) + "/images/" + my_array + "/pipeline/.")
                        if (os.path.isfile(my_pipelineDirectory + '/almagal/original.cont.dat') == True):
                            os.system("cp -rp " + my_pipelineDirectory + "/almagal/original.cont.dat " + my_individualPath + "/" + str(my_source) + "/images/" + my_array + "/pipeline/.")
                        
                        print("... " + my_array + " pipeline products are being compressed")
                        
                        my_runningDirectoryTMP = os.getcwd()
                        os.chdir(my_pipelineDirectory+'/almagal')
                        my_pipelineName = [f for f in os.listdir(my_pipelineDirectory+'/almagal') if f.endswith(".context")][0][:-8]
                        my_pipelineName = str(my_pipelineName) + " cont.dat"
                        if (os.path.isfile(my_pipelineDirectory + '/almagal/original.cont.dat') == True):
                            my_pipelineName = str(my_pipelineName) + " original.cont.dat"
                        os.system("tar -cf pipeline-weblog.tar " + str(my_pipelineName))
                        os.system("mv pipeline-weblog.tar ../")
                        
                        os.chdir(my_pipelineDirectory)
                        os.system("tar -cf almagal.tar almagal finished_step*")
                        
                        print("... " + my_array + " clean up the pipeline directory")
                        
                        os.system("rm -rf almagal")
                        os.system("rm -rf finished*.txt")
                        os.system("touch finished_all.txt")
                        os.chdir(my_runningDirectoryTMP)
                    
                    else:
                        
                        print("... " + my_array + " pipeline products already compressed")
                    
                    # Create FITS files of the final images and compress the images
                    #
                    my_ImageDirectory = my_individualPath + "/" + str(my_source) + "/images/" + my_array
                    
                    if (os.path.isfile(my_ImageDirectory + '/pipeline-fits.tar') == False):
                        
                        # Create FITS files of the final images and compress the images
                        #
                        #my_ImageDirectory = my_individualPath + "/" + str(my_source) + "/images/" + my_array
                        #
                        #if (os.path.isfile(my_ImageDirectory + '/pipeline-fits.tar') == False):
                        
                        print("... " + my_array + " create FITS images")
                        
                        # Determine which pipeline stages were used when producing the final images
                        #
                        if (os.path.isfile(my_ImageDirectory + '/pipeline/original.cont.dat') == True):
                            
                            # Define the basenames of the images to be converted into FITS
                            #
                            if (my_array == '7M'):
                                my_ImageNames = ["oussid.s13_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
                                my_DirtyNames = ["oussid.s13_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
                            if (my_array == 'TM2'):
                                my_ImageNames = ["oussid.s19_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s21_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s23_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s25_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s27_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
                                my_DirtyNames = ["oussid.s19_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s21_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s23_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s25_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s27_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
                            
                            # Create a CASA python script to convert IMAGE files into FITS files
                            #
                            my_CASAscriptFileName = "tmpExecute_" + str(my_source) + ".py"
                            os.system("rm -rf " + my_CASAscriptFileName)
                            os.system("touch " + my_CASAscriptFileName)
                            
                            with open(my_CASAscriptFileName, 'w') as writer:
                                for my_ImageName in my_ImageNames:
                                    if (os.path.isdir(my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image") == True):
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image.fits', dropdeg=True, overwrite=True)\n")
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image.pbcor',fitsimage='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image.pbcor.fits',dropdeg=True, overwrite=True)\n")
                                    elif (os.path.isdir(my_ImageDirectory+"/pipeline/"+my_ImageName+".image") == True):
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".image', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".image.fits', dropdeg=True, overwrite=True)\n")
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".image.pbcor', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".image.pbcor.fits', dropdeg=True, overwrite=True)\n")
                                
                                for my_DirtyName in my_DirtyNames:
                                    if (os.path.isdir(my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image") == True):
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image.fits', dropdeg=True, overwrite=True)\n")
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image.pbcor',fitsimage='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image.pbcor.fits',dropdeg=True, overwrite=True)\n")
                                    elif (os.path.isdir(my_ImageDirectory+"/pipeline/"+my_DirtyName+".image") == True):
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".image', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".image.fits', dropdeg=True, overwrite=True)\n")
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".image.pbcor', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".image.pbcor.fits', dropdeg=True, overwrite=True)\n")
                        
                        else:
                            
                            # Define the basenames of the images to be converted into FITS
                            #
                            if (my_array == '7M'):
                                my_ImageNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
                                my_DirtyNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
                            if (my_array == 'TM2'):
                                my_ImageNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s11_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s13_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
                                my_DirtyNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s11_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s13_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
                            
                            # Create a CASA python script to convert IMAGE files into FITS files
                            #
                            my_CASAscriptFileName = "tmpExecute_" + str(my_source) + ".py"
                            os.system("rm -rf " + my_CASAscriptFileName)
                            os.system("touch " + my_CASAscriptFileName)
                            
                            with open(my_CASAscriptFileName, 'w') as writer:
                                for my_ImageName in my_ImageNames:
                                    if (os.path.isdir(my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image") == True):
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image.fits', dropdeg=True, overwrite=True)\n")
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image.pbcor',fitsimage='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".reclean.image.pbcor.fits',dropdeg=True, overwrite=True)\n")
                                    elif (os.path.isdir(my_ImageDirectory+"/pipeline/"+my_ImageName+".image") == True):
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".image', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".image.fits', dropdeg=True, overwrite=True)\n")
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".image.pbcor', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_ImageName+".image.pbcor.fits', dropdeg=True, overwrite=True)\n")
                                
                                for my_DirtyName in my_DirtyNames:
                                    if (os.path.isdir(my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image") == True):
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image.fits', dropdeg=True, overwrite=True)\n")
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image.pbcor',fitsimage='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".reclean.image.pbcor.fits',dropdeg=True, overwrite=True)\n")
                                    elif (os.path.isdir(my_ImageDirectory+"/pipeline/"+my_DirtyName+".image") == True):
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".image', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".image.fits', dropdeg=True, overwrite=True)\n")
                                        writer.write("exportfits(imagename='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".image.pbcor', fitsimage='"+my_ImageDirectory+"/pipeline/"+my_DirtyName+".image.pbcor.fits', dropdeg=True, overwrite=True)\n")
                        
                        #
                        # Modify the default-init.py file
                        #
                        os.system("cp -rp default-transfer-init.py tmp_default-transfer-init.py")
                        fin = open("tmp_default-transfer-init.py", "rt")
                        data = fin.read()
                        data = data.replace("ToModifySOFTWAREPATH", str(my_softwarePath))
                        fin.close()
                        fin = open("tmp_default-transfer-init.py", "wt")
                        fin.write(data)
                        fin.close()
                        
                        os.system('mkdir -p .myRCDIR_' + str(i) + '_' + str(my_array) + '.mycasa')
                        os.system('cp -rp ' + my_mainPath + '/mpi-runs/tmp_default-transfer-init.py .myRCDIR_' + str(i) + '_' + str(my_array) + '.mycasa/init.py')
                        
                        os.system(my_softwarePath + "/casa-pipeline-release-5.6.1-8.el7/bin/casa --rcdir .myRCDIR_" + str(i) + "_" + str(my_array) + ".mycasa --nologger --nogui -c "+ my_CASAscriptFileName)
                        
                        os.system('rm -rf ' + my_ImageDirectory + '/pipeline/cont.dat')
                        os.system('rm -rf ' + my_ImageDirectory + '/pipeline/original.cont.dat')
                        my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_ImageDirectory+'/pipeline'))
                        print("... number of files available (FITS files): " + str(len(my_TMPfiles)))
                        my_runningDirectoryTMP = os.getcwd()
                        os.chdir(my_ImageDirectory)
                        os.system("tar -cf pipeline-fits.tar pipeline/*.fits")
                        # Commented out to save disk space
                        #os.system("tar -cf pipeline-products.tar pipeline/*.*")
                        
                        '''
                        print("... " + my_array + " clean up the image directory")
                        
                        os.system("rm -rf pipeline")
                        os.chdir(my_runningDirectoryTMP)
                        '''
                        #os.system('rm -rf ' + my_pipelineDirectory + '/transferred.txt')
                        
                    else:
                        
                        print("... " + my_array + " FITS images created and compressed")
                    
                    if (os.path.isfile(my_pipelineDirectory + '/almagal.tar') == True) and (os.path.isfile(my_ImageDirectory + '/pipeline-fits.tar') == True):
                        
                        print("... " + my_array + " already compressed")
                        
                        # Transfer to storage directory, only if this is different to the main directory
                        #
                        if (my_storagePath != my_mainPath):
                            
                            print("... storage path is " + my_storagePath)
                            
                            if (os.path.isfile(my_pipelineDirectory + '/transferred.txt') == False):
                                
                                print("... " + my_array + " data being transferred")
                                
                                # Copy calibrated data to LARGEDATA
                                #
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/')
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/' + my_array)
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB')
                                os.system('cp -rp ' + my_individualPath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB/*.* ' + my_individualStoragePath + '/' + str(my_source) + '/calibrated/' + my_array + '/perEB/.')
                                
                                # Copy pipeline products to LARGEDATA
                                #
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/')
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/' + my_array)
                                os.system('cp -rp ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array + '/*.* ' + my_individualStoragePath + '/' + str(my_source) + '/pipeline/' + my_array + '/.')
                                
                                # Copy image products to LARGEDATA
                                #
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/images/')
                                os.system('mkdir -p ' + my_individualStoragePath + '/' + str(my_source) + '/images/' + my_array)
                                os.system('cp -rp ' + my_individualPath + '/' + str(my_source) + '/images/' + my_array + '/*.* ' + my_individualStoragePath + '/' + str(my_source) + '/images/' + my_array + '/.')
                                
                                # Create dummy file to indicate that data were transferred
                                #
                                os.system('touch ' + my_pipelineDirectory + '/transferred.txt')
                                
                                # Clean up directory in SCRATCH
                                os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/pipeline/' + my_array + '/*.tar')
                                os.system('rm -rf ' + my_individualPath + '/' + str(my_source) + '/images/' + my_array + '/*.tar')
                                
                                
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
                
        # If data NOT available
        #
        elif len(my_sourceSBFiles) == 0:
            
            print("... " + "No data yet for source " + str(my_source) + " with the " + my_array + " array")
