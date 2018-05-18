#!/usr/bin/env python

"""This is the test module for XConceptExtension.

This module tests XConceptExtension.
"""


from opyenxes.extension.std.XConceptExtension import XConceptExtension


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


def test_create_extension():
    extension = XConceptExtension()
    assert extension is not None
