
Model Inputs
============

Every model requires inputs, and ALPHA is no exception.  In order to run the model it is necessary to populate the Matlab workspace with the data structures required to run the model.

Model inputs can be provided from ``.m`` files, referred to as param files, or a previously saved workspace may be loaded from a ``.mat`` file.  For information on saving simulation workspaces, see :ref:`saving_the_input_workspace` and :ref:`saving_the_output_workspace`

Param Files
^^^^^^^^^^^

Param files are simply Matlab scripts that instantiate required data structures and objects.  It's possible to create a single script that creates every variable required by the model, however it's best practice (enforced by the batch process) to separate param files by type.

The batch process canonical expected param file types are:

* an engine param file, using the ``ENG:`` tag, for non battery-electric vehicles
* a transmission file, using the ``TRANS:`` tag
* a vehicle file, using the ``VEH:`` tag, that defines vehicle characterstics such as test weight, roadload, tire radius, etc
* a param file to define the electrical system and/or accessory loads, using the ``ELEC:`` and/or ``ACC:`` tags.  The electrical and accessory files may be separate or are sometimes combined
* a controls param file, using the ``CON:`` tag, that defines the overall vehicle behavior such as engine start-top, etc
* an optional driver param file, using the ``DRV:`` tag, that tunes the response of the "cyberdriver" drive cycle trace follower.  If none is provided then the batch process will load the default parameters
* an optional ambient param file, using the ``AMB:`` tag, that defines the ambient test conditions.  If none is provided then the batch process will load the default parameters

The param files are loaded by ``class_REVS_sim_params`` which is called from the ``class_REVS_sim_case`` ``preprocess_workspace`` method as called by the ``preprocess_and_load_workspace`` method.

Also required, and loaded by ``class_REVS_sim_case`` from the ``preprocess_workspace`` method:

* one or more drive cycle file names, using the ``CYC:`` tag, to define the target vehicle speeds versus time, etc.  If multiple drive cycle file names are provided they combined using ``REVS_combine_drive_cycles`` as outlined in :ref:`making_custom_drive_cycles`

As part of the batch process, each of the above tags may load multiple param files by providing a cell array of strings of the names of the param files, for example:

::

    '... + CYC:{''EPA_UDDS'',''EPA_HWFET'',''EPA_US06'',''CARB_LA92''} + ...'

Note the use of double single-quotes, ``''``, as opposed to single double-quotes, ``"``, this is required in order for the batch process to evaluate the cell array properly.

If multiple files are provided, they are loaded in left-to-right order, so param files that have dependencies should be listed to the right of the files they depend on.

Workspace Data Structures
^^^^^^^^^^^^^^^^^^^^^^^^^

The following variables must be present in the workspace prior to running the model, and are saved by ``class_REVS_sim_case`` in the ``preprocess_and_load_workspace`` mehtod if the ``save_input_workspace`` property of the ``sim_batch`` is set to ``true``.

``REVS``
--------

An instance of ``class_REVS_setup`` that stores the top-level settings that control the simulation.  ``REVS`` is created by the ``preprocess_workspace`` method of ``class_REVS_sim_case``.

::

    >> REVS

    REVS =

      class_REVS_setup with properties:

              current_model: 'REVS_VM'
                    verbose: 1
          global_decimation: 1
                 output_fid: 1
         sim_step_time_secs: 0.01
        sim_start_time_secs: -5
         sim_stop_time_secs: Inf
             logging_config: [1×1 class_REVS_logging_config]


``ambient``
-----------

An instance of ``class_REVS_ambient`` which defines the ambient environmental conditions of the simulation.  The atmospheric properties come into play when using Cd / frontal area drag coefficients, as opposed to ABC roadload coefficients.  See :ref:`abc_coefficients` and :ref:`drag_coefficients` for more information on vehicle roadload calculations.

::

    >> ambient

    ambient =

      class_REVS_ambient with properties:

                  variant: 'default ambient'
         temperature_degC: 20
              pressure_Pa: 98210
        air_density_kgpm3: 1.16771071212578
               Rgas_JpkgK: 286.9
             gravity_mps2: 9.80665

``driver``
----------

An instance of ``class_REVS_driver`` that defines the response of the drive cycle trace-following driver model.  These settings typically won't need adjustment, with the exception of ``distance_compensate_enable`` which should be set ``true`` for drive cycles with road grade.  See :ref:`drive_cycles` for more information on drive cycles, including grade.

::

    >> driver

    driver =

      class_REVS_driver with properties:

                                   variant: 'default driver'
                                        Kp: 1
                                        Ki: 3
                                        Kd: 0
                 proportional_fade_in_secs: 1
        proportional_fade_in_min_speed_mps: 2
                            lookahead_secs: 0.25
                    launch_anticipate_secs: 0.5
               dynamic_gain_lookahead_secs: 3.75
                distance_compensate_enable: 0
                              late_braking: 0
                         human_mode_enable: 0
                           brake_gain_norm: 0.13
            accel_pedal_response_speed_mps: [0 5 20 70]
                 accel_pedal_response_norm: [0.125 0.2 1 1]


``drive_cycle``
---------------

An instance of ``class_REVS_drive_cycle`` that defines the simulation drive cycle.  For more information on drive cycles, see :ref:`drive_cycles`.

::

    >> drive_cycle

    drive_cycle =
      class_REVS_drive_cycle with properties:

                       name: 'EPA_UDDS'
        sample_start_enable: 1
                 phase_name: ["1"    "2"]
                      phase: [1 2]
                 phase_time: [0 505]
                 cycle_time: [1370×1 double]
            cycle_speed_mps: [1370×1 double]
                    in_gear: [0 1]
               in_gear_time: [0 15]
                   ignition: [1 1]
              ignition_time: [0 1369]
               grade_dist_m: [0 11990.238656]
                  grade_pct: [0 0]
          cfr_max_speed_mps: [1370×1 double]
          cfr_min_speed_mps: [1370×1 double]


``accessories``
---------------

An instance of ``class_REVS_ALPHA_accessories`` that defines electrical and mechanical accessory loads.

::

    >> accessories

    accessories =

      class_REVS_ALPHA_accessories with properties:

                   name: 'accessory_EPS_param'
           generic_loss: [1×1 class_REVS_accessory_load]
                    fan: [1×1 class_REVS_accessory_load]
         power_steering: [1×1 class_REVS_accessory_load]
        air_conditioner: [1×1 class_REVS_accessory_load]

``electric``
------------

An instance of ``class_REVS_electric`` that defines the vehicle's electrical system, for both hybrid and conventional vehicles.  Not all properties are populated, depending on the powertrain.

::

    >> electric

    electric =

      class_REVS_electric with properties:

                      name: 'electric_EPS_midsize_car'
            matrix_vintage: present
                   starter: [1×1 class_REVS_starter]
                alternator: [1×1 class_REVS_alternator]
          low_voltage_DCDC: [1×1 class_REVS_DCDC_converter]
         high_voltage_DCDC: [1×1 class_REVS_DCDC_converter]
                   battery: [1×1 class_REVS_battery]
         accessory_battery: [0×0 class_REVS_battery]
        propulsion_battery: [0×0 class_REVS_battery]
                     P0_MG: [0×0 class_REVS_emachine_geared]
               drive_motor: [0×0 class_REVS_emachine]
                       MG1: [0×0 class_REVS_emachine_geared]
                       MG2: [0×0 class_REVS_emachine_geared]

``controls``
------------

A data structure that defines control system parameters.  The example below is for a conventional vehicle, that may or may not enable engine start-stop.

::

    >> controls

    controls =
      class_REVS_CVM_control with properties:

                      start_stop_enable: 0
              start_stop_off_delay_secs: 0
            start_stop_warmup_condition: '(@cycle_pos_secs >= 100) && (@cycle_pos_secs <= 3406)'
        hot_soak_warmup_start_condition: '@cycle_pos_secs > 0 '
                         pedal_map_type: max_engine_power
             pedal_map_engine_torque_Nm: [1×1 class_REVS_dynamic_lookup]
                 shift_inertia_est_kgm2: 0.187389225679636
                                variant: ''

``engine``
----------

For conventional or hybrid vehicles, an instance of ``class_REVS_engine`` that defines engine properties such as torque limits, fuel consumption rates as a function of speed and load, etc.

::

    >> engine

    engine =
      class_REVS_engine with properties:

                            full_throttle_speed_radps: [17×1 double]
                              full_throttle_torque_Nm: [17×1 double]
                          closed_throttle_speed_radps: [6×1 double]
                            closed_throttle_torque_Nm: [6×1 double]
                      naturally_aspirated_speed_radps: [17×1 double]
                        naturally_aspirated_torque_Nm: [17×1 double]
                             power_time_constant_secs: 0.2
                             boost_time_constant_secs: 0.5
                     boost_falling_time_constant_secs: 0.3
                     run_state_activation_speed_radps: 1
                      run_state_activation_delay_secs: 0.5
                   run_state_deactivation_speed_radps: 0
                              idle_target_speed_radps: [1×1 class_REVS_dynamic_lookup]
                                      idle_control_Kp: 25
                                      idle_control_Ki: 65
                                      idle_control_Kd: 1
                              idle_control_ramp_radps: 10.471975511966
                          idle_control_ramp_time_secs: 1.5
                       idle_control_torque_reserve_Nm: 10
              idle_control_slow_est_time_constant_sec: 0.2
                                 fuel_map_speed_radps: [18×1 double]
                                   fuel_map_torque_Nm: [26×1 double]
                                         fuel_map_gps: [26×18 double]
                                    deac_fuel_map_gps: [26×18 double]
                                        deac_strategy: [1×1 struct]
                                   deac_num_cylinders: 0
                     deac_transition_on_duration_secs: 0.99
                    deac_transition_off_duration_secs: 0.11
                  deac_transition_off_fuel_multiplier: [1 1]
        deac_transition_off_fuel_multiplier_time_secs: [0 0.1]
        deac_transition_off_fuel_multiplier_limit_gps: Inf
                         fast_torque_fuel_adjust_norm: 0
                                DFCO_enable_condition: '@veh_spd_mps>5'
                               DFCO_min_duration_secs: 2.1
                               DFCO_refuel_multiplier: [1 1.3 1]
                     DFCO_refuel_multiplier_time_secs: [0 0.1 1.1]
                     DFCO_refuel_multiplier_limit_gps: Inf
                            transient_correction_mult: 1.4
                                                 name: '2018 Toyota 2.5L A25A-FKS Engine Tier 3 Fuel converted to 2.46L'
                                      source_filename: 'engine_2018_Toyota_A25AFKS_2L5_Tier3'
                                       matrix_vintage: present
                                              variant: 'basic engine'
                                      combustion_type: spark_ignition
                                       displacement_L: 2.46445235878698
                                              bore_mm: 87.2347659681488
                                            stroke_mm: 103.086569155504
                                        num_cylinders: 4
                                    compression_ratio: 13
                                        configuration: []
                                         inertia_kgm2: 0.143041293924769
                                                 fuel: [1×1 class_REVS_fuel]
                                            base_fuel: [0×0 class_REVS_fuel]
                             nominal_idle_speed_radps: 61.7846555205993
                                        max_torque_Nm: 247.20140331587
                           max_torque_min_speed_radps: 504.1
                           max_torque_max_speed_radps: 551
                           max_torque_avg_speed_radps: 526.233333333333
                                        min_torque_Nm: -50.7899054656206
                                          max_power_W: 149994.914232163
                            max_power_min_speed_radps: 660.6
                            max_power_max_speed_radps: 698.4
                            max_power_avg_speed_radps: 683.366666666667
                                 max_test_speed_radps: 694.6

``transmission``
----------------

An instance of ``class_REVS_AT_transmission``, ``class_REVS_CVT_transmission``, ``class_REVS_DCT_transmission``, ``class_REVS_AMT_transmission``, etc, that supports the powertrain of the vehicle to be modeled.  Below is an example for an automatic transmission.

::

    >> transmission

     transmission =
      class_REVS_AT_transmission with properties:

                    type: automatic
                 variant: 'automatic transmission system'
          matrix_vintage: present
                    name: 'transmission_6AT_FWD_midsize_car'
         rated_torque_Nm: 284.281613813251
                    gear: [1×1 class_REVS_gearbox]
        torque_converter: [1×1 class_REVS_torque_converter]
                 control: [1×1 class_REVS_AT_control]
                 thermal: [1×1 struct]
            pump_loss_Nm: [1×1 class_REVS_dynamic_lookup]
           gear_strategy: [1×1 class_REVS_ALPHAshift]
            tcc_strategy: [1×1 class_REVS_uber_dynamic_lockup]

``vehicle``
-----------

An instance of ``class_REVS_vehicle`` that defines vehicle properties such as roadload, test weight, axle definitions, etc.  For more information on roadloads and test weight see :ref:`alpha_roadloads_and_test_weight`.

::

    >> vehicle

    vehicle =
      class_REVS_vehicle with properties:

                               name: []
                              class: 'midsize_car'
                               fuel: [1×1 class_REVS_fuel]
                            variant: 'default vehicle'
                 powertrain_variant: 'CVM / P0'
                  driveline_variant: 'one axle drive'
                   controls_variant: 'CVM control'
                    powertrain_type: conventional
               delta_mass_static_kg: [1×1 class_REVS_dynamic_lookup]
              delta_mass_dynamic_kg: [1×1 class_REVS_dynamic_lookup]
                   use_abc_roadload: 1
               coastdown_target_A_N: 133.44666
            coastdown_target_B_Npms: 0
           coastdown_target_C_Npms2: 0.445167735635058
                       dyno_set_A_N: []
                    dyno_set_B_Npms: []
                   dyno_set_C_Npms2: []
               coastdown_adjust_A_N: 0
            coastdown_adjust_B_Npms: 0
           coastdown_adjust_C_Npms2: 0
                    frontal_area_m2: 0
             aerodynamic_drag_coeff: 0
                         driveshaft: [1×1 class_REVS_driveshaft]
                      transfer_case: [1×1 class_REVS_transfer_case]
                         steer_axle: [1×1 class_REVS_drive_axle]
                        drive_axle1: [1×1 class_REVS_drive_axle]
                        drive_axle2: [1×1 class_REVS_drive_axle]
                      trailer_axle1: [1×1 class_REVS_drive_axle]
                      trailer_axle2: [1×1 class_REVS_drive_axle]
                  max_brake_force_N: 26818.456903
             coastdown_target_A_lbf: 30
         coastdown_target_B_lbfpmph: 0
        coastdown_target_C_lbfpmph2: 0.02
                     dyno_set_A_lbf: []
                 dyno_set_B_lbfpmph: []
                dyno_set_C_lbfpmph2: []
             coastdown_adjust_A_lbf: 0
         coastdown_adjust_B_lbfpmph: 0
        coastdown_adjust_C_lbfpmph2: 0
                             ETW_kg: 1587.572
                     mass_static_kg: 1563.75842
                    mass_dynamic_kg: 1611.38558
                       mass_curb_kg: 1427.68082
                    mass_ballast_kg: 136.0776
                            ETW_lbs: 3500
                      mass_curb_lbs: 3147.5
                   mass_ballast_lbs: 300
                    mass_static_lbs: 3447.5
                   mass_dynamic_lbs: 3552.5
