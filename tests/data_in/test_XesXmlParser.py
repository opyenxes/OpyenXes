#!/usr/bin/env python

"""This is the test module for XesXmlParser.

This module tests the XesXmlParser.
"""


import pytest, os, tempfile
from opyenxes.data_in.XesXmlParser import XesXmlParser
from opyenxes.data_out.XesXmlSerializer import XesXmlSerializer
from opyenxes.factory.XFactory import XFactory
from opyenxes.classification.XEventNameClassifier import XEventNameClassifier
from opyenxes.extension.XExtensionParser import XExtensionParser
from opyenxes.extension.XExtensionManager import XExtensionManager


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


@pytest.fixture()
def cleandir():
    # make empty directory to conduct tests
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)


@pytest.fixture(scope='module')
def log():
    log = XFactory.create_log()
    # add log classifier
    clf = XEventNameClassifier()
    log.get_classifiers().append(clf)
    # add global trace attributes
    glb_t_attr = XFactory.create_attribute_discrete('glb_t_attr', 0)
    log.get_global_trace_attributes().append(glb_t_attr)
    # add global event attributes
    glb_e_attr = XFactory.create_attribute_discrete('glb_e_attr', 0)
    log.get_global_event_attributes().append(glb_e_attr)
    # add log attributes
    str_attr = XFactory.create_attribute_literal('l_attr', 'UNKNOWN')
    log.get_attributes()['l_attr'] = str_attr
    # add extension
    meta_concept = XExtensionParser().parse("http://www.xes-standard.org/meta_concept.xesext")
    log.get_extensions().add(meta_concept)
    # add a trace
    tracelen = 2
    trace0 = XFactory.create_trace()
    # add some trace attributes
    bool_attr = XFactory.create_attribute_boolean('t_attr', True)
    # add some trace features
    trace0.get_attributes()['t_attr'] = bool_attr
    for i in range(tracelen):
        event = XFactory.create_event()
        # add an attribute
        int_attr = XFactory.create_attribute_discrete('e_attr', 0)
        event.get_attributes()['e_attr0'] = int_attr
        trace0.append(event)
    log.append(trace0)
    return log


def export_log(log, fpath):
    with open(fpath, 'w') as f:
        XesXmlSerializer().serialize(log, f)


# clean directory fixture is ran before every test method
@pytest.mark.usefixtures('cleandir')
class TestXesXmlParser:
    @pytest.fixture(autouse=True)
    def setup(self, log):
        self.log = log
        self.parser = XesXmlParser()

    def read_log(self, fpath):
        with open(fpath, 'r') as log_file:
            log = self.parser.parse(log_file)[0]
        return log

    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []

    def test_cwd_starts_with_log(self):
        export_log(self.log, 'log.xes')
        assert os.listdir(os.getcwd()) == ['log.xes']

    def test_can_parse_log(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        assert log is not None

    def test_parsed_log_has_features(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        log_features = log.get_features()
        # there are a standard number of features
        assert len(log_features) == 3
        assert 'openxes.version' in log_features
        assert 'xes.features' in log_features
        assert 'xes.version' in log_features
        assert log_features['openxes.version'] == '1.0RC7'
        assert log_features['xes.features'] == 'nested-attributes'
        assert log_features['xes.version'] == '1.0'

    def test_parsed_log_has_attributes(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        log_attrs = log.get_attributes()
        assert len(log_attrs) == 1
        assert 'l_attr' in log_attrs
        attr0 = log_attrs['l_attr']
        assert attr0.get_value() == 'UNKNOWN'

    def test_parsed_log_has_global_trace_attributes(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        glb_t_attrs = log.get_global_trace_attributes()
        assert len(glb_t_attrs) == 1
        glb_t_attr = glb_t_attrs[0]
        assert glb_t_attr.get_key() == 'glb_t_attr'
        assert glb_t_attr.get_value() == 0

    def test_parsed_log_has_global_event_attributes(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        glb_e_attrs = log.get_global_event_attributes()
        assert len(glb_e_attrs) == 1
        glb_e_attr = glb_e_attrs[0]
        assert glb_e_attr.get_key() == 'glb_e_attr'
        assert glb_e_attr.get_value() == 0

    def test_parsed_log_has_extensions(self):
        export_log(self.log, 'log.xes')
        # register new extension
        meta_concept = XExtensionParser().parse(
         "http://www.xes-standard.org/meta_concept.xesext")
        XExtensionManager().register(meta_concept)
        log = self.read_log('log.xes')
        exts = log.get_extensions()
        assert len(exts) == 1
        ext = exts.pop()
        assert ext.get_name() == 'MetaData_Concept'

    def test_parsed_log_has_proper_trace_and_events(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        assert len(log) == 1
        trace = log[0]
        trace_attrs = trace.get_attributes()
        assert len(trace_attrs) == 1
        assert 't_attr' in trace_attrs
        t_attr = trace_attrs['t_attr']
        assert t_attr.get_value() == True
        assert len(trace) == 2
        e0 = trace[0]
        event_attrs_0 = e0.get_attributes()
        assert len(event_attrs_0) == 1
        assert 'e_attr' in event_attrs_0
        e_attr_0 = event_attrs_0['e_attr']
        assert e_attr_0.get_value() == 0
        e1 = trace[1]
        event_attrs_1 = e1.get_attributes()
        assert len(event_attrs_1) == 1
        assert 'e_attr' in event_attrs_1
        e_attr_1 = event_attrs_1['e_attr']
        assert e_attr_1.get_value() == 0
