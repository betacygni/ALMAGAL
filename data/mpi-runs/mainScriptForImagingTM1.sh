#!/bin/bash
echo "::: ALMAGAL command ::: Script created by Alvaro Sanchez-Monge"

df -h
du -sh /dev/shm

#
my_runningComputer=ToModifyRUNNINGCOMPUTER
#my_runningComputer=JSC
if [ "$my_runningComputer" = JSC ]; then
    echo "::: ALMAGAL command ::: Load modules and library path in JSC"
    #unset LD_LIBRARY_PATH
    module purge
    module use $OTHERSTAGES
    module use Stages/2020
    module load Stages/2020
    module load GCCcore/.9.3.0 X11
    export CASALD_LIBRARY_PATH=$LD_LIBRARY_PATH
fi

# 
echo "::: ALMAGAL command ::: Define main paths to be used"
my_mainPath=ToModifyMAINPATH
my_runningPath=ToModifyRUNNINGPATH
my_softwarePath=ToModifySOFTWAREPATH

#
echo "::: ALMAGAL command ::: Temporary file to indicate that the process is active"
mkdir -p $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline
mkdir -p $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE
rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/inQueue.txt
touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt

#
echo "::: ALMAGAL command ::: Create processing directory in the running directory"
rm -rf $my_runningPath/almagal
mkdir $my_runningPath/almagal
mkdir $my_runningPath/almagal/processing

# 
if [ "$my_runningPath" = "$my_mainPath" ]; then

    #
    echo "::: ALMAGAL command ::: Processing directory can not be the same as the main directory"
    
else
        
    #
    echo "::: ALMAGAL command ::: Copy CASA installation to the running directory"
    cp -rp $my_softwarePath/casa-pipeline-release-5.6.1-8.el7 $my_runningPath/almagal/.
    my_casaPath=$my_runningPath/almagal
    
    #
    if [ "$my_runningComputer" = JSC ]; then
        echo "::: ALMAGAL command ::: Load modules and library path in JSC"
        export CASALD_LIBRARY_PATH=$CASALD_LIBRARY_PATH:$my_casaPath/casa-pipeline-release-5.6.1-8.el7/lib
    fi
    
    #
    echo "::: ALMAGAL command ::: Copy python packages to the running directory"
    cp -rp $my_softwarePath/python $my_runningPath/almagal/.
    
    #
    echo "::: ALMAGAL command ::: Copy analysisUtils packages to the running directory"
    cp -rp $my_softwarePath/analysisUtils/analysis_scripts $my_runningPath/almagal/.
    
    #
    echo "::: ALMAGAL command ::: Copy data to be processed to the running directory"
    #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/* /dev/shm/almagal/.
    my_startedPipelineFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step0.txt
    if [ -f "$my_startedPipelineFile" ]; then
        #
        echo "::: ALMAGAL command ::: Copy data (processing, pipeline and cont file)"
        #cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/* $my_runningPath/almagal/.
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/processing $my_runningPath/almagal/.
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/pipeline-202* $my_runningPath/almagal/.
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/cont.dat $my_runningPath/almagal/.
        cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/original.cont.dat $my_runningPath/almagal/.
        #
        # Copy files necesary for step 6
        my_runningStepFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step6.txt
        if [ -f "$my_runningStepFile" ]; then
            #
            echo "::: ALMAGAL command ::: Copy data for step 6"
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s9*.image $my_runningPath/almagal/.
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s9*.mom8_fc $my_runningPath/almagal/.
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s11*.image $my_runningPath/almagal/.
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s11*.mom8_fc $my_runningPath/almagal/.
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s13*.image $my_runningPath/almagal/.
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s13*.mom8_fc $my_runningPath/almagal/.
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s15*.image $my_runningPath/almagal/.
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s15*.mom8_fc $my_runningPath/almagal/.
        fi
        #
        # Copy files necesary for steps 11, 12, 13 and 14
        my_runningStepFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step10.txt
        if [ -f "$my_runningStepFile" ]; then
            #
            # Evaluate if the REFIND continuum was necessary
            my_refindStatusFile=$my_runningPath/almagal/original.cont.dat
            if [ -f "$my_refindStatusFile" ]; then
                #
                echo "::: ALMAGAL command ::: Copy data for steps 11, 12, 13 and 14 (new continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s21*.image $my_runningPath/almagal/.
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s23*.image $my_runningPath/almagal/.
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s25*.image $my_runningPath/almagal/.
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s27*.image $my_runningPath/almagal/.
            else
                #
                echo "::: ALMAGAL command ::: Copy data for steps 11, 12, 13 and 14 (original continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s9*.image $my_runningPath/almagal/.
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s11*.image $my_runningPath/almagal/.
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s13*.image $my_runningPath/almagal/.
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s15*.image $my_runningPath/almagal/.
            fi
        fi
        #
        # Copy files necesary for step 11
        my_runningStepFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step11.txt
        if [ -f "$my_runningStepFile" ]; then
            #
            # Evaluate if the REFIND continuum was necessary
            my_refindStatusFile=$my_runningPath/almagal/original.cont.dat
            if [ -f "$my_refindStatusFile" ]; then
                #
                echo "::: ALMAGAL command ::: Copy data for step 11 (new continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s21* $my_runningPath/almagal/.
                ls -ltr /dev/shm/almagal
                echo "::: ALMGAL ::: ls above"
            else
                #
                echo "::: ALMAGAL command ::: Copy data for step 11 (original continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s9* $my_runningPath/almagal/.
            fi
        fi
        #
        # Copy files necesary for step 12
        my_runningStepFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step12.txt
        if [ -f "$my_runningStepFile" ]; then
            #
            # Evaluate if the REFIND continuum was necessary
            my_refindStatusFile=$my_runningPath/almagal/original.cont.dat
            if [ -f "$my_refindStatusFile" ]; then
                #
                echo "::: ALMAGAL command ::: Copy data for step 12 (new continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s23* $my_runningPath/almagal/.
            else
                #
                echo "::: ALMAGAL command ::: Copy data for step 12 (original continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s11* $my_runningPath/almagal/.
            fi
        fi
        #
        # Copy files necesary for step 13
        my_runningStepFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step13.txt
        if [ -f "$my_runningStepFile" ]; then
            #
            # Evaluate if the REFIND continuum was necessary
            my_refindStatusFile=$my_runningPath/almagal/original.cont.dat
            if [ -f "$my_refindStatusFile" ]; then
                #
                echo "::: ALMAGAL command ::: Copy data for step 13 (new continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s25* $my_runningPath/almagal/.
            else
                #
                echo "::: ALMAGAL command ::: Copy data for step 13 (original continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s13* $my_runningPath/almagal/.
            fi
        fi
        #
        # Copy files necesary for step 14
        my_runningStepFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step14.txt
        if [ -f "$my_runningStepFile" ]; then
            #
            # Evaluate if the REFIND continuum was necessary
            my_refindStatusFile=$my_runningPath/almagal/original.cont.dat
            if [ -f "$my_refindStatusFile" ]; then
                #
                echo "::: ALMAGAL command ::: Copy data for step 14 (new continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s27* $my_runningPath/almagal/.
            else
                #
                echo "::: ALMAGAL command ::: Copy data for step 14 (original continuum)"
                cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/almagal/oussid.s15* $my_runningPath/almagal/.
            fi
        fi
    fi
    
    #
    echo "::: ALMAGAL command ::: Copy script to be executed to the running directory"
    cp -rp $my_mainPath/mpi-runs/ToModifySCRIPT.py $my_runningPath/almagal/.
    cp -rp $my_mainPath/mpi-runs/REFIND.py $my_runningPath/almagal/.
    
    #
    echo "::: ALMAGAL command ::: Move your working directory to the running directory"
    cd $my_runningPath/almagal
    
    #
    echo "::: ALMAGAL command ::: Copy the init file to the running directory"
    mkdir $my_runningPath/almagal/.ToModifyRCDIR.mycasa
    cp -rp $my_mainPath/mpi-runs/tmp_default-init.py $my_runningPath/almagal/.ToModifyRCDIR.mycasa/init.py
    
    #
    #echo "::: ALMAGAL command ::: Set the OMP_NUM_THREADS for CASA"
    export OMP_NUM_THREADS=12
    
    #
    df -h
    du -sh /dev/shm
    echo "::: ALMAGAL command ::: Execute CASA to the running directory"
    # --logfile $my_runningPath/casaLogger_SCRIPT.log
    $my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/casa  -x OMP_NUM_THREADS --rcdir $my_runningPath/almagal/.ToModifyRCDIR.mycasa --nologger --nogui --pipeline -c ToModifySCRIPT.py
    #mpicasa -n OMP_NUM_THREADS $my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/casa --rcdir $my_runningPath/almagal/.ToModifyRCDIR.mycasa --nologger --nogui --pipeline -c ToModifySCRIPT.py
    
    #
    echo "::: ALMAGAL command ::: Clean-up software directories"
    rm -rf $my_runningPath/almagal/casa-pipeline-release-5.6.1-8.el7
    rm -rf $my_runningPath/almagal/python
    rm -rf $my_runningPath/almagal/analysis_scripts
    
    #
    my_workedFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_ToModifyCURRENTSTEP.txt
    if [ -f "$my_workedFile" ]; then
        echo "::: ALMAGAL command ::: Copy the product results to the original data directory"
        cp -pr $my_runningPath/almagal $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/.
    fi
    
    #
    #echo "::: ALMAGAL command ::: Processed finished, create check file"
    #rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt
    #rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step*
    if [ -f "$my_workedFile" ]; then
        echo "::: ALMAGAL command ::: Processed finished, create check file"
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step*
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_ToModifyCURRENTSTEP.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_ToModifyCURRENTSTEP.txt
    fi
    
    #
    echo "::: ALMAGAL command ::: Move outside the running directory"
    cd ..
    
    #
    echo "::: ALMAGAL command ::: Remove the running directory"
    rm -rf $my_runningPath/almagal

fi
