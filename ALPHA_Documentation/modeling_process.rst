.. _simulation_process:

Modeling Process Details
========================

This chapter contains a more detailed description of ALPHA batch simulation, how it is set up and gives an overview of how to use the provided features to conduct multiple simulations, perhaps sweeping model parameters or implementing custom pre or post processing to a batch run.

Batch Simulation Overview
^^^^^^^^^^^^^^^^^^^^^^^^^
ALPHA batch simulation is implemented via ``class_REVS_sim_batch`` which contains a variety of properties that control the simulation process. The following list is a summary of the contents of the more prominent class members which are detailed subsequently:
  
    * Configuration Key Definitions - What options are available to construct or modify the individual simulations

    * Configuration Set - List of simulations requested to be run defined via configuration Keys

    * Pre-processing Scripts - Scripts used to transform the configuration set into the model input workspace

    * Logging Configuration - What signals are to be logged and outputs generated

    * Post-processing Scripts - Scripts used to alter or interpret the simulation output data

These many different pieces work in concert to complete the batch simulation process. An analogy may be helpful in understanding how the different pieces work together. The configuration keys define the available knobs the user can turn to influence the simulation. The configuration set is a list of settings for each knob. The scripts (pre and post) are the linkage that connects the knobs to the model and output processing. 

Understanding Config Keys, Config Scripts & Config Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ALPHA batch simulation process, organized in ``class_REVS_sim_batch``, is is controlled via configuration keys. The keys defined for a for a given batch are stored in the ``sim_batch.config_keys`` property and can be viewed in a tabular format via the ``sim_batch.show_keys`` method. 

Config keys influence the simulation process through the pre- and post-processing scripts. The pre-processing scripts are stored the the ``sim_batch.case_preprocess_scripts``. These scripts may handle loading data for the simulation, modifying simulation parameters. Similarly, the ``sim_batch.case_postprocess_scripts`` and ``sim_batch.batch_postprocess_scripts`` enable some post processing or aggregation of the output data.

Given that Config Keys and Config Scripts work together to produce the simulation results they are commonly organized into config option packages. The packages included with ALPHA that can provide many commonly requested operations are stored in ``REVS_Common\config_packages``, with some metapackages, bundles of config options, covering each powertrain type.

The set of simulations to be run is defined using the config keys. The desired simulations (config set) are loaded into ``sim_batch.config_set``. This can be accomplished via two different methods that are discussed further in this section. The config set can be entered directly, or via config strings which are interpreted is the ``sim_batch.load_config_strings`` method. ALPHA also includes the capability to perform full-factorial expansion for given simulation configurations. This expanded set is accessible as an N x 1 structure in ``sim_batch.sim_configs``.  The example below shows a sample config string where a variety of tags are used. This string is then loaded into the batch which can then be viewed

::

    >> config_string = 'VEH:vehicle_FWD_midsize_car + ENG:engine_2013_Chevrolet_Ecotec_LCV_2L5_Reg_E10 + 
    TRANS:transmission_6AT_FWD_midsize_car + ELEC:electric_starter_alternator_param + ACC:accessory_HPS_param + 
    CYC:{''EPA_FTP_NOSOAK'',''EPA_HWFET''} + CON:CVM_controls_param_midsize_car + TRGA_LBS:30.62 + 
    TRGB_LBS:-0.0199 + TRGC_LBS:0.01954';

    >> sim_batch.load_config_strings(config_strings); % parse config strings
    >> sim_batch.config_set{1}

        struct with fields:

        aggregation_keys: {}
             drive_cycle: {{1×2 cell}}
                 vehicle: {'vehicle_FWD_midsize_car'}
            target_A_lbs: 30.6200
            target_B_lbs: -0.0199
            target_C_lbs: 0.0195
                  engine: {'engine_2013_Chevrolet_Ecotec_LCV_2L5_Reg_E10'}
            transmission: {'transmission_6AT_FWD_midsize_car'}
                electric: {'electric_starter_alternator_param'}
               accessory: {'accessory_HPS_param'}
                controls: {'CVM_controls_param_midsize_car'}


Config Keys & Tags
------------------
As mentioned previously the config keys are stored in ``sim_batch.config_keys`` and can be viewed via the ``sim_batch.show_keys`` method, an example of this is shown below. This will display a list of potential ``sim_config`` fieldnames in the 'Key' column, the key tags, for use in the config string, in the 'Tag' column, optional default values, an optional description and the name of the script which defined the key in the 'Provided by' column.

::

    >> sim_batch.show_keys

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

As mentioned previousy config keys are generally defined with their processing scripts within a pacakge constructed from ``class_REVS_sim_config_options`` where each key is an instance of a ``class_REVS_sim_config_key``.  For example:

::

    package = class_REVS_sim_config_options();

    package.keys = [ ...
        class_REVS_sim_config_key('drive_cycle',         'tag', 'CYC',    'eval', false);
        class_REVS_sim_config_key('ETW_lbs',             'tag', 'ETW_LBS');
        class_REVS_sim_config_key('roadload_multiplier', 'tag', 'RL_MLT', 'default', 1.0);
        ...
        ]

The arguments to the ``class_REVS_sim_config_key`` constructor are the property name, followed by optional name value pairs of 'tag' for the tag used in config strings, 'eval' for the tag evaluation type,  'default' for the default value to use if not provided in the config set, and 'description' to provide a plaintext description of the key's purpose.

Literal vs Eval Config Tags
---------------------------
When defining simulations via config strings the contents of some tags (keys) need to be evaluated while in other situations it may be preferred the value is retained in its string form. In the above example ``ETW_lbs`` key is an 'eval' tag which means its value will be automatically evaluated when loading the config strings.  If the eval tag is created with a default value, that value will be used if the tag is not specified by the user.  Eval tags are generally numeric, and must be an evaluatable expression.  An eval tag may evaluate to a single value or a vector of multiple values to perform variable sweeps.  For example, the following would all be valid eval tags within a config string:

::

    ETW_LBS:3625
    ETW_LBS:[3000:500:5000]
    ETW_LBS:4454*[0.8,1,1.2]

The first case evaluates to a single number, 3625.  The second case evaluates to a vector, [3000 3500 4000 4500 5000] as does the last case which becomes [3563.2 4454 5344.8].  Any valid Matlab syntax may be used in an eval tag including mathematical operations such as multiply, divide, etc.  If addition is used, there must not be any spaces surrounding the + sign because ' + ' (space, plus-sign, space) is the separator used to build composite config strings and will result in an erroneously split string.

In the previously referenced example above, the ``drive_cycle`` property holds a non-evaluated tag, which means the part of the string associated with that tag will not automatically be evaluated (turned into a numeric or other value, but rather taken as a string literal).  Typically this would be used for something like file names or other strings.  Literal tags may be evaluated in user scripts.  For example, if the literal tag was the name of a script, then that script may be called in the user pre- or post-processing scripts at the appropriate time to perform whatever its function is.  Literal tags can be used to hold a single value or, when combined with delayed evaluation (in a user script, instead of during config string parsing) may hold multiple values.  For example, within a config string, these are possible uses of the CYC: tag:

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

Building Config Set Directly
----------------------------
One workflow option is to build the config set by directly setting the ``sim_batch.config_set`` property. This property must be either a structure or cell array of structures. The latter allows a batch consisting of multiple groups of simulations to be constructed from different config keys. An example of a batch config set configured directly can be seen below:

::

    >> sim_batch.config_set.drive_cycle = {{'EPA_FTP_NOSOAK','EPA_HWFET'}}
    >> sim_batch.config_set.vehicle = {'vehicle_FWD_midsize_car'};
    >> sim_batch.config_set.engine = {'engine_2013_Chevrolet_Ecotec_LCV_2L5_Reg_E10'};
    >> sim_batch.config_set.transmission = {'transmission_6AT_FWD_midsize_car'};
    >> sim_batch.config_set.electric = {'electric_starter_alternator_param'};
    >> sim_batch.config_set.accessory = {'accessory_EPS_param'};
    >> sim_batch.config_set.controls = {'CVM_controls_param_midsize_car'};
    >> sim_batch.config_set.ETW_lbs = [3000:1000:5000];
    >> sim_batch.config_set.start_stop = [false, true];


In this example many of the config keys are set directly. Notice that the various string based keys are stored as cell arrays of strings. The reason for this will be discussed in the next section. It should also be noted that not all config keys need to be specified, and those not specified will use the default value established when that config key was defined. 

Config Set Expansion
--------------------
Individual config set entries are expanded full factorial to create multiple sim configs which become the cases in ``sim_batch.sim_case`` when the batch is executed. In the example above this single config set will yield 6 simulations, three different ETW values multiplied by two options for start stop. Note that while drive cycle may appear to contain multiple entries it is contained within an outer cell array and thus is a single entry. The expanded config set is accessible via ``sim_batch.sim_configs`` and each index represents a planned simulation. As shown below the the sim configs contain entries for all defined config keys, not just those specified in the config set.

::

    >> sim_batch.sim_configs

    ans = 

    6×1 struct array with fields:

        test_data
        test_data_index
        external_drive_cycle
        external_trans_temp
        external_shift
        external_lockup
        external_accessory_elec
        external_accessory_mech
        external_cyl_deac
        ambient
        package
        drive_cycle
        vehicle
        driver
        vehicle_lbs
        vehicle_kg
        performance_mass_penalty_kg
        ETW_lbs
        ETW_kg
        ETW_multiplier
        target_A_lbs
        target_B_lbs
        target_C_lbs
        dyno_set_A_lbs
        dyno_set_B_lbs
        dyno_set_C_lbs
        calc_ABC_adjustment
        target_A_N
        target_B_N
        target_C_N
        dyno_set_A_N
        dyno_set_B_N
        dyno_set_C_N
        adjust_A_lbs
        adjust_B_lbs
        adjust_C_lbs
        adjust_A_N
        adjust_B_N
        adjust_C_N
        roadload_multiplier
        NV_ratio
        FDR
        FDR_efficiency_norm
        powertrain_type
        vehicle_type
        vehicle_manufacturer
        vehicle_model
        vehicle_description
        tire_radius_mm
        engine
        fuel
        engine_vintage
        engine_modifiers
        engine_scale_pct
        engine_scale_kW
        engine_scale_hp
        engine_scale_Nm
        engine_scale_ftlbs
        engine_scale_L
        engine_scale_adjust_BSFC
        engine_scale_num_cylinders
        engine_deac_type
        engine_deac_num_cylinders
        engine_deac_scale_pct
        engine_deac_max_reduction_pct
        engine_deac_reduction_curve
        engine_deac_activation_delay_secs
        engine_DCP
        engine_CCP
        engine_GDI
        engine_transient_fuel_penalty
        engine_fuel_octane_compensation
        transmission
        transmission_vintage
        TC_K_factor
        TC_stall_rpm
        TC_torque_ratio
        TC_lockup_efficiency_pct
        transmission_autoscale
        electric
        propulsion_battery
        accessory_battery
        propulsion_battery_initial_soc_norm
        propulsion_battery_reference_soc_norm
        accessory_battery_initial_soc_norm
        propulsion_battery_cells_in_series
        propulsion_battery_cells_in_parallel
        propulsion_battery_cell_capacity_Ah
        MG1
        MG2
        P0_MG
        P2_MG
        MOT
        MG1_max_power_kW
        MG2_max_power_kW
        P0MG_max_power_kW
        P2MG_max_power_kW
        MOT_max_power_kW
        MG1_max_torque_Nm
        MG2_max_torque_Nm
        P0MG_max_torque_Nm
        P2MG_max_torque_Nm
        MOT_max_torque_Nm
        accessory
        controls
        start_stop
        base_hash
        aggregation_hash
        simulation_hash

A deeper look into the ``sim_batch.sim_configs`` structure array shows how some of the keys supplied vary across the cases providing full factorial coverage.

::

    >> [sim_batch.sim_configs.vehicle]

    ans =

        'vehicle_FWD_midsize_carvehicle_FWD_midsize_carvehicle_FWD_midsize_carvehicle_FWD_midsize_carvehicle_FWD_midsize_carvehicle_FWD_midsize_car'

    >> {sim_batch.sim_configs.vehicle}

    ans =

    1×6 cell array

        {'vehicle_FWD_midsize_car'}    {'vehicle_FWD_midsize_car'}    {'vehicle_FWD_midsize_car'}    {'vehicle_FWD_midsize_car'}    {'vehicle_FWD_midsize_car'}    {'vehicle_FWD_midsize_car'}

    >> {sim_batch.sim_configs.ETW_lbs}

    ans =

    1×6 cell array

        {[3000]}    {[4000]}    {[5000]}    {[3000]}    {[4000]}    {[5000]}

    >> {sim_batch.sim_configs.start_stop}

    ans =

    1×6 cell array

        {[0]}    {[0]}    {[0]}    {[1]}    {[1]}    {[1]}


One note regarding config set expansion is that only the horizontal dimension of a matrix or cell array is considered. Thus a column vector would not be expanded and the entire vector would be passed to each configuration. Similarly, if a 4 x 5 matrix was passed into a config set it would yield 5 different cases each passed a 4 x 1 vector.

Config Set Aggregation
----------------------
When conducting a large number of simulations it may be desirable to examine or aggregate the results over different subsets of the full collection of sim configs.  In the above example it can be noted that there are three hashes computed in relation to the sim configs. ``base_hash`` corresponds to the original (unexpanded) config set entry that created the resulting sim config. ``simulation_hash`` corresponds to the specific sim config or sim_case to be run. ``aggregation_hash`` is supplied to allow the user to specify groups by which they may want to aggregate the results. The ``sim_batch.config_set`` object by default includes a special member ``aggregation_keys`` where the string for each key the user wants to aggregate over can be included. Each unique set of values for the keys not specified in ``aggregation_keys`` will end up with the same ``aggregation_hash``, which can then be used to the batch post processing the generate the desired outputs.

Building Config Set via Config Strings
--------------------------------------
Config strings offer the ability to construct a simulation or set of simulations via a one line string. As seen above it can be tedious to set a large number of config keys individually. A config string is constructed via tag-value pairs separated by : and joined by the + symbol.  Within each element spaces cannot be used.  The config string representation of the above config set would look like:

::

    >> config_string = 'VEH:vehicle_FWD_midsize_car + ENG:engine_2013_Chevrolet_Ecotec_LCV_2L5_Reg_E10 + 
    TRANS:transmission_6AT_FWD_midsize_car + ELEC:electric_starter_alternator_param + ACC:accessory_EPS_param + 
    CYC:{''EPA_FTP_NOSOAK'',''EPA_HWFET''} + CON:CVM_controls_param_midsize_car + ETW_LBS:[3000:1000:5000] + SS:[0,1];
    
As mentioned previously the ``sim_batch.load_config_strings`` method is used to load these strings and would set the ``sim_batch.config_set`` matching the prior example and would also result in matching ``sim_bat.sim_configs`` output.  

If multiple config strings are desired they can be provided as a cell array. This would be analogous to config set being a cell array as well.

The aggregation of sim configs / sim cases is implemented in config strings via the \|\| operator. All tags are expanded, but only those to the left of the \|\| are used to generate the aggregation hash meaning all combinations to the right of the \|\| can used to compute each aggregate result. Again, it is good to note that how this aggregation is handled depends on the batch postprocessing and by default no processing is conducted. As shown below this example generates the same six simulation cases, but only two aggregation cases are generated. In this exammple one would correspond to ``SS:0`` and the other to ``SS:1``.

    >> config_string = 'VEH:vehicle_FWD_midsize_car + ENG:engine_2013_Chevrolet_Ecotec_LCV_2L5_Reg_E10 + 
    TRANS:transmission_6AT_FWD_midsize_car + ELEC:electric_starter_alternator_param + ACC:accessory_EPS_param + 
    CYC:{''EPA_FTP_NOSOAK'',''EPA_HWFET''} + CON:CVM_controls_param_midsize_car + SS:[0,1] || ETW_LBS:[3000:1000:5000]';

    >> sim_batch.load_config_strings(config_string);

    >> {sim_batch.sim_configs.aggregation_hash}'

    ans =

    6×1 cell array

        {'dfd9bb5cce637383ef2e7d668d2fd9649f0acf72'}
        {'dfd9bb5cce637383ef2e7d668d2fd9649f0acf72'}
        {'dfd9bb5cce637383ef2e7d668d2fd9649f0acf72'}
        {'97b691b8a096dffec2b5ac6fc85d436ab5142ef2'}
        {'97b691b8a096dffec2b5ac6fc85d436ab5142ef2'}
        {'97b691b8a096dffec2b5ac6fc85d436ab5142ef2'}

Creating New Config Keys or Config Options
------------------------------------------

The many config option packages included with ALPHA (stored in ``REVS_Common\config_packages``) define quite a few useful keys and tags that should cover many modeling applications but new ones are easy to add. There are two different approaches for adding new keys and associated processing functions. One approach is to create a new config option package, this is discussed further in :ref:`constructing_config_options`. The remainder of this section shows how to add custom keys and associated processing for a single batch. A demo that uses this feature can be found in ``run_ALPHA_demo.m``.

The first step is adding the key to the batch.  This is done using the ``sim_batch.add_key`` method. Similar to the the ``class_REVS_sim_config_key`` constructor the first argument is a string containing the key name. The other options listed below can be used can configure how the key is processed:

============       =======================================
Parameter          Usage
============       =======================================
tag                Tag for use with config strings
eval               Evaluate tag value used in config strings
default            Default value to use if none provided
description        Description to display in show keys
============       =======================================




.. _constructing_config_options:

Constructing Config Options
---------------------------





Adding a new tag is as simple as adding a new property to ``class_REVS_sim_config``:

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

This section describes how to control the datalogging and auditing features of ALPHA. It may be helpful to understand the different data objects generated, which can be found in :ref:`workspace_outputs`.

Controlling Datalogging
-----------------------

Datalogging and auditing are controlled by the settings stored in the ``logging_config`` property of the ``class_REVS_sim_batch`` object.  ``logging_config`` is an object of class ``class_REVS_logging_config``.  The ``add_log`` method of ``class_REVS_sim_batch`` is used to add logging packages that define signals to log within the ALPHA model.  Many predefined log lists are contained in the ``REVS_Common\log_packages`` folder including metapackages that are intended to provide an easy bundle of packages. These packages will control what data is avaialble in the ``datalog``, ``result`` and ``model_data`` output variables.

The following are typical examples of creating a sim batch and setting up the datalogging:

::

    sim_batch = class_REVS_sim_batch();
    sim_batch.add_log(REVS_log_default);

``REVS_log_default`` logs only the bare minimum required to calculate fuel economy and GHG emissions, this runs the fastest

::

    sim_batch = class_REVS_sim_batch();
    sim_batch.add_log(REVS_log_all);

``REVS_log_all`` logs every available signal, this runs the slowest

Log packages can also be combined to tailor the output to a projects needs:

::

    sim_batch = class_REVS_sim_batch();
    sim_batch.add_log(REVS_log_default);
    sim_batch.logging_config.add_log(REVS_log_engine_all);
    sim_batch.logging_config.add_log(REVS_log_transmission);

Logs the minimum required signals and adds all the engine signals and many common transmission datalogs. 

.. _constructing_log_packages:

Constructing Log Packages
-------------------------
Log packages are built as functions that return a ``class_REVS_log_package`` object or an array of objects. The package functions generally consist of three parts. The first is the list of signals to log stored into the ``log_list`` property. These are the signals specified in the logging blocks of the model, and wildcards can be used to select multiple items. Note that as mentioned in :ref:`workspace_outputs` additional signals may be available if they can be calculated from the logged output. Next, stored in the ``package_list`` property is the name of any contained packages. The list of packages is available for the post processing to determine is necessary signals are available to complete a given calculation. Generally, the name of the log package function is used. The final item, stored in the ``postprocess_list`` property is a list of scripts to run after simulation, which can be used to calculate or adjust and outputs.  Below the ``REVS_log_all`` package is shown which demonstrates selecting signals via wildcard, using mfilename for package naming and uses an array of postprocessing scripts. 

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

Auditing of the energy flows within the model is another feature of ALPHA that can be controlled by the audit flags of the ``logging_config`` propertry of ``class_REVS_sim_batch`` and their usage is shown below.

::

    sim_batch.logging_config.audit_total = true;

Audits the total energy flow for the entire drive cycle.

Or:

::

    sim_batch.logging_config.audit_phase = true;

Audits the total energy flow for the entire drive cycle and also audits each drive cycle phase individually.

By default both flags are set to false, only one flag or the other needs to be set.  To print the audit to the console, use the ``print`` method of the ``audit`` variable that is generated in the workspace:

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

The workspace is saved after all pre-processing scripts have been run so the workspace contains everything required to replicate the simulation at a later time.  This can be useful when running too many simulations to retain the workspaces in memory while also providing the ability to run individual cases later without having to set up a custom sim batch.  The workspace may be loaded by using the load command, or double-clicking the filename in the Matlab Current Folder file browser.

.. _saving_the_output_workspace:

Saving the Output Workspace
---------------------------

The simulation workspace may be saved after simulation by setting the sim batch ``save_output_workspace`` property to true:

::

    sim_batch.save_output_workspace = true;

This will create a timestamped ``.mat`` file in the sim batch output folder.  The filename also includes the index of the sim case.  For example, the output workspace for the first simulation (``sim_1``) in a batch:

::

    output\2019_02_11_16_52_39_sim_1_output_workspace.mat

The workspace is saved after all post-processing scripts have been run so the workspace contains everything required to replicate the simulation at a later time and also all of the datalogs, audits, etc.  The simulation may be run again or the outputs examined directly without the need for running the simulation.  Keep in mind that output workspaces will always be bigger than input workspaces and also take longer to save.  The workspace may be loaded by using the load command or double-clicking the filename in the Matlab Current Folder file browser. Also note that the resulting mat file will contain variables constructed from various REVS classes and will require ``REVS_common`` to be on the MATLAB path to operate property.

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



