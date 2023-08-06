# -*- coding: utf-8 -*-

"""
control_parameters_step
A step for control parameters in SEAMM
"""

# Bring up the classes so that they appear to be directly in
# the control_parameters_step package.

from control_parameters_step.control_parameters import (  # noqa: F401
    ControlParameters,
)
from control_parameters_step.control_parameters_parameters import (  # noqa: F401, E501
    ControlParametersParameters,
)
from control_parameters_step.control_parameters_step import (  # noqa: F401
    ControlParametersStep,
)
from control_parameters_step.tk_control_parameters import (  # noqa: F401
    TkControlParameters,
)

# Handle versioneer
from ._version import get_versions

__author__ = """Paul Saxe"""
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
