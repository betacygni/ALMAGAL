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
my_storagePath=ToModifySTORAGEPATH
my_softwarePath=ToModifySOFTWAREPATH
my_mpiCores=ToModifyMPICORES

#
echo "::: ALMAGAL command ::: Temporary file to indicate that the process is active"
mkdir -p $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline
mkdir -p $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE
rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/inQueue.txt
touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt

#
echo "::: ALMAGAL command ::: Create processing directory in the running directory"
my_almagalRunningDir=almagal_ToModifySOURCE
rm -rf $my_runningPath/$my_almagalRunningDir
mkdir $my_runningPath/$my_almagalRunningDir
mkdir $my_runningPath/$my_almagalRunningDir/processing

# 
if [ "$my_runningPath" = "$my_mainPath" ]; then

    #
    echo "::: ALMAGAL command ::: Processing directory can not be the same as the main directory"
    
else
        
    #
    echo "::: ALMAGAL command ::: Copy CASA installation to the running directory"
    cp -rp $my_softwarePath/casa-pipeline-release-5.6.1-8.el7 $my_runningPath/$my_almagalRunningDir/.
    my_casaPath=$my_runningPath/$my_almagalRunningDir
    
    #
    if [ "$my_runningComputer" = JSC ]; then
        echo "::: ALMAGAL command ::: Load modules and library path in JSC"
        export CASALD_LIBRARY_PATH=$CASALD_LIBRARY_PATH:$my_casaPath/casa-pipeline-release-5.6.1-8.el7/lib
    fi
    
    #
    echo "::: ALMAGAL command ::: Copy python packages to the running directory"
    cp -rp $my_softwarePath/python $my_runningPath/$my_almagalRunningDir/.
    
    #
    echo "::: ALMAGAL command ::: Copy analysisUtils packages to the running directory"
    cp -rp $my_softwarePath/analysisUtils/analysis_scripts $my_runningPath/$my_almagalRunningDir/.
    
    #
    echo "::: ALMAGAL command ::: Copy script to be executed to the running directory"
    cp -rp $my_mainPath/mpi-runs/ToModifySCRIPT.py $my_runningPath/$my_almagalRunningDir/.
    cp -rp $my_mainPath/mpi-runs/REFIND.py $my_runningPath/$my_almagalRunningDir/.
    
    #
    echo "::: ALMAGAL command ::: Move your working directory to the running directory"
    cd $my_runningPath/$my_almagalRunningDir
    
    #
    echo "::: ALMAGAL command ::: Copy the init file to the running directory"
    mkdir $my_runningPath/$my_almagalRunningDir/.ToModifyRCDIR.mycasa
    cp -rp $my_mainPath/mpi-runs/ToModifySOURCE_default-init.py $my_runningPath/$my_almagalRunningDir/.ToModifyRCDIR.mycasa/init.py
    
    #
    #echo "::: ALMAGAL command ::: Set the OMP_NUM_THREADS for CASA"
    export OMP_NUM_THREADS=20
    
    #
    df -h
    du -sh /dev/shm
    echo "::: ALMAGAL command ::: Execute CASA to the running directory"
    # --logfile $my_runningPath/casaLogger_SCRIPT.log
    if [ $my_mpiCores = 0 ]; then
        $my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/casa  -x OMP_NUM_THREADS --rcdir $my_runningPath/$my_almagalRunningDir/.ToModifyRCDIR.mycasa --nologger --nogui --pipeline -c ToModifySCRIPT.py
    fi
    if [ $my_mpiCores != 0 ]; then
        $my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/mpicasa -n ToModifyMPICORES $my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/casa --rcdir $my_runningPath/$my_almagalRunningDir/.ToModifyRCDIR.mycasa --nologger --nogui --pipeline -c ToModifySCRIPT.py
    fi
    #$my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/casa  -x OMP_NUM_THREADS --rcdir $my_runningPath/$my_almagalRunningDir/.ToModifyRCDIR.mycasa --nologger --nogui --pipeline -c ToModifySCRIPT.py
    #mpicasa -n 12 $my_casaPath/casa-pipeline-release-5.6.1-8.el7/bin/casa --rcdir $my_runningPath/$my_almagalRunningDir/.ToModifyRCDIR.mycasa --nologger --nogui --pipeline -c ToModifySCRIPT.py
    
    #
    echo "::: ALMAGAL command ::: Clean-up software directories"
    rm -rf $my_runningPath/$my_almagalRunningDir/casa-pipeline-release-5.6.1-8.el7
    rm -rf $my_runningPath/$my_almagalRunningDir/python
    rm -rf $my_runningPath/$my_almagalRunningDir/analysis_scripts
    
    #
    my_workedFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_step10.txt
    if [ -f "$my_workedFile" ]; then
        #echo "::: ALMAGAL command ::: Copy the product results to the original data directory"
        #cp -pr $my_runningPath/$my_almagalRunningDir $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/.
        
        echo "::: ALMAGAL command ::: Processed finished, create check file"
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step*
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_step*
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step0.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step1.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step2.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step3.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step4.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step5.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step6.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step7.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step8.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step9.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step10.txt
    fi
    #
    my_workedFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_step14.txt
    if [ -f "$my_workedFile" ]; then
        #echo "::: ALMAGAL command ::: Copy the product results to the original data directory"
        #cp -pr $my_runningPath/$my_almagalRunningDir $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/.
        
        echo "::: ALMAGAL command ::: Processed finished, create check file"
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step*
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_step*
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step11.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step12.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step13.txt
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_step14.txt
    fi
    #
    my_workedFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_step90.txt
    if [ -f "$my_workedFile" ]; then
        #echo "::: ALMAGAL command ::: Copy the product results to the original data directory"
        #cp -pr $my_runningPath/$my_almagalRunningDir $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/.
        
        echo "::: ALMAGAL command ::: Processed finished, create check file"
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step*
        rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_step*
        touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_all.txt
        
        if [ "$my_storagePath" != "$my_mainPath" ]; then
            echo "::: ALMAGAL command ::: Products available in the main directory"
            echo "::: ALMAGAL command ::: Copying products to storage directory"
            cp -rp $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished* $my_storagePath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/.
        fi
    fi
    

    #
    #my_workedFile=$my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_ToModifyCURRENTSTEP.txt
    #if [ -f "$my_workedFile" ]; then
    #    echo "::: ALMAGAL command ::: Copy the product results to the original data directory"
    #    cp -pr $my_runningPath/$my_almagalRunningDir $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/.
    #fi

    #
    ##echo "::: ALMAGAL command ::: Processed finished, create check file"
    ##rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt
    ##rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step*
    #if [ -f "$my_workedFile" ]; then
    #    echo "::: ALMAGAL command ::: Processed finished, create check file"
    #    rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/active.txt
    #    rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/running_step*
    #    rm $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/worked_ToModifyCURRENTSTEP.txt
    #    touch $my_mainPath/2019.1.00195.L/sources/ToModifySOURCE/pipeline/ToModifyTELESCOPE/finished_ToModifyCURRENTSTEP.txt
    #fi
    
    #
    echo "::: ALMAGAL command ::: Move outside the running directory"
    cd ..
    
    #
    echo "::: ALMAGAL command ::: Remove the running directory"
    rm -rf $my_runningPath/$my_almagalRunningDir

fi
