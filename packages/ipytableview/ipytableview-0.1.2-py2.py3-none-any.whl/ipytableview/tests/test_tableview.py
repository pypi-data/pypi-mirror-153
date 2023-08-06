#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Juan F. Esteban Müller.
# Distributed under the terms of the Modified BSD License.

from ..tableview_widget import TableViewWidget


def test_tableview_creation_blank():
    w = TableViewWidget()
    assert w.selected == -1
