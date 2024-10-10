ALMAGAL - Processing scripts and instructions for the ALMAGAL project
-----------------------------------------------------------------------------------

This README file contains a brief description of the procedures and scripts that are used to process the ALMAGAL data. If you encounter problems or find out that some files may be missing, contact Alvaro Sanchez-Monge at asanchez < at > ice.csic.es

**ALMAGAL** is a ALMA Cycle 7 Large Program that observes 1017 high-mass star-forming regions distributed throughout the Milky Way. See more details at: [ALMAGAL website](http://www.almagal.org/)

If you find some of the information contained in this GitHub repository useful in your work, please cite this publication:

**Sanchez-Monge et al. 2024, submitted to Astronomy & Astrophysics**

The paper describes in detail the different steps used for processing the ALMAGAL dataset, including an improved continuum determination strategy, the implemented automatized self-calibration procedures, and the imaging strategy for joint-deconvolved, combined ALMA arrays

<br/>
<br/>

There are nine major sections in this document. They are intended to help you navigate through the different files and to understand the procesures used. The sections include information on:
  - [**Data calibration and preparation**](https://github.com/betacygni/ALMAGAL#data-calibration-and-preparation)
  - [**Pipeline imaging and continuum determination**](https://github.com/betacygni/ALMAGAL#pipeline-imaging-and-continuum-determination)
  - [**Self-calibration**](https://github.com/betacygni/ALMAGAL#self-calibration)
  - [**Data combination**](https://github.com/betacygni/ALMAGAL#data-combination)
  - [**Transfer of products to your local workstation**](https://github.com/betacygni/ALMAGAL#transfer-of-products-to-your-local-workstation)
  - [**Directory structure**](https://github.com/betacygni/ALMAGAL#directory-structure)
  - [**Order of execution of the scripts**](https://github.com/betacygni/ALMAGAL#order-of-execution-of-the-scripts)
  - [**Information on science data products**](https://github.com/betacygni/ALMAGAL#information-on-science-data-products)
  - [**Download and usage of GitHub repository**](https://github.com/betacygni/ALMAGAL#download-and-usage-of-github-repository)
  

------------------------------------
Data calibration and preparation
------------------------------------

We use data calibrated using the standard pipeline procedures that the ALMA observatory and its staff run when preparing the data to be stored at the ALMA science archive.

The calibrated data can therefore be obtained using three different methods:

  - **Method 1.-**  
  Download raw data and standard calibration scripts from the [ALMA archive website](https://almascience.eso.org/asax/) and follow instructions to produce the necessary calibrated measurement sets.
  - **Method 2.-**  
  Request calibrated measurement sets through the ALMA helpdesk. To do this, you can consider the following instructions. After that, you will receive an email with download links from where you have access to the calibrated measurment sets.
    - log in at the [ALMA helpdesk](https://help.almascience.org/)
    - select "Submit Helpdesk Ticket"
    - add your name and e-mail address
    - indicate the department "Archive and Retrieval Data (EU)"
    - for subject, you can type: Data request (calibrated MS) for 2019.1.00195.L
    - message can be formatted as:  
      With the following helpdesk ticket, I would like to request for the calibrated data of the following MOUS (belonging to the project 2019.1.00195.L).  
      1.- Project code: 2019.1.00195.L - MOUS: uid://A001/X1288/X1046  
      2.- Project code: 2019.1.00195.L - MOUS: uid://A001/X1288/X1048
    - you need to provide the MOUS codes. These can be found in the SnooPI webpage for the corresponding project
    - submit the ticket
  - **Method 3.-**  
  All the available data are already processed in some workstations (e.g. Juelich). Therefore, you can access the calibrated data by transfering them from Juelich to your computer. In order to do this, follow the instructions given in [Transfer of products to your local workstation](https://github.com/betacygni/ALMAGAL#transfer-of-products-to-your-local-workstation).
  
Once downloaded, the calibrated measurement sets are stored in (see [Directory structure](https://github.com/betacygni/ALMAGAL#directory-structure) below for more information)

```
data/2019.1.00195.L/science_goal.uid___A001_X1467_X1d3
data/2019.1.00195.L/science_goal.uid___A001_X146c_X95
```

These "science_goal" directories are based on the SGOUS (Science Goal Obs Unit Set) that exist in the directory structure of the ALMA science archive. They contain "group" directories based on the GOUS (Group Obs Unit Set), which ultimately contain the MOUS (Member Obs Unit Set) directories. Inside these MOUS directories, it is possible to find a calibrated directory containing the calibrated measurement set files.

The calibrated measurement sets exist for each individual execution block (EB). These execution blocks may contain multiple sources (from a few to several hundred sources). The imaging scripts have been prepared to independently process individual sources. Therefore, it is necessary to split / divide the data contained in the calibrated measurement sets for each individual source. This is done using the script **scriptToSplitSources.py** (see [Order of execution of the scripts]((https://github.com/betacygni/ALMAGAL#order-of-execution-of-the-scripts)) below), with the command

```
python scriptToSplitSources.py
```

The script uses CASA 5.6.1 and the function split to create individual measurement sets for each source, for each execution block. The final measurement sets are compressed with a tar command to reduce the number of files that have to be stored. In order to execute the scriptToSplitSources.py script, it is necessary to have access to the source names and the different MOUS (Member Obs Unit Set) where each source was observed. This information is stored in the excel table **database.xslx** that is available within the directory ```data/database``` which is read using a pandas frame python function. The sources are then listed with an identifier from 0 to 1016 (total number of sources 1017). The data of each source is stored in

```
data/2019.1.00195.L/sources/SOURCE_NAME/ARRAY/perEB
```

where ```SOURCE_NAME``` is the ALMAGAL name of the source (e.g., 543150) and ```ARRAY``` is the configuration of the telescope (e.g., 7M, TM2, TM1).


------------------------------------
Pipeline imaging and continuum determination
------------------------------------

The main goal of the scripts presented in this section is to process each source (for each individual array) through a series of pipeline and additional CASA tasks in order to produce: (1) images of the continuum and data cubes for each source and array individually, (2) production of a ```cont.dat``` file containing the frequency ranges that can be used for continuum determination, (3) a series of pipeline weblogs and casalogs that contain information that will be used when combining different arrays.

There are three major steps to be executed to achive the above mentioned goals:
  - Setting up the configALMAGAL.py file
  - Execution of (pipeline and additional) imaging procedures
  - Storage of products for following analysis (e.g., data combination)

<br/>

**Setting up the configALMAGAL.py file**

This config file is intended to include and store relevant information for the execution of the scripts. Information that can not be hardcoded in the scripts, because it is expected to change from workstation to workstation. Currently, there are two major sets of variables to be defined. The first block is necessary for transfering data from Juelich to your local workstation (see below), while the second block is necessary for the execution of the processing scripts.

For the current purpose, edit the following information:
  - ```my_workstation``` : name of the workstation / computer where you will process the data
  - ```my_mainPath``` : path where scripts and data are stored
  - ```my_runningPath``` : path where data will be processed (e.g. /dev/shm indicates the memory disk commonly used in supercomputers)
  - ```my_softwarePath``` : path where software is stored
  - ```my_storagePath``` : path where you plan to compress and store the products. It can be set to be the same as my_mainPath in case you do not have access to a cold-storage location

<br/>

**Execution of (pipeline and additional) imaging procedures**

The main script to be executed is **createIndividual_scriptForImaging.py**, which requires a series of additional scripts (see  [Order of execution of the scripts]((https://github.com/betacygni/ALMAGAL#order-of-execution-of-the-scripts)) below). You can explore the main commands using

```python createIndividual_scriptForImaging.py --help```

There are two main parameters that have to be set up when executing the script: (1) array to be processed (i.e., 7M, TM2, TM1), and (2) the identifiers (ID) of the sources to be processed. Remember, this identifiers are determined on the basis of the database excel files discussed above (i.e., database.xslx). Some examples are:

Prepare imaging scripts for source ID 0 and for the array 7M  
```python createIndividual_scriptForImaging.py --array 7M --id 0```

Prepare imaging scripts for source ID 600 and for the array TM2  
```python createIndividual_scriptForImaging.py --array TM2 --id 600```

Prepare imaging scripts for sources in the ID range 0 to 10 and for the array T7M  
```python createIndividual_scriptForImaging.py --array 7M --idrange 0 10```

The product of this script is a series of files tuned in to process one of the steps for the selected source and array. For example, in the first example, the products are the following scripts: 

```mainScriptForImaging7M_0_7M.sh```  
```run_mainScriptForImaging7M_0_7M```  
```scriptForImaging7M_0_7M.py```  

In addition to these scripts, you will have an additional bash script:

```my_executeImaging.sh``` (or alternatively ```my_executeImagingStep0.sh``` necessary in JSC)

To proceed with the imaging of the selected source / array, you just need to execute the last indicated bash script:

```./my_executeImaging.sh```

After the script has finished, you can **repeat to proceed with the following steps**. Currently, there are 6 different processing steps when processing 7M data, and 15 steps for the TM2 data. Once all the steps are executed, you can proceed to the last step.

<br/>

**Storage of products for following analysis (e.g., self-calibration and data combination)**

The main script to be executed is ```tarPipelineProducts.py```

This script has to be executed twice for each source. In the first execution, the pipeline products are processed to create (i) FITS files of the continuum and data cubes, which are then compressed in the tar file **pipeline-fits.tar**, (ii) a tar file containing the pipeline weblogs, casalogs and the cont.dat file containing the continuum frequency ranges and named **pipeline-weblogs.tar**, and (iii) a tar file containing all the pipeline processing files named **almagal.tar**

In the second execution, if a cold-storage space exists, the newly produced tar files will be transferred to that location.


------------------------------------
Self-calibration
------------------------------------

The main goal of the scripts presented in this section is to perform an automatic self-calibration on each source (for each individual array). For this, we follow the standard interferometric guidelines that suggest that for phase-only self-calibration we need to detect the target with a signal-to-noise ratio (SNR) > 3 in a solution time shorter than time for significant phase variations for all baselines to a single antenna. Based on this, the SNR necessary to do self-calibration is defined as:

$$SNR_\mathrm{selfcal} = \frac{I_\mathrm{peak,cont}}{\mathrm{rms} _\mathrm{cont} \times \sqrt{N _\mathrm{ant}-3} \times \sqrt{t _\mathrm{exp} / t _\mathrm{int}}}$$

where $I_\mathrm{peak,cont}$ is the peak intensity of the continuum emission, $\mathrm{rms}_ \mathrm{cont}$ is the rms noise level of the continuum iamge, $N _\mathrm{ant}$ is the number of antennas available during the observation, $t _\mathrm{exp}$ is the total on-source observing time, and $t _\mathrm{int}$ is the solution time interval, that we equal to the integration time of the observations.

There are two major steps to be executed to achive the above mentioned goals:
  - Execution of self-calibration procedures
  - Storage of products (i.e., self-calibrated visibilities) for following analysis (e.g., data combination)

<br/>

**Execution of self-calibration procedures**

The main script to be executed is **createIndividual_scriptForSelfCalibration.py**, which requires a series of additional scripts (see  [Order of execution of the scripts]((https://github.com/betacygni/ALMAGAL#order-of-execution-of-the-scripts)) below). You can explore the main commands using

```python createIndividual_scriptForSelfCalibration.py --help```

There is one parameter that have to be set up when executing the script: (1) the identifiers (ID) of the sources to be processed. Remember, these identifiers are determined on the basis of the database excel files discussed above (i.e., database.xslx). Some examples are:

Prepare self-calibration scripts for source ID 0 
```python createIndividual_scriptForSelfCalibration.py --id 0```

Prepare self-calibration scripts for sources in the ID range 0 to 10
```python createIndividual_scriptForSelfCalibration.py --idrange 0 10```

The product of this script is a series of files tuned in to process one of the steps for the selected source and array. For example, in the first example, the products are the following scripts: 

```mainScriptForSelfCalibration_0.sh```  
```run_mainScriptForSelfCalibration_0```  
```scriptForSelfCalibration_0.py```  

In addition to these scripts, you will have an additional bash script:

```my_executeSelfCalibration.sh```

To proceed with the imaging of the selected source, you just need to execute the last indicated bash script:

```./my_executeSelfCalibration.sh```

This will execute the self-calibration for the three arrays individually (i.e., 7M, TM2 and TM1).

<br/>

**Storage of products for following analysis (e.g., data combination)**

The main script to be executed is ```tarSelfCalibrationProducts.py```



------------------------------------
Data combination
------------------------------------

Following self-calibration, the next major goal is to produce combined images (i.e., images in which the data from different array configurations are used together). For this, we follow a CLEANing strategy in which the mask grows gradually to avoid divergence and to ensure recovery and CLEANing of the extended (fainter) emission. Details on the procedure are described in the published paper (see above). The following scripts can be used to image both combined arrays as well as individual arrays.

There are two major steps to be executed to achive the above mentioned goals:
  - Execution of joint-deconvolved imaging procedures
  - Storage of final products

<br/>

**Execution of joint-deconvolved imaging procedures**

The main script to be executed is **createIndividual_scriptForJointDeconvolution.py**, which requires a series of additional scripts (see  [Order of execution of the scripts]((https://github.com/betacygni/ALMAGAL#order-of-execution-of-the-scripts)) below). You can explore the main commands using

```python createIndividual_scriptForJointDeconvolution.py --help```

There are two main parameters that have to be set up when executing the script: (1) array or combination of arrays to be processed (i.e., 7M, TM2, TM1, 7MTM2, 7MTM2TM1), and (2) the identifiers (ID) of the sources to be processed. Remember, these identifiers are determined on the basis of the database excel files discussed above (i.e., database.xslx). Some examples are:

Prepare joint-deconvolution imaging scripts for source ID 0 and all three arrays combined
```python createIndividual_scriptForSelfCalibration.py --array 7MTM2TM1 --id 0```

Prepare joint-deconvolution imaging scripts for sources in the ID range 0 to 10 and two arrays (7M and TM2) combined
```python createIndividual_scriptForSelfCalibration.py --array 7MTM2 --idrange 0 10```

The product of this script is a series of files tuned in to process one of the steps for the selected source and array. For example, in the first example, the products are the following scripts: 

```mainScriptForSelfCalibration7MTM2TM1_0_7MTM2TM1.sh```  
```run_mainScriptForSelfCalibration7MTM2TM1_0_7MTM2TM1```  
```scriptForSelfCalibration7MTM2TM1_0_7MTM2TM1.py```  

In addition to these scripts, you will have an additional bash script:

```my_executeJointDeconvolution.sh```

To proceed with the imaging of the selected source, you just need to execute the last indicated bash script:

```./my_executeJointDeconvolution.sh```

This will execute the joint-deconvolution imaging for the array (or combination or arrays) and source selected..

<br/>

**Storage of final products**

The main script to be executed is ```tarJointDeconvolutionProducts.py```



------------------------------------
Transfer of products to your local workstation
------------------------------------

Transfer of the data is done by using the python script **scriptToFetchData.py**

The following information is intended to help you when executing the script to transfer data from the Juelich computer to your local computer. This is only available for the members of the ALMAGAL consortium, and it will be superseeded in the near future when the final storage repository is completely set up. If you encounter problems or strange behaviours, please contact Alvaro Sanchez-Monge at asanchez < at > ice.csic.es

  - **Step 0.- Usage of the data**  
  The data products currently available are for use by ALMAGAL consortium members. They will be made publicly available once the corresponding papers are finalized and published.
  
  - **Step 1.- Access to Juelich computers**  
  Follow the instructions given in the file **Instructions_to_access_JSC.pdf** which can be found in the directory ```data/documents```  
  First important note, set up your ssh-key with a file named:  
  ```> ~/.ssh/id_ed25519_jsc```  
  Second important note, when connecting to the JSC computers to transfer data to your local computer, you will need to connect from the same IP address that you indicated when uploading the ssh-key
  
  - **Step 2.- Location of scriptToFetchData.py**  
  After cloning the GitHub repository you should find the script **scriptToFetchData.py** in the directory ```data/mpi-runs``` together with two other files: **idfile.dat** and **srcdata.dat** that are provided as examples (see below), and the **configALMAGAL.py** file, necessary to set up you path and workstation information  
  The file to be executed is scriptToFetchData.py  
  You do NOT have to change the location of this file
  
  - **Step 3.- Update your configALMAGAL.py file**  
  Edit the required information in the **configALMAGAL.py** file. In particular, define:  
    - ```my_usernameJSC``` : your username in the Juelich computers. If you do not have a user, follow instructions in the documents directory.
    - ```my_workstationTransfer``` : name of the workstation / computer where you will transfer the data to
    - ```my_storagePathTransfer``` : path where the data will be stored in your local workstation / computer
  
  - **Step 4.- Execute scriptToFetchData.py**  
  You can explore the arguments of the python script by exploring its help:  
  ```> python scriptToFetchData.py --help```  
  Some examples on how to execute the script:  
    - Transfer the available FITS products for the 7M array for source 49143  
      ```> python scriptToFetchData.py --fitsProducts --array 7M  --source 49143```
    - Transfer the available FITS products for the TM2 array for source 49143  
      ```> python scriptToFetchData.py --fitsProducts --array TM2 --source 49143```
    - Transfer the available FITS products for all the arrays for source 49143  
      ```> python scriptToFetchData.py --fitsProducts --array ALL --source 49143```
    - Transfer the available FITS products for the 7M data for the sources included in the file sourcefile.dat  
      ```> python scriptToFetchData.py --fitsProducts --array 7M  --srcfile sourcefile.dat```

Depending on the configuration of the ssh-keys in your computer, you may be asked by the passphrase everytime that you transfer a file from Juelich to your workstation. If this is the case, you can do the following:

```> eval $(ssh-agent)```

```> ssh-add ~/.ssh/id_ed25519_jsc```

------------------------------------
Directory structure
------------------------------------

The ALMAGAL GitHub project is structured to enable an easy storage of the data and an effective processing of the data, considering that new data are expected to arrive in the forthcoming months, and that new re-executions of scripts may be necessary. Also, the major structure of the files has been determined in part based on the execution and storage capabilities existing at the Juelich Supercomputer Center, where most of the processing of the data is performed.

The ALMAGAL directory is divided in two major directories **data** and **software**, each one containing multiple sub-directories:

| Directory | Description |
| --- | --- |
| `data` | Contains the data and scripts |
| `data/2019.1.00195.L` | **Main directory** with calibrated and imaged products. This is not existing in the GitHub due to is large size |
| `data/cleanUp` | Contains a basic bash script to clean-up the mpi-runs directory, which tends to be populated by scripts during the processing of the data |
| `data/database` | Contains a csv and excel file with information of the ALMAGAL source sample. These files are used by multiple scripts to iterate over different sources |
| `data/database/products` | Contains csv files with information about the scientific products (e.g., image information, self-calibration information) |
| `data/documents` | Contains relevant documents that can be used to gather more information about the scripts and procedures |
| `data/mpi-runs` | **Main directory** with the scripts to be executed |
| `software` | Contains the software packages necessary for processing the data |
| `software/analysisUtils` | Contains a number of CASA functions necessary for processing the data |
| `software/casa-pipeline-release-5.6.1-8.el7` | CASA version to be used for the ALMAGAL project*** |
| `software/python` | Required python packages |

*** Note that CASA is not included in this Git repository because of the large size of the file. The version used is CASA 5.6.1-8 and it is available for download [here](https://casa.nrao.edu/download/distro/casa-pipeline/release/el7/casa-pipeline-release-5.6.1-8.el7.tar.gz)

------------------------------------
Order of execution of the scripts
------------------------------------

- **Step 0** : **Download calibrated data from ALMA science archive**  
  Store data in ```$SCRATCH``` and ```$DATA1``` (in Juelich Supercomputer Center, JSC; DATA1 corresponds to the old LARGEDATA)  
  Untar the copy stored in ```$SCRATCH```

- **Step 1** : **Set up the configuration file**  
  
  ```configALMAGAL.py```    

- **Step 2** : **Split calibrated data per source and EB (execution block)**  
  
  ```scriptToSplitSources.py```  
  
  Required:
    - database.csv file containing names and MOUS directory tree
    - calibrated MOUS files

- **Step 3** : **Create pipeline products for individual arrays**  
  
  ```createIndividual_scriptForImaging.py```  
  
  Required:  
    - database.xlsx file containing names and MOUS directory tree  
    - calibrated split files produced with scriptToSplitSources.py  
    - master scripts:  
          REFIND.py  
          scriptForImaging7M.py  
          run_mainScriptForImaging7M  
          mainScriptForImaging7M.sh  
          scriptForImagingTM2.py  
          run_mainScriptForImagingTM2  
          mainScriptForImagingTM2.sh  
          scriptForImagingTM1.py  
          run_mainScriptForImagingTM1  
          mainScriptForImagingTM1.sh  
          scriptForImagingTM1_serial.py  
          run_mainScriptForImagingTM1_serial  
          mainScriptForImagingTM1_serial.sh  

- **Step 4** : **Store pipeline products and weblogs**  
  
  ```tarPipelineProducts.py```  
  
  Required:
    - database.csv file containing names and MOUS directory tree
    - pipeline products created by createIndividual_scriptForImaging.py

- **Step 6** : **Apply self-calibration to each EB**  
  
  ```createIndividual_scriptForSelfCalibration.py```  
  
  Required:
    - database.csv file containing names and MOUS directory tree
    - calibrated split files produced with scriptToSplitSources.py
    - pipeline-weblog tar file produced with scriptToSplitSources.py and stored with tarPipelineProducts.py
    - master scripts:  
          scriptForSelfCalibration.py  

- **Step 7** : **Store self-calibration products**  
  
  ```tarSelfCalibrationProducts.py```  
  
  Required:
    - database.csv file containing names and MOUS directory tree
    - self-calibration products created by createIndividual_scriptForSelfCalibration.py

- **Step 8** : **Create joint-deconvolved image of multiple arrays**  
  
  ```createIndividual_scriptForJointDeconvolution.py```  
  
  Required:
    - database.xlsx file containing names and MOUS directory tree
    - calibrated split files produced after evaluting self-calibration
    - pipeline-weblog tar files stored with tarPipelineProducts.py
    - master scripts:  
          scriptForJointDeconvolution7M.py  
          run_mainScriptForJointDeconvolution7M  
          mainScriptForJointDeconvolution7M.sh
          scriptForJointDeconvolutionTM2.py  
          run_mainScriptForJointDeconvolutionTM2  
          mainScriptForJointDeconvolutionTM2.sh
          scriptForJointDeconvolutionTM1.py  
          run_mainScriptForJointDeconvolutionTM1  
          mainScriptForJointDeconvolutionTM1.sh
          scriptForJointDeconvolution7MTM2.py  
          run_mainScriptForJointDeconvolution7MTM2  
          mainScriptForJointDeconvolution7MTM2.sh
          scriptForJointDeconvolutionTM2TM1.py  
          run_mainScriptForJointDeconvolutionTM2TM1  
          mainScriptForJointDeconvolutionTM2TM1.sh
          scriptForJointDeconvolution7MTM2TM1.py  
          run_mainScriptForJointDeconvolution7MTM2TM1  
          mainScriptForJointDeconvolution7MTM2TM1.sh

- **Step 9** : **Store joint-deconvolution products**  
  
  ```tarJointDeconvolutionProducts.py```  
  
  Required:
    - database.xlsx file containing names and MOUS directory tree
    - pipeline products created by createIndividual_scriptForImaging.py

------------------------------------
Information on science data products
------------------------------------

The final FITS files of both continuum and cubes will be distributed by the ALMAGAL consortium in the near future. Here we provide some tables with information on the generated products. For example, properties of the produced images (both individual array and combined arrays), information on the self-calibration conditions and properties for the different sources and arrays, and additional potentially useful files. All this information is stored in a series of ```csv``` table files that are available within the ```data/database/products``` directory. In more detail, we provide:

**Basic information on the produced images**

The main script to be executed is ```tarJointDeconvolutionProducts.py```

**Information on the self-calibration products**

These files contain information about the rms noise, intensity peak, beam size of the different images produced during the iterative self-calibration process. In the following we list the name of the files and the labels of the header row, which can be used to identify the content included in each file:

- ```7M_almagal_selfcalibrationParameters.csv```
  - < empty > corresponding to the source ID
  - Source
  - 7M_i0_n_BMAJ
  - 7M_i0_n_BMIN
  - 7M_i0_n_BPA
  - 7M_i0_n_PEAK
  - 7M_i0_n_RMSSTD
  - 7M_i0_n_RMSMAD
  - 7M_i0_n_SNRSTD
  - 7M_i0_n_SNRMAD
  - 7M_i1_n_BMAJ
  - 7M_i1_n_BMIN
  - 7M_i1_n_BPA
  - 7M_i1_n_PEAK
  - 7M_i1_n_RMSSTD
  - 7M_i1_n_RMSMAD
  - 7M_i1_n_SNRSTD
  - 7M_i1_n_SNRMAD
  - 7M_i1_y_BMAJ
  - 7M_i1_y_BMIN
  - 7M_i1_y_BPA
  - 7M_i1_y_PEAK
  - 7M_i1_y_RMSSTD
  - 7M_i1_y_RMSMAD
  - 7M_i1_y_SNRSTD
  - 7M_i1_y_SNRMAD
  - ... and it repeats for iterations ```i2```, ```i3``` and ```i4```
 
- ```TM2_almagal_selfcalibrationParameters.csv```
  - the same as for 7M but for TM2

- ```TM1_almagal_selfcalibrationParameters.csv```
  - The same as for 7M but for TM1

The columns depict different iterations, with ```i0``` corresponding to no self-calibration attempted, and ```i1``` to ```i4``` the different steps (see publication listed in REFERENCE). The label ```n``` and ```y``` indicates if self-calibration solutions are not or yes applied (this helps to compare e.g., how the noise improves after self-calibration). The main parameters are information on the beam size (```BMAJ```, ```BMIN``` and ```BPA```), information on the peak intensity (```PEAK```), information on the noise measured in two different ways (```RMSSTD``` and ```RMSMAD```), and information on the signal-to-noise ratio (```SNRSTD``` and ```STDMAD```).

**Information on the fraction of bandwidth used for continuum determination**

These files contain information on the fraction of bandwidth used for the continuum determination for each source, individual array and spectral window. In the following we list the name of the file and the labels of the header row, which can be used to identify the content included in each file:

- ```almagal_continuumRanges.csv```
  - < empty > corresponding to the source ID
  - Source
  - contrange_spw0_7M
  - contrange_spw1_7M
  - contrange_spw2_7M
  - contrange_spw3_7M
  - contrange_spw0_TM2
  - contrange_spw1_TM2
  - contrange_spw2_TM2
  - contrange_spw3_TM2
  - contrange_spw0_TM1
  - contrange_spw1_TM1
  - contrange_spw2_TM1
  - contrange_spw3_TM1



------------------------------------
Download and usage of GitHub repository
------------------------------------

You can download and use the here provided scripts following the standard git functions. Major commands are listed here:
  - Move to the directory where you want to download, store and execute ALMAGAL data
  - Initialize git by typing
    ```git init```
  - Download / clone this repository by typing
    ```git clone https://github.com/betacygni/ALMAGAL```

<br/>
You will need to have CASA downloaded on your computer. Two different versions of CASA were used for different steps in the ALMAGAL processing workflow (see above). The two versions of CASA are not provided within the GitHub downloadable files because of the size of the CASA files, but they can be accessed in these weblinks:

  - [CASA 5.6.1](https://casa.nrao.edu/download/distro/casa-pipeline/release/el7/casa-pipeline-release-5.6.1-8.el7.tar.gz)
  - [CASA 6.2.0](https://casa.nrao.edu/download/distro/casa/release/rhel/casa-6.2.0-124.tar.xz)

The CASA packages have to be stored in the ```software``` directory that is downloaded from the GitHub page. Next steps require to un-compress certain files stored in the software directory. Move to that directory and untar the download CASA files, the ```python.tar.gz``` and ```python3.tar.gz``` files, and the ```analysisUtils.tar.gz```

Finally, setup the ```configALMAGAL.py``` file as indicated in different sections above.
