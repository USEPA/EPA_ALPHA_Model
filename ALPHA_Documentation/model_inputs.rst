
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

``drive_cycle``
---------------

``accessories``
---------------

``electric``
------------

``controls``
------------

``engine``
----------

``transmission``
----------------

``vehicle``
-----------
