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
        echo "::: ALMAGAL command ::: Copy data (processed files from step 0)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/processing $my_runningPath/almagal/.
    fi
    
    #
    # For spectral window 0
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step12.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 0 (merging all sub-cubes)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step13.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 0 (smoothing to commong beam)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0* $my_runningPath/almagal/.
    fi
    #
    # For spectral window 1
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step24.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 1 (merging all sub-cubes)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step25.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 1 (smoothing to commong beam)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1* $my_runningPath/almagal/.
    fi
    #
    # For spectral window 2
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step36.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 2 (merging all sub-cubes)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step37.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 2 (smoothing to commong beam)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2* $my_runningPath/almagal/.
    fi
    #
    # For spectral window 3
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step48.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy created chunks for spectral window 3 (merging all sub-cubes)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
    fi
    my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step49.txt
    if [ -f "$my_runningJointDeconvolutionFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy merged cube for spectral window 3 (smoothing to commong beam)"
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3* $my_runningPath/almagal/.
    fi
    
    #
    echo "::: ALMAGAL command ::: Copy script (and auxiliary scripts) to be executed to the running directory"
    cp -rp $my_mainPath/mpi-runs/ToModifySCRIPT.py $my_runningPath/almagal/.
    cp -rp $my_mainPath/mpi-runs/configALMAGAL.py $my_runningPath/almagal/analysis_scripts/.
    cp -rp $my_mainPath/mpi-runs/functionsALMAGAL.py $my_runningPath/almagal/analysis_scripts/.
    
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
        cp -pr $my_runningPath/almagal $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/.
        
        #
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step12.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chunk files after having merged them (spectral window 0)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw0*chunk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step24.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chunk files after having merged them (spectral window 1)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw1*chunk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step36.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chunk files after having merged them (spectral window 2)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw2*chunk*
        fi
        my_runningJointDeconvolutionFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/running_step48.txt
        if [ -f "$my_runningJointDeconvolutionFile" ]; then
            #
            echo "::: ALMAGAL command ::: Delete chunk files after having merged them (spectral window 3)"
            rm -rf $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/images/combined/ToModifyTELESCOPE/almagal/ToModifySOURCE*spw3*chunk*
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
