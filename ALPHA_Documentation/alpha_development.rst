.. _alpha_development:

ALPHA Development
=================

This chapter will give some information on ALPHA development guidelines and more details on the Simulink model itself and review some of the critical data structures.

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

REVS_VM
^^^^^^^

This section will provide an overview of the Simulink model, ``REVS_VM``.  ALPHA represents various vehicle powertrains through the use of variant subsystems which are instantiated by the top-level model rather than by using separate models.

Overview
--------

The top-level of ``REVS_VM`` consists of the following blocks:

* ``ambient`` - provides the ambient test conditions, logs the time signal and provides the drive cycle road grade as a function of distance travelled.
* ``driver`` - implements the trace-following driver model that produces the accelerator / brake pedal signals and other driver-related signals to the rest of the model.  ``driver`` also contains the drive cycle lookups for target vehicle speed.
* ``powertrain`` - implements the various powertrains for conventional, hybrid or electric vehicles.
* ``vehicle`` - contains the vehicle roadload calculations (except for tire rolling resistance and losses, which are handled in the ``powertrain`` subsystems) and the vehicle speed integrator.

Each of the top-level blocks can be customized by the variant control properties ``ambient.variant``, ``driver.variant``, ``vehicle.variant`` and ``vehicle.powertrain_variant``.  These are string properties that contain the name of the desired variant subsystem to instantiate.

Also at the top level of the model is the system bus and the vehicle speed chart which shows target and achieved vehicle speeds.

Powertrain Variants
-------------------

The ``powertrain`` variant subsystem is in many ways the heart of the ALPHA model.  At this time there are two available powertrain variants:

* ``CVM / BAS / ISG`` - implements CVM, the Conventional Vehicle Model and mild hybrid vehicles (BAS, Belt-Alternator-Starter and ISG, Integrated-Starter-Generator)
* ``EVM`` - implements EVM, the Electric Vehicle Model

Powersplit hybrid models are also under development (the component models of which are available for experimentation in the ``electric_lib`` and ``transmission_lib``)

``CVM / BAS / ISG``
+++++++++++++++++++

The top level of the conventional vehicle model contains the following blocks:

* ``controls`` - handles engine start-stop logic and other control system algorithms.  This variant subsystem is determined by the ``vehicle.controls_variant`` string property.
* ``engine`` - contains the engine model.  This variant subsystem is determined by the ``engine.variant`` string property.
* ``transmission`` - contains the transmission model. This variant subsystem is determined by the ``transmission.variant`` string property.
* ``driveline`` - contains the axle models which contain the wheels, tires, final drive and driveshafts, etc.  This variant subsystem is determined by the ``vehicle.driveline_variant`` string property.
* ``electric & accessories`` - implements the vehicle's electrical energy storage system, electrical accessories and mechanical engine accessory loads.  The engine starting and battery charging system is also implemented here.  This block is not itself a variant subsystem but the ``starting / charging`` and ``energy storage`` subsystems are variants, determined by the ``vehicle.powertrain_type`` enumeration property.

``EVM``
+++++++

The top level of the electric vehicle model contains the following blocks:

* ``controls`` - handles control system algorithms such as acceleration and regeneration limits.  This variant subsystem is determined by the ``vehicle.controls_variant`` string property.
* ``drive_motor`` - implements a single propulsion motor-generator model.
* ``transmission`` - contains the transmission model. This variant subsystem is determined by the ``transmission.variant`` string property.
* ``driveline`` - contains the axle models which contain the wheels, tires, final drive and driveshafts, etc.  This variant subsystem is determined by the ``vehicle.driveline_variant`` string property.
* ``electric & accessories`` - implements the vehicle's electrical energy storage system and electrical accessories.  This block is not itself a variant subsystem but the ``starting / charging`` and ``energy storage`` subsystems are variants, determined by the ``vehicle.powertrain_type`` enumeration property.

Understanding the Simulink Libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section provides an overview of the several Simulink libraries that hold the various component models and subsystem blocks.

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

Component Development
^^^^^^^^^^^^^^^^^^^^^

Data Structures and Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^
