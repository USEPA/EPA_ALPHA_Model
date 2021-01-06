
Model Inputs
============

Every model requires inputs, and ALPHA is no exception.  In order to run the model it is necessary to populate the Matlab workspace with the data structures required to run the model.

Model inputs can be provided from ``.m`` files, referred to as param files, or a previously saved workspace may be loaded from a ``.mat`` file.  For information on saving simulation workspaces, see :ref:`_saving_the_input_workspace` and :ref:`_saving_the_output_workspace`

Param Files
^^^^^^^^^^^

Param files are simply Matlab scripts that instantiate required data structures and objects.  It's possible to create a single script that creates every variable required by the model, however it's best practice (enforced by the batch process) to separate param files by type.

The batch process canonical expected param file types are:

* an engine param file, using the `ENG:` tag, for non battery-electric vehicles
* a transmission file, using the `TRANS:` tag
* a vehicle file, using the `VEH:` tag, that defines vehicle characterstics such as test weight, roadload, tire radius, etc
* a param file to define the electrical system and/or accessory loads, using the `ELEC:` and/or `ACC:` tags.  The electrical and accessory files may be separate or are sometimes combined
* a controls param file, using the `CON:` tag, that defines the overall vehicle behavior such as engine start-top, etc
* an optional driver param file, using the `DRV:` tag, that tunes the response of the "cyberdriver" drive cycle trace follower.  If none is provided then the batch process will load the default parameters
* an optional ambient param file, using the `AMB:` tag, that defines the ambient test conditions.  If none is provided then the batch process will load the default parameters

The param files are loaded by ``class_REVS_sim_params`` which is called from the ``class_REVS_sim_case`` ``preprocess_workspace`` method as called by the ``preprocess_and_load_workspace`` method.

Also required, and loaded by ``class_REVS_sim_case`` from the ``preprocess_workspace`` method:

* one or more drive cycle file names, using the `CYC:` tag, to define the target vehicle speeds versus time, etc.  If multiple drive cycle file names are provided they combined using ``REVS_combine_drive_cycles`` as outlined in :ref:`making_custom_drive_cycles`

As part of the batch process, each of the above tags may load multiple param files by providing a cell array of strings of the names of the param files, for example:

::

    '... + CYC:{''EPA_UDDS'',''EPA_HWFET'',''EPA_US06'',''CARB_LA92''} + ...'

Note the use of double single-quotes, ``''``, as opposed to single double-quotes, ``"``, this is required in order for the batch process to evaluate the cell array properly.

If multiple files are provided, they are loaded in left-to-right order, so param files that have dependencies should be listed to the right of the files they depend on.
