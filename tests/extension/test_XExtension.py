#!/usr/bin/env python

"""This is the test module for XExtension.

This module tests XExtension.
"""

from opyenxes.extension.XExtension import XExtension
from urllib.parse import urlencode
import pytest


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


@pytest.fixture()
def extension():
    name = 'ext0'
    prefix = 'ext'
    uri = urlencode({'uri': 'value'})
    extension = XExtension(name, prefix, uri)
    return extension


def test_create_extension():
    name = 'ext0'
    prefix = 'ext'
    uri = urlencode({'arg': 'value'})
    extension = XExtension(name, prefix, uri)
    assert extension is not None
    assert extension.get_uri() == uri
    assert extension.get_name() == name
    assert extension.get_prefix() == prefix


def test_get_defined_attributes(extension):
    defined_attrs = extension.get_defined_attributes()
    assert len(defined_attrs) == 0
