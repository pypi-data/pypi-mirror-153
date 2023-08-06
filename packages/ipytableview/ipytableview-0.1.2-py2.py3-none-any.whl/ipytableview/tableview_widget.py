#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Juan F. Esteban Müller.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, List, Int
from ._frontend import module_name, module_version


@register
class TableViewWidget(DOMWidget, ValueWidget):
    """TODO: Add docstring here"""

    _model_name = Unicode("TableModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("TableView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    table_body = List([]).tag(sync=True)
    headers = List([]).tag(sync=True)
    selected = Int(-1).tag(sync=True)

    def __init__(self, headers=None, *args):
        if headers is not None:
            self.headers = headers

        super().__init__(*args)
