
Model Inputs
============

Every model requires inputs, and ALPHA is no exception.  In order to run the model it is necessary to populate the Matlab workspace with the data structures required to run the model.

Model inputs can be provided from ``.m`` files, referred to as param files, or a previously saved workspace may be loaded from a ``.mat`` file.

Param Files
^^^^^^^^^^^

Param files are simply Matlab scripts that instantiate required data structures and objects.  It's possible to create a single script that creates every variable required by the model, however it's best practice (enforced by the batch process) to separate param files by type.

The batch process canonical expected param file types are:

* an engine param file, for non battery-electric vehicles
* a transmission file
* a vehicle file that defines vehicle characterstics such as test weight, roadload, tire radius, etc
* a param file to define the electrical system and/or accessory loads.  The electrical and accessory files may be separate or are sometimes combined
* a controls param file that defines the overall vehicle behavior such as engine start-top, etc
* an optional driver param file that tunes the response of the "cyberdriver" drive cycle trace follower.  If none is provided then the batch process will load the default parameters
* an optional ambient param file that defines the ambient test conditions.  If none is provided then the batch process will load the default parameters

The param files are loaded by ``class_REVS_sim_params`` which is called from the ``class_REVS_sim_case`` ``preprocess_workspace`` method as called by the ``preprocess_and_load_workspace`` method.

Also required, and loaded by ``class_REVS_sim_case`` from the ``preprocess_workspace`` method:

* one or more drive cycle file names to define the target vehicle speeds versus time, etc.  If multiple drive cycle file names are provided they combined using ``REVS_combine_drive_cycles`` as outlined in :ref:`making_custom_drive_cycles`


::

    TBD
