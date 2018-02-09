#!/usr/bin/env python

"""This is the test module for XExtensionManager.

This module tests XExtensionManager.
"""

__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


from opyenxes.extension import *


def test_create_extension_manager():
    manager = XExtensionManager()
    assert manager is not None

