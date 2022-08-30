.. _simulation_process:

Modeling Process Details
========================

This chapter describes how to set up a sim batch and gives an overview of how to control the modeling process and understand the pre- and post-processing that occurs during the batch process.

Understanding Simulation Pre- and Post-Processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The goal of simulation pre-processing is to set up the simulation workspace before simulation, including any modifications to data loaded from the specified param files.  For example, users may load a particular vehicle param file and then want to change the test weight or roadload in some manner and then run the simulation, perhaps as part of a sweep of test weight values.  Any arbitrary M-script can be run in order to prepare the simulation workspace.

The ``REVS_VM`` model itself performs some post-processing to create simulation results (phase integrated results, for example), datalogs, and to perform any auditing that may be desired.  These tasks are handled by creating ``result``, ``datalog`` and ``audit`` objects in the workspace from the ``class_REVS_result``, ``class_REVS_datalog`` and ``class_REVS_audit`` classes respectively.  These objects are created in the model's ``StopFcn`` callback which can be seen in the model's Model Properties dialog box.

Simulation post-processing may be used to take the raw simulation outputs and calculate fuel economy or GHG emissions.  The default simulation post-processing is generally used but any M-script may be run if desired.

Batch post-processing may be used to examine the total set of simulation results and perform additional processing such as finding performance-neutral results from among a set of runs and then outputting those results to a separate file.  Any arbitrary M-script may be run if desired.

There are a few ``class_REVS_sim_batch`` properties that control pre- and post-processing of the simulation data by determining which processing scripts to run.

    * ``sim_case_preprocess_script``: by default is set to ``REVS_preprocess_sim_case`` which performs pre-processing for the most common overrides that should apply to pretty much any simulation case, regardless of the type of project being worked on.  The overrides/modifiers come from optional config string tags.  For example, the ``ETW_LBS:`` tag may be used to override the vehicle test weight from the vehicle param file.  For application-specific pre-processing, create a custom script that would (generally) call ``REVS_preprocess_sim_case`` and then perform additional pre-processing.  The custom script may handle user-defined application-specific config tags.  For example, regarding 2025 Mid-Term Evaluation work, the ``MTE_batch_sim_case_preprocess`` script calls ``REVS_preprocess_sim_case`` and then performs MTE-related overrides and defaults for aspects such as transmission sizing or behavior.

    * ``sim_case_postprocess_script``: by default is set to ``REVS_postprocess_sim_case`` which handles calculating fuel economy for the three main powertrain types (Conventional, Hybrid, and Electric).  This script calculates cold-corrected FTP and weighted FTP-HWFET results from the raw phase results, among other things.

    * ``postprocess_script``: by default is set to ``REVS_postprocess_sim_batch`` which has code for finding performance-neutral runs out of a simulation set that provides a performance baseline for one or more sets of runs.  The selected runs, if any, are output to a separate output file.

Understanding Config Strings (Keys)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Formatting for the config strings is defined by vectors of one or more instances of ``class_REVS_sim_config_options``.  The easiest way to see which config tags are available to a sim batch is to use the ``sim_batch.show_keys`` method.

This will display a list of ``sim_config`` fieldnames in the 'Key' column, the key tags in the 'Tag' column, option default values, an optional description and the name of the script which defines the key in the 'Provided by' column.  A partial list, for example:

::

    sim_batch.show_keys

::

	   Key                                    |     Tag                |     Default Value                  |     Provided by                |     Description
	-------------------------------------------------------------------------------------------------------------------------------------------------------
	aggregation_keys                          |                        |                                    |  class_REVS_sim_batch          |
	test_data                                 |  DATA                  |                                    |  REVS_config_external_data     |
	test_data_index                           |  DATA_INDEX            |  1                                 |  REVS_config_external_data     |
	external_drive_cycle                      |  XCYC                  |  0                                 |  REVS_config_external_data     |
	external_trans_temp                       |  XTTMP                 |  false                             |  REVS_config_external_data     |
	external_shift                            |  XSHFT                 |  false                             |  REVS_config_external_data     |
	external_lockup                           |  XLOCK                 |  false                             |  REVS_config_external_data     |
	external_accessory_elec                   |  XEACC                 |                                    |  REVS_config_external_data     |
	external_accessory_mech                   |  XMACC                 |                                    |  REVS_config_external_data     |
	external_cyl_deac                         |  XDEAC                 |  false                             |  REVS_config_external_data     |
	ambient                                   |  AMB                   |  {ambient=class_REVS_ambient;}     |  REVS_config_ambient           |
	package                                   |  PKG                   |                                    |  REVS_config_vehicle           |
	drive_cycle                               |  CYC                   |                                    |  REVS_config_vehicle           |
	vehicle                                   |  VEH                   |                                    |  REVS_config_vehicle           |
	driver                                    |  DRV                   |  {driver=class_REVS_driver;}       |  REVS_config_vehicle           |
	vehicle_lbs                               |  VEH_LBS               |                                    |  REVS_config_vehicle           |
	vehicle_kg                                |  VEH_KG                |                                    |  REVS_config_vehicle           |
	performance_mass_penalty_kg               |  PERF_KG               |  0                                 |  REVS_config_vehicle           |
	ETW_lbs                                   |  ETW_LBS               |                                    |  REVS_config_vehicle           |
	ETW_kg                                    |  ETW_KG                |                                    |  REVS_config_vehicle           |
	ETW_multiplier                            |  ETW_MLT               |  1                                 |  REVS_config_vehicle           |
	target_A_lbs                              |  TRGA_LBS              |                                    |  REVS_config_vehicle           |
	target_B_lbs                              |  TRGB_LBS              |                                    |  REVS_config_vehicle           |
	target_C_lbs                              |  TRGC_LBS              |                                    |  REVS_config_vehicle           |
    ...

``sim_config`` is a struct variable created automatically by ``class_REVS_sim_batch`` and is made available to the simulation workspace prior to simulation. The ``sim_config`` fieldnames give at least a preliminary understanding of what a tag means and can be further examined by taking a look at the default pre- and post-processing scripts.

Within a ``class_REVS_sim_config_options`` package each key is an instance of a ``class_REVS_sim_config_key``.  For example:

::

    package = class_REVS_sim_config_options();

    package.keys = [ ...
        class_REVS_sim_config_key('drive_cycle',         'tag', 'CYC',    'eval', false);
        class_REVS_sim_config_key('ETW_lbs',             'tag', 'ETW_LBS');
        class_REVS_sim_config_key('roadload_multiplier', 'tag', 'RL_MLT', 'default', 1.0);
        ...
        ]

The arguments to the ``class_REVS_sim_config_key`` constructor are the property name, optional 'tag' followed by the tag string, optional 'eval' followed by tag evaluation type, optional 'default' followed by a default value, and optional 'description' followed by a plaintext description of the key's purpose.

Literal Config Tags
-------------------
In the example above, the ``drive_cycle`` property holds a non-evaluated tag, which means the part of the string associated with that tag will not automatically be evaluated (turned into a numeric or other value, but rather taken as a string literal).  Typically this would be used for something like file names or other strings.  Literal tags may be evaluated in user scripts.  For example, if the literal tag was the name of a script, then that script may be called in the user pre- or post-processing scripts at the appropriate time to perform whatever its function is.  Literal tags can be used to hold a single value or, when combined with delayed evaluation (in a user script, instead of during config string parsing) may hold multiple values.  For example, within a config string, these are possible uses of the CYC: tag:

::

    CYC:EPA_IM240
    CYC:{''EPA_FTP_NOSOAK'',''EPA_HWFET'',''EPA_US06''}

In the first example, the CYC: tag refers to a single drive cycle file, ``EPA_IM240.mat`` which will be used for the simulation.  In the second case, the CYC: tag is used to store a string representation of a Matlab cell array of drive cycle strings.  In this case, ``sim_config.drive_cycle`` would be:

::

    '{''EPA_FTP_NOSOAK'',''EPA_HWFET'',''EPA_US06''}'

which would evaluate (using the Matlab ``eval()`` or ``evalin()`` command) the cell array of strings:

::

    {'EPA_FTP_NOSOAK','EPA_HWFET','EPA_US06'}

Drive cycle loading of a single cycle or the combining of multiple cycles into a single cycle is automatically handled in ``class_REVS_sim_case.load_drive_cycles()`` but the same concept can apply to user-defined literal tags initiated by user scripts.  Drive cycle creation and handling will be discussed in further detail later.

Eval Config Tags
----------------

As shown previously, the ``ETW_lbs`` key is an 'eval' tag which means its value will be automatically evaluated during pre-processing.  If the eval tag is created with a default value, that value will be used if the tag is not specified by the user.  Eval tags should be numeric or should refer to variables available in the workspace.  An eval tag may evaluate to a single value or a vector of multiple values to perform variable sweeps.  For example, the following would all be valid eval tags within a config string:

::

    ETW_LBS:3625
    ETW_LBS:[3000:500:5000]
    ETW_LBS:4454*[0.8,1,1.2]

The first case evaluates to a single number, 3625.  The second case evaluates to a vector, [3000 3500 4000 4500 5000] as does the last case which becomes [3563.2 4454 5344.8].  Any valid Matlab syntax may be used in an eval tag including mathematical operations such as multiply, divide, etc.  If addition is used, there must not be any spaces surrounding the + sign because ' + ' (space, plus-sign, space) is the separator used to build composite config strings and will result in an erroneously split string.

Config String Expansion
-----------------------

Each string in the sim batch ``config_set`` cell array is evaluated to determine how many simulations are defined.  As previously explained, each tag may be used to define multiple values.  Each config string is expanded to a full factorial combination of all of its elements.  The expanded set of strings is stored in the sim batch ``expanded_config_set`` property after the ``expand_config_set()`` method is called.  Config set expansion is handled automatically by the ``class_REVS_sim_batch`` ``run_sim_cases()`` method but under certain circumstances it may also be useful to manually expand the config set, although this is not typically done.  Manual expansion could be used to examine the number of cases represented by a config set without having to commit to running any simulations.

For example, the following tag could be used within a config string to run simulations with and without engine start-stop:

::

    + SS:[1,0] +

which would turn into two strings in the expanded config set:

::

    + SS:1 +
    + SS:0 +

An example with multiple tags with multiple values, this time for start-stop and normalized torque converter lockup:

::

    + SS:[1,0] + LU:[0,1] +

which would turn into four strings in the expanded config set, representing all four cases:

::

    + SS:0 + LU:0 +
    + SS:0 + LU:1 +
    + SS:1 + LU:0 +
    + SS:1 + LU:1 +

String expansion provides a simple and powerful method for defining entire sets of simulations within a single user-defined config string.

Config String Left-Hand-Side and Right-Hand-Side and Unique Key Numbers
-----------------------------------------------------------------------

A special string separator, || (double vertical bars), may be used to separate the left and right hand sides of a config string.  This is typically used for processing performance neutral runs but could also be used for any user-defined purpose.  For performance neutral runs the left hand side of the string defines the unique simulation case and the right hand side is used to define multiple engine scaling levels to evaluate for performance neutrality and GHG emissions.  The ``REVS_postprocess_sim_batch`` script considers all cases with the same left hand side to represent a single simulation case and then chooses the result from that set that meets performance criteria and has the lowest GHG emissions.  Each unique left hand side is assigned a unique key number through the UKN: tag by the ``class_REVS_sim_batch gen_unique_config_set()`` method.

For example, this:

::

    'SS:[1,0] + LU:[0,1]'

becomes this, representing four unique cases:

::

    'UKN:1 + SS:1 + LU:0'
    'UKN:2 + SS:1 + LU:1'
    'UKN:3 + SS:0 + LU:0'
    'UKN:4 + SS:0 + LU:1'

On the other hand, this:

::

    'SS:[1,0] || LU:[0,1]'

becomes this four simulations that represent two unique cases:

::

    'UKN:1 + SS:1 || LU:0'
    'UKN:1 + SS:1 || LU:1'
    'UKN:2 + SS:0 || LU:0'
    'UKN:2 + SS:0 || LU:1'

In this way, subsets of simulation batches may be considered as groups and the unique key number can be used to find these groups in the output file and then process them accordingly.  In either case, all four simulations will run and all four results will be available in the output summary file.

Creating New Config Tags
------------------------

``class_REVS_sim_config`` defines quite a few useful tags that should cover many modeling applications but new ones are easy to add.  Adding a new tag is as simple as adding a new property to ``class_REVS_sim_config``:

::

    new_config  = class_REVS_config_element('NEWTAG:', 'eval', 42);

which would show up as the following when calling ``class_REVS_sim_config.show_tags``:

::

    'NEWTAG:42  -> sim_config.new_config'

The default value (if provided) is shown next to the tag, in this case the default value for ``sim_config.new_config`` is 42.  The variable ``sim_config.new_config`` would now be available for use in user pre- and post- processing scripts.

How to Use ``sim_config`` Values
--------------------------------

The value of a ``sim_config`` property is accessed through the value property.  In addition, the ``has_value()`` method can be used to check if a value has been set by the user before being used in a script.  For example, from ``REVS_preprocess_sim_case``:

::

    if sim_config.adjust_A_lbs.has_value
        vehicle.coastdown_adjust_A_lbf = sim_config.adjust_A_lbs.value;
    end

A default value, if provided, is always available even if the user has not provided a value (i.e. ``has_value()`` returns false).

Output Summary File Keys
------------------------

The ``has_value()`` method is also used to cull unnecessary tags from the config string that appear in the output summary file Key column.  Culling empty or default value tags from the Key column makes the strings easier to read and understand but still specifies the correct simulation parameters.

Keys from the output file can be used directly in new config sets by cutting and pasting them into user batch file config sets.  In this way, an end-user of the simulation results can select runs to examine further or may even create new config strings to be run.  Because the output summary file is a .csv file, commas in the Key column are replaced with # symbols to prevent incorrect column breaks.  Even though the # symbol is not a valid Matlab operator, these strings can still be used directly in new config sets.  The batch process converts #'s to commas before parsing the strings.

.. _controlling_datalogging_and_auditing:

Controlling Datalogging and Auditing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section describes how to control the datalogging and auditing features of ALPHA.

Controlling Datalogging
-----------------------

Datalogging and auditing are controlled by the ``logging_config`` property of the ``class_REVS_sim_batch`` object.  ``logging_config`` is an object of class ``class_REVS_logging_config``.  The constructor of ``class_REVS_sim_batch`` takes a single optional argument which is the default log list.  A log list is a ``class_REVS_log_package`` object.  Many predefined log lists are contained in the ``REVS_Common\log_packages`` folder.

The following are typical examples of creating a sim batch and setting up the default datalogging:

::

    sim_batch = class_REVS_sim_batch(REVS_log_default);

Logs only the bare minimum required to calculate fuel economy and GHG emissions, this runs the fastest

::

    sim_batch = class_REVS_sim_batch(REVS_log_all);

Logs every available signal, this runs the slowest

::

    sim_batch = class_REVS_sim_batch(REVS_log_engine);

Logs the most common engine signals of interest

::

    sim_batch = class_REVS_sim_batch(REVS_log_engine_all);

Logs every available engine signal

Log packages can also be combined by using the ``logging_config.add_log()`` method:

::

    sim_batch = class_REVS_sim_batch(REVS_log_default);
    sim_batch.logging_config.add_log(REVS_log_engine);
    sim_batch.logging_config.add_log(REVS_log_transmission);

        Logs the minimum required signals and adds common engine and transmission datalogs

Understanding the ``datalog`` and ``model_data`` Objects
--------------------------------------------------------

The datalog object has hierarchical properties.  The top level should look something like this:

::

    datalog =
      class_REVS_datalog with properties:

         accessories: [1×1 class_REVS_logging_object]
            controls: [1×1 class_REVS_logging_object]
         drive_cycle: [1×1 class_REVS_logging_object]
              driver: [1×1 class_REVS_logging_object]
            electric: [1×1 class_REVS_logging_object]
              engine: [1×1 class_REVS_logging_object]
        transmission: [1×1 class_REVS_logging_object]
             vehicle: [1×1 class_REVS_logging_object]
                time: [137402×1 double]

For example, vehicle speed can be plotted versus time:

::

    plot(datalog.time, datalog.vehicle.output_spd_mps);

The datalog object is also associated with a ``class_test_data`` object called ``model_data``.  The primary difference between the two is that ``model_data`` represents a subset of the logged data and has a common, high-level namespace that can be used to compare model data with test data or data from multiple model runs or even data different models.  For example, vehicle speed can be plotted versus time:

::

    plot(model_data.time, model_data.vehicle.speed_mps);

Generally the best option is to use ``model_data`` for most analysis if it contains what is needed.  Datalogs are copied to the ``model_data`` object through the ``REVS_postprocess_XXX`` M-scripts in the ``REVS_Common/log_packages`` folder.

For example, ``REVS_postprocess_engine_basics_log.m``:

::

    model_data.vehicle.fuel.mass_g               = datalog.engine.fuel_consumed_g;

    model_data.engine.speed_radps                = datalog.engine.crankshaft_spd_radps;
    model_data.engine.crankshaft_torque_Nm       = datalog.engine.crankshaft_trq_Nm;
    model_data.engine.load_at_current_speed_norm = datalog.engine.load_norm;

    model_data.engine.fuel.density_kgpL_15C      = engine.fuel.density_kgpL_15C;
    model_data.engine.fuel.energy_density_MJpkg  = engine.fuel.energy_density_MJpkg;
    model_data.engine.fuel.flow_rate_gps         = datalog.engine.fuel_rate_gps;
    model_data.engine.fuel.mass_g                = datalog.engine.fuel_consumed_g;

As demonstrated in this example, the fuel properties are pulled from multiple sources (the engine itself and the engine datalogs) and put into a common location in the ``model_data`` object.  Generally, the datalogs are model-centric and may contain shorthand notation (trq versus torque) whereas the model data is more function- or component-centric and uses a more universal naming convention.  There is no automatic method for populating the ``model_data properties`` (scripts must be written by the user) and not all datalogs have (or should have) an associated property in the model data.  Postprocess scripts are associated with ``class_REVS_log_package`` objects through the ``postprocess_list`` property which is a cell array of scripts to run after datalogging.

For example, the ``REVS_log_all`` package is:

::

    function [log_package] = REVS_log_all()

    log_package = class_REVS_log_package;

    log_package.log_list = {
        'result.*'
        'datalog.*'
        };

    log_package.package_list = {mfilename};

    log_package.postprocess_list = {'REVS_postprocess_accessory_battery_log',
                                    'REVS_postprocess_alternator_log',
                                    'REVS_postprocess_DCDC_log',
                                    'REVS_postprocess_drive_motor_log',
                                    'REVS_postprocess_engine_basics_log',
                                    'REVS_postprocess_engine_idle_log',
                                    'REVS_postprocess_mech_accessories_log',
                                    'REVS_postprocess_propulsion_battery_log',
                                    'REVS_postprocess_transmission_log',
                                    'REVS_postprocess_vehicle_basics_log',
                                    'REVS_postprocess_vehicle_performance_log',
                                    };

    end

.. _auditing:

Auditing
--------

Auditing can be controlled by setting a sim batch ``logging_config`` audit flag:

::

    logging_config.audit_total = true;

Audits the total energy flow for the entire drive cycle.

Or:

::

    logging_config.audit_phase = true;

Audits the total energy flow for the entire drive cycle and also audits each drive cycle phase individually.

By default both flags are set to false, only one flag or the other needs to be set.  To print the audit to the console, use the ``print()`` method:

::

    audit.print

This should return something like the following for a conventional vehicle:

::

       EPA_UDDS audit: -----------------

             ---- Energy Audit Report ----

    Gross Energy Provided            = 28874.34 kJ
        Fuel Energy                  = 28868.08 kJ     99.98%
        Stored Energy                =     6.26 kJ      0.02%
        Kinetic Energy               =     0.00 kJ      0.00%
        Potential Energy             =     0.00 kJ      0.00%

    Net Energy Provided              =  7641.47 kJ
        Engine Energy                =  7637.05 kJ   99.94%
             Engine Efficiency       =    26.46 %
        Stored Energy                =     4.41 kJ    0.06%
        Kinetic Energy               =     0.00 kJ    0.00%
        Potential Energy             =     0.00 kJ    0.00%

    Energy Consumed by ABC roadload  =  3007.20 kJ     39.35%
    Energy Consumed by Gradient      =     0.00 kJ      0.00%
    Energy Consumed by Accessories   =   823.48 kJ     10.78%
        Starter                      =     0.40 kJ      0.01%
        Alternator                   =   286.81 kJ      3.75%
        Battery Stored Charge        =     0.00 kJ      0.00%
        Engine Fan                   =     0.00 kJ      0.00%
             Electrical              =     0.00 kJ      0.00%
             Mechanical              =     0.00 kJ      0.00%
        Power Steering               =     0.00 kJ      0.00%
             Electrical              =     0.00 kJ      0.00%
             Mechanical              =     0.00 kJ      0.00%
        Air Conditioning             =     0.00 kJ      0.00%
             Electrical              =     0.00 kJ      0.00%
             Mechanical              =     0.00 kJ      0.00%
        Generic Loss                 =   536.27 kJ      7.02%
             Electrical              =   536.27 kJ      7.02%
             Mechanical              =     0.00 kJ      0.00%
        Total Electrical Accessories =   536.27 kJ      7.02%
        Total Mechanical Accessories =     0.00 kJ      0.00%
    Energy Consumed by Driveline     =  3811.03 kJ     49.87%
         Engine                      =     0.00 kJ      0.00%
         Launch Device               =   541.63 kJ      7.09%
         Gearbox                     =  1572.46 kJ     20.58%
             Pump Loss               =   874.74 kJ     11.45%
             Spin Loss               =   382.50 kJ      5.01%
             Gear Loss               =   256.71 kJ      3.36%
             Inertia Loss            =    58.51 kJ      0.77%
         Final Drive                 =     0.00 kJ      0.00%
         Friction Brakes             =  1669.65 kJ     21.85%
         Tire Slip                   =    27.30 kJ      0.36%
    System Kinetic Energy Gain       =     0.44 kJ      0.01%
                                        ------------
    Total Loss Energy                =  7642.15 kJ
    Simulation Error                 =    -0.68 kJ
    Energy Conservation              =  100.009 %

How to Save and Restore Simulation Workspaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several methods available to save and restore simulation workspaces.  Generally, only one approach will be used at a time, but it is possible to combine approaches if desired.

.. _retain_workspaces_in_memory:

Retain Workspaces in Memory
---------------------------

The simplest approach, for a relatively small number of simulations, is to retain the workspace in memory.  Set the sim batch ``retain_output_workspace`` property to true.  For example:

::

    sim_batch.retain_output_workspace = true;

The workspace will be contained in the sim batch ``sim_case`` property which holds one or more ``class_REVS_sim_case`` objects.  To pull the workspace into the top-level workspace, use the sim case's ``extract_workspace()`` method:

::

    sim_batch.sim_case(1).extract_workspace;

The workspace is contained in the sim case workspace property but extracting the workspace to the top-level makes it easier to work with.

.. _saving_the_input_workspace:

Saving the Input Workspace
--------------------------

The simulation workspace may be saved prior to simulation by setting the sim batch ``save_input_workspace`` property to true:

::

    sim_batch.save_input_workspace = true;

This will create a timestamped ``.mat`` file in the sim batch output folder's ``sim_input`` directory.  The filename also includes the index of the sim case.  For example, the input workspace for the first simulation (``sim_1``) in a batch:

::

    output\sim_input\2019_02_11_16_46_37_sim_1_input_workspace.mat

The workspace is saved after all pre-processing scripts have been run so the workspace contains everything required to replicate the simulation at a later time.  This can be useful when running too many simulations to retain the workspaces in memory while also providing the ability to run individual cases later without having to set up a sim batch.  The workspace may be loaded by using the load command, or double-clicking the filename in the Matlab Current Folder file browser.

.. _saving_the_output_workspace:

Saving the Output Workspace
---------------------------

The simulation workspace may be saved after simulation by setting the sim batch ``save_output_workspace`` property to true:

::

    sim_batch.save_output_workspace = true;

This will create a timestamped ``.mat`` file in the sim batch output folder.  The filename also includes the index of the sim case.  For example, the output workspace for the first simulation (``sim_1``) in a batch:

::

    output\2019_02_11_16_52_39_sim_1_output_workspace.mat

The workspace is saved after all post-processing scripts have been run so the workspace contains everything required to replicate the simulation at a later time and also all of the datalogs, audits, etc.  The simulation may be run again or the outputs examined directly without the need for running the simulation.  Keep in mind that output workspaces will always be bigger than input workspaces and also take longer to save.  The workspace may be loaded by using the load command or double-clicking the filename in the Matlab Current Folder file browser.

.. _post_simulation_data_analysis:

Post-Simulation Data Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As mentioned, a ``model_data`` object is created in the output workspace and may contain various model outputs.  One of the easiest ways to take a look at simulation data is to run a Data Observation Report (DOR) on the model data.  There are DORs for conventional (CVM), hybrid (HVM) and electric vehicles (EVM).  To run the default conventional vehicle model DOR, use the ``REVS_DOR_CVM()`` function:

::

    REVS_DOR_CVM({}, model_data);

The first parameter (unused, in this case) allows the model outputs to be compared with one or more sets of test data in the form of ``class_test_data`` objects.  If there are multiple sets of test data, the first input would be a cell array of ``class_test_data`` objects.   The default DOR generates a number of plots representing some of the most commonly observed outputs such as vehicle speed, engine speed, transmission gear number, etc.  For example:

.. csv-table:: Sample Figures from ``REVS_DOR_CVM()``
    :file: tables/sample_figures.csv

The various DORs support several optional arguments, known as varargs in Matlab.  Optional arguments are passed in after the ``model_data`` and consist of strings and/or string-value pairs.  For example:

::

    REVS_DOR_CVM({}, model_data, 'name of some vararg', vararg_value_if_required);

The top-level DOR calls sub-DORs that are grouped by component, for example ``REVS_DOR_CVM()`` calls ``REVS_DOR_vehicle()``, ``REVS_DOR_engine()``, etc.  Each component DOR may have its own unique varargs in addition to supporting some common varargs.  Varargs passed to the top-level DOR are automatically passed to the component DORs.  Available varargs are listed in :numref:`(Table %s) <dortable>`.

.. _dortable:

.. csv-table:: List of Available DOR Varargs
    :file: tables/DOR.csv
    :widths: 42 35 30 50
    :header-rows: 1


Understanding Datalogging
^^^^^^^^^^^^^^^^^^^^^^^^^

This section will provide details on how to control and understand the datalogging process in ALPHA.

Logging Overview
----------------
Logging model internal signals is probably one of the most important things the model does, it is also one of the things that has the biggest impact on model run time.  Simulink seems to incur quite a bit of overhead related to logging data to the workspace.  As a result, ALPHA implements a flexible system to control how much or how little data is logged from the model.  In this way, the user can trade off run time speed and the logging of signals of interest.

The ``REVS_Common\log_packages`` folder contains functions to define pre-made 'packages' of signals for datalogging, and also scripts for post-processing the data if required.

``class_REVS_log_package`` defines the data structure used to define datalogs.  Each package has three properties:

* ``log_list`` - a list of ``datalog`` or ``result`` signals to enable.  Signal names can include ``*`` wildcards.  For example, ``result.engine.crankshaft*`` would log all result signals that start contain ``engine.crankshaft`` such as ``result.phase.engine.crankshaft_tot_kWh`` or ``result.phase.engine.crankshaft_pos_kJ``.  Result signals are a unique form of datalog that record final values for each phase of the drive cycle.  So for each phase of the drive cycle a ``result`` will contain a scalar value for each signal.  The result may be a sum or an average or other statistical data such as a minimum or maximum.  See the ``logging_lib`` for more details.

* ``package_list`` - a package may contain other packages, however in practice, each package lists itself in the ``package_list`` and the total package list is the unique set of all the individual packages.  So, each ``REVS_log_XXX.m`` will contain ``log_package.package_list = {mfilename};``.  Metapackages are formed by creating a list of packages, such as ``REVS_log_CVM_metapackage`` which creates the metapackage of conventional vehicle model (CVM) datalogs:

::

    function [log_package] = REVS_log_CVM_metapackage()

    log_package = [
                   REVS_log_vehicle_basics
                   REVS_log_engine_basics
                   REVS_log_transmission
                   REVS_log_alternator
                   REVS_log_accessory_battery
                   REVS_log_mech_accessories
                  ];

    end

* ``postprocess_list`` - contains a list of one or more post-processing scripts to run after the workspace has been populated with data.  For example, ``REVS_log_engine_basics`` lists ``REVS_postprocess_engine_basics_log`` to post-process data from raw simulation signals into the ``model_data`` structure for more universal use in post-processing scripts such as plotting simulation data versus real-world test data as in a ``DOR``.

Logging Details
---------------
Since it's not possible for Simulink datalogs to directly create stuctured output, there is a process for populating hierarchical data structures from individual workspace datalog variables.  This possible through the naming scheme employed by the datalogging blocks.  For example, the raw post-simulation workspace will contain variables such as:

::

    audit__accessories__air_conditioner__elec_neg_kJ
    dl__engine__crankshaft_trq_Nm
    rsltp__engine__fuel_consumed_g

The prefix determines the top-level data structure.  ``audit`` maps to the ``audit`` data structure, ``dl`` maps to ``datalog`` and ``rsltp`` maps to the ``phase`` property of the ``result`` data structure, as in ``result.phase``.

The double underscores, ``__``, define the hierarchical structure.  For example, ``audit__accessories__air_conditioner__elec_neg_kJ`` will become ``audit.accessories.air_conditioner.elec_neg_kJ`` in the final workspace.  Single underscores are taken as part of the property name.

The construction of the raw workspace variable names is handled by the mask of the datalog blocks and can determined by the structure of the model.  For example, datalogs in the ``engine`` block model will automatically be placed in the ``datalog.engine`` structure without having to be explicitly named as such.  For example, the ``datalog.engine.fuel_rate_gps`` signal is set up as follows:

.. image:: figures/engine_fuel_rate_gps_mask.jpg

The only user-specified part of the name is ``fuel_rate_gps``, the rest is automatic, and the final result is previewed in the ``Datalog Name`` text box.

Understanding Auditing
^^^^^^^^^^^^^^^^^^^^^^
Auditing is controlled through the ``sim_batch`` object ``audit_total`` and ``audit_phase`` boolean properties.

If ``audit_total`` is ``true`` then an audit for the drive cycle as a whole will be performed and the resulting summary will be sent the console or an output file.  This is the most commonly used approach for enabling an audit.

If ``audit_phase`` is ``true`` then an audit for each drive cycle phase **and** the total drive cycle will be produced.

Setting both ``audit_total`` and ``audit_phase`` to ``true`` results in the same output as setting ``audit_phase`` by itself.

The ``audit`` structure, like the ``result`` structure, contains only scalar values.

For example:

::

    >> audit.total.engine

        ans =

            class_REVS_logging_object with properties:

                 crankshaft_delta_KE_kJ: 0.3309
                crankshaft_delta_KE_kWh: 9.1911e-05
                      crankshaft_neg_kJ: 604.0453
                     crankshaft_neg_kWh: 0.1678
                      crankshaft_pos_kJ: 7.4220e+03
                     crankshaft_pos_kWh: 2.0617
                      crankshaft_tot_kJ: 6.8180e+03
                     crankshaft_tot_kWh: 1.8939
                        fuel_consumed_g: 703.2932
                           gross_neg_kJ: 450.6905
                          gross_neg_kWh: 0.1252
                           gross_pos_kJ: 8.0877e+03
                          gross_pos_kWh: 2.2466
                           gross_tot_kJ: 7.6371e+03
                          gross_tot_kWh: 2.1214

    >> audit.phase.engine

        ans =

          class_REVS_logging_object with properties:

             crankshaft_delta_KE_kJ: [0.3321 -0.0017]
            crankshaft_delta_KE_kWh: [9.2236e-05 -4.6631e-07]
                  crankshaft_neg_kJ: [250.3882 353.6571]
                 crankshaft_neg_kWh: [0.0696 0.0982]
                  crankshaft_pos_kJ: [3.6640e+03 3.7581e+03]
                 crankshaft_pos_kWh: [1.0178 1.0439]
                  crankshaft_tot_kJ: [3.4136e+03 3.4044e+03]
                 crankshaft_tot_kWh: [0.9482 0.9457]
                    fuel_consumed_g: [319.6850 383.6047]
                       gross_neg_kJ: [192.0876 258.6029]
                      gross_neg_kWh: [0.0534 0.0718]
                       gross_pos_kJ: [3.9019e+03 4.1858e+03]
                      gross_pos_kWh: [1.0839 1.1627]
                       gross_tot_kJ: [3.7098e+03 3.9272e+03]
                      gross_tot_kWh: [1.0305 1.0909]

It should be noted here that the total and phase audits may appear to have discrepancies.  In other words, the sum of the phase audit results may not add up to the total result for the same variable, such as ``fuel_consumed_g``.  This is because the phase audit results are only for phase numbers greater than zero.  In the case of a drive cycle where the engine start is not sampled (not part of the phase results), the first five seconds may be phase zero.  Also, it takes a couple of simulation time steps at the end of the drive cycle to shut down the model, and those are also phase zero.

Enabling the audits populates the workspace with audit data, via the ``class_REVS_audit`` class.  ``class_REVS_audit`` is also responsible for calling the report generators for each unique powertrain type, as follows:

* ``class_REVS_CVM_audit`` - calculates and reports energy balances for Conventional Vehicle Models

* ``class_REVS_EVM_audit`` - calculates and reports energy balances for Electric Vehicle Models

* ``class_REVS_HVM_audit`` - calculates and reports energy balances for Hybrid Vehicle Models

There is no automatic method for the Simulink model itself to comprehend the correct sources and sinks of energy within the model, this is determined by the creator of the model and is based on the underlying physics of the powertrain components.

The audit classes for the various powertrains inherit methods and properties from a base class, ``class_REVS_VM_audit``, which handles audit calculations common to all powertrains, i.e. brakes, tires, roadload losses, etc.

The audit energy datalogs (as seen above) are tallied according to whether they are sources of energy or sinks of energy in the ``calc_audit`` methods of the audit classes.  If the model, audit datalogging and audit calculations are correct then the sum of the energy in the audit sinks will equal the sum of the energy in the audit sources.  The sources and sinks are tallied in the ``energy_balance`` property of the audit class.

::

    >> audit.total.energy_balance

    ans =

      struct with fields:

                         source: [1×1 struct]
                           sink: [1×1 struct]
            simulation_error_kJ: -0.5840
        energy_conservation_pct: 100.0157

    >> audit.total.energy_balance.source

    ans =

      struct with fields:

              KE_kJ: 0
        gradient_kJ: 0
              gross: [1×1 struct]
                net: [1×1 struct]

    >> audit.total.energy_balance.sink

    ans =

      struct with fields:

            KE_kJ: 0.4379
          vehicle: [1×1 struct]
        accessory: [1×1 struct]
         total_kJ: 3.7313e+03

The audit sources consist of ``gross`` and ``net`` categories, where ``gross`` refers to fuel chemical energy and energy stored in batteries, for example.  ``net`` refers to energy used to power the vehicle and/or run electrical accessories, for example.

::

    >> audit.total.energy_balance.source.gross

    ans =

      struct with fields:

          fuel_kJ: 1.3157e+04
        stored_kJ: 8.0583
         total_kJ: 1.3165e+04

    >> audit.total.energy_balance.source.net

    ans =

      struct with fields:

                    engine_kJ: 3.7237e+03
        engine_efficiency_pct: 28.3017
                    stored_kJ: 7.0347
                     total_kJ: 3.7307e+03


The difference between the net source energy and the total sink energy is the simulation error, which should be very small and is recorded as the energy balance ``energy_conservation_pct`` where 100% is the desired value.

::

    >> audit.total.energy_balance.source.net.total_kJ

    ans =

       3.7307e+03

    >> audit.total.energy_balance.sink.total_kJ

    ans =

       3.7313e+03

    >> audit.total.energy_balance.energy_conservation_pct

    ans =

      100.0157

Typical sources of simulation error are clutch / driveline re-engagements where the small modeled disparity in speeds at lockup causes a small gain or loss of kinetic energy.  If the audit is off by a larger amount then either there is a problem with the model or a problem with the audit itself.  Most of the time the audit is incorrect when there's a discrepancy.  For example, a new component may have been added to the model but the ``calc_audit`` function has not been updated to include the energy as a source or sink, or perhaps the audit datalog has been placed on the wrong signal line or at the incorrect point in the model.  One technique for sorting out whether an error is a just a simulation error due to approximation (like the slightly mismatched speeds) or due to an actual or accounting error is to run the model at a finer timestep.  Generally, simulation errors should decrease as the step size decreases and audit or accounting errors should remain unchanged.

When creating an audit for a new component it's very important to understand that the topology of the blocks in the model in most cases is not the same as the topology of the sources and sinks of energy in the model.  It's tempting to place an audit datalog at the inputs and outputs of the blocks in the model, but if the block is not properly a source or sink of energy then the audit will likely fail.  For example, torques and speeds may pass through several Simulink blocks, but each block is not necessarily a "source" of energy for the next block downstream.

In any case, it's important to track down audit issues if and when they occur.
