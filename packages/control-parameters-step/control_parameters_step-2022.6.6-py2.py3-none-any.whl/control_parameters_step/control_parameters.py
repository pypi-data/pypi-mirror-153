# -*- coding: utf-8 -*-

"""Non-graphical part of the Control Parameters step in a SEAMM flowchart

The Control Parameters step allows the person creating the flowchart
to specify an arbitrary number of parameters that can be set when the
flowchart is run, typically by command-line arguments. Parameters may
be positional or optional, in which case they indicated by a 'flag' on
the command line, e.g. --n 10.

By default, these parameters will not replace a current value if it
already exists, though this can be changed. This allows embedding
flowcharts within other flowcharts without overriding parameters, but
ensuring that all parameters are set.

Parameters have a specified type:

        str     A text string
        int     An integer
        float   A floating point number
        bool    A boolean value: 1/0, True/False, Yes/No

Typically parameters have one value associated with them; however, any
parameter may have a specified or variable number of values, including
none. The possibilities are:

        a single value          This is the default
        N values                Where N is an integer >= 1
        an optional value       If not present, the default is used
        zero or more values
        one or more values

An optional parameter need not have a default, in which case if it
does not appear on the command-line it is not set in the SEAMM
environment.

Rather than allow any value of the correct type, an option can be
restricted to a list of choices. For example, a convergence citerion
might be 'normal', 'tight' or 'loose' or an MPn quantum calculation
might allow n to be 2, 3, or 4.

In addition to command-line arguments, this module supports
environment variables and a control file with a simple format of `key
= value`. If a parameter appears in multiple places, the precedence is
command-line > environment variable > file > default.

Positional parameters must appear in the right place on the command
line. Optional parameters are given with a flag of form '--<name>',
e.g. '--P' or '--nsteps'.

The environment variable by default is SEAMM_<name>, in all capital
letters, e.g. SEAMM_P or SEAMM_nsteps.

In a control file, the variable name is used as-is followed by the
value, or = value or : value. Or it can look like a command line argument:

        P 1.0
        P=1.0
        P: 10
        --P 50
        nsteps 50
        nsteps = 50
        nsteps:50
        --nsteps 50

Positional arguments cannot be put in a control file. If the value is
a list, encase it in square brackets:

        pressures = [1.0, 2.0, 5.0, 10.0]

Internally the parameter definitions are stored in a dictionary with
the parameter name as key and the value is itself a dictionary labeled
by the item in the definition, e.g. 'name', 'default', and 'nargs':

        "T": {
            "type": "float",
            "nargs": "a single value",
            "optional": "Yes",
            "default": "298.15",
            "choices": "[]",
            "overwrite": "No",
            "help": "The temperature"
        },

"""

import json
import logging
import pprint  # noqa: F401
import textwrap

from tabulate import tabulate

import control_parameters_step
import seamm
import seamm_util
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# In addition to the normal logger, two logger-like printing facilities are
# defined: 'job' and 'printer'. 'job' send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# 'printer' sends output to the file 'step.out' in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("Control Parameters")


types = {
    "file": str,
    "str": str,
    "int": int,
    "float": float,
    "choice": list,
    "bool": bool,
    "list": list,
}

nargs_values = {
    "a single value": None,
    "an optional value": "?",
    "zero or more values": "*",
    "one or more values": "+",
}


class ControlParameters(seamm.Node):
    """
    The non-graphical part of a Control Parameters step in a flowchart.

    Attributes
    ----------
    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : ControlParametersParameters
        The control parameters for Control Parameters.

    See Also
    --------
    TkControlParameters,
    ControlParameters, ControlParametersParameters
    """

    def __init__(
        self, flowchart=None, title="Parameters", extension=None, logger=logger
    ):
        """A step for Control Parameters in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug("Creating Control Parameters {}".format(self))

        super().__init__(
            flowchart=flowchart,
            title="Parameters",
            extension=extension,
            logger=logger,
        )  # yapf: disable

        self.parameters = control_parameters_step.ControlParametersParameters()

    @property
    def version(self):
        """The semantic version of this module."""
        return control_parameters_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return control_parameters_step.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.
        Returns
        -------
        str
            A description of the current step.
        """
        if not P:
            P = self.parameters.values_to_dict()

        lines = []
        lines.append(
            textwrap.fill(
                "The following variables will be set from command-line "
                "arguments, or if not present, to the default value."
            )
        )
        variables = self.parameters["variables"]
        lines.append("")

        table = {"Variable": [], "Type": [], "Default": [], "Description": []}

        for name, data in variables.value.items():
            table["Variable"].append(name)
            table["Type"].append(data["type"])
            table["Default"].append(data["default"])
            table["Description"].append(textwrap.fill(data["help"], width=40))

        lines.append(tabulate(table, headers="keys", tablefmt="grid"))

        return self.header + "\n" + textwrap.indent("\n".join(lines), 4 * " ")

    def run(self):
        """Run a Control Parameters step.

        Parameters
        ----------
        None

        Returns
        -------
        seamm.Node
            The next node object in the flowchart.
        """
        self.logger.debug("Entering the control parameters step run method")
        next_node = super().run(printer)

        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        variables = P["variables"]

        # Print what we are doing
        printer.important(
            self.header
            + "\n"
            + str(
                __(
                    "The following variables have been set from command-line "
                    "arguments, environment variables, a configuration file, "
                    "(.ini), or a default value, in that order.",
                    indent=4 * " ",
                )
            )
            + "\n"
        )

        # Get the parser
        parser = seamm_util.getParser()
        options = parser.get_options("SEAMM")
        origins = parser.get_origins("SEAMM")

        self.logger.debug(f"  Parsed options:\n{pprint.pformat(options)}\n")
        self.logger.debug(f"Origin of values:\n{pprint.pformat(origins)}\n")

        table = {
            "Variable": [],
            "Value": [],
            "O": [],
            "Set From": [],
            "Description": [],
        }

        have_overwrite = False
        used_ini_file = False
        for dest, data in variables.items():
            table["Variable"].append(dest)

            value = options[dest]

            if dest in origins:
                where = origins[dest]
            else:
                where = "command line"

            if self.variable_exists(dest):
                if data["overwrite"] == "Yes":
                    if data["type"] == "file":
                        if isinstance(value, list):
                            paths = []
                            tmp = []
                            for val in value:
                                path = self.file_path(val)
                                tmp.append(str(path))
                                paths.append(path)
                            value = tmp
                            self.set_variable(dest, paths)
                        else:
                            path = self.file_path(value)
                            value = str(path)
                            self.set_variable(dest, path)
                    else:
                        self.set_variable(dest, value)
                    table["O"].append("*")
                    have_overwrite = True
                else:
                    value = self.get_variable(dest)
                    where = "existing"
                    table["O"].append("")
            else:
                if data["type"] == "file":
                    if isinstance(value, list):
                        paths = []
                        tmp = []
                        for val in value:
                            path = self.file_path(val)
                            tmp.append(str(path))
                            paths.append(path)
                        value = tmp
                        self.set_variable(dest, paths)
                    else:
                        path = self.file_path(value)
                        value = str(path)
                        self.set_variable(dest, path)
                else:
                    self.set_variable(dest, value)

            if isinstance(value, list):
                if len(value) > 5:
                    table["Value"].append("\n".join(value[0:5]) + "\n...")
                else:
                    table["Value"].append("\n".join(value))
            else:
                table["Value"].append(value)

            if where == "configfile":
                used_ini_file = True

            table["Set From"].append(where)
            table["Description"].append(textwrap.fill(data["help"], width=40))

        if not have_overwrite:
            del table["O"]

        printer.normal(
            __(
                tabulate(table, headers="keys", tablefmt="grid"),
                indent=4 * " ",
                wrap=False,
                dedent=False,
            )
        )

        if have_overwrite:
            printer.normal(
                __(
                    "\n* = this variable existed, but was overwritten.",
                    indent=4 * " ",
                    dedent=False,
                )
            )

        if used_ini_file:
            printer.normal(
                __(
                    (
                        "\nThe following .ini files were used: "
                        f'{", ".join(parser.get_ini_files())}.'
                    ),
                    indent=4 * " ",
                    dedent=False,
                )
            )

        printer.normal("")

        # Add other citations here or in the appropriate place in the code.
        # Add the bibtex to data/references.bib, and add a self.reference.cite
        # similar to the above to actually add the citation to the references.

        self.logger.debug("Leaving the control parameters step run method")

        return next_node

    def create_parser(self):
        """Setup the command-line / config file parser"""
        parser_name = "control-parameters-step"
        parser = seamm_util.getParser()

        # Remember if the parser exists ... this type of step may have been
        # found before
        # parser_exists = parser.exists(parser_name)

        # Create the standard options, e.g. log-level
        result = super().create_parser(name=parser_name)

        # This node is special in that the run() method is actually parsing
        # the options -- and they are in the SEAMM space. So set that up here

        variables = self.parameters["variables"].value

        # plugins = parser.add_argument_group('plug-ins')
        for dest, data in variables.items():
            data_type = data["type"]
            type_ = types[data_type]
            default = type_(data["default"])
            if data["optional"] == "Yes":
                name = "--" + dest
            else:
                name = dest
            nargs = nargs_values[data["nargs"]]
            choices = data["choices"]
            if choices == "":
                choices = None
            else:
                # choices is a string representation of a list
                choices = json.loads(choices.replace("'", '"'))
                if len(choices) == 0:
                    choices = None

            parser.add_argument(
                "SEAMM",
                name,
                type=type_,
                nargs=nargs,
                default=default,
                choices=choices,
                help=data["help"],
            )

        return result
