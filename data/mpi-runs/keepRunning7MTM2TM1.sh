#!/bin/bash

for i in {1..500}
    do
        echo "::: ALMAGAL command ::: Create individual script files"
        #gomodule
        #gopython
        python createIndividual_scriptForJointDeconvolution.py --array 7MTM2TM1 --idrange 10 100
        if [ -f "my_executeJointDeconvolution.sh" ]; then
            echo "::: ALMAGAL command ::: Execute available sources for processing"
            if [ $i  -lt 10 ]; then
                ./my_executeJointDeconvolution.sh > my_executeJointDeconvolution_7MTM2TM1_auto000$i.log
            fi
            if [ $i  -ge 10 ] && [ $i -lt 100 ]; then
                ./my_executeJointDeconvolution.sh > my_executeJointDeconvolution_7MTM2TM1_auto00$i.log
            fi
            if [ $i  -ge 100 ] && [ $i -lt 1000 ]; then
                ./my_executeJointDeconvolution.sh > my_executeJointDeconvolution_7MTM2TM1_auto0$i.log
            fi
            if [ $i  -ge 1000 ] && [ $i -lt 10000 ]; then
                ./my_executeJointDeconvolution.sh > my_executeJointDeconvolution_7MTM2TM1_auto$i.log
            fi
        fi
        
        # Wait for 2 minutes until next execution
        echo "::: ALMAGAL command ::: Wait 2 minutes after having executed step $i"
        sleep 2m 
    done
