#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `control_parameters_step` package."""

import pytest  # noqa: F401
import control_parameters_step  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = control_parameters_step.ControlParameters()
    assert str(type(result)) == (
        "<class 'control_parameters_step.control_parameters.ControlParameters'>"  # noqa: E501
    )
