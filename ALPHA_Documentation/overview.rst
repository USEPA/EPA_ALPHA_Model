Overview
========

This chapter is meant to give a quick overview of how to run a pre-configured ALPHA simulation and understand the modeling process.

Running ALPHA - Quickstart
--------------------------
Launch Matlab and make sure ``REVS_Common`` and ``NVFEL_MATLAB_Tools`` are on the Matlab path as described in the installation instructions.  As a quick check execute the following Matlab command and if successful, the path to the top-level ALPHA model should return:

::

    which REVS_VM

If the command fails, double check the path setup.

Change the Matlab working directory to the ``ALPHA_Projects\ALPHA_DEMO`` folder and run ``run_ALPHA_quickstart``.  The ``REVS_VM`` model will open up (to watch the vehicle speed trace in real-time), compile and then run an EPA UDDS drive cycle.  When the simulation is complete there will be two files in the output folder.  The file names are prefixed with a timestamp, \YYYY_MM_DD_hh_mm_ss_, followed by ``quickstart_results.csv`` and ``quickstart_1_console.txt``.  For example, ``2019_02_01_09_36_23_ALPHA_quickstart_results.csv`` and ``2019_02_01_09_36_23_quickstart_1_console.txt``, for files created on February 1st 2019, 23 seconds after 9:36 AM.  The ``sim_results`` file contains a summary of the simulation inputs, settings and outputs.  The ``console.txt`` file captures anything that would have been output to the Matlab console window.  In this case the file contains the UDDS cycle phase summaries and the energy audit.

Examining the Matlab workspace after the model runs reveals a single variable, the ``sim_batch`` object.  The outputs from this model are contained in the output files.  More information on datalogging and model outputs will be discussed later.  To populate the top-level workspace with the simulation input and output data structures, execute the following command:

::

    sim_batch.sim_case(1).extract_workspace

Understanding the Modeling Process
----------------------------------

The fundamental modeling process consists of creating a Matlab workspace that contains all the variables necessary to run the ``REVS_VM`` (REVS Vehicle Model) Simulink model.  There are several ways to accomplish this.  The first approach below will be the primary focus of this document due to its numerous advantages as outlined below.

1. Create and execute a batch run using ``class_REVS_sim_batch``.

    * Consistent approach to the modeling process
    * Ability with sim batch to run any number of simulations
    * Standard output summary results
    * Framework for pre- and post-processing simulations
    * Convenient capability to sweep variables and define multiple simulation scenarios
    * Framework for running "performance neutral" simulations
    * Capability to run simulations in parallel, on one or multiple computers 
    * Automatically collates the results into a single output summary file
    * Framework for controlling simulation datalogging and auditing
    * Framework for controlling the amount ("verbosity") of output summary data
    * Framework for saving Matlab workspaces at various points in the modeling process
    * Easy and convenient method to define and reuse sim batches across multiple projects

2.	Load a saved workspace available in a ``.mat`` file and then run the model.  In this case the pre- and post-processing must be handled by the user, this is somewhat of an advanced use case but can be very useful under the right circumstances.

3.	Create an ad-hoc script to load individual param files (Matlab scripts containing component data structures) and manually perform the pre- and post-processing.  This was the process prior to the standardized batch process, which can lead to duplication of effort and  inconsistent approaches across users and therefore should be avoided.

What is a Sim Batch?
--------------------
A ``class_REVS_sim_batch`` object actually contains a vector of ``class_REVS_sim_case`` objects stored in the ``sim_case`` property.  A ``sim_case`` could be created and run without a batch but there is no advantage to doing so since the batch process provides all the necessary pre- and post-processing and is much easier to use.  Typically the only reason to manipulate a particular ``sim_case`` would be to extract its local workspace to populate the top-level workspace for direct access.  This will be covered in more detail later in the discussion on working with workspaces.

Understanding the ALPHA Quickstart Script
-----------------------------------------
The ``run_ALPHA_quickstart`` M-script demonstrates the simplest possible batch process - a single simulation run with the default settings and only the minimum required input files and minimal outputs.

    run_ALPHA_quickstart.m:

1.  ``clear; clear classes; clc;``

    * Clears the Matlab workspace, classes and console which is highly recommended before running a batch.

2.  ``sim_batch = class_REVS_sim_batch(REVS_log_default);``

    * Creates ``sim_batch``, an object of class ``class_REVS_sim_batch``, and instructs it to log only the minimum required signals in the model.  Datalogging will be discussed in more detail later.

3.  ``sim_batch.output_file.descriptor = strrep(mfilename, 'run_', '');``

    * Provides a descriptor string that identifies output files

4.  ``sim_batch.retain_output_workspace = true;``

    * Retains the simulation workspace in memory, for easier examination post-simulation

5.  ``sim_batch.logging_config.audit_total = true;``

    * Enables the simulation energy audit datalogging.  Disabling the audit speeds up model execution

6.  ``sim_batch.param_path = 'param_files/midsize_car';``

    * The batch needs to know where to find param files that are not in the ``REVS_Common`` folder.  In this case the param files are located in the ``midsize_car`` subfolder of the local ``param_files`` folder.

7.  ``sim_batch.config_set = {'VEH:vehicle_2020_midsize_car + ENG:engine_2013_Chevrolet_Ecotec_LCV_2L5_Reg_E10 + TRANS:TRX11_FWD + ELEC:electric_EPS + CYC:EPA_UDDS + CON:midsize_car_CVM_controls_param'};``

    * The ``sim_batch.config_set`` defines the set of the simulations to be run by creating a cell array of one or more config strings.  Within the config string are the tags VEH:, ENG:, TRANS:, ELEC:, CYC: and CON:.  Following each tag is the name of a file that contains simulation inputs.  The VEH: tag loads the vehicle information such as roadload, test weight, etc.  The ENG: tag loads the engine information, in this case the engine is actually loaded from ``REVS_Common`` since it is one of the data packet engines, the other param files are loaded from the local param file directory.  The TRANS: tag loads the transmission parameters, in this case for a 6-speed automatic.  The ELEC: tag loads parameters that define the electrical system and accessories for this vehicle.  The CYC: tag tells the simulation which drive cycle to run, in this case an EPA UDDS drive cycle.  Lastly, the CON: tag tells the simulation which controls settings to use.  In this case, the controls settings show that start-stop is disabled for this run.  The CVM in ``MPW_LRL_CVM_controls_param`` stands for Conventional Vehicle Model.  Other abbreviations that may be encountered are EVM for Electric Vehicle Model and HVM for Hybrid Vehicle Model.  Electric vehicles and hybrid vehicles have their own control parameters.

5.	``open REVS_VM;``

    * This simply opens the top-level Simulink model so the simulation progress can be observed via the vehicle speed and drive cycle plot that comes from the top-level scope block.  This step is optional.

6.	sim_batch.run_sim_cases();

    * This handles simulation pre-processing, running and post-processing.
