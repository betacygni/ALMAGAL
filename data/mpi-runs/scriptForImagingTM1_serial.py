# This script runs the ALMAGAL TM1-array imaging pipeline procedure,
# and then if needed it:
#
# - refinds: redoes the findcontinuum using the cleaned cubes from the
#   first run. It requires the REFIND.py script
#
# - recleans bright unmasked channels after amending the mask to "seed"
#   these channels with a starting mask
#
# This script assumes that it will be run on only one TARGET
# Major parts of the script written by Crystal Brogan and Todd Hunter
#
# This is a template/master script that is updated when running:
# > python createIndividual_scriptForImaging.py
#

#-----------------------------------------------------------------------
#
# Import python packages
#
import os
import sys
import glob
import numpy as np
import astropy
from astropy.io import fits
import subprocess
import shutil
import analysisUtils as au

#-----------------------------------------------------------------------
# Define main paths, variables and steps to process
#
# Paths:
#
my_mainPath = 'ToModifyMAINPATH'             # e.g. '/p/scratch/almagal/data'
my_runningPath = 'ToModifyRUNNINGPATH'       # e.g. '/dev/shm'
my_almagalRunDir = 'almagal_ToModifySOURCE'  # e.g. 'almagal_SOURCE'

# Variables:
#
my_source = 'ToModifySOURCE'                 # e.g. '49143'
my_telescope = 'ToModifyTELESCOPE'           # e.g. 'TM1'

# Steps to process:
#
mysteps = ToModifySTEPS                      # e.g. [0] or [0, 1, 2, 3, 4]
mycurrentstep = 'ToModifyCURRENTSTEP'        # e.g. "step0" or "steps"

#-----------------------------------------------------------------------
# Define steps environment
#
thesteps = [0]
step_title = {0: 'Image continuum and individual spectral windows',
              11: 'Re-clean bright unmasked channels'}
try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps


#-----------------------------------------------------------------------
#
# Define functions
#

# Function to image the cubes for different spectral windows
#
def my_functionImagingCube(function_spw):
    
    Target = my_source 
    vispath = str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/'
    
    # Read pipeline context filename
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/cont.dat') == True):
        my_pipelinePath = str(my_runningPath) + '/' + str(my_almagalRunDir)
        my_pipelineName = [f for f in os.listdir(my_pipelinePath) if f.endswith(".context")][0][:-8]
        my_pipelinePath = my_pipelinePath + "/" + my_pipelineName
    elif (os.path.isfile(my_runningPath + '/cont.dat') == True):
        my_pipelinePath = str(my_runningPath)
        my_pipelineName = [f for f in os.listdir(my_pipelinePath) if f.endswith(".context")][0][:-8]
        my_pipelinePath = my_pipelinePath + "/" + my_pipelineName
    
    h_resume(str(my_pipelineName)+'.context')
    hif_makeimlist(intent='TARGET', robust=0.5, parallel='automatic', specmode='cube', spw=str(function_spw))
    hif_makeimages(tlimit=2.0,
                    hm_perchanweightdensity=True, 
                    hm_masking='auto',
                    hm_minbeamfrac=0.3,
                    hm_noisethreshold=5.0,
                    hm_sidelobethreshold=3.0,
                    hm_lownoisethreshold=1.5,
                    hm_negativethreshold=7.0,
                    parallel='automatic')
    h_save(str(my_pipelineName)+'.context')


# Function to re-image the cubes if some channels were originally not
# properly masked.
#
def my_functionReImagingCube(function_spw):
    
    Target = my_source 
    vispath = str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/'
    
    print('::: ALMAGAL command ::: Check information for unmasked cleaning')
    print(cubeInfo)
    print("    ...")
    print(cubeInfo[3])
    print("    ...")
    
    # Determine the threshold that was used to produce the images
    # Originally it was read from the weblog
    # parameter: float(cubeInfo[3][2].split()[0])
    # However, for some sources the weblog information is not 
    # stored (some bug in the pipeline task ?)
    # This is avoided by reading this value from the casapy.log file
    #
    cleanrms = 0.0 # initialize to 0
    cleanCommands = au.extractTcleanCommands(pipeLog+'/html/stage'+str(stage)+'/casapy.log',task='tclean', 
                                                stage=stage,spw=str(function_spw))
    for cleanCommand in cleanCommands:
        iterImage = 1
        if cleanCommand.find("iter%d" % (iterImage)) > 0:
            parts = cleanCommand.split(",")
            for part in parts:
                if part.find("threshold") > 0 and part.find("Jy") > 0:
                    subparts = part.split("'")
                    for subpart in subparts:
                        if subpart.find("mJy") > 0:
                            cleanrms = float(subpart[:-3])
                        elif subpart.find("Jy") > 0:
                            cleanrms = float(subpart[:-2])
    print("The cleaning threshold used is:")
    print(cleanrms)
    
    # Main function
    # Written by Crystal Brogan and Todd Hunter
    #
    print("my function spw is:")
    print(function_spw)
    for spw in [function_spw]: 
        if (cleanrms > 0.0):
            print(spw)
            cubeName=cubes[spw]
            print(cubes)
            print(cubeName)
            os.system('rm -rf '+cubeName+'.reclean.*')
            extrachannels=au.amendMaskForCube(cubeName,
                                              intensityThreshold=cleanrms*3.,  # times 3 added by ASM
                                              maskThreshold=cleanrms*maskThreshFactor,
                                              maskThresholdFraction=maskThreshFraction,
                                              npixels=25,pblimit=0.3,overwriteMask=False,cleanup=True,
                                              masknameInsert='.reclean',
                                              verbose=False,dryrun=False)
            #extrachannels=au.amendMaskForCube(cubeName,
            #                                  intensityThreshold=float(cubeInfo[3][spw].split()[0]),
            #                                  maskThreshold=float(cubeInfo[3][spw].split()[0])*maskThreshFactor,
            #                                  maskThresholdFraction=maskThreshFraction,
            #                                  npixels=25,pblimit=0.3,overwriteMask=False,cleanup=True,
            #                                  masknameInsert='.reclean',
            #                                  verbose=False,dryrun=False)
            if len(extrachannels) == 0:
                print('::: ALMAGAL command ::: No bright channels are unmasked')
                casalog.post("FOR SPW=%d NO BRIGHT CHANNELS ARE UNMASKED"%(spw))
                immoments(imagename=cubeName.replace('.image','')+'.residual',moments=[8],
                          outfile=cubeName.replace('.image','')+'.residual.mom8')
                au.pipelineImview(cubeName.replace('.image','')+'.residual.mom8',plotfile=True)
            else:
                casalog.post("FOR SPW=%d THE UNMASKED BRIGHT CHANNELS ARE %s"%(spw,extrachannels))      
                for i in ['.image','.residual','.psf','.model','.pb','.sumwt']:
                    shutil.copytree(cubeName.replace('.image',i),cubeName.replace('.image','')+'.reclean'+i)

                au.plotSpectrumFromMask(cubeName,plotfile=True,
                                        overlayCleanMaskChannels=extrachannels)
                cleanCommand = au.extractTcleanCommandsAndModify(pipeLog+'/html/stage'+str(stage)+'/casapy.log',task='tclean', 
                                                                 stage=stage,spw=str(spw),imagenameAppend='.reclean',
                                                                 visPrepend=vispath,
                                                                 newGrowiterations=newGrow,iterImage=1,
                                                                 output='restart_'+cubeName+'.py')
                print('::: ALMAGAL command ::: Restart imaging with new mask')
                execfile('restart_'+cubeName+'.py')
                au.plotSpectrumFromMask(cubeName.replace('.image','')+'.reclean.image',
                                        plotfile=True,
                                        overlayCleanMaskChannels=extrachannels)
                for moment in [0,8]:
                    immoments(imagename=cubeName.replace('.image','')+'.reclean.image',moments=[moment],
                              outfile=cubeName.replace('.image','')+'.reclean.image.mom'+str(moment))        
                
                immoments(imagename=cubeName.replace('.image','')+'.reclean.residual',moments=[8],
                          outfile=cubeName.replace('.image','')+'.reclean.residual.mom8')
                au.pipelineImview(cubeName.replace('.image','')+'.reclean.image.mom8',plotfile=True)
                au.pipelineImview(cubeName.replace('.image','')+'.reclean.residual.mom8',plotfile=True)


########################################################################
#
# STEP 0: 
# 
# Image continuum and individual spectral windows
#
mystep = 0
if(mystep in thesteps):
    
    # Copy data to be processed in the running disk
    #
    os.system("mkdir -p " + str(my_runningPath) + "/" + str(my_almagalRunDir))
    os.system("mkdir -p " + str(my_runningPath) + "/" + str(my_almagalRunDir) + "/processing")
    os.system("cp -rp " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/calibrated/" + my_telescope + "/perEB/* " + str(my_runningPath) + "/" + str(my_almagalRunDir) + "/processing/.")
    #os.system("cp -rp /p/largedata/almagaldata/data/archive/2019.1.00195.L/sources" + my_source + "/calibrated/" + my_telescope + "/perEB/* " + str(my_runningPath) + "/" + str(my_almagalRunDir) + "/processing/.")
    
    # Evaluate files and directories copied in the processing directory
    #
    my_sourcePaths, my_sourceDirs, my_sourceFiles = next(os.walk(str(my_runningPath)+'/'+str(my_almagalRunDir)+'/processing'))
    
    # Untar the visibility files
    #
    for my_sourceFile in my_sourceFiles:
        os.system('tar -xf ' + str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/' + str(my_sourceFile) + ' -C ' + str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/.')
    os.system('rm -rf ' + str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/*.tar')
    
    # Move the untar'ed file to the processing directory
    #
    os.system('mv ' + str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/2019.1.00195.L/sources/' + my_source + '/calibrated/' + my_telescope + '/perEB/* ' + str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/.')
    #os.system('mv ' + str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing' + str(my_mainPath) + '/2019.1.00195.L/sources/' + my_source + '/calibrated/' + my_telescope + '/perEB/* ' + str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/.')
    os.system('rm -rf ' + str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/2019.1.00195.L')
    
    #-------------------------------------------------------------------
    #
    # Initial run of adopted pipeline procedure
    #
    Target = my_source
    vispath = str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/'
    vislist = sorted(glob.glob(vispath+'*cal'))
    for vis in vislist:
        au.updateRepresentativeSource(vis,Target)
    import findContinuumCycle8 as fc


    __rethrow_casa_exceptions = True
    context = h_init()
    context.set_state('ProjectSummary', 'proposal_code', '2019.1.00195.L')
    context.set_state('ProjectSummary', 'proposal_title', 'ALMAGAL')
    print vislist

    print('::: ALMAGAL command ::: Starting the pipeline procedures, step ' + str(mystep))


    # Prepare files and directories and determine continuum with pipeline
    #
    # Main tasks:  stage1:   hifa_importdata
    #
    hifa_importdata(dbservice=False, asimaging=True, vis=vislist)
    h_save()
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step0.txt")
    
    # Prepare files and directories and determine continuum with pipeline
    #
    # Main tasks:  stage2:   hif_makeimlist
    #              stage3:   hif_findcont
    #              stage4:   hif_uvcontfit
    #              stage5:   hif_uvcontsub
    #              stage6:   hif_makeimlist
    #              stage7:   hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step1.txt")
    
    my_pipelineName = [f for f in os.listdir(str(my_runningPath)+'/'+str(my_almagalRunDir)) if f.endswith(".context")][0][:-8]
    h_resume(str(my_pipelineName)+'.context')
    hif_makeimlist(intent='TARGET', robust=0.5, parallel='automatic', specmode='mfs')
    hif_findcont(parallel='automatic')
    hif_uvcontfit(fitorder=1, solint='int')
    hif_uvcontsub(pipelinemode="automatic")
    hif_makeimlist(spw='0,1', intent='TARGET', robust=0.5, parallel='automatic', specmode='cont')
    hif_makeimages(tlimit=2.0,
                    hm_masking='auto',
                    hm_minbeamfrac=0.3,
                    hm_noisethreshold=5.0,
                    hm_sidelobethreshold=3.0,
                    hm_lownoisethreshold=1.5,
                    hm_negativethreshold=0.0,
                    parallel='automatic')
    h_save(str(my_pipelineName)+'.context')
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step1.txt")
    
    
    # Create cube image of spectral window 0
    #
    # Main tasks:  stage8:   hif_makeimlist
    #              stage9:   hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step2.txt")
    
    my_functionImagingCube(0)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step2.txt")
    
    
    # Create cube image of spectral window 1
    #
    # Main tasks:  stage10:  hif_makeimlist
    #              stage11:  hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step3.txt")
    
    my_functionImagingCube(1)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step3.txt")
    
    
    # Create cube image of spectral window 2
    #
    # Main tasks:  stage12:  hif_makeimlist
    #              stage13:  hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step4.txt")
    
    my_functionImagingCube(2)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step4.txt")
    
    
    # Create cube image of spectral window 3
    #
    # Main tasks:  stage14:  hif_makeimlist
    #              stage15:  hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step5.txt")
    
    my_functionImagingCube(3)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step5.txt")
    
    
    ########################################################################
    # REFIND procedure:
    # Notes from Crystal Brogan
    #
    # For ALMAGAL, the default pipeline findcont has two distinct reasons
    # that the results can be non-optimal (i.e. significant residual
    # emission in the "continuum channels" fc channels, as revealed by the
    # mom8_fc image):
    #
    # 1) Strong hot core sources require a compact mask to form the
    #    meanSpectrum to avoid beam dilution, otherwise the weaker hot core
    #    lines are visible to the mom8_fc, but are not adequately
    #    represented in the meanSpectrum. 
    # 2) Sources can also have spatially distinct weaker emission that is
    #    not included in the more restrictive mask that helps to overcome
    #    (1), and thus can never reach the mom_fc peaksigCut. This is
    #    especially true for the 13CO.
    #
    # The REFIND.py script starts at the "hot core" value of mom8minsnr=10
    # (default=4), and does an fc on the cleaned cube image. It then
    # compares the mom8_fc to the peaksigCut (maximum allowed residual in
    # fc channels), if it is above the limit, the sigmaFC is lowered to
    # exclude more channel ranges. This proceeds until the criteria is
    # met, or 5 iterations have been done. In order to address issue (2),
    # after 3 iterations, any bright emission in the current mom8_fc that
    # is outside the fc joint.mask is added to the joint.mask used by fc
    # and then a new meanSpectrum is created, the iterations then
    # continue. At this stage, the test datasets tend to reach a plateau
    # at around 8-10 sigma -- where findcont cannot distinguish the bad
    # ranges from good, though eventually the final bad channels are
    # thrown out if you do enough iterations (typically 12) usually a fair
    # amount of "good" badwidth is lost. So for the 6th iteration, 
    # we simply remove any remaining channels above sigmaCut.
    #
    # The InitpeaksigCut is currently set to 7 sigma in the mom8_fc, while
    # the peaksigCut used in the REFIND is 6. If one spw is found to be
    # above the limit, all spws are redone. It would be difficult to get
    # all the bits correct, if only spws above the limit are done. It will
    # have to wait for a future improvement. Note, it is not clear to me
    # that residuals of 6 or even 7 are all that consequential. After a 
    # larger sample it is done, we might want to raise at least the
    # InitpeaksigCut. 
    #
    # Key diagnostics are written to the casalog and can be grepped by a
    # search for "REFIND"
    #
    # A cont.dat file of the form required by the pipline is then
    # consolodated using fc.combineContDat, the original one is moved to
    # original.cont.dat.
    #
    # Further notes by Alvaro Sanchez-Monge
    # The method below, originally assumed that it was run in the same
    # instance of CASA that ran the first section. However, it is possible
    # to re-start every section/step. You need to:
    # - use the already existing context file
    #   e.g., h_resume('pipeline-20200516T155623.context')
    #         h_save('pipeline-20200516T155623.context')
    # - and you have to make sure that all the files are stored in the
    #   same directory where they were created. I.e., the full directory
    #   path to the working directory is the same as when the first
    #   section ran
    #
    ########################################################################
    #
    # Information needed for following STEPS
    #    
    print('::: ALMAGAL command ::: Setting up the information for the next steps')
    
    Target = my_source 
    vispath = str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/'
    
    # Read pipeline context filename
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/cont.dat') == True):
        my_pipelinePath = str(my_runningPath) + '/' + str(my_almagalRunDir)
        my_pipelineName = [f for f in os.listdir(my_pipelinePath) if f.endswith(".context")][0][:-8]
        my_pipelinePath = my_pipelinePath + "/" + my_pipelineName
    elif (os.path.isfile(my_runningPath + '/cont.dat') == True):
        my_pipelinePath = str(my_runningPath)
        my_pipelineName = [f for f in os.listdir(my_pipelinePath) if f.endswith(".context")][0][:-8]
        my_pipelinePath = my_pipelinePath + "/" + my_pipelineName
    
    # Create pipeline directory containing merged html output files (called stage90)
    os.system('mkdir -p ' + my_pipelinePath + '/html/stage90/')
    
    # Merge the output of the previous four steps into a single file for further processing
    os.system('cat ' + my_pipelinePath + '/html/stage9/casapy.log ' + my_pipelinePath + '/html/stage11/casapy.log ' + my_pipelinePath + '/html/stage13/casapy.log ' + my_pipelinePath + '/html/stage15/casapy.log > ' + my_pipelinePath + '/html/stage90/casapy.log')
    os.system('cat ' + my_pipelinePath + '/html/stage9/t2-4m_details.html ' + my_pipelinePath + '/html/stage11/t2-4m_details.html ' + my_pipelinePath + '/html/stage13/t2-4m_details.html ' + my_pipelinePath + '/html/stage15/t2-4m_details.html > ' + my_pipelinePath + '/html/stage90/t2-4m_details.html')
    os.system('cat ' + my_pipelinePath + '/html/stage9/t2-4m_details-container.html ' + my_pipelinePath + '/html/stage11/t2-4m_details-container.html ' + my_pipelinePath + '/html/stage13/t2-4m_details-container.html ' + my_pipelinePath + '/html/stage15/t2-4m_details-container.html > ' + my_pipelinePath + '/html/stage90/t2-4m_details-container.html')
    
    # Pick the most recent pipeline directory
    # and the stage number of the hif_makeimages for cubes
    # stage 90 is where the merge result of stage 9, 11, 13 and 15 is stored
    #
    pipeLog = sorted(glob.glob('pipeline-202*'), reverse=True)[1]
    stage = 90
    cubeInfo = au.cubeInfoFromWeblog(pipeLog, stage=stage, returnLists=True)
    #cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))
    stage = 9
    #cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))
    cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))
    stage = 11
    #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
    cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
    stage = 13
    #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
    cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
    stage = 15
    #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
    cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
    print("Test of cubes printed:")
    print(cubes)
    
    InitpeaksigCut = 7.0
    peaksigCut = 6.0        # peak S/N in mom8_fc
    npixCut = 10            # number of pixels above peaksigCut to be valid
    mom8minsnrmask = 10     # mask threshold for mom8 in fc joint.mask, independent rms calc
    
    Refind = False
    for spw in cubeInfo[1]:
        cube = cubes[spw]
        rms = float(cubeInfo[8][spw].split()[0])
        mom = cube+'.mom8_fc'
        stats = imstat(mom)
        peaksig = stats['max'][0]/rms
        npix = imstat(mom, mask='"'+mom+'"'+'>'+str(peaksigCut*rms))['npts']
        if len(npix) > 0:
            npix = npix[0]
        else:
            npix = 0
        if peaksig > InitpeaksigCut and npix > npixCut:
            Refind = True
        casalog.post("REFIND Initial: %s, %.3f, %.3f, %d"%(mom,stats['max'][0],peaksig,npix))
    
    
    # Refind the continuum if necessary
    #
    # Main tasks:  stage16:  hif_uvcontfit
    #              stage17:  hif_uvcontsub
    #              stage18:  hif_makeimlist
    #              stage19:  hif_makeimages
    #
    #-------------------------------------------------------------------
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step6.txt")
    
    Target = my_source 
    vispath = str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/'
    
    print('::: ALMAGAL command ::: Starting the pipeline procedures, step ' + str(mystep))
    if Refind == True:
        execfile('REFIND.py')
        newDats = sorted(glob.glob('*image_findContinuum.dat'))
        os.rename('cont.dat','original.cont.dat')
        fc.combineContDat(newDats)
        h_resume(str(my_pipelineName)+'.context')
        hif_uvcontfit(fitorder=1, solint='int')
        hif_uvcontsub(pipelinemode="automatic")
        hif_makeimlist(spw='0,1', intent='TARGET', robust=0.5, parallel='automatic', specmode='cont')
        hif_makeimages(tlimit=2.0,
                        hm_masking='auto', 
                        hm_minbeamfrac=0.3, 
                        hm_noisethreshold=5.0,
                        hm_sidelobethreshold=3.0,
                        hm_lownoisethreshold=1.5, 
                        hm_negativethreshold=0.0,
                        parallel='automatic')
        h_save(str(my_pipelineName)+'.context')
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step6.txt")
    
    
    # Re-image cube image of spectral window 0 if necessary
    #
    # Main tasks:  stage20:  hif_makeimlist
    #              stage21:  hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step7.txt")
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        
        my_functionImagingCube(0)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step7.txt")
    
    
    # Re-image cube image of spectral window 1 if necessary
    #
    # Main tasks:  stage22:  hif_makeimlist
    #              stage23:  hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step8.txt")
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        
        my_functionImagingCube(1)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step8.txt")
    
    
    # Main tasks:  stage24:  hif_makeimlist
    #              stage25:  hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step9.txt")
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        
        my_functionImagingCube(2)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step9.txt")
    
    
    # Main tasks:  stage26:  hif_makeimlist
    #              stage27:  hif_makeimages
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step10.txt")
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        
        my_functionImagingCube(3)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step10.txt")
    
    
    # Main tasks:  create FITS files and compress final products
    #              adapted from tarPipelineProducts.py script
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step90.txt")
    
    my_individualPath = my_mainPath + "/2019.1.00195.L/sources/"
    my_pipelineDirectory = my_individualPath + "/" + str(my_source) + "/pipeline/" + my_telescope
    my_ImageDirectory = my_individualPath + "/" + str(my_source) + "/images/" + my_telescope
    os.system('mkdir -p ' + my_ImageDirectory)
    
    # Create FITS files of the final images
    #
    print("... " + my_telescope + " pipeline completed")
    print("... " + my_telescope + " create FITS images")
    
    # Determine which pipeline stages were used when producing the final images
    #
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        
        # Define the basenames of the images to be converted into FITS
        #
        if (my_telescope == '7M'):
            my_ImageNames = ["oussid.s13_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
            my_DirtyNames = ["oussid.s13_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
        if (my_telescope == 'TM2'):
            my_ImageNames = ["oussid.s19_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s21_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s23_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s25_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s27_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
            my_DirtyNames = ["oussid.s19_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s21_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s23_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s25_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s27_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
        if (my_telescope == 'TM1'):
            my_ImageNames = ["oussid.s19_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s21_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s23_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s25_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s27_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
            my_DirtyNames = ["oussid.s19_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s21_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s23_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s25_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s27_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
        
        # Convert IMAGE files into FITS files
        #
        for my_ImageName in my_ImageNames:
            if (os.path.isdir(my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image") == True):
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image.fits",
                           dropdeg = True,
                           overwrite = True)
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image.pbcor",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image.pbcor.fits",
                           dropdeg = True,
                           overwrite = True)
            elif (os.path.isdir(my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image") == True):
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image.fits",
                           dropdeg = True,
                           overwrite = True)
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image.pbcor",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image.pbcor.fits",
                           dropdeg = True,
                           overwrite = True)
        
        for my_DirtyName in my_DirtyNames:
            if (os.path.isdir(my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image") == True):
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image.fits",
                           dropdeg = True,
                           overwrite = True)
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image.pbcor",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image.pbcor.fits",
                           dropdeg = True,
                           overwrite = True)
            elif (os.path.isdir(my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image") == True):
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image.fits",
                           dropdeg = True,
                           overwrite = True)
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image.pbcor",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image.pbcor.fits",
                           dropdeg = True,
                           overwrite = True)
    
    else:
        
        # Define the basenames of the images to be converted into FITS
        #
        if (my_telescope == '7M'):
            my_ImageNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
            my_DirtyNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
        if (my_telescope == 'TM2'):
            my_ImageNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s11_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s13_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
            my_DirtyNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s11_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s13_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
        if (my_telescope == 'TM1'):
            my_ImageNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter1", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter1", "oussid.s11_0._" + str(my_source) + "__sci.spw1.cube.I.iter1", "oussid.s13_0._" + str(my_source) + "__sci.spw2.cube.I.iter1", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter1"]
            my_DirtyNames = ["oussid.s7_0._" + str(my_source) + "__sci.spw0_1.cont.I.iter0", "oussid.s9_0._" + str(my_source) + "__sci.spw0.cube.I.iter0", "oussid.s11_0._" + str(my_source) + "__sci.spw1.cube.I.iter0", "oussid.s13_0._" + str(my_source) + "__sci.spw2.cube.I.iter0", "oussid.s15_0._" + str(my_source) + "__sci.spw3.cube.I.iter0"]
        
        # Convert IMAGE files into FITS files
        #
        for my_ImageName in my_ImageNames:
            if (os.path.isdir(my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image") == True):
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image.fits",
                           dropdeg = True,
                           overwrite = True)
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image.pbcor",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".reclean.image.pbcor.fits",
                           dropdeg = True,
                           overwrite = True)
            elif (os.path.isdir(my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image") == True):
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image.fits",
                           dropdeg = True,
                           overwrite = True)
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image.pbcor",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_ImageName+".image.pbcor.fits",
                           dropdeg = True,
                           overwrite = True)
        
        for my_DirtyName in my_DirtyNames:
            if (os.path.isdir(my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image") == True):
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image.fits",
                           dropdeg = True,
                           overwrite = True)
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image.pbcor",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".reclean.image.pbcor.fits",
                           dropdeg = True,
                           overwrite = True)
            elif (os.path.isdir(my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image") == True):
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image.fits",
                           dropdeg = True,
                           overwrite = True)
                exportfits(imagename = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image.pbcor",
                           fitsimage = my_runningPath+"/"+my_almagalRunDir+"/"+my_DirtyName+".image.pbcor.fits",
                           dropdeg = True,
                           overwrite = True)
    
    print("... " + my_telescope + " FITS images being copied")
    
    os.system('mkdir -p ' + my_individualPath + '/' + str(my_source) + '/images/' + my_telescope + '/pipeline')
    #os.system("cp -rp " + my_runningPath + "/" + my_almagalRunDir + "/*image " + my_individualPath + "/" + str(my_source) + "/images/" + my_telescope + "/pipeline/.")
    #os.system("cp -rp " + my_runningPath + "/" + my_almagalRunDir + "/*image.pbcor " + my_individualPath + "/" + str(my_source) + "/images/" + my_telescope + "/pipeline/.")
    os.system("cp -rp " + my_runningPath + "/" + my_almagalRunDir + "/*.fits " + my_individualPath + "/" + str(my_source) + "/images/" + my_telescope + "/pipeline/.")
    os.system("cp -rp " + my_runningPath + "/" + my_almagalRunDir + "/cont.dat " + my_individualPath + "/" + str(my_source) + "/images/" + my_telescope + "/pipeline/.")
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        os.system("cp -rp " + my_runningPath + "/" + my_almagalRunDir + "/original.cont.dat " + my_individualPath + "/" + str(my_source) + "/images/" + my_telescope + "/pipeline/.")
    
    os.system('rm -rf ' + my_ImageDirectory + '/pipeline/cont.dat')
    os.system('rm -rf ' + my_ImageDirectory + '/pipeline/original.cont.dat')
    my_TMPpath, my_TMPdirs, my_TMPfiles = next(os.walk(my_ImageDirectory+'/pipeline'))
    print("... number of files available (FITS files): " + str(len(my_TMPfiles)))
    my_runningDirectoryTMP = os.getcwd()
    os.chdir(my_ImageDirectory)
    os.system("tar -cf pipeline-fits.tar pipeline/*.fits")
    # Commented out to save disk space
    #os.system("tar -cf pipeline-products.tar pipeline/*.*")
    
    print("... " + my_telescope + " clean up the image directory")
    
    os.system("rm -rf pipeline")
    os.chdir(my_runningDirectoryTMP)
    
    print("... " + my_telescope + " pipeline products are being compressed")
    
    my_runningDirectoryTMP = os.getcwd()
    os.chdir(my_runningPath+'/'+my_almagalRunDir)
    my_pipelineName = [f for f in os.listdir(my_runningPath+'/'+my_almagalRunDir) if f.endswith(".context")][0][:-8]
    my_pipelineName = str(my_pipelineName) + " cont.dat"
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        my_pipelineName = str(my_pipelineName) + " original.cont.dat"
    os.system("tar -cf pipeline-weblog.tar " + str(my_pipelineName))
    os.system("cp -rp pipeline-weblog.tar " + str(my_mainPath) + "/2019.1.00195.L/sources/" + str(my_source) + "/pipeline/" + str(my_telescope) + "/.")
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step90.txt")




########################################################################
#
# STEP 11: 
#
# Re-clean bright unmasked channels
#
mystep = 11
if(mystep in thesteps):
    
    ########################################################################
    # RECLEAN of bright unmasked channels:
    # Notes from Crystal Brogan
    #
    # This sequence assesses whether there are bright channels
    # (> clean threshold) with no clean mask. If there are, it then creates
    # an amended mask that uses the max of 2 x clean threshold or 0.4 x peak
    # line intensity to amend the mask. It then restarts the clean with
    # growiterations=1 (the default is 75, without this, channels with 
    # extensive emission tend to get fully masked, including negative bowl
    # regions. 
    #
    # The outcome for each cube is inserted into the casalog, you can grep
    # UNMASK to locate them.
    #
    ########################################################################
    #
    # Information needed for following steps
    #
    
    Target = my_source 
    vispath = str(my_runningPath) + '/' + str(my_almagalRunDir) + '/processing/'
    
    print('::: ALMAGAL command ::: Setting up the information for the next steps')
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
    #if Refind == True:
        
        # Read pipeline context filename
        if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/cont.dat') == True):
            my_pipelinePath = str(my_runningPath) + '/' + str(my_almagalRunDir)
            my_pipelineName = [f for f in os.listdir(my_pipelinePath) if f.endswith(".context")][0][:-8]
            my_pipelinePath = my_pipelinePath + "/" + my_pipelineName
        elif (os.path.isfile(my_runningPath + '/cont.dat') == True):
            my_pipelinePath = str(my_runningPath)
            my_pipelineName = [f for f in os.listdir(my_pipelinePath) if f.endswith(".context")][0][:-8]
            my_pipelinePath = my_pipelinePath + "/" + my_pipelineName
        
        # Create pipeline directory containing merged html output files (called stage150)
        os.system('mkdir -p ' + my_pipelinePath + '/html/stage150/')
        
        # Merge the output of the previous four steps into a single file for further processing
        os.system('cat ' + my_pipelinePath + '/html/stage21/casapy.log ' + my_pipelinePath + '/html/stage23/casapy.log ' + my_pipelinePath + '/html/stage25/casapy.log ' + my_pipelinePath + '/html/stage27/casapy.log > ' + my_pipelinePath + '/html/stage150/casapy.log')
        os.system('cat ' + my_pipelinePath + '/html/stage21/t2-4m_details.html ' + my_pipelinePath + '/html/stage23/t2-4m_details.html ' + my_pipelinePath + '/html/stage25/t2-4m_details.html ' + my_pipelinePath + '/html/stage27/t2-4m_details.html > ' + my_pipelinePath + '/html/stage150/t2-4m_details.html')
        os.system('cat ' + my_pipelinePath + '/html/stage21/t2-4m_details-container.html ' + my_pipelinePath + '/html/stage23/t2-4m_details-container.html ' + my_pipelinePath + '/html/stage25/t2-4m_details-container.html ' + my_pipelinePath + '/html/stage27/t2-4m_details-container.html > ' + my_pipelinePath + '/html/stage150/t2-4m_details-container.html')
    
    
    pipeLog = sorted(glob.glob('pipeline-202*'), reverse=True)[1]
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
    #if Refind == True:
        print("::: ALMAGAL ::: original.cont.dat")
        stage = 150
        cubeInfo = au.cubeInfoFromWeblog(pipeLog, stage=stage, returnLists=True)
        #cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))
        stage = 21
        #cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))
        cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))
        stage = 23
        #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
        cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
        stage = 25
        #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
        cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
        stage = 27
        #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
        cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
    else:
        print("::: ALMAGAL ::: cont.dat")
        stage = 90
        cubeInfo = au.cubeInfoFromWeblog(pipeLog, stage=stage, returnLists=True)
        #cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))
        stage = 9
        #cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))
        cubes = sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))
        stage = 11
        #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
        cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
        stage = 13
        #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
        cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
        stage = 15
        #cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter1.image'))[0])
        cubes.append(sorted(glob.glob('oussid.s'+str(stage)+'*cube.I.iter?.image'))[0])
    
    
    # The outcome is fairly sensitive to the following parameters:
    #
    maskThreshFactor = 2      # Lower limit of the seed mask
    maskThreshFraction = 0.4  # Fraction of line peak line intensity (per channel) to seed the mask
    newGrow = 1               # Number of iterations that can be used in a "grow" sequence. 


    # Create masks for un-masked channels and re-image if necessary spectral window 0
    #    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step11.txt")
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        stage = 21
    else:
        stage = 9
    
    my_functionReImagingCube(0)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step11.txt")
    
    
    # Create masks for un-masked channels and re-image if necessary spectral window 1
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step12.txt")
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        stage = 23
    else:
        stage = 11
    
    my_functionReImagingCube(1)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step12.txt")
    
    
    # Create masks for un-masked channels and re-image if necessary spectral window 2
    #    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step13.txt")
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        stage = 25
    else:
        stage = 13
    
    my_functionReImagingCube(2)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step13.txt")
    
    
    # Create masks for un-masked channels and re-image if necessary spectral window 3
    #
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/running_step14.txt")
    
    if (os.path.isfile(my_runningPath + '/' + my_almagalRunDir + '/original.cont.dat') == True):
        stage = 27
    else:
        stage = 15
    
    my_functionReImagingCube(3)
    
    os.system("touch " + my_mainPath + "/2019.1.00195.L/sources/" + my_source + "/pipeline/" + my_telescope + "/worked_step14.txt")
