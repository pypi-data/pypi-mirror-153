# -*- coding: utf-8 -*-

"""The graphical part of a Control Parameters step"""

import seamm
from seamm_util import ureg, Q_, units_class  # noqa: F401
import seamm_widgets as sw
import control_parameters_step  # noqa: F401
import Pmw
import pprint  # noqa: F401
import tkinter as tk
import tkinter.ttk as ttk


class TkControlParameters(seamm.TkNode):
    """
    The graphical part of a Control Parameters step in a flowchart.

    Attributes
    ----------
    tk_flowchart : TkFlowchart = None
        The flowchart that we belong to.
    node : Node = None
        The corresponding node of the non-graphical flowchart
    namespace : str
        The namespace of the current step.
    sub_tk_flowchart : TkFlowchart
        A graphical Flowchart representing a subflowchart
    canvas: tkCanvas = None
        The Tk Canvas to draw on
    dialog : Dialog
        The Pmw dialog object
    x : int = None
        The x-coordinate of the center of the picture of the node
    y : int = None
        The y-coordinate of the center of the picture of the node
    w : int = 200
        The width in pixels of the picture of the node
    h : int = 50
        The height in pixels of the picture of the node
    self[widget] : dict
        A dictionary of tk widgets built using the information
        contained in Control Parameters_parameters.py

    See Also
    --------
    ControlParameters, TkControlParameters,
    ControlParametersParameters,
    """

    def __init__(
        self, tk_flowchart=None, node=None, canvas=None, x=None, y=None, w=200, h=50
    ):
        """
        Initialize a graphical node.

        Parameters
        ----------
        tk_flowchart: Tk_Flowchart
            The graphical flowchart that we are in.
        node: Node
            The non-graphical node for this step.
        namespace: str
            The stevedore namespace for finding sub-nodes.
        canvas: Canvas
           The Tk canvas to draw on.
        x: float
            The x position of the nodes center on the canvas.
        y: float
            The y position of the nodes cetner on the canvas.
        w: float
            The nodes graphical width, in pixels.
        h: float
            The nodes graphical height, in pixels.

        Returns
        -------
        None
        """
        self.dialog = None
        self._variables = None  # temporary copy when editing
        self._new_variable_dialog = None
        self._new = {}  # Widgets for the new variable dialog
        self._edit_variable_dialog = None
        self._edit = {}  # Widgets for the edit variable dialog

        super().__init__(
            tk_flowchart=tk_flowchart, node=node, canvas=canvas, x=x, y=y, w=w, h=h
        )

    def create_dialog(self):
        """
        Create the dialog. A set of widgets will be chosen by default
        based on what is specified in the Control Parameters_parameters
        module.

        Parameters
        ----------
        None

        Returns
        -------
        None

        See Also
        --------
        TkControlParameters.reset_dialog
        """
        frame = super().create_dialog("Edit Parameters")

        # make it large!
        screen_w = self.dialog.winfo_screenwidth()
        screen_h = self.dialog.winfo_screenheight()
        w = int(0.9 * screen_w)
        h = int(0.8 * screen_h)
        x = int(0.05 * screen_w / 2)
        y = int(0.1 * screen_h / 2)

        self.dialog.geometry("{}x{}+{}+{}".format(w, h, x, y))

        # The information about widgets is held in self['xxxx'], i.e. this
        # class is in part a dictionary of widgets. This makes accessing
        # the widgets easier and allows loops, etc.

        # Shortcut for parameters
        P = self.node.parameters

        # Then create the widgets
        self["variables"] = sw.ScrolledColumns(
            frame,
            columns=[
                "",
                "Name",
                "Type",
                "NArgs",
                "Optional",
                "Overwrite?",
                "Default",
                "Help",
            ],
        )
        # any remaining widgets
        for key in P:
            if key not in self:
                self[key] = P[key].widget(frame)

    def reset_dialog(self, widget=None):
        """Layout the widgets in the dialog.

        The widgets are chosen by default from the information in
        Control Parameters_parameter.

        This function simply lays them out row by row with
        aligned labels. You may wish a more complicated layout that
        is controlled by values of some of the control parameters.
        If so, edit or override this method

        Parameters
        ----------
        widget : Tk Widget = None

        Returns
        -------
        None

        See Also
        --------
        TkControlParameters.create_dialog
        """

        # Remove any widgets previously packed
        frame = self["frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # Shortcut for parameters
        P = self.node.parameters

        # keep track of the row in a variable, so that the layout is flexible
        # if e.g. rows are skipped to control such as 'method' here
        row = 0
        widgets = []

        # Variables table first
        key = "variables"
        self[key].grid(row=row, column=0, sticky=tk.NSEW)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(row, weight=1)
        widgets.append(self[key])
        row += 1

        for key in P:
            if self[key] not in widgets:
                self[key].grid(row=row, column=0, sticky=tk.EW)
                widgets.append(self[key])
                row += 1

        # Align the labels
        sw.align_labels(widgets)

    def right_click(self, event):
        """
        Handles the right click event on the node.

        Parameters
        ----------
        event : Tk Event

        Returns
        -------
        None

        See Also
        --------
        TkControlParameters.edit
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the Control Parameters input

        Parameters
        ----------
        None

        Returns
        -------
        None

        See Also
        --------
        TkControlParameters.right_click
        """

        if self.dialog is None:
            self.create_dialog()

        P = self.node.parameters
        self._variables = P["variables"].value
        self.reset_dialog()
        self.reset_table()

        self.dialog.activate(geometry="centerscreenfirst")

    def handle_dialog(self, result):
        """Handle the closing of the edit dialog

        What to do depends on the button used to close the dialog. If
        the user closes it by clicking the 'x' of the dialog window,
        None is returned, which we take as equivalent to cancel.

        Parameters
        ----------
        result : None or str
            The value of this variable depends on what the button
            the user clicked.

        Returns
        -------
        None
        """

        if result is None or result == "Cancel":
            self.dialog.deactivate(result)
            self._variables = None
            return

        if result == "Help":
            # display help!!!
            return

        if result != "OK":
            self.dialog.deactivate(result)
            raise RuntimeError("Don't recognize dialog result '{}'".format(result))

        self.dialog.deactivate(result)
        # Shortcut for parameters
        P = self.node.parameters

        # Get the values for all the widgets.
        P["variables"].value = self._variables
        self._variables = None

        for key in P:
            if key != "variables":
                P[key].set_from_widget()

    def handle_help(self):
        """Shows the help to the user when click on help button.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print("Help not implemented yet for Control Parameters!")

    def add_variable(self):
        """Add a new variable to the table."""
        # Post dialog to fill out the new variable
        if self._new_variable_dialog is None:
            self.create_new_variable_dialog()

        self._new["name"].set("")
        self._new["type"].set("float")
        self._new["optional"].set("Yes")
        self._new["nargs"].set("a single value")
        self._new["overwrite"].set("No")
        self._new["default"].set("")
        self._new["choices"].set("[]")
        self._new["help"].set("")

        self._new_variable_dialog.activate(geometry="centerscreenfirst")

    def create_new_variable_dialog(self):
        """
        Create a dialog for adding new variables.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self._new_variable_dialog is not None:
            return

        dialog = self._new_variable_dialog = Pmw.Dialog(
            self.dialog.interior(),
            buttons=("OK", "Cancel"),
            defaultbutton="OK",
            title="Add Variable",
            command=self.handle_new_variable_dialog,
        )
        self._new_variable_dialog.withdraw()

        # Create a frame to hold everything in the dialog
        frame = self._new["frame"] = ttk.Frame(dialog.interior())
        frame.pack(expand=tk.YES, fill=tk.BOTH)

        # Then create the widgets
        self._new["name"] = sw.LabeledEntry(frame, labeltext="Name")
        self._new["optional"] = sw.LabeledCombobox(
            frame, labeltext="Optional?:", values=("Yes", "No"), state="readonly"
        )
        self._new["type"] = sw.LabeledCombobox(
            frame,
            labeltext="Type:",
            values=(
                "str",
                "int",
                "float",
                "bool",
                "file",
            ),
            state="readonly",
        )
        self._new["nargs"] = sw.LabeledCombobox(
            frame,
            labeltext="Number of values:",
            values=(
                "a single value",
                "an optional value",
                "zero or more values",
                "one or more values",
            ),
            state="readonly",
        )
        self._new["overwrite"] = sw.LabeledCombobox(
            frame,
            labeltext="Overwrite if exists:",
            values=("Yes", "No"),
            state="readonly",
        )
        self._new["default"] = sw.LabeledEntry(frame, labeltext="Default:")
        self._new["choices"] = sw.LabeledEntry(frame, labeltext="Choices:")
        self._new["help"] = sw.LabeledEntry(frame, labeltext="Help:", width=80)

        # and lay them out
        self.reset_new_variable_dialog()

    def reset_new_variable_dialog(self):
        """Lay the dialog out based on the contents."""
        # Remove any widgets previously packed
        frame = self._new["frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        row = 0
        widgets = []

        for key in ("name", "type", "nargs", "optional", "overwrite"):
            self._new[key].grid(row=row, column=0, sticky=tk.EW)
            widgets.append(self._new[key])
            row += 1

        type_ = self._new["type"].get()
        if type_ != "bool":
            w = self._new["default"]
            w.grid(row=row, column=0, sticky=tk.EW)
            widgets.append(w)
            row += 1
            w = self._new["choices"]
            w.grid(row=row, column=0, sticky=tk.EW)
            widgets.append(w)
            row += 1
        self._new["help"].grid(row=row, column=0, sticky=tk.EW)
        widgets.append(self._new["help"])
        row += 1

        sw.align_labels(widgets)

    def handle_new_variable_dialog(self, result):
        """Handle the closing of the new variable dialog

        What to do depends on the button used to close the dialog. If
        the user closes it by clicking the 'x' of the dialog window,
        None is returned, which we take as equivalent to cancel.

        Parameters
        ----------
        result : None or str
            The value of this variable depends on what the button
            the user clicked.

        Returns
        -------
        None
        """

        if result is None or result == "Cancel":
            self._new_variable_dialog.deactivate(result)
            return

        if result != "OK":
            self._new_variable_dialog.deactivate(result)
            raise RuntimeError(f"Don't recognize new variable dialog result '{result}'")

        self._new_variable_dialog.deactivate(result)

        name = self._new["name"].get()
        if name in self._variables:
            raise KeyError(f"Duplicate variable name: '{name}'")

        data = self._variables[name] = {}
        for key, w in self._new.items():
            if key not in ("frame", "name"):
                data[key] = w.get()

        self.reset_table()

    def reset_table(self):
        """Update the table of variables to the current data."""
        table = self["variables"]

        frame = table.table.interior()
        table.clear()

        row = 0
        for name, data in self._variables.items():
            table[row, 0] = ttk.Button(
                frame,
                text="-",
                width=5,
                command=lambda nm=name: self.remove_variable(nm),
                takefocus=True,
            )
            table[row, 1] = ttk.Button(
                frame,
                text="Edit",
                width=5,
                command=lambda nm=name: self.edit_variable(nm),
                takefocus=True,
            )
            table[row, 2] = name
            table[row, 3] = data["type"]
            table[row, 4] = data["nargs"]
            table[row, 5] = data["optional"]
            table[row, 6] = data["overwrite"]
            if data["type"] != "bool":
                table[row, 7] = data["default"]
            table[row, 8] = data["help"]
            row += 1

        # a button to add new variables...
        table[row, 0] = ttk.Button(
            frame, text="+", width=5, command=self.add_variable, takefocus=True
        )

        table.update_idletasks()

    def edit_variable(self, name):
        """Edit the values associated with a variable."""
        # Post dialog to fill out the new variable
        if self._edit_variable_dialog is None:
            self.create_edit_variable_dialog()

        self._edit_variable_dialog.configure(
            command=lambda result, nm=name: self.handle_edit_variable_dialog(
                nm, result
            )  # noqa: E501
        )

        data = self._variables[name]
        for key, w in self._edit.items():
            if key == "name":
                w.set(name)
            elif key != "frame":
                w.set(data[key])

        self._edit_variable_dialog.activate(geometry="centerscreenfirst")

    def create_edit_variable_dialog(self):
        """
        Create a dialog for adding edit variables.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self._edit_variable_dialog is not None:
            return

        dialog = self._edit_variable_dialog = Pmw.Dialog(
            self.dialog.interior(),
            buttons=("OK", "Cancel"),
            defaultbutton="OK",
            title="Edit Variable",
            command=lambda: self.handle_edit_variable_dialog,
        )
        self._edit_variable_dialog.withdraw()

        # Create a frame to hold everything in the dialog
        frame = self._edit["frame"] = ttk.Frame(dialog.interior())
        frame.pack(expand=tk.YES, fill=tk.BOTH)

        # Then create the widgets
        self._edit["name"] = sw.LabeledEntry(frame, labeltext="Name")
        self._edit["optional"] = sw.LabeledCombobox(
            frame, labeltext="Type:", values=("Yes", "No"), state="readonly"
        )
        self._edit["type"] = sw.LabeledCombobox(
            frame,
            labeltext="Type:",
            values=(
                "str",
                "int",
                "float",
                "bool",
                "file",
            ),
            state="readonly",
        )
        self._edit["nargs"] = sw.LabeledCombobox(
            frame,
            labeltext="Number of values:",
            values=(
                "a single value",
                "an optional value",
                "zero or more values",
                "one or more",
            ),
            state="readonly",
        )
        self._edit["overwrite"] = sw.LabeledCombobox(
            frame,
            labeltext="Overwrite if exists:",
            values=("Yes", "No"),
            state="readonly",
        )
        self._edit["default"] = sw.LabeledEntry(frame, labeltext="Default:")
        self._edit["choices"] = sw.LabeledEntry(frame, labeltext="Choices:")
        self._edit["optional"] = sw.LabeledCombobox(
            frame, labeltext="Optional?:", values=("Yes", "No"), state="readonly"
        )
        self._edit["help"] = sw.LabeledEntry(frame, labeltext="Help:", width=80)

        # and lay them out
        self.reset_edit_variable_dialog()

    def reset_edit_variable_dialog(self):
        """Lay the dialog out based on the contents."""
        # Remove any widgets previously packed
        frame = self._edit["frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        row = 0
        widgets = []

        for key in ("name", "type", "nargs", "optional", "overwrite"):
            self._edit[key].grid(row=row, column=0, sticky=tk.EW)
            widgets.append(self._edit[key])
            row += 1

        type_ = self._edit["type"].get()
        if type_ != "bool":
            w = self._edit["default"]
            w.grid(row=row, column=0, sticky=tk.EW)
            widgets.append(w)
            row += 1
            w = self._edit["choices"]
            w.grid(row=row, column=0, sticky=tk.EW)
            widgets.append(w)
            row += 1
        self._edit["help"].grid(row=row, column=0, sticky=tk.EW)
        widgets.append(self._edit["help"])
        row += 1

        sw.align_labels(widgets)

    def handle_edit_variable_dialog(self, name, result):
        """Handle the closing of the edit variable dialog

        What to do depends on the button used to close the dialog. If
        the user closes it by clicking the 'x' of the dialog window,
        None is returned, which we take as equivalent to cancel.

        Parameters
        ----------
        result : None or str
            The value of this variable depends on what the button
            the user clicked.

        Returns
        -------
        None
        """

        if result is None or result == "Cancel":
            self._edit_variable_dialog.deactivate(result)
            return

        if result != "OK":
            self._edit_variable_dialog.deactivate(result)
            raise RuntimeError(
                f"Don't recognize edit variable dialog result '{result}'"
            )

        self._edit_variable_dialog.deactivate(result)

        new_name = self._edit["name"].get().lstrip("-")
        if new_name == name:
            data = self._variables[name]
        else:
            del self._variables[name]
            name = new_name
            data = self._variables[name] = {}

        for key, w in self._edit.items():
            if key not in ("frame", "name"):
                data[key] = w.get()

        self.reset_table()

    def remove_variable(self, name):
        """Remove a variable variable."""
        del self._variables[name]
        self.reset_table()
