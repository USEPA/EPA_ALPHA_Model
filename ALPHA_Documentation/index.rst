.. The following section demonstrates how to insert a header into the documentation file
.. that will be recorded when the auto-documentation is built.
.. "EPA ALPHA Model Documentation" will be the name of the main document using the
.. formatting shown.
.. The chapters in the document are listed below (introduction, overview, etc.) that refer
.. to the actual .rst files to be used when building the auto-documentation.

ALPHA Documentation
===================

.. toctree::
    :caption: Model Documentation
    :maxdepth: 3

    introduction
    overview
    modeling_process
    common_use_cases
    model_inputs
    model_outputs
    alpha_development

.. toctree::
    :caption: Contact

    contact_information
    agency_information

.. toctree::
    :caption: Reference

    reference_documentation_style_guide
    python_documentation_style_guide

    genindex

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`