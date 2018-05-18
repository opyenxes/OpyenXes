#!/usr/bin/env python

"""This is the test module for XExtensionParser.

This module tests XExtensionParser.
"""


from opyenxes.extension.XExtensionManager import XExtensionParser

__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


def test_create_extension_parser():
    parser = XExtensionParser()
    assert parser is not None
