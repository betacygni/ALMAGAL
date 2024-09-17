Instructions for scriptToFetchData.py                        v 2021 Mar
------------------------------------------------------------------------

Transfer of the data is done by using the python script scriptToFetchData.py

The following information is intended to help you when executing the 
script to transfer data from the Juelich computer to your local 
computer. If you encounter problems or strange behaviours, please 
contact Alvaro Sanchez-Monge at sanchez < at > ph1.uni-koeln.de


!.......................................................................
!
!   Step 0.- Usage of the data
!

The data products currently available are not final science-ready
products. They are distributed:
(1) to evaluate that the processing worked fine,
(2) to identify possible problems or errors that need to be fixed, and
(3) to initiate and evaluate possible science case studies.

Regarding the scientific usage of the data I refer to the guidelines
and information presented by Sergio Molinari during the all-hands
meeting on July 20, 2020


!.......................................................................
!
!   Step 1.- Access to Juelich computers
!

Follow the instructions given in Instructions_to_access_JSC.pdf

First important note, set up your ssh-key with a file named:
> ~/.ssh/id_ed25519_jsc

Second important note, when connecting to the JSC computers to transfer
data to your local computer, you will need to connect from the same IP
address that you indicated when uploading the ssh-key


!.......................................................................
!
!   Step 2.- Location of this file
!

After untaring the provided file, you should have the following:


ALMAGAL
 |
 |-- data
      |
      |-- database
      |     |
      |     |-- almagal_physicalParameters.xlsx
      |     |
      |     |-- database.csv
      |     |
      |     |-- database.xlsx
      |
      |-- documents
      |     |
      |     |-- Instructions_to_acccess_JSC.pdf
      |     |
      |     |-- READMEscriptToFetchData.txt
      |
      |-- mpi-runs
            |
            |-- configALMAGAL.py
            |
            |-- scriptToFetchData.py
            |
            |-- idfile.dat
            |
            |-- srcfile.dat

The file to be executed is scriptToFetchData.py
You do NOT have to change the location of this file


!.......................................................................
!
!   Step 3.- Update your configALMAGAL.py file
!

Edit the required information in the configALMAGAL.py file. In 
particular, define:

> my_usernameJSC :         your username in the Juelich computers. If
                           you do not have a user, follow instructions
                           in the documents directory.
> my_workstationTransfer : name of the workstation / computer where you
                           will transfer the data to
> my_storagePathTransfer : path where the data will be stored in your
                           local workstation / computer


You will need a series of python packages. The versions for which the
script has been tested are:

   - astropy (version tested 2.0.8)
   - argparse (version tested 1.1)
   - pandas (version tested 0.18.1)


!.......................................................................
!
!   Step 4.- Executing scriptToFetchData.py
!

You can explore the arguments of the python script by exploring its help:
> python scriptToFetchData.py --help

Some examples on how to execute the script:

Transfer the available FITS products for the 7M array for source 49143
> python scriptToFetchData.py --fitsProducts --array 7M  --source 49143

Transfer the available FITS products for the TM2 array for source 49143
> python scriptToFetchData.py --fitsProducts --array TM2 --source 49143

Transfer the available FITS products for all the arrays for source 49143
> python scriptToFetchData.py --fitsProducts --array ALL --source 49143

Transfer the available FITS products for the 7M data for the sources included in the file sourcefile.dat
> python scriptToFetchData.py --fitsProducts --array 7M  --srcfile sourcefile.dat
