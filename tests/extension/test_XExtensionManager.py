#!/usr/bin/env python

"""This is the test module for XExtensionManager.

This module tests XExtensionManager.
"""

__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


import pytest
from urllib.parse import urlparse
from opyenxes.extension.XExtensionManager import XExtensionManager
from opyenxes.extension.std.XConceptExtension import XConceptExtension
from opyenxes.extension.std.XCostExtension import XCostExtension
from opyenxes.extension.std.XIdentityExtension import XIdentityExtension
from opyenxes.extension.std.XLifecycleExtension import XLifecycleExtension
from opyenxes.extension.std.XMicroExtension import XMicroExtension
from opyenxes.extension.std.XOrganizationalExtension import XOrganizationalExtension
from opyenxes.extension.std.XSemanticExtension import XSemanticExtension
from opyenxes.extension.std.XTimeExtension import XTimeExtension


@pytest.fixture(scope='function')
def instance():
    return XExtensionManager()


def test_create_extension_manager():
    manager = XExtensionManager()
    assert manager is not None


def test_get_by_name(instance):
    concept_ext = instance.get_by_name('Concept')
    cost_ext = instance.get_by_name('Cost')
    identity_ext = instance.get_by_name('Identity')
    lifecycle_ext = instance.get_by_name('Lifecycle')
    micro_ext = instance.get_by_name('Micro')
    org_ext = instance.get_by_name('Organizational')
    semantic_ext = instance.get_by_name('Semantic')
    time_ext = instance.get_by_name('Time')

    assert isinstance(concept_ext, XConceptExtension)
    assert isinstance(cost_ext, XCostExtension)
    assert isinstance(identity_ext, XIdentityExtension)
    assert isinstance(lifecycle_ext, XLifecycleExtension)
    assert isinstance(micro_ext, XMicroExtension)
    assert isinstance(org_ext, XOrganizationalExtension)
    assert isinstance(semantic_ext, XSemanticExtension)
    assert isinstance(time_ext, XTimeExtension)


def test_get_by_prefix(instance):
    concept_ext = instance.get_by_prefix('concept')
    cost_ext = instance.get_by_prefix('cost')
    identity_ext = instance.get_by_prefix('identity')
    lifecycle_ext = instance.get_by_prefix('lifecycle')
    micro_ext = instance.get_by_prefix('micro')
    org_ext = instance.get_by_prefix('org')
    semantic_ext = instance.get_by_prefix('semantic')
    time_ext = instance.get_by_prefix('time')

    assert isinstance(concept_ext, XConceptExtension)
    assert isinstance(cost_ext, XCostExtension)
    assert isinstance(identity_ext, XIdentityExtension)
    assert isinstance(lifecycle_ext, XLifecycleExtension)
    assert isinstance(micro_ext, XMicroExtension)
    assert isinstance(org_ext, XOrganizationalExtension)
    assert isinstance(semantic_ext, XSemanticExtension)
    assert isinstance(time_ext, XTimeExtension)


def test_get_by_uri(instance):
    concept_ext = instance.get_by_uri(urlparse("http://www.xes-standard.org/concept.xesext"))
    cost_ext = instance.get_by_uri(urlparse("http://www.xes-standard.org/cost.xesext"))
    identity_ext = instance.get_by_uri(urlparse("http://www.xes-standard.org/identity.xesext"))
    lifecycle_ext = instance.get_by_uri(urlparse("http://www.xes-standard.org/lifecycle.xesext"))
    micro_ext = instance.get_by_uri(urlparse("http://www.xes-standard.org/micro.xesext"))
    org_ext = instance.get_by_uri(urlparse("http://www.xes-standard.org/org.xesext"))
    semantic_ext = instance.get_by_uri(urlparse("http://www.xes-standard.org/semantic.xesext"))
    time_ext = instance.get_by_uri(urlparse("http://www.xes-standard.org/time.xesext"))

    assert isinstance(concept_ext, XConceptExtension)
    assert isinstance(cost_ext, XCostExtension)
    assert isinstance(identity_ext, XIdentityExtension)
    assert isinstance(lifecycle_ext, XLifecycleExtension)
    assert isinstance(micro_ext, XMicroExtension)
    assert isinstance(org_ext, XOrganizationalExtension)
    assert isinstance(semantic_ext, XSemanticExtension)
    assert isinstance(time_ext, XTimeExtension)
