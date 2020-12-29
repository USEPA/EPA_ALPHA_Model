
ALPHA Development
=================

.. _ad-crossref-1:

Conventions and Guidelines
^^^^^^^^^^^^^^^^^^^^^^^^^^
There are a few guidelines that cover the use of variable names within the modeling environment and other conventions.  Understanding and following the guidelines facilitates collaboration, ease of use and understanding of the modeling environment.

* Class definitions start with ``class_``.

* Enumerated datatype definitions start with ``enum_``.

* Physical unit conversions should be accomplished using the ``unit_convert`` class.  For example ``engine_max_torque_ftlbs`` = ``engine_max_torque_Nm`` * ``unit_convert.Nm2ftlbs``.  Avoid hard-coded conversion constants.

* Any variable that has corresponding units should take the form ``variable_units``, such as ``vehicle_speed_kmh`` or ``shaft_torque_Nm``.  SI units are preferred whenever possible unless superseded by convention (such as roadload ABCs).  Units commonly use lowercase 'p' for 'per'.  For example mps = meters per second, radps = radians per second.  Readability outweighs consistency if convention and context allows, for example ``vehicle_speed_mph`` is understood to be vehicle speed in miles per hour, not meters per hour.

* English units are used by a class, but that class should also provide SI equivalents.  REVS provides some framework and examples of automatic unit conversions that may be used.

* Variable names should be concise but abbreviations or acronyms are generally to be avoided unless superseded by convention.  For example, ``datalog.transmission.gearbox``, not ``dl.trns.gbx``.  Exceptions are bus signal names and the port names on Simulink blocks (long names reduce readability rather than enhancing it) - for example, torque may be trq and speed may be spd. Simulink block names may also receive abbreviated names to enhance readability.

* Underscores are preferred for workspace and data structure variable names, for example ``selected_gear_num``.  Camelcase is preferred for variables defined in Simulink masks and local block workspaces so they may be distinguished from ordinary workspace variables.

* Most functions that are specific to the REVS modeling platform start with ``REVS_``.

* The 'goto' and 'from' flags are to be avoided in Simulink blocks as they significantly decrease the readability and understanding of block connections.  Exceptions to this rule are the ``REVS_VM top-level system_bus`` component sub-buses, the ``global_stop_flag`` and the ``REVS_audit_phase_flag`` which must be made available throughout the model.

* Trivial Simulink blocks (such as multiplication, addition, etc) may have their block names hidden to enhance readability; non-trivial blocks should have names which concisely and accurately describe their function.

* Simulink blocks should have a white background and a black foreground.  Exceptions are red foreground for blocks that are deprecated or orange foreground for blocks that may be unproven or experimental.

* Useful Simulink blocks should be added to the appropriate ``REVS_Common`` model library if they are likely to be reused.

* Simulink block names are lowercase unless superseded by convention and words are separated by spaces (as opposed to underscores).

* Simulink blocks that take in the system bus should have ``system_bus`` as input port 1.

* Simulink blocks that produce a signal bus should have ``bus_out`` as output port 1.

* Whenever possible, variant subsystem blocks should be controlled by a ``variant`` string property that matches the name of the block to be selected.

Customizing the Batch Process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Custom Pre- and Post-Processing
-------------------------------

Creating and Using Config String Tags
-------------------------------------

Custom Output Summary File Formats
----------------------------------

REVS_VM
^^^^^^^

Overview
--------
Powertrain Variants
-------------------


Understanding the Simulink Libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
accessory_lib
-------------
Contains blocks for describing mechanical and electrical accessory loads.

ambient_lib
-----------
The ``ambient`` variant block is the source of road grade (as a function of distance) and ambient temperature.  The time ``datalog`` is also created here.  Alternative ambient blocks can be created and selected using the ``ambient.version`` property

controls_lib
------------
Contains the ``controls`` variant block and other controls-related blocks.  The control blocks determine engine start-stop and control strategies for hybrid vehicles.

driver_lib
----------
Contains the ``driver`` variant block, which determines the closed-loop drive cycle follower.  The ``driver`` block produces the accelerator and brake pedal signals to the rest of the model as well as a few other signals such as the drive cycle speed, phase, and position in seconds.  Alternative driver blocks can be created and selected using the ``driver.version`` property

electric_lib
------------
Contains energy storage (battery) models and other electrical components such as starter, alternator, and e-machine (motor-generator) models.

engine_lib
----------
Contains the ``engine`` variant block and engine and engine-related models, such as cylinder deactivation logic.

general_lib
-----------
Contains various utility blocks that may be used throughout the model, such as dynamic lookup tables, dynamic equations and other handy functions.

logging_lib
-----------
Contains the blocks that handle dynamic data logging within the model, including ``audit`` logging and drive cycle phase ``result`` values.

powertrain_lib
--------------
Contains the top-level ``powertrain`` variant block, and defines the available powertrains for conventional and hybrid vehicles.

transmission_lib
----------------
Contains transmission models for conventional and hybrid vehicles, and component models for things like clutches and torque converters.

vehicle_lib
-----------
Contains models of brakes, tires and other driveline components like axles, as well as the vehicle roadload calculations.

Understanding Datalogging
^^^^^^^^^^^^^^^^^^^^^^^^^
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

.. image:: <figures/engine fuel_rate_gps mask.png>

Understanding Auditing
^^^^^^^^^^^^^^^^^^^^^^

Component Development
^^^^^^^^^^^^^^^^^^^^^

Data Structures and Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^




