#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `opyenxes` package."""

import pytest

from click.testing import CliRunner

from opyenxes import cli

# test import everything
from opyenxes.classification import XEventAndClassifier
from opyenxes.classification import XEventAttributeClassifier
from opyenxes.classification import XEventClass
from opyenxes.classification import XEventClasses
from opyenxes.classification import XEventLifeTransClassifier
from opyenxes.classification import XEventNameClassifier
from opyenxes.classification import XEventResourceClassifier

from opyenxes.data_in import XesXmlGZIPParser
from opyenxes.data_in import XesXmlParser
from opyenxes.data_in import XMxmlGZIPParser
from opyenxes.data_in import XMxmlParser
from opyenxes.data_in import XParserRegistry
from opyenxes.data_in import XUniversalParser

from opyenxes.extension import XExtension
from opyenxes.extension import XExtensionManager
from opyenxes.extension import XExtensionParser

from opyenxes.extension.std import XAbstractNestedAttributeSupport
from opyenxes.extension.std import XConceptExtension
from opyenxes.extension.std import XCostExtension
from opyenxes.extension.std import XExtendedEvent
from opyenxes.extension.std import XIdentityExtension
from opyenxes.extension.std import XLifecycleExtension
from opyenxes.extension.std import XMicroExtension
from opyenxes.extension.std import XOrganizationalExtension
from opyenxes.extension.std import XSemanticExtension
from opyenxes.extension.std import XTimeExtension

from opyenxes.factory import XFactory
from opyenxes.factory import XFactoryRegistry

from opyenxes.id import XID
from opyenxes.id import XIDFactory

from opyenxes.info import XAttributeInfo
from opyenxes.info import XAttributeNameMap
from opyenxes.info import XGlobalAttributeNameMap
from opyenxes.info import XLogInfo
from opyenxes.info import XLogInfoFactory
from opyenxes.info import XTimeBounds

from opyenxes.log import XLogging
from opyenxes.log import XStdoutLoggingListener

from opyenxes.model import XAttributable
from opyenxes.model import XAttribute
from opyenxes.model import XAttributeBoolean
from opyenxes.model import XAttributeCollection
from opyenxes.model import XAttributeContinuous
from opyenxes.model import XAttributeDiscrete
from opyenxes.model import XAttributeID
from opyenxes.model import XAttributeList
from opyenxes.model import XAttributeLiteral
from opyenxes.model import XAttributeMap
from opyenxes.model import XAttributeTimestamp
from opyenxes.model import XElement
from opyenxes.model import XEvent
from opyenxes.model import XLog
from opyenxes.model import XTrace

from opyenxes.out import XesXmlGZIPSerializer
from opyenxes.out import XesXmlSerializer
from opyenxes.out import XMxmlGZIPSerializer
from opyenxes.out import XMxmlSerializer
from opyenxes.out import XSerializerRegistry

from opyenxes.utils import CompareUtils
from opyenxes.utils import SingletonClassGenerator
from opyenxes.utils import XAttributeUtils
from opyenxes.utils import XRegistry
from opyenxes.utils import XRuntimeUtils
from opyenxes.utils import XsDateTimeConversion
from opyenxes.utils import XTimer
from opyenxes.utils import XTokenHelper


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'opyenxes.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
