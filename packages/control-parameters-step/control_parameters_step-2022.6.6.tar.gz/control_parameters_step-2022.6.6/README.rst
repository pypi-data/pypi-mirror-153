=======================
Control Parameters Step
=======================

.. image:: https://img.shields.io/github/issues-pr-raw/molssi-seamm/control_parameters_step
   :target: https://github.com/molssi-seamm/control_parameters_step/pulls
   :alt: GitHub pull requests

.. image:: https://github.com/molssi-seamm/control_parameters_step/workflows/CI/badge.svg
   :target: https://github.com/molssi-seamm/control_parameters_step/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/molssi-seamm/control_parameters_step/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/molssi-seamm/control_parameters_step
   :alt: Code Coverage

.. image:: https://img.shields.io/lgtm/grade/python/g/molssi-seamm/control_parameters_step.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/molssi-seamm/control_parameters_step/context:python
   :alt: Code Quality

.. image:: https://github.com/molssi-seamm/control_parameters_step/workflows/Documentation/badge.svg
   :target: https://molssi-seamm.github.io/control_parameters_step/index.html
   :alt: Documentation Status

.. image:: https://pyup.io/repos/github/molssi-seamm/control_parameters_step/shield.svg
   :target: https://pyup.io/repos/github/molssi-seamm/control_parameters_step/
   :alt: Updates for Dependencies

.. image:: https://img.shields.io/pypi/v/control_parameters_step.svg
   :target: https://pypi.python.org/pypi/control_parameters_step
   :alt: PyPi VERSION

Description
-----------

A SEAMM plug-in for defining command-line parameters for a
flowchart. This plug-in provides a step in a SEAMM flowchart where a
user can define required and optional arguments for the flowchart as a
whole. When the flowchart is run, the command-line is parsed and the
arguments placed in variables that can then be used by other steps.

This can be used to pass file names or SMILES strings for the
molecules to run; or give the temperature and pressure; or any
appropriate parameters that the flowchart author feels are relevant.

When run from the command-line, giving the option `--help` provides
help on these control parameters as well as other options for the run::

    bash-3.2$ ../flowcharts/psi4.flow --help
    usage: ../flowcharts/psi4.flow [options] plug-in [options] plug-in [options] ...
    
    positional arguments:
      SMILES                The SMILES string for the input molecule
    
    optional arguments:
      -h, --help            show this help message and exit
      --method {b3lyp-d3mbj,mp2,ccsd}
                            The type of calculation
    ... 

- Free software: BSD-3-Clause
- Documentation: https://molssi-seamm.github.io/control_parameters_step/index.html


Features
--------

- Graphical user interface (GUI) to define the parameters.
- Mandatory and optional arguments, as well as flags for boolean
  options.
- Default values for optional arguments.
- Follows standard, familiar  Unix conventions for command-line
  arguments.
- Help provided by `-h` or `--help` options.

Credits
---------

This package was created with Cookiecutter_ and the `molssi-seamm/cookiecutter-seamm-plugin`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`molssi-seamm/cookiecutter-seamm-plugin`: https://github.com/molssi-seamm/cookiecutter-seamm-plugin

Developed by the Molecular Sciences Software Institute (MolSSI_),
which receives funding from the `National Science Foundation`_ under
award OAC-1547580 and CHE-2136142.

.. _MolSSI: https://www.molssi.org
.. _`National Science Foundation`: https://www.nsf.gov

