Model Outputs
=============

When using the batch process, a standardized, customizable output file is created in the ``output`` folder.  When running from a saved workspace, or running from a batch, outputs are always produced in the simulation workspace.

Workspace Outputs
^^^^^^^^^^^^^^^^^

From a batch, the simulation output workspace can be pulled up to the Matlab top-level workspace using the ``extract_workspace`` method of ``class_REVS_sim_case``:

::

    sim_batch.sim_case(sim_number).extract_workspace

where ``sim_number`` is a number >= 1 that represents the simulation to be investigated.

For the workspace to be extractable, it must be retained in memory by setting the ``retain_output_workspace`` property of the ``class_REVS_sim_batch`` to ``true``.  For more information see :ref:`retain_workspaces_in_memory`.  See :ref:`post_simulation_data_analysis` and :ref:`controlling_datalogging_and_auditing` for more information on controlling and using workspace outputs.

There are four primary model output variables generated in the simulation workspace, ``datalog``, ``model_data``, ``result`` and ``audit``.

The datalog Output
------------------
The ``datalog`` output variable contains continuous model outputs. It has hierarchical properties that somewhat mirror the model structure.  The top level should look something like this:

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

``datalog`` is constructed from a ``class_REVS_logging_object`` which calculates some values that have not been computed and output from the model itself. An example of this would be engine power, there is no logging block within the model for engine power, but if ``datalog.engine.crankshaft_speed_radps`` and ``datalog.engine.crankshaft_torque_Nm`` are logged a property will be generated for ``datalog.engine.crankshaft_power_W`` to compute the value when needed.

Controlling what signals are included in the datalog as well as the frequency of the output is discussed in :ref:`controlling_datalogging_and_auditing`.

The model_data Output
---------------------
The datalog object is also associated with a ``class_test_data`` object called ``model_data``. The primary difference between the two is that ``model_data`` represents a subset of the logged data and has a common, high-level namespace that can be used to compare model data with test data or data from multiple model runs or even data different models.  For example, vehicle speed can be plotted versus time:

::

    plot(model_data.time, model_data.vehicle.speed_mps);

The results Output
------------------
The ``result`` variable is a ``class_REVS_result`` object that contains summarized simulation results. The top level should look something like this:

::

    result =

      class_REVS_result with properties:

              phase: [1×1 class_REVS_CVM_result]
           weighted: [1×4 class_REVS_CVM_result]
           map_fuel: [1×1 class_REVS_fuel]
         unadjusted: [1×1 class_REVS_result]
        performance: [1×1 class_REVS_logging_object]
        output_fuel: [1×1 class_REVS_fuel]

The ``phase`` property contains the result data from each simulation phase while ``weighted`` contains the data aggregated over the drive cycles. The intention of the ``result`` object is storing scalar values for each drive cycle phase and cycle. ``class_REVS_result`` contains methods to print the results to the console, an example of which is shown below:

::

    >> result.print_weighted()
    ---############### Weighted Results ##############---
       EPA_FTP: ---------------------------------
           Percent Time Missed by 2mph =   0.00 %
           Distance                    = 11.109 mi
           Fuel Consumption            = 1028.6233 grams
           Fuel Consumption            = 0.3590 gallons
           Fuel Economy (Volumetric)   = 30.399 mpg
           Fuel Economy (CAFE)         = 30.821 mpg
           Fuel Consumption            = 94.266 g/mile
           CO2 Emission                = 285.72 g/mile

       EPA_HWFET: -------------------------------
           Percent Time Missed by 2mph =   0.00 %
           Distance                    = 10.269 mi
           Fuel Consumption            = 698.1742 grams
           Fuel Consumption            = 0.2436 gallons
           Fuel Economy (Volumetric)   = 42.146 mpg
           Fuel Economy (CAFE)         = 42.731 mpg
           Fuel Consumption            = 67.992 g/mile
           CO2 Emission                = 206.08 g/mile

       EPA_HWFET: -------------------------------
           Percent Time Missed by 2mph =   0.00 %
           Distance                    = 10.269 mi
           Fuel Consumption            = 698.1571 grams
           Fuel Consumption            = 0.2436 gallons
           Fuel Economy (Volumetric)   = 42.147 mpg
           Fuel Economy (CAFE)         = 42.732 mpg
           Fuel Consumption            = 67.990 g/mile
           CO2 Emission                = 206.08 g/mile

       REVS_Performance_cruise75mph: ------------
           Percent Time Missed by 2mph =  79.83 %
           Distance                    =  6.559 mi
           Fuel Consumption            = 2035.1302 grams
           Fuel Consumption            = 0.7102 gallons
           Fuel Economy (Volumetric)   =  9.235 mpg
           Fuel Economy (CAFE)         =  9.364 mpg
           Fuel Consumption            = 310.283 g/mile
           CO2 Emission                = 940.47 g/mile


The ``result`` object also contains other summary values from the model such as integrated fuel consumption or battery current and are controlled similarly to the ``datalog`` outputs, see :ref:`controlling_datalogging_and_auditing` for more details. An example of this is displaying transmission data for each phase is shown below:

::

    >> result.phase.transmission

    ans =

      class_REVS_logging_object with properties:

                output_pos_kJ: [2.9296e+03 2.7390e+03 2.9296e+03 7.2149e+03 7.2148e+03 1.0335e+04 4.9111e+03 6.9897e+03]
               output_pos_kWh: [0.8138 0.7608 0.8138 2.0041 2.0041 2.8707 1.3642 1.9416]
               num_downshifts: [25 46 25 7 7 0 1 1]
                   num_shifts: [51 92 51 15 15 5 5 4]
        num_target_downshifts: [25 46 25 7 7 0 5 1]
          num_target_upshifts: [26 46 26 8 8 5 4 3]
                 num_upshifts: [26 46 26 8 8 5 4 3]

Note that as with ``datalog`` the ``result`` object is constructed from ``class_REVS_logging_object``, so additional calculated properties are added based on what signals are logged directly in the model. This can be seen in the example above where ``output_pos_kWh`` is calculated from ``output_pos_kJ``.

The audit Output
----------------
The ``audit`` structure, like the ``result`` structure, contains scalar values for each phase, or total simulation.

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

The audit energy logs (as seen above) are tallied according to whether they are sources of energy or sinks of energy in the ``calc_audit`` methods of the audit classes.  If the model, audit logging and audit calculations are correct then the sum of the energy in the audit sinks will equal the sum of the energy in the audit sources.  The sources and sinks are tallied in the ``energy_balance`` property of the audit class.

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

Logging Details
---------------
Since it's not possible for Simulink To Workspace blocks to directly create the output objects described above, there is a process for populating these data structures from individual logged workspace variables.  This ia accomplished through employing a naming scheme for the logged signals that can then be loaded into the appropriate objects.  For example, the raw post-simulation workspace will contain variables such as:

::

    audit__accessories__air_conditioner__elec_neg_kJ
    dl__engine__crankshaft_trq_Nm
    rsltp__engine__fuel_consumed_g

The prefix determines the top-level data structure.  ``audit`` maps to the ``audit`` data structure, ``dl`` maps to ``datalog`` and ``rsltp`` maps to the ``phase`` property of the ``result`` data structure, as in ``result.phase``.

The double underscores, ``__``, define the hierarchical structure.  For example, ``audit__accessories__air_conditioner__elec_neg_kJ`` will become ``audit.accessories.air_conditioner.elec_neg_kJ`` in the final workspace.  Single underscores are taken as part of the property name.

The construction of the raw workspace variable names is handled by the mask of the datalog blocks and can determined by the structure of the model.  For example, datalogs in the ``engine`` block model will automatically be placed in the ``datalog.engine`` structure without having to be explicitly named as such.  For example, the ``datalog.engine.fuel_rate_gps`` signal is set up as follows:

.. image:: figures/engine_fuel_rate_gps_mask.jpg

The only user-specified part of the name is ``fuel_rate_gps``, the rest is automatic, and the final result is previewed in the ``Datalog Name`` text box.

File Outputs
^^^^^^^^^^^^

By default, when a batch file runs, it produces several files in the simulation ``output`` folder.

The primary output file is the results file.  The filename format is ``YYYY_MM_DD_hh_mm_ss_BATCHNAME_results.csv`` where ``Y``/``M``/``D`` represent the year, month and day, and ``h``/``m``/``s`` are hour, minute, and seconds respectively.

If ``sim_batch.verbose`` is > 0 then console outputs will also be produced in the ``output`` folder.  The filename format is ``YYYY_MM_DD_hh_mm_ss_BATCHNAME_N_console.txt``, as above, where ``N`` is the simulation number.  The console outputs will include basic information on the drive cycle results as well as audit results if they are enabled.  For more information on auditing, see :ref:`auditing`.

The basic console outputs for a drive cycle phase look like:

::

       1: ------------------------
       Percent Time Missed by 2mph =   0.00 %
       Distance                    =  3.592 mi
       Fuel Consumption            = 320.5339 grams
       Fuel Consumption            = 0.1119 gallons
       Fuel Economy (Volumetric)   = 32.111 mpg
       Fuel Economy (CAFE)         = 32.557 mpg
       Fuel Consumption            = 89.240 g/mile
       CO2 Emission                = 270.49 g/mile

Where the "``1:``" represents the drive cycle phase, which in this case is named "1".

SAEJ2951 drive quality metrics are available in ``result.phase.drive_quality`` as produced by the ``REVS_SAEJ2951`` function.  See also `<https://www.sae.org/standards/content/j2951_201111/>`_.

.. _post_processing_output_file_scripts:

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

* ``header_cell_str``, a cell array of strings.  The first string is the column name, located in the first row of the output file.  The second string is an optional string meant to represent the units of the variable or a supporting description of the variable and occupies the second row of the output file.
* ``format_str``, a standard Matlab ``fprintf`` ``formatSpec`` string.
* ``eval_str`` is a string that gets evaluated by the Matlab ``evalin`` function and should return a numeric or string value that can be printed.  Any variable available in the simulation output workspace can be referenced in the ``eval_str``.
* ``verbose`` is a numeric value that refers to the ``class_REVS_sim_batch`` ``output_verbose`` property.  Output columns will be produced for columns where ``verbose`` is >= ``output_verbose``.  In this way the output file size and complexity can be controlled.  The value of ``verbose`` is ``0`` unless overridden during the definition, as it was above.  Columns with a ``verbose`` of ``0`` will always be output.

The ``data_columns`` vector is created by ``REVS_setup_data_columns_VM`` and appended with each data column object, as shown below:

::

    data_columns(end+1) = class_data_column({'Test Weight lbs','lbs'},'%f','vehicle.ETW_lbs',2);

The data_columns are evaluated one at a time by the ``class_REVS_sim_batch`` ``postprocess_sim_case`` method via the ``write_column_row`` function which is located in the ``NVFEL_MATLAB_Tools\utilities\export`` folder.

.. _custom_output_summary_file_formats:

Custom Output Summary File Formats
----------------------------------

There are at least a couple methods to modify the output file format: edit the various ``setup_data_columns`` scripts, or populate the ``class_REVS_sim_batch`` ``setup_data_columns`` property with the name of a custom output column definition script, which can be created using the default scripts as a guide.  The custom script will be called after the default columns are created and therefore the custom columns will appear to the right of the previously defined columns in the output file.

For example, in the batch script:

::

    sim_batch.setup_data_columns = 'setup_custom_data_columns';

In ``setup_custom_data_columns.m``:

::

    % setup up custom data columns

    data_columns(end+1) = class_data_column({' ',' '}, separator, '0');
    data_columns(end+1) = class_data_column({'ETW_HP','LB/HP'}, '%.3f', 'sim_config.pounds_per_hp', 1);
    data_columns(end+1) = class_data_column({'RLHP20','HP/LB'}, '%.3f', 'sim_config.roadload_hp20plb', 1);
    data_columns(end+1) = class_data_column({'RLHP60','HP/LB'}, '%.3f', 'sim_config.roadload_hp60plb', 1);
    data_columns(end+1) = class_data_column({'HP_ETW','HP/LB'}, '%.3f', '1/sim_config.pounds_per_hp', 1);
    data_columns(end+1) = class_data_column({'ETW','lbs'},'%f','vehicle.ETW_lbs',2);
