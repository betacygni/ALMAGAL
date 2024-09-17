########################################################################
#
#                      ALMAGAL config pipeline
#
#
# 
# Auxiliary script number 1              created by Alvaro Sanchez-Monge
#
# Description:      Python script to define user variables
#                   This information is used by processing scripts, and
#                   by the scripts that transfer data from Juelich to
#                   your local computer
# 
#-----------------------------------------------------------------------
# 
# Define variables for data transfer
#
# Variables are:
#
#    my_usernameJSC         : your username in the Juelich computers
#                             if you do not have a user, follow
#                             instructions in the documents directory
#    my_workstationTransfer : name of the workstation / computer where
#                             you will transfer the data to
#    my_storagePathTransfer : path where the data will be stored in
#                             your local workstation / computer
#
# Example:
#
# Alvaro Sanchez-Monge wants to transfer data from Juelich to his
# computer named ashur. His username in Juelich is sanchez-monge1.
# He wants to store the data in a partition named localdata.
# In this case, the variables that are defined are:
#
#   my_usernameJSC = 'sanchez-monge1'
#   my_workstationTransfer = 'ashur'
#   my_storagePathTransfer = '/localdata/projects/ALMA/ALMAGAL/ALMAGAL/data'
#
my_usernameJSC = 'sanchez-monge1'
my_workstationTransfer = 'ashur'
my_storagePathTransfer = '/localdata/projects/ALMA/ALMAGAL/ALMAGAL/data'


#-----------------------------------------------------------------------
#
# Define variables for data processing
#
# Variables are:
#
#    my_workstation         : name of the workstation / computer where
#                             you will process the data
#    my_mainPath            : path where scripts and data are stored
#    my_runningPath         : path where data will be processed
#                             e.g. /dev/shm indicates the memory disk
#                                  commonly used in supercomputers
#    my_softwarePath        : path where software is stored
#    my_storagePath         : path where you plan to compress and store 
#                             the products. It can be set to be the
#                             same as my_mainPath in case you do not
#                             have access to a cold-storage location
#
# Example 1:
#
# Alvaro Sanchez-Monge wants to process data in Juelich (JSC).
# The data directory tree of the ALMAGAL project exist in the path
#   /p/scratch/almagal/ALMAGAL/data
# However, this is not the location for calculations. In the JSC
# supercomputer, it is necessary to use the memory disk (/dev/shm)
# The required software (CASA, analysis utils, python packages) is
# stored in the path
#   /p/scratch/almagal/ALMAGAL/software
# Finally, once all the data are processed, he has access to a cold
# storage directory named
#   /p/data1/almagaldata/ALMAGAL/data
# Alternatively, he would use the same variable as for my_mainPath
# In this case, the variables that are defined are:
#
#   my_workstation = 'JSC'
#   my_mainPath = '/p/scratch/almagal/ALMAGAL/data'
#   my_runningPath = '/dev/shm'
#   my_softwarePath = '/p/scratch/almagal/ALMAGAL/software'
#   my_storagePath = '/p/data1/almagaldata/ALMAGAL/data'
#
# Example 2:
#
# Alvaro Sanchez-Monge wants to process data in his computer (ashur).
# The data directory tree of the ALMAGAL project exist in the path
#   /localdata/projects/ALMA/ALMAGAL/ALMAGAL/data
# However, this is not the location for calculations. The processing is
# done in the directory running with full path
#   /localdata/projects/ALMA/ALMAGAL/ALMAGAL/data/running
# The required software (CASA, analysis utils, python packages) is
# stored in the path
#   /localdata/projects/ALMA/ALMAGAL/ALMAGAL/software
# Finally, since he has no additional cold sotrage directory, he uses
# the same directory where the data are stored in first place. This 
# corresponds to the mainPath variable:
#   /localdata/projects/ALMA/ALMAGAL/ALMAGAL/data
# In this example, the variables that are defined are:
#
#   my_workstation = 'ashur'
#   my_mainPath = '/localdata/projects/ALMA/ALMAGAL/ALMAGAL/data'
#   my_runningPath = '/localdata/projects/ALMA/ALMAGAL/ALMAGAL/data/running'
#   my_softwarePath = '/localdata/projects/ALMA/ALMAGAL/ALMAGAL/software'
#   my_storagePath = '/localdata/projects/ALMA/ALMAGAL/ALMAGAL/data'
#
my_workstation = 'JSC'
my_mainPath = '/p/scratch/almagal/2-ALMAGAL/ALMAGAL/data'
my_runningPath = '/p/scratch/almagal/2-ALMAGAL/ALMAGAL/data/running'
my_softwarePath = '/p/scratch/almagal/2-ALMAGAL/ALMAGAL/software'
my_storagePath = '/p/data1/almagaldata/ALMAGAL/data'

