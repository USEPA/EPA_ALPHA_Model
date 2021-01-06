Model Outputs
=============

When using the batch process, a standardized, customizable output file is created in the ``output`` folder.  When running from a saved workspace, or running from a batch, outputs are always produced in the simulation workspace.

Workspace Outputs
^^^^^^^^^^^^^^^^^

From a batch, the simulation output workspace can be pulled up to the Matlab top-level workspace using the ``extract_workspace`` method of ``class_REVS_sim_case``:

::

    sim_batch.sim_case(sim_number).extract_workspace

where ``sim_number`` is a number >= 1 that represents the simulation to be investigated.

For the workspace to be extractable, it must be retained in memory by setting the ``retain_output_workspace`` property of the sim batch to ``true``.  For more information see :ref:`retain_workspaces_in_memory`.  See :ref:`post_simulation_data_analysis` and :ref:`controlling_datalogging_and_auditing` for more information on controlling and using workspace outputs.

File Outputs
^^^^^^^^^^^^

By default, when a batch file runs, it produces one or more files in the simulation ``output`` folder.

The primary output file is the results file.  The filename format is ``YYYY_MM_DD_hh_mm_ss_BATCHNAME_results.csv`` where ``Y``/``M``/``D`` represent the year, month and day, and ``h``/``m``/``s`` are hour, minute, and seconds respectively.

If ``sim_batch.verbose`` is > 0 then console outputs will also be produced in the ``output`` folder.  The filename format is ``YYYY_MM_DD_hh_mm_ss_BATCHNAME_N_console.csv``, as above, where ``N`` is the simulation number.  The console outputs will include basic information on the drive cycle results as well as audit results if they are enabled.  For more information on auditing, see :ref:`auditing`.

The basic outputs for a simulation look like:

::

    SAE J2951 Drive Quality Metrics:
    Time secs         510.000000
    CEt MJ            2.840796
    CEt_dist J/m      491.558031
    CEd MJ            2.834872
    CEd_dist J/m      490.429212
    ER %             -0.21
    DR %             0.02
    EER %            -0.23
    ASCt              0.204903
    ASCd              0.205609
    ASCR %           0.34
    Dt mi             3.591008
    Dt m              5779.167465
    Dd mi             3.591768
    Dd m              5780.390388
    Distance Error mi -0.000760
    RMSSE_mph         0.104691

       1: ------------------------
       Percent Time Missed by 2mph =   0.00 %
       Distance                    =  3.592 mi
       Fuel Consumption            = 320.5339 grams
       Fuel Consumption            = 0.1119 gallons
       Fuel Economy (Volumetric)   = 32.111 mpg
       Fuel Economy (CFR)          = 32.557 mpg
       Fuel Consumption            = 89.240 g/mile
       CO2 Emission                = 270.49 g/mile

Where the "``1:``" represents the drive cycle phase, which in this case is named "1".  The First section outlines the SAEJ2951 drive quality metrics as produced by the ``REVS_SAEJ2951`` function.  See also `<https://www.sae.org/standards/content/j2951_201111/>`_.

Post Processing Output File Scripts
-----------------------------------

The results output file is created within the ``postprocess_sim_case`` method of ``class_REVS_sim_batch``.  At this time there are three output scripts, depending on the type of vehicle powertrain: ``REVS_setup_data_columns_CVM``, ``REVS_setup_data_columns_HVM``, and ``REVS_setup_data_columns_EVM`` that are located in ``REVS_Common\helper_scripts``.  These output scripts call various sub-scripts for various output file column groups.  For example, ``REVS_setup_data_columns_CVM``:

::

    %% define standard CVM output columns

    REVS_setup_data_columns_VM;

    REVS_setup_data_columns_transmission;

    REVS_setup_data_columns_engine;

    REVS_setup_data_columns_MPG;

    REVS_setup_data_columns_vehicle_performance;

    REVS_setup_data_columns_audit;

    REVS_setup_data_columns_battery;

    REVS_setup_data_columns_driveline_stats;

These scripts populate a variable called ``data_columns``, a vector of ``class_data_column`` objects.  Data column objects define the name and format of each output column.  An example instance of ``class_data_column``.

::

    >> class_data_column({'Test Weight lbs','lbs'},'%f','vehicle.ETW_lbs',2)

    ans =

      class_data_column with properties:

        header_cell_str: {'Test Weight lbs'  'lbs'}
             format_str: '%f'
               eval_str: 'vehicle.ETW_lbs'
                verbose: 2:

``class_data_column`` objects have the following properties:

* ``header_cell_str``, a cell array of strings.  The first string is the column name, located in the first row of the output file.  The second string is an optional string meant to represent the units of the variable or a supporting description of the variable.
* ``format_str``, a standard Matlab ``fprintf`` ``formatSpec`` string.
* ``eval_str`` is a string that gets evaluated by the Matlab ``evalin`` function and should return a numeric or string value that can be printed.  Any variable available in the simulation output workspace can be referenced in the ``eval_str``.
* ``verbose`` is a numeric value that refers to the sim batch ``output_verbose`` property.  Output columns will be produced for columns where ``verbose`` is >= ``output_verbose``.  In this way the output file size and complexity can be controlled.  The value of ``verbose`` is ``0`` unless overridden during the definition, as it was above.  Columns with a ``verbose`` of ``0`` will always be output.

The ``data_columns`` vector is created by ``REVS_setup_data_columns_VM`` and appended with each data column object, as shown below:

::

    data_columns(end+1) = class_data_column({'Test Weight lbs','lbs'},'%f','vehicle.ETW_lbs',2);

Custom Output Summary File Formats
----------------------------------
