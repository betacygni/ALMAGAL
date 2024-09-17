#!/bin/bash
echo "::: ALMAGAL command ::: Script created by Alvaro Sanchez-Monge"

df -h
df -sh /dev/shm

#
my_runningComputer=ToModifyRUNNINGCOMPUTER
#my_runningComputer=JSC
if [ "$my_runningComputer" = JSC ]; then
    echo "::: ALMAGAL command ::: Load modules and library path in JSC"
    #unset LD_LIBRARY_PATH
    #
    # For casa 5.6.1:
    #module purge
    #module use $OTHERSTAGES
    #module use Stages/2020
    #module load Stages/2020
    #module load GCCcore/.9.3.0 X11
    #
    # For casa 6.2.0:
    export PYTHONPATH=""
    module --force purge
    module restore
    
    export CASALD_LIBRARY_PATH=$LD_LIBRARY_PATH
fi

# 
echo "::: ALMAGAL command ::: Define main paths to be used"
my_mainPath=ToModifyMAINPATH
my_runningPath=ToModifyRUNNINGPATH
my_softwarePath=ToModifySOFTWAREPATH

#
echo "::: ALMAGAL command ::: Temporary file to indicate that the process is active"
mkdir -p $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images
mkdir -p $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined
mkdir -p $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE
rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/inQueue.txt
touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/active.txt

#
echo "::: ALMAGAL command ::: Create processing directory in the running directory"
rm -rf $my_runningPath/almagal
mkdir $my_runningPath/almagal
mkdir $my_runningPath/almagal/processing
ls $my_runningPath/almagal

# 
if [ "$my_runningPath" = "$my_mainPath" ]; then

    #
    echo "::: ALMAGAL command ::: Processing directory can not be the same as the main directory"
    
else
        
    #
    echo "::: ALMAGAL command ::: Copy CASA installation to the running directory"
    cp -rp $my_softwarePath/casa-6.2.0-124 $my_runningPath/almagal/.
    #cp -rp $my_softwarePath/casa-pipeline-release-5.6.1-8.el7 $my_runningPath/almagal/.
    my_casaPath=$my_runningPath/almagal
    
    #
    if [ "$my_runningComputer" = JSC ]; then
        echo "::: ALMAGAL command ::: Load modules and library path in JSC"
        export CASALD_LIBRARY_PATH=$CASALD_LIBRARY_PATH:$my_casaPath/casa-6.2.0-124/lib
        #export CASALD_LIBRARY_PATH=$CASALD_LIBRARY_PATH:$my_casaPath/casa-pipeline-release-5.6.1-8.el7/lib
    fi
    
    #
    echo "::: ALMAGAL command ::: Copy python packages to the running directory"
    cp -rp $my_softwarePath/python3 $my_runningPath/almagal/python
    #cp -rp $my_softwarePath/python $my_runningPath/almagal/.
    
    #
    echo "::: ALMAGAL command ::: Copy analysisUtils packages to the running directory"
    cp -rp $my_softwarePath/analysisUtils/analysis_scripts $my_runningPath/almagal/.
    
    #
    #echo "::: ALMAGAL command ::: Copy near / far source lists"
    #cp -rp /localdata/projects/ALMA/2019.1.00195.L/processing/mpi-runs/near_sample.py $my_runningPath/almagal/.
    #cp -rp /localdata/projects/ALMA/2019.1.00195.L/processing/mpi-runs/far_sample.py $my_runningPath/almagal/.
    
    #
    echo "::: ALMAGAL command ::: Copy data to be processed to the running directory"
    my_startedJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/finished_step0.txt
    if [ -f "$my_startedJointDeconvolutionFile" ]; then
        #
        my_chunk1SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step33.txt
        my_chunk2SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step34.txt
        my_chunk3SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step35.txt
        my_chunk4SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step36.txt
        my_chunk5SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step37.txt
        my_chunk6SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step38.txt
        #
        my_chunk1SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step79.txt
        my_chunk2SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step80.txt
        my_chunk3SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step81.txt
        my_chunk4SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step82.txt
        my_chunk5SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step83.txt
        my_chunk6SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step84.txt
        #
        my_chunk1SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step125.txt
        my_chunk2SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step126.txt
        my_chunk3SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step127.txt
        my_chunk4SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step128.txt
        my_chunk5SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step129.txt
        my_chunk6SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step130.txt
        #
        my_chunk1SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step171.txt
        my_chunk2SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step172.txt
        my_chunk3SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step173.txt
        my_chunk4SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step174.txt
        my_chunk5SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step175.txt
        my_chunk6SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step176.txt
        #
        my_chonk1SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step39.txt
        my_chonk2SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step40.txt
        my_chonk3SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step41.txt
        my_chonk4SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step42.txt
        my_chonk5SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step43.txt
        my_chonk1SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step85.txt
        my_chonk2SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step86.txt
        my_chonk3SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step87.txt
        my_chonk4SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step88.txt
        my_chonk5SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step89.txt
        my_chonk1SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step131.txt
        my_chonk2SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step132.txt
        my_chonk3SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step133.txt
        my_chonk4SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step134.txt
        my_chonk5SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step135.txt
        my_chonk1SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step177.txt
        my_chonk2SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step178.txt
        my_chonk3SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step179.txt
        my_chonk4SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step180.txt
        my_chonk5SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step181.txt
        #
        my_smooth1SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step44.txt
        my_smooth2SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step45.txt
        my_smooth3SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step46.txt
        my_smooth4SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step47.txt
        my_smooth5SPW0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step48.txt
        my_smooth1SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step90.txt
        my_smooth2SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step91.txt
        my_smooth3SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step92.txt
        my_smooth4SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step93.txt
        my_smooth5SPW1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step94.txt
        my_smooth1SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step136.txt
        my_smooth2SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step137.txt
        my_smooth3SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step138.txt
        my_smooth4SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step139.txt
        my_smooth5SPW2CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step140.txt
        my_smooth1SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step182.txt
        my_smooth2SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step183.txt
        my_smooth3SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step184.txt
        my_smooth4SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step185.txt
        my_smooth5SPW3CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step186.txt
        #
        if [[ -f "$my_chonk1SPW0CheckFile" ]] || [[ -f "$my_chonk1SPW1CheckFile" ]] || [[ -f "$my_chonk1SPW2CheckFile" ]] || [[ -f "$my_chonk1SPW3CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chonk files for merging to final files"
        elif [[ -f "$my_chonk2SPW0CheckFile" ]] || [[ -f "$my_chonk2SPW1CheckFile" ]] || [[ -f "$my_chonk2SPW2CheckFile" ]] || [[ -f "$my_chonk2SPW3CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chonk files for merging to final files"
        elif [[ -f "$my_chonk3SPW0CheckFile" ]] || [[ -f "$my_chonk3SPW1CheckFile" ]] || [[ -f "$my_chonk3SPW2CheckFile" ]] || [[ -f "$my_chonk3SPW3CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chonk files for merging to final files"
        elif [[ -f "$my_chonk4SPW0CheckFile" ]] || [[ -f "$my_chonk4SPW1CheckFile" ]] || [[ -f "$my_chonk4SPW2CheckFile" ]] || [[ -f "$my_chonk4SPW3CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chonk files for merging to final files"
        elif [[ -f "$my_chonk5SPW0CheckFile" ]] || [[ -f "$my_chonk5SPW1CheckFile" ]] || [[ -f "$my_chonk5SPW2CheckFile" ]] || [[ -f "$my_chonk5SPW3CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chonk files for merging to final files"
        elif [[ -f "$my_chunk1SPW0CheckFile" ]] || [[ -f "$my_chunk2SPW0CheckFile" ]] || [[ -f "$my_chunk3SPW0CheckFile" ]] || [[ -f "$my_chunk4SPW0CheckFile" ]] || [[ -f "$my_chunk5SPW0CheckFile" ]] || [[ -f "$my_chunk6SPW0CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chunk files for merging files of SPW0"
        elif [[ -f "$my_chunk1SPW1CheckFile" ]] || [[ -f "$my_chunk2SPW1CheckFile" ]] || [[ -f "$my_chunk3SPW1CheckFile" ]] || [[ -f "$my_chunk4SPW1CheckFile" ]] || [[ -f "$my_chunk5SPW1CheckFile" ]] || [[ -f "$my_chunk6SPW1CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chunk files for merging files of SPW1"
        elif [[ -f "$my_chunk1SPW2CheckFile" ]] || [[ -f "$my_chunk2SPW2CheckFile" ]] || [[ -f "$my_chunk3SPW2CheckFile" ]] || [[ -f "$my_chunk4SPW2CheckFile" ]] || [[ -f "$my_chunk5SPW2CheckFile" ]] || [[ -f "$my_chunk6SPW2CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chunk files for merging files of SPW2"
        elif [[ -f "$my_chunk1SPW3CheckFile" ]] || [[ -f "$my_chunk2SPW3CheckFile" ]] || [[ -f "$my_chunk3SPW3CheckFile" ]] || [[ -f "$my_chunk4SPW3CheckFile" ]] || [[ -f "$my_chunk5SPW3CheckFile" ]] || [[ -f "$my_chunk6SPW3CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting chunk files for merging files of SPW3"
        elif [[ -f "$my_smooth1SPW0CheckFile" ]] || [[ -f "$my_smooth2SPW0CheckFile" ]] || [[ -f "$my_smooth3SPW0CheckFile" ]] || [[ -f "$my_smooth4SPW0CheckFile" ]] || [[ -f "$my_smooth5SPW0CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting files for smoothing to common beam / preparing cropped FITS files"
        elif [[ -f "$my_smooth1SPW1CheckFile" ]] || [[ -f "$my_smooth2SPW1CheckFile" ]] || [[ -f "$my_smooth3SPW1CheckFile" ]] || [[ -f "$my_smooth4SPW1CheckFile" ]] || [[ -f "$my_smooth5SPW1CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting files for smoothing to common beam / preparing cropped FITS files"
        elif [[ -f "$my_smooth1SPW2CheckFile" ]] || [[ -f "$my_smooth2SPW2CheckFile" ]] || [[ -f "$my_smooth3SPW2CheckFile" ]] || [[ -f "$my_smooth4SPW2CheckFile" ]] || [[ -f "$my_smooth5SPW2CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting files for smoothing to common beam / preparing cropped FITS files"
        elif [[ -f "$my_smooth1SPW3CheckFile" ]] || [[ -f "$my_smooth2SPW3CheckFile" ]] || [[ -f "$my_smooth3SPW3CheckFile" ]] || [[ -f "$my_smooth4SPW3CheckFile" ]] || [[ -f "$my_smooth5SPW3CheckFile" ]]; then
            echo "::: ALMAGAL command ::: Setting files for smoothing to common beam / preparing cropped FITS files"
        else
            echo "::: ALMAGAL command ::: Copy data (processed files from step 0)"
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/processing.tar $my_runningPath/almagal/.
            echo "::: ALMAGAL command ::: Untar processing directory"
            cwd=$(pwd)
            cd $my_runningPath/almagal/
            tar -xf processing.tar
            rm -rf processing.tar
            cd $cwd
        fi
        my_croppingCheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step2.txt
        if [[ -f "$my_croppingCheckFile" ]]; then
            echo "::: ALMAGAL command ::: Copy combined cont tar files, for cropping"
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/combined-cont-fits.tar $my_runningPath/almagal/.
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/auxiliary-cont-fits.tar $my_runningPath/almagal/.
        fi
        #echo "::: ALMAGAL command ::: Copy data (processed files from step 0)"
        #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/processing $my_runningPath/almagal/.
        #
        echo "::: ALMAGAL command ::: Copy tcleanParameters.txt file (created during step 0)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/tcleanParameters.txt $my_runningPath/almagal/.
        #
        echo "::: ALMAGAL command ::: Copy channelsForEachSPW.txt files (created during step 0)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/channelsForEachSPW_7M.txt $my_runningPath/almagal/.
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/channelsForEachSPW_TM2.txt $my_runningPath/almagal/.
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/channelsForEachSPW_TM1.txt $my_runningPath/almagal/.
        #
        echo "::: ALMAGAL command ::: Copy croppingCoordinates file (created during step 2)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_ToModifyTELESCOPE_croppedCoordinates.txt $my_runningPath/almagal/.
    fi
    
    #
    # For spectral window 0
    #my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step32.txt
    #if [ -f "$my_runningJointDeconvolutionFile" ]; then
    #    #
    #    echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
    #    for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
    #        if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
    #            cp -rp $chunked_file $my_runningPath/almagal/.
    #            #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
    #        fi
    #    done
    #fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step33.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_chunk1."* ]] || [[ "$chunked_file" == *"_chunk2."* ]] || [[ "$chunked_file" == *"_chunk3."* ]] || [[ "$chunked_file" == *"_chunk4."* ]] || [[ "$chunked_file" == *"_chunk5."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step34.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_chunk6."* ]] || [[ "$chunked_file" == *"_chunk7."* ]] || [[ "$chunked_file" == *"_chunk8."* ]] || [[ "$chunked_file" == *"_chunk9."* ]] || [[ "$chunked_file" == *"_chunk10."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step35.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_chunk11."* ]] || [[ "$chunked_file" == *"_chunk12."* ]] || [[ "$chunked_file" == *"_chunk13."* ]] || [[ "$chunked_file" == *"_chunk14."* ]] || [[ "$chunked_file" == *"_chunk15."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step36.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_chunk16."* ]] || [[ "$chunked_file" == *"_chunk17."* ]] || [[ "$chunked_file" == *"_chunk18."* ]] || [[ "$chunked_file" == *"_chunk19."* ]] || [[ "$chunked_file" == *"_chunk20."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step37.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_chunk21."* ]] || [[ "$chunked_file" == *"_chunk22."* ]] || [[ "$chunked_file" == *"_chunk23."* ]] || [[ "$chunked_file" == *"_chunk24."* ]] || [[ "$chunked_file" == *"_chunk25."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step38.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_chunk26."* ]] || [[ "$chunked_file" == *"_chunk27."* ]] || [[ "$chunked_file" == *"_chunk28."* ]] || [[ "$chunked_file" == *"_chunk29."* ]] || [[ "$chunked_file" == *"_chunk30."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step39.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_image_chonk1."* ]] || [[ "$chunked_file" == *"_image_chonk2."* ]] || [[ "$chunked_file" == *"_image_chonk3."* ]] || [[ "$chunked_file" == *"_image_chonk4."* ]] || [[ "$chunked_file" == *"_image_chonk5."* ]] || [[ "$chunked_file" == *"_image_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step40.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_model_chonk1."* ]] || [[ "$chunked_file" == *"_model_chonk2."* ]] || [[ "$chunked_file" == *"_model_chonk3."* ]] || [[ "$chunked_file" == *"_model_chonk4."* ]] || [[ "$chunked_file" == *"_model_chonk5."* ]] || [[ "$chunked_file" == *"_model_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step41.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_pb_chonk1."* ]] || [[ "$chunked_file" == *"_pb_chonk2."* ]] || [[ "$chunked_file" == *"_pb_chonk3."* ]] || [[ "$chunked_file" == *"_pb_chonk4."* ]] || [[ "$chunked_file" == *"_pb_chonk5."* ]] || [[ "$chunked_file" == *"_pb_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step42.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_psf_chonk1."* ]] || [[ "$chunked_file" == *"_psf_chonk2."* ]] || [[ "$chunked_file" == *"_psf_chonk3."* ]] || [[ "$chunked_file" == *"_psf_chonk4."* ]] || [[ "$chunked_file" == *"_psf_chonk5."* ]] || [[ "$chunked_file" == *"_psf_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step43.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$chunked_file" == *"_residual_chonk1."* ]] || [[ "$chunked_file" == *"_residual_chonk2."* ]] || [[ "$chunked_file" == *"_residual_chonk3."* ]] || [[ "$chunked_file" == *"_residual_chonk4."* ]] || [[ "$chunked_file" == *"_residual_chonk5."* ]] || [[ "$chunked_file" == *"_residual_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
            fi
        done
    fi
    #
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step44.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 0 (smoothing to commong beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$smooth_file" == *"_jointdeconv.image" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
            if [[ "$smooth_file" == *"_jointdeconv.pb" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step45.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 0 (smoothing to commong beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$smooth_file" == *"_jointdeconv.residual" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step46.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 0 (smoothing to commong beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$smooth_file" == *"_jointdeconv.psf" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step47.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 0 (smoothing to commong beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$smooth_file" == *"_jointdeconv.pb" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step48.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 0 (smoothing to commong beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*; do
            if [[ "$smooth_file" == *"_jointdeconv.model" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    #
    # For spectral window 1
    #my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step64.txt
    #if [ -f "$my_runningJointDeconvolutionFile" ]; then
    #    #
    #    echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
    #    for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
    #        if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
    #            cp -rp $chunked_file $my_runningPath/almagal/.
    #            #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
    #        fi
    #    done
    #fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step79.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_chunk1."* ]] || [[ "$chunked_file" == *"_chunk2."* ]] || [[ "$chunked_file" == *"_chunk3."* ]] || [[ "$chunked_file" == *"_chunk4."* ]] || [[ "$chunked_file" == *"_chunk5."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step80.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_chunk6."* ]] || [[ "$chunked_file" == *"_chunk7."* ]] || [[ "$chunked_file" == *"_chunk8."* ]] || [[ "$chunked_file" == *"_chunk9."* ]] || [[ "$chunked_file" == *"_chunk10."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step81.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_chunk11."* ]] || [[ "$chunked_file" == *"_chunk12."* ]] || [[ "$chunked_file" == *"_chunk13."* ]] || [[ "$chunked_file" == *"_chunk14."* ]] || [[ "$chunked_file" == *"_chunk15."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step82.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_chunk16."* ]] || [[ "$chunked_file" == *"_chunk17."* ]] || [[ "$chunked_file" == *"_chunk18."* ]] || [[ "$chunked_file" == *"_chunk19."* ]] || [[ "$chunked_file" == *"_chunk20."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step83.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_chunk21."* ]] || [[ "$chunked_file" == *"_chunk22."* ]] || [[ "$chunked_file" == *"_chunk23."* ]] || [[ "$chunked_file" == *"_chunk24."* ]] || [[ "$chunked_file" == *"_chunk25."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step84.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_chunk26."* ]] || [[ "$chunked_file" == *"_chunk27."* ]] || [[ "$chunked_file" == *"_chunk28."* ]] || [[ "$chunked_file" == *"_chunk29."* ]] || [[ "$chunked_file" == *"_chunk30."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    #
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step85.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_image_chonk1."* ]] || [[ "$chunked_file" == *"_image_chonk2."* ]] || [[ "$chunked_file" == *"_image_chonk3."* ]] || [[ "$chunked_file" == *"_image_chonk4."* ]] || [[ "$chunked_file" == *"_image_chonk5."* ]] || [[ "$chunked_file" == *"_image_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step86.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_model_chonk1."* ]] || [[ "$chunked_file" == *"_model_chonk2."* ]] || [[ "$chunked_file" == *"_model_chonk3."* ]] || [[ "$chunked_file" == *"_model_chonk4."* ]] || [[ "$chunked_file" == *"_model_chonk5."* ]] || [[ "$chunked_file" == *"_model_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step87.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_pb_chonk1."* ]] || [[ "$chunked_file" == *"_pb_chonk2."* ]] || [[ "$chunked_file" == *"_pb_chonk3."* ]] || [[ "$chunked_file" == *"_pb_chonk4."* ]] || [[ "$chunked_file" == *"_pb_chonk5."* ]] || [[ "$chunked_file" == *"_pb_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step88.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_psf_chonk1."* ]] || [[ "$chunked_file" == *"_psf_chonk2."* ]] || [[ "$chunked_file" == *"_psf_chonk3."* ]] || [[ "$chunked_file" == *"_psf_chonk4."* ]] || [[ "$chunked_file" == *"_psf_chonk5."* ]] || [[ "$chunked_file" == *"_psf_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step89.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$chunked_file" == *"_residual_chonk1."* ]] || [[ "$chunked_file" == *"_residual_chonk2."* ]] || [[ "$chunked_file" == *"_residual_chonk3."* ]] || [[ "$chunked_file" == *"_residual_chonk4."* ]] || [[ "$chunked_file" == *"_residual_chonk5."* ]] || [[ "$chunked_file" == *"_residual_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
            fi
        done
    fi
    #
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step90.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 1 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$smooth_file" == *"_jointdeconv.image" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
            if [[ "$smooth_file" == *"_jointdeconv.pb" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step91.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 1 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$smooth_file" == *"_jointdeconv.residual" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step92.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 1 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$smooth_file" == *"_jointdeconv.psf" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step93.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 1 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$smooth_file" == *"_jointdeconv.pb" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step94.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 1 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*; do
            if [[ "$smooth_file" == *"_jointdeconv.model" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    #
    # For spectral window 2
    #my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step96.txt
    #if [ -f "$my_runningJointDeconvolutionFile" ]; then
    #    #
    #    echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
    #    for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
    #        if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
    #            cp -rp $chunked_file $my_runningPath/almagal/.
    #            #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
    #        fi
    #    done
    #fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step125.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_chunk1."* ]] || [[ "$chunked_file" == *"_chunk2."* ]] || [[ "$chunked_file" == *"_chunk3."* ]] || [[ "$chunked_file" == *"_chunk4."* ]] || [[ "$chunked_file" == *"_chunk5."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step126.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_chunk6."* ]] || [[ "$chunked_file" == *"_chunk7."* ]] || [[ "$chunked_file" == *"_chunk8."* ]] || [[ "$chunked_file" == *"_chunk9."* ]] || [[ "$chunked_file" == *"_chunk10."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step127.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_chunk11."* ]] || [[ "$chunked_file" == *"_chunk12."* ]] || [[ "$chunked_file" == *"_chunk13."* ]] || [[ "$chunked_file" == *"_chunk14."* ]] || [[ "$chunked_file" == *"_chunk15."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step128.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_chunk16."* ]] || [[ "$chunked_file" == *"_chunk17."* ]] || [[ "$chunked_file" == *"_chunk18."* ]] || [[ "$chunked_file" == *"_chunk19."* ]] || [[ "$chunked_file" == *"_chunk20."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step129.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_chunk21."* ]] || [[ "$chunked_file" == *"_chunk22."* ]] || [[ "$chunked_file" == *"_chunk23."* ]] || [[ "$chunked_file" == *"_chunk24."* ]] || [[ "$chunked_file" == *"_chunk25."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step130.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_chunk26."* ]] || [[ "$chunked_file" == *"_chunk27."* ]] || [[ "$chunked_file" == *"_chunk28."* ]] || [[ "$chunked_file" == *"_chunk29."* ]] || [[ "$chunked_file" == *"_chunk30."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    #
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step131.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_image_chonk1."* ]] || [[ "$chunked_file" == *"_image_chonk2."* ]] || [[ "$chunked_file" == *"_image_chonk3."* ]] || [[ "$chunked_file" == *"_image_chonk4."* ]] || [[ "$chunked_file" == *"_image_chonk5."* ]] || [[ "$chunked_file" == *"_image_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step132.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_model_chonk1."* ]] || [[ "$chunked_file" == *"_model_chonk2."* ]] || [[ "$chunked_file" == *"_model_chonk3."* ]] || [[ "$chunked_file" == *"_model_chonk4."* ]] || [[ "$chunked_file" == *"_model_chonk5."* ]] || [[ "$chunked_file" == *"_model_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step133.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_pb_chonk1."* ]] || [[ "$chunked_file" == *"_pb_chonk2."* ]] || [[ "$chunked_file" == *"_pb_chonk3."* ]] || [[ "$chunked_file" == *"_pb_chonk4."* ]] || [[ "$chunked_file" == *"_pb_chonk5."* ]] || [[ "$chunked_file" == *"_pb_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step134.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_psf_chonk1."* ]] || [[ "$chunked_file" == *"_psf_chonk2."* ]] || [[ "$chunked_file" == *"_psf_chonk3."* ]] || [[ "$chunked_file" == *"_psf_chonk4."* ]] || [[ "$chunked_file" == *"_psf_chonk5."* ]] || [[ "$chunked_file" == *"_psf_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step135.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$chunked_file" == *"_residual_chonk1."* ]] || [[ "$chunked_file" == *"_residual_chonk2."* ]] || [[ "$chunked_file" == *"_residual_chonk3."* ]] || [[ "$chunked_file" == *"_residual_chonk4."* ]] || [[ "$chunked_file" == *"_residual_chonk5."* ]] || [[ "$chunked_file" == *"_residual_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
            fi
        done
    fi
    #
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step136.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 2 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$smooth_file" == *"_jointdeconv.image" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
            if [[ "$smooth_file" == *"_jointdeconv.pb" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step137.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 2 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$smooth_file" == *"_jointdeconv.residual" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step138.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 2 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$smooth_file" == *"_jointdeconv.psf" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step139.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 2 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$smooth_file" == *"_jointdeconv.pb" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step140.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 2 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*; do
            if [[ "$smooth_file" == *"_jointdeconv.model" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    #
    # For spectral window 3
    #my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step128.txt
    #if [ -f "$my_runningJointDeconvolutionFile" ]; then
    #    #
    #    echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
    #    for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
    #        if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
    #            cp -rp $chunked_file $my_runningPath/almagal/.
    #            #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
    #        fi
    #    done
    #fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step171.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_chunk1."* ]] || [[ "$chunked_file" == *"_chunk2."* ]] || [[ "$chunked_file" == *"_chunk3."* ]] || [[ "$chunked_file" == *"_chunk4."* ]] || [[ "$chunked_file" == *"_chunk5."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step172.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_chunk6."* ]] || [[ "$chunked_file" == *"_chunk7."* ]] || [[ "$chunked_file" == *"_chunk8."* ]] || [[ "$chunked_file" == *"_chunk9."* ]] || [[ "$chunked_file" == *"_chunk10."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step173.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_chunk11."* ]] || [[ "$chunked_file" == *"_chunk12."* ]] || [[ "$chunked_file" == *"_chunk13."* ]] || [[ "$chunked_file" == *"_chunk14."* ]] || [[ "$chunked_file" == *"_chunk15."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step174.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_chunk16."* ]] || [[ "$chunked_file" == *"_chunk17."* ]] || [[ "$chunked_file" == *"_chunk18."* ]] || [[ "$chunked_file" == *"_chunk19."* ]] || [[ "$chunked_file" == *"_chunk20."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step175.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_chunk21."* ]] || [[ "$chunked_file" == *"_chunk22."* ]] || [[ "$chunked_file" == *"_chunk23."* ]] || [[ "$chunked_file" == *"_chunk24."* ]] || [[ "$chunked_file" == *"_chunk25."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step176.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_chunk26."* ]] || [[ "$chunked_file" == *"_chunk27."* ]] || [[ "$chunked_file" == *"_chunk28."* ]] || [[ "$chunked_file" == *"_chunk29."* ]] || [[ "$chunked_file" == *"_chunk30."* ]]; then
                if [[ "$chunked_file" != *"_v01"* ]] && [[ "$chunked_file" != *"_v02"* ]] && [[ "$chunked_file" != *"_v03"* ]]; then
                    cp -rp $chunked_file $my_runningPath/almagal/.
                    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
                fi
            fi
        done
    fi
    #
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step177.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_image_chonk1."* ]] || [[ "$chunked_file" == *"_image_chonk2."* ]] || [[ "$chunked_file" == *"_image_chonk3."* ]] || [[ "$chunked_file" == *"_image_chonk4."* ]] || [[ "$chunked_file" == *"_image_chonk5."* ]] || [[ "$chunked_file" == *"_image_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step178.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_model_chonk1."* ]] || [[ "$chunked_file" == *"_model_chonk2."* ]] || [[ "$chunked_file" == *"_model_chonk3."* ]] || [[ "$chunked_file" == *"_model_chonk4."* ]] || [[ "$chunked_file" == *"_model_chonk5."* ]] || [[ "$chunked_file" == *"_model_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step179.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_pb_chonk1."* ]] || [[ "$chunked_file" == *"_pb_chonk2."* ]] || [[ "$chunked_file" == *"_pb_chonk3."* ]] || [[ "$chunked_file" == *"_pb_chonk4."* ]] || [[ "$chunked_file" == *"_pb_chonk5."* ]] || [[ "$chunked_file" == *"_pb_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step180.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_psf_chonk1."* ]] || [[ "$chunked_file" == *"_psf_chonk2."* ]] || [[ "$chunked_file" == *"_psf_chonk3."* ]] || [[ "$chunked_file" == *"_psf_chonk4."* ]] || [[ "$chunked_file" == *"_psf_chonk5."* ]] || [[ "$chunked_file" == *"_psf_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step181.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        for chunked_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$chunked_file" == *"_residual_chonk1."* ]] || [[ "$chunked_file" == *"_residual_chonk2."* ]] || [[ "$chunked_file" == *"_residual_chonk3."* ]] || [[ "$chunked_file" == *"_residual_chonk4."* ]] || [[ "$chunked_file" == *"_residual_chonk5."* ]] || [[ "$chunked_file" == *"_residual_chonk6."* ]]; then
                cp -rp $chunked_file $my_runningPath/almagal/.
                #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
            fi
        done
    fi
    #
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step182.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 3 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$smooth_file" == *"_jointdeconv.image" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
            if [[ "$smooth_file" == *"_jointdeconv.pb" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step183.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 3 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$smooth_file" == *"_jointdeconv.residual" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step184.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 3 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$smooth_file" == *"_jointdeconv.psf" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step185.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 3 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$smooth_file" == *"_jointdeconv.pb" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step186.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 3 (smoothing to common beam)"
        for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
            if [[ "$smooth_file" == *"_jointdeconv.model" ]]; then
                cp -rp $smooth_file $my_runningPath/almagal/.
            fi
        done
    fi
    #
    #my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step153.txt
    #if [ -f "$my_runningJointDeconvolutionFile" ]; then
    #    #
    #    echo "::: ALMAGAL command ::: Copy merged cube for spectral window 3 (smoothing to commong beam)"
    #    for smooth_file in $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*; do
    #        if [ "$smooth_file" == *"_jointdeconv."* ]; then
    #            cp -rp $smooth_file $my_runningPath/almagal/.
    #            #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
    #        fi
    #    done
    #fi
    
    #
    echo "::: ALMAGAL command ::: Copy script to be executed to the running directory"
    cp -rp $my_mainPath/mpi-runs/ToModifySCRIPT.py $my_runningPath/almagal/.
    cp -rp $my_mainPath/mpi-runs/configALMAGAL.py $my_runningPath/almagal/.
    cp -rp $my_mainPath/mpi-runs/functionsALMAGAL.py $my_runningPath/almagal/.
    
    #
    echo "::: ALMAGAL command ::: Move your working directory to the running directory"
    cd $my_runningPath/almagal
    
    #
    echo "::: ALMAGAL command ::: Copy the init file to the running directory"
    mkdir $my_runningPath/almagal/.ToModifyRCDIR.mycasa
    cp -rp $my_mainPath/mpi-runs/tmp_default-init.py $my_runningPath/almagal/.ToModifyRCDIR.mycasa/init.py
    
    #
    #echo "::: ALMAGAL command ::: Set the OMP_NUM_THREADS for CASA"
    export OMP_NUM_THREADS=2
    
    #
    echo "::: ALMAGAL command ::: Execute CASA to the running directory"
    # --logfile $my_runningPath/casaLogger_SCRIPT.log
    $my_casaPath/casa-6.2.0-124/bin/casa  -x OMP_NUM_THREADS --nologger --nogui -c ToModifySCRIPT.py
    #$my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/casa  -x OMP_NUM_THREADS --rcdir $my_runningPath/almagal/.ToModifyRCDIR.mycasa --nologger --nogui --pipeline -c ToModifySCRIPT.py
    #mpicasa -n OMP_NUM_THREADS $my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/casa --rcdir $my_runningPath/almagal/.ToModifyRCDIR.mycasa --nologger --nogui --pipeline -c ToModifySCRIPT.py
    
    #
    echo "::: ALMAGAL command ::: Clean-up software directories"
    rm -rf $my_runningPath/almagal/casa-6.2.0-124
    #rm -rf $my_runningPath/almagal/casa-pipeline-release-5.6.1-8.el7
    rm -rf $my_runningPath/almagal/python
    rm -rf $my_runningPath/almagal/analysis_scripts
    
    #
    my_workedFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/worked_ToModifyCURRENTSTEP.txt
    if [ -f "$my_workedFile" ]; then
        echo "::: ALMAGAL command ::: Copy the product results to the original data directory"
        
        #
        my_step0CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step0.txt
        my_step1CheckFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step1.txt
        if [[ -f "$my_step0CheckFile" ]] || [[ -f "$my_step1CheckFile" ]]; then
            #
            echo "COOOOOMO"
            cwd=$(pwd)
            cd $my_runningPath/almagal
            tar -cf processing.tar processing
            rm -rf processing
            cd $cwd
        else
            echo "PUES NO"
            cwd=$(pwd)
            cd $my_runningPath/almagal
            rm -rf processing.tar
            rm -rf processing
            cd $cwd
        fi
        echo "::: ALMAGAL command ::: Transfer almagal running directory"
        cp -rp $my_runningPath/almagal $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/.
        #
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step39.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chunk files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*chunk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step40.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/image files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*image_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step41.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/model files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*model_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step42.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/pb files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*pb_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step43.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/psf files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*psf_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step44.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/residual files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*chonk*
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw0_ToModifyTELESCOPE_jointdeconv.image
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step45.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete residual files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw0_ToModifyTELESCOPE_jointdeconv.residual
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step46.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete psf files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw0_ToModifyTELESCOPE_jointdeconv.psf
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step47.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete pb files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw0_ToModifyTELESCOPE_jointdeconv.pb
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step48.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete model files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw0_ToModifyTELESCOPE_jointdeconv.model
        fi
        #
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step85.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chunk files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*chunk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step86.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/image files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*image_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step87.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/model files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*model_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step88.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/pb files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*pb_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step89.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/psf files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*psf_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step90.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/residual files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*chonk*
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw1_ToModifyTELESCOPE_jointdeconv.image
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step91.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete residual files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw1_ToModifyTELESCOPE_jointdeconv.residual
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step92.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete psf files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw1_ToModifyTELESCOPE_jointdeconv.psf
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step93.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete pb files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw1_ToModifyTELESCOPE_jointdeconv.pb
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step94.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete model files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw1_ToModifyTELESCOPE_jointdeconv.model
        fi
        #
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step131.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chunk files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*chunk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step132.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/image files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*image_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step133.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/model files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*model_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step134.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/pb files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*pb_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step135.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/psf files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*psf_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step136.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/image files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*chonk*
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw2_ToModifyTELESCOPE_jointdeconv.image
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step137.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete residual files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw2_ToModifyTELESCOPE_jointdeconv.residual
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step138.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete psf files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw2_ToModifyTELESCOPE_jointdeconv.psf
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step139.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete pb files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw2_ToModifyTELESCOPE_jointdeconv.pb
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step140.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete model files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw2_ToModifyTELESCOPE_jointdeconv.model
        fi
        #
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step177.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chunk files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*chunk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step178.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/image files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*image_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step179.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/model files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*model_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step180.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/pb files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*pb_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step181.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/psf files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*psf_chonk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step182.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chonk/image files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*chonk*
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw3_ToModifyTELESCOPE_jointdeconv.image
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step183.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete residual files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw3_ToModifyTELESCOPE_jointdeconv.residual
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step184.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete psf files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw3_ToModifyTELESCOPE_jointdeconv.psf
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step185.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete pb files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw3_ToModifyTELESCOPE_jointdeconv.pb
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step186.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete model files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE_spw3_ToModifyTELESCOPE_jointdeconv.model
        fi
    fi
    
    #
    #echo "::: ALMAGAL command ::: Processed finished, create check file"
    #rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt
    #rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step*
    if [ -f "$my_workedFile" ]; then
        echo "::: ALMAGAL command ::: Processed finished, create check file"
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/active.txt
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step*
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/worked_ToModifyCURRENTSTEP.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/finished_ToModifyCURRENTSTEP.txt
    fi
    
    #
    echo "::: ALMAGAL command ::: Move outside the running directory"
    cd ..
    
    #
    echo "::: ALMAGAL command ::: Remove the running directory"
    rm -rf $my_runningPath/almagal

fi
